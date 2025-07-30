#!/usr/bin/env python3
"""
openai_compatible.py
--------------------

Run **any** owlsight text-generation processor behind a FastAPI server that
behaves like the real OpenAI **Chat Completions** API – including streaming –  
so that tools such as **Aider**, **LiteLLM**, LangChain, etc. can talk to your
*local* model without any changes to their existing OpenAI integration layer.

The program is essentially a light wrapper that:

1. Instantiates an :class:`~owlsight.processors.text_generation_processors.TextGenerationProcessor`
   implementation for the model specified on the command-line.
2. Starts a FastAPI application that **mirrors** the request/response schema of
   the official ``/v1/chat/completions`` endpoint.
3. Translates between the OpenAI JSON payloads and the internal owlsight API,
   supporting both *synchronous* and *streaming* generation modes.

# Example Usage (GGUF example with Aider, assuming Windows OS):

1. Download the GGUF model from Hugging Face and serve it with this script:
python examples/openai_compatible.py --model [model_from_huggingface] --port 8000

For example, to serve the DeepSeek-R1-0528-Qwen3-8B-GGUF model from Hugging Face to the GPU:
```cmd
python examples\openai_compatible.py ^
  --model unsloth/DeepSeek-R1-0528-Qwen3-8B-GGUF ^
  --gguf__filename DeepSeek-R1-0528-Qwen3-8B-Q4_K_M.gguf ^
  --gguf__n_ctx 8192 ^
  --gguf__verbose true ^
  --gguf__n_gpu_layers -1 ^
  --port 8000
```
2. Test through swagger UI if the server is running:
http://localhost:8000/docs

send a request to the model:
{
    "model": "unsloth/DeepSeek-R1-0528-Qwen3-8B-GGUF",
    "messages": [
        {
            "role": "user",
            "content": "Tell me a joke"
        }
    ],
    "stream": false,
    "max_new_tokens": 512,
    "temperature": 0.7,
    "top_p": 0.9
}


or get all available models:
{
    "model": "list"
}

3. Install Aider (pip install globally, not in a virtual environment):
```cmd
pip install aider-install
aider-install
```

4. Set enviroment variables and start aider
```cmd
REM 1 – current window (good for testing)
set OPENAI_BASE_URL=http://localhost:8000/v1
set OPENAI_API_KEY=dummy

REM 2 – confirm
echo %OPENAI_BASE_URL%
echo %OPENAI_API_KEY%

REM 3 – launch aider
aider --model openai/unsloth/DeepSeek-R1-0528-Qwen3-8B-GGUF
```

-----
* Only a **single** model can be served by a running process. A mismatch
  between the ``model`` field in the incoming request and the server's
  configuration results in a ``400 Bad Request``.
* Unknown ``--key value`` pairs on the command line are forwarded verbatim
  to the processor constructor, making it possible to pass backend-specific
  settings without modifying this file.
"""

# ---------------------------------------------------------------------- #
#  Imports                                                               #
# ---------------------------------------------------------------------- #
import argparse
import json
import logging
import time
import uuid
from typing import Any, Dict, List, Optional, Type

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from owlsight import select_processor_type
from owlsight.processors.text_generation_processors import TextGenerationProcessor

# ---------------------------------------------------------------------- #
#  Logging                                                               #
# ---------------------------------------------------------------------- #
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

app = FastAPI(title="Chat Completion API", version="1.0.0")

# Allow calls from browser-based IDEs running on any host/port (can be
# narrowed via env vars if needed).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#: Model identifier configured at server start-up.
SERVER_MODEL_ID: Optional[str] = None

#: The instantiated owlsight processor (created in :func:`main`).
processor: Optional[TextGenerationProcessor] = None

#: Default generation parameters collected from command-line flags.
default_params: Dict[str, Any] = {}

# Timestamp used for the “created” field of the model metadata.
START_TIME: int = int(time.time())

# ---------------------------------------------------------------------- #
#  Helper: streaming chunk builder                                       #
# ---------------------------------------------------------------------- #
def _wrap_openai_chunk(
    content: str = "",
    *,
    model: str,
    index: int = 0,
    finish: bool = False,
    first: bool = False,
) -> Dict[str, Any]:
    """Return a single streaming *chunk* in the OpenAI format.

    Parameters
    ----------
    content : str, optional
        Token or text fragment generated by the model.
    model : str
        The model name to embed into the response. Must match the model
        specified at server start-up.
    index : int, default 0
        ``choices[index]`` selected by the client. Only ``0`` is currently
        used because the server emits **one** completion per request.
    finish : bool, default False
        If *True* the ``finish_reason`` of the choice is set to ``"stop"``.
        This should be emitted exactly once – after the final token.
    first : bool, default False
        When *True* the ``role`` field ("assistant") is included in the
        ``delta`` so that downstream clients have all mandatory metadata
        in the first message.

    Returns
    -------
    dict
        A JSON-serialisable dictionary that mirrors the structure returned
        by the official OpenAI API for streaming chat completions.
    """
    delta: Dict[str, str] = {}
    if first:
        delta["role"] = "assistant"
    if content:
        delta["content"] = content
    return {
        "id": f"chatcmpl-{uuid.uuid4()}",
        "object": "chat.completion.chunk",
        "created": int(time.time()),
        "model": model,
        "choices": [
            {
                "delta": delta,
                "index": index,
                "finish_reason": "stop" if finish else None,
            }
        ],
    }


# ---------------------------------------------------------------------- #
#  Error wrapper                                                         #
# ---------------------------------------------------------------------- #
def _wrap_openai_error(message: str, status_code: int) -> Dict[str, Any]:
    """Translate an internal error into OpenAI's error schema.

    Parameters
    ----------
    message : str
        Human-readable description of the problem.
    status_code : int
        The HTTP status code associated with the error.

    Returns
    -------
    dict
        Error payload compatible with the OpenAI REST API.
    """
    return {
        "error": {
            "message": message,
            "type": "server_error" if status_code >= 500 else "invalid_request_error",
            "code": status_code,
        }
    }


# ---------------------------------------------------------------------- #
#  Pydantic request schema                                               #
# ---------------------------------------------------------------------- #
class Message(BaseModel):
    """Single message in the chat conversation."""

    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    """Subset of the OpenAI *Chat Completions* request payload.

    Only the fields required by this lightweight proxy are enforced. All
    additional keys are accepted and forwarded to the underlying processor
    thanks to Pydantic's ``model_config = {"extra": "allow"}``.

    Attributes
    ----------
    messages : list[Message]
        Full conversation history (system, user, assistant).
    model : str
        Name of the model. *Must* match ``SERVER_MODEL_ID``.
    stream : bool, default ``False``
        If *True* the response is returned as an HTTP *event-stream* (Server Sent
        Events) compatible with the OpenAI SDK's streaming mode.
    stop : str | list[str] | None
        Generation will halt if the model emits any of the stop sequences.
    max_new_tokens : int, default 2048
        Maximum number of tokens to sample, unless overridden explicitly
        with ``--max-new-tokens`` at launch time.
    """

    messages: List[Message]
    model: str
    stream: bool = False
    max_new_tokens: int = 2048
    stop: Optional[Any] = None
    temperature: Optional[float] = None

    model_config = {"extra": "allow"}


# ---------------------------------------------------------------------- #
#  Main endpoint                                                         #
# ---------------------------------------------------------------------- #
@app.post("/v1/chat/completions")
async def completions(body: ChatCompletionRequest, raw_request: Request):
    """Implementation of ``POST /v1/chat/completions``.

    This single endpoint covers both *streaming* and *non-streaming* modes.
    Because FastAPI runs the handler in a thread-pool (by default), the
    underlying owlsight processor **can** be synchronous.

    Parameters
    ----------
    body : ChatCompletionRequest
        Parsed request body.
    raw_request : fastapi.Request
        The unparsed request – used here only to access the headers and to
        detect whether the connection was terminated during streaming.

    Returns
    -------
    fastapi.responses.StreamingResponse or fastapi.responses.JSONResponse
        Depending on ``body.stream``.

    Raises
    ------
    fastapi.HTTPException
        * ``400`` – `body.model` does not match the server's model.
        * ``500`` – The model failed to load or is otherwise unavailable.
    """
    global processor, SERVER_MODEL_ID

    # ------------------------------------------------------------------ #
    #  Fast validation                                                    #
    # ------------------------------------------------------------------ #
    if body.model != SERVER_MODEL_ID:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid model '{body.model}'. Server is configured for '{SERVER_MODEL_ID}'.",
        )

    if processor is None:
        raise HTTPException(status_code=500, detail="Model processor not available.")

    # Tolerate but *ignore* the Authorization header. The proxy is designed
    # for **local** use, so authentication is delegated to the reverse proxy
    # (nginx, Traefik, Caddy, …) if needed.
    _ = raw_request.headers.get("authorization")

    # ------------------------------------------------------------------ #
    #  Collect generation parameters                                      #
    # ------------------------------------------------------------------ #
    request_dict = body.model_dump()
    messages_payload = [m.model_dump() for m in body.messages]

    known_params = {
        "max_new_tokens", "temperature", "top_p", "top_k",
        "repetition_penalty", "n", "frequency_penalty",
        "presence_penalty", "seed", "stream", "stop",
    }

    # Merge parameters from the request, CLI defaults, and hard-coded fallbacks
    filtered_params: Dict[str, Any] = {
        k: v for k, v in request_dict.items()
        if k in known_params and v is not None
    }
    filtered_params.update({k: v for k, v in default_params.items() if k not in filtered_params})

    # ------------------------------------------------------------------ #
    #  Streaming mode                                                    #
    # ------------------------------------------------------------------ #
    if body.stream:
        logging.info("[stream] params=%s", filtered_params)
        token_gen = processor.generate_openai_comp(messages_payload, **filtered_params)

        async def event_generator():
            """Yields Server-Sent Event (SSE) messages one by one."""
            try:
                # First chunk: includes role
                yield f"data: {json.dumps(_wrap_openai_chunk(model=SERVER_MODEL_ID, first=True))}\n\n"
                # Stream response tokens
                print(f"\n{SERVER_MODEL_ID} response (stream): ", end="")
                for token in token_gen:   # synchronous generator
                    # Abort early if client closed connection (browser tab, etc.)
                    if await raw_request.is_disconnected():
                        break
                    print(token, end="", flush=True)  # Print token to console
                    yield f"data: {json.dumps(_wrap_openai_chunk(token, model=SERVER_MODEL_ID))}\n\n"
                print() # Newline after all tokens are printed
                # Final chunk
                yield f"data: {json.dumps(_wrap_openai_chunk(model=SERVER_MODEL_ID, finish=True))}\n\n"
                yield "data: [DONE]\n\n"
            except Exception as exc:
                logging.exception("streaming error:")
                # Only attempt to send an error if the client is still connected
                if not await raw_request.is_disconnected():
                    err = _wrap_openai_error(str(exc), 500)
                    yield f"data: {json.dumps(err)}\n\n"
                    yield "data: [DONE]\n\n"

        return StreamingResponse(event_generator(), media_type="text/event-stream")

    # ------------------------------------------------------------------ #
    #  Non-streaming mode                                                #
    # ------------------------------------------------------------------ #
    logging.info("[sync] params=%s", filtered_params)
    response_json = processor.generate_openai_comp(messages_payload, **filtered_params)
    return JSONResponse(content=response_json)


# ---------------------------------------------------------------------- #
#  Models endpoint                                                       #
# ---------------------------------------------------------------------- #
@app.get("/v1/models")
async def list_models():
    """Return a minimal list of available models (single-model for now)."""
    return {
        "object": "list",
        "data": [
            {
                "id": SERVER_MODEL_ID,
                "object": "model",
                "created": START_TIME,
                "owned_by": "local",
            }
        ],
    }


@app.get("/v1/models/{model_id}")
async def retrieve_model(model_id: str):
    """Return metadata for the requested model or 404 if not served."""
    if model_id != SERVER_MODEL_ID:
        raise HTTPException(status_code=404, detail=f"Model '{model_id}' not found.")
    return {
        "id": SERVER_MODEL_ID,
        "object": "model",
        "created": START_TIME,
        "owned_by": "local",
    }


# ---------------------------------------------------------------------- #
#  Error handler                                                         #
# ---------------------------------------------------------------------- #
@app.exception_handler(HTTPException)
async def openai_http_exception_handler(request: Request, exc: HTTPException):
    """Convert :class:`fastapi.HTTPException` into an OpenAI-style error."""
    return JSONResponse(
        status_code=exc.status_code,
        content=_wrap_openai_error(str(exc.detail), exc.status_code),
    )


# ---------------------------------------------------------------------- #
#  CLI bootstrap                                                         #
# ---------------------------------------------------------------------- #
def main():
    """Parse CLI flags, initialise the processor, and run the server."""
    parser = argparse.ArgumentParser(description="Start an OpenAI-compatible chat completion server.")
    parser.add_argument("--model", required=True, help="Model identifier (e.g. 'gpt-neox-20b').")
    parser.add_argument("--port", type=int, default=8000, help="TCP port to listen on (default: 8000).")
    parser.add_argument("--host", default="0.0.0.0", help="Bind address (default: 0.0.0.0).")
    parser.add_argument("--log-level", default="info", help="Log level passed to uvicorn.")
    # Optional default generation params
    parser.add_argument("--temperature", type=float, help="Sampling temperature.")
    parser.add_argument("--top-p", dest="top_p", type=float, help="Nucleus sampling probability mass.")
    parser.add_argument("--top-k", dest="top_k", type=int, help="Top-k sampling cutoff.")
    parser.add_argument("--max-new-tokens", dest="max_new_tokens", type=int, help="Token limit.")
    parser.add_argument("--seed", type=int, help="Random seed (for deterministic sampling).")
    args, unknown = parser.parse_known_args()

    global SERVER_MODEL_ID, processor, default_params
    SERVER_MODEL_ID = args.model

    # ------------------------------------------------------------------ #
    #  Build default generation params                                   #
    # ------------------------------------------------------------------ #
    for k in ("temperature", "top_p", "top_k", "max_new_tokens", "seed"):
        v = getattr(args, k)
        if v is not None:
            default_params[k] = v

    # ------------------------------------------------------------------ #
    #  Parse unknown CLI args                                            #
    # ------------------------------------------------------------------ #
    def _parse(val: str):
        """Best-effort conversion of CLI strings to *bool*, *int*, *float*, or *str*."""
        low = val.lower()
        if low == "true":
            return True
        if low == "false":
            return False
        try:
            return int(val)
        except ValueError:
            try:
                return float(val)
            except ValueError:
                return val  # fallback to string

    init_kwargs: Dict[str, Any] = {}
    it = iter(unknown)
    for tok in it:
        if tok.startswith("--"):
            key = tok[2:]
            nxt = next(it, None)
            if nxt and not nxt.startswith("--"):
                init_kwargs[key] = _parse(nxt)
            else:
                # Flag-style option (boolean)
                init_kwargs[key] = True
                if nxt:  # put back the next token for re-processing
                    it = (v for v in [nxt] + list(it))

    logging.info("initialising processor '%s' with %s", SERVER_MODEL_ID, init_kwargs)
    proc_cls: Type[TextGenerationProcessor] = select_processor_type(SERVER_MODEL_ID)
    processor = proc_cls(model_id=SERVER_MODEL_ID, **init_kwargs)

    display_host = "localhost" if args.host == "0.0.0.0" else args.host
    logging.info("Server ready on http://%s:%d", display_host, args.port)
    logging.info("Using model %s", SERVER_MODEL_ID)
    logging.info("Using parameters %s", init_kwargs)
    logging.info("Swagger UI available at http://%s:%d/docs", display_host, args.port)
    uvicorn.run(app, host=args.host, port=args.port, log_level=args.log_level.lower())


if __name__ == "__main__":
    main()
