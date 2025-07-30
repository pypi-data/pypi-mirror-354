import time
import uuid
import threading
import warnings
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Generator, Union

from transformers import PreTrainedTokenizer

from owlsight.utils.logger import logger
from owlsight.processors.constants import DEFAULT_MAX_TOKENS, DEFAULT_TEMPERATURE


class TextGenerationProcessor(ABC):
    """Abstract base class for text generation processors implementing basic generation."""

    def __init__(
        self,
        model_id: str,
        apply_chat_history: bool,
        system_prompt: str,
        model_kwargs: Optional[Dict[str, Any]] = None,
        apply_tools: Optional[List[dict]] = None,
    ):
        """
        Initialize the text generation processor.

        Parameters
        ----------
        model_id : str
            The model ID to use for generation.
            Usually the name of the model or the path to the model.
        apply_chat_history : bool
            Whether or not to save the history of inputs and outputs.
        system_prompt : str
            The system prompt to use for generation.
        model_kwargs : Optional[Dict[str, Any]]
            Additional keyword arguments for the model. Default is None.
        apply_tools : Optional[List[dict]]
            A list of tools to call from the processor. Default is None.
            Also see: https://medium.com/@malumbea/function-tool-calling-using-gemma-transform-instruction-tuned-it-model-bc8b05585377
        """
        if not model_id:
            raise ValueError("Model ID cannot be empty.")

        self.model_id = model_id
        self.apply_chat_history = apply_chat_history
        self.system_prompt = system_prompt
        self.chat_history: List[Dict[str, str]] = []
        self.model_kwargs = model_kwargs or {}
        self.apply_tools = apply_tools

        # Ensures minimal thread‑safety for history / prompt swaps
        self._lock = threading.Lock()

    def apply_chat_template(
        self,
        input_data: str,
        tokenizer: PreTrainedTokenizer,
    ) -> str:
        """
        Apply chat template to the input text.
        This is used to format the input text before generating a response and should be universal across all models.

        Parameters
        ----------
        input_data : str
            The input text to apply the template to.
        tokenizer : PreTrainedTokenizer
            The tokenizer to use for applying the template.

        Returns
        -------
        str
            The formatted text with the chat template applied.
        """
        if tokenizer.chat_template is not None:
            messages = self.get_history() if self.apply_chat_history else []
            messages.append({"role": "user", "content": input_data})
            return tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=bool(self.apply_tools),
            )

        logger.warning("Chat template not found in tokenizer. Using input text as is.")
        return input_data

    def update_history(self, input_data: str, generated_text: str) -> None:
        """Update the chat history with the input and generated text."""
        self.chat_history.append({"role": "user", "content": input_data})
        self.chat_history.append({"role": "assistant", "content": generated_text.strip()})

    def clear_history(self) -> None:
        """Clear the chat history."""
        self.chat_history = []
        logger.info("Chat history cleared.")

    def get_history(self) -> List[Dict[str, str]]:
        """Get the chat history."""
        messages = self.chat_history.copy()
        if self.system_prompt:
            messages.insert(0, {"role": "system", "content": self.system_prompt})
        return messages

    def generate_openai_comp(
        self,
        messages: List[Dict[str, str]],
        **openai_kwargs: Any,
    ) -> Union[Dict[str, Any], Generator[Dict[str, Any], None, None]]:
        """
        OpenAI-compatible wrapper around ``generate`` / ``generate_stream``.

        Parameters
        ----------
        messages
            Same structure as OpenAI Chat API: `[{role: ..., content: ...}, …]`
        openai_kwargs
            Any ChatCompletion parameters - a *subset* is interpreted here
            (`stream`, `max_tokens`, `temperature`, `stop`, `top_p`, `top_k`, etc);
            unrecognised keys are forwarded to the underlying model through
            ``generation_kwargs``.

        Returns
        -------
        dict  |  generator
            - If ``stream`` is **False** (default) a *single* dictionary that
              matches the ChatCompletion response.
            - If ``stream`` is **True** a generator that yields ChatCompletion
              *chunk* dictionaries suitable for Server-Sent-Events.
        """
        if not messages:
            raise ValueError("`messages` cannot be empty.")

        # --------------------  parameter extraction  -------------------- #
        stream: bool = bool(openai_kwargs.pop("stream", False))
        # max_new_tokens is the OpenAI parameter, max_tokens is the HuggingFace parameter
        if "max_new_tokens" in openai_kwargs:
            max_new_tokens: int = int(openai_kwargs.pop("max_new_tokens"))
        elif "max_tokens" in openai_kwargs:
            max_new_tokens: int = int(openai_kwargs.pop("max_tokens"))
        else:
            max_new_tokens = DEFAULT_MAX_TOKENS

        temperature: float = float(openai_kwargs.pop("temperature", DEFAULT_TEMPERATURE))

        # Extract and process 'stop' parameter
        stop_param: Optional[Union[str, List[str]]] = openai_kwargs.pop("stop", None)
        stop_words_list: Optional[List[str]] = None
        if isinstance(stop_param, str):
            stop_words_list = [stop_param]
        elif isinstance(stop_param, list):
            # Ensure all elements are strings, filter out None or empty strings if necessary
            stop_words_list = [s for s in stop_param if isinstance(s, str) and s]
            if not stop_words_list:  # If list becomes empty after filtering
                stop_words_list = None

        generation_kwargs: Dict[str, Any] = {}
        # Explicitly pop known OpenAI parameters to prevent them from being unknown kwargs for some models
        # and to ensure they are handled consistently if the underlying model supports them directly
        # or via a specific transformation (like 'stop' to 'stop_words').
        known_openai_params = (
            "top_p",
            "top_k",
            "repetition_penalty",
            "presence_penalty",
            "frequency_penalty",
            "seed",
            "n",
            "logit_bias",
            "logprobs",
            "top_logprobs",
            "user",
        )
        for key in known_openai_params:
            if key in openai_kwargs:
                value = openai_kwargs.pop(key)
                if value is not None:  # Only add if not None, as some models might not like None for these
                    generation_kwargs[key] = value

        # Anything *else* the caller supplied is also forwarded unchanged
        # 'stop' and other known params have already been popped.
        generation_kwargs.update(openai_kwargs)

        # --------------------  prepare inputs & history  ---------------- #
        with self._lock:
            original_system_prompt = self.system_prompt
            original_chat_history = list(self.chat_history)

            # Work on a *copy* so we can safely pop without side-effects
            msgs = list(messages)

            # Extract system prompt if present
            if msgs and msgs[0]["role"] == "system":
                self.system_prompt = msgs.pop(0)["content"]

            if not msgs:
                # Restore and bail if nothing left
                self.system_prompt = original_system_prompt
                self.chat_history = original_chat_history
                raise ValueError("No user message found to generate from.")

            user_input = msgs[-1]["content"]
            self.chat_history = msgs[:-1]

        # --------------------  helpers  --------------------------------- #
        def _build_final_response(completion: str) -> Dict[str, Any]:
            now = int(time.time())
            resp_id = f"chatcmpl-{uuid.uuid4().hex}"

            prompt_tokens = completion_tokens = 0
            if getattr(self, "tokenizer", None):
                try:
                    prompt_tokens = len(self.tokenizer.encode(user_input))
                    completion_tokens = len(self.tokenizer.encode(completion))
                except Exception:
                    # Token counting is *best-effort* only
                    pass

            return {
                "id": resp_id,
                "object": "chat.completion",
                "created": now,
                "model": self.model_id,
                "choices": [
                    {
                        "index": 0,
                        "message": {"role": "assistant", "content": completion},
                        "finish_reason": "stop",
                    }
                ],
                "usage": {
                    "prompt_tokens": prompt_tokens,
                    "completion_tokens": completion_tokens,
                    "total_tokens": prompt_tokens + completion_tokens,
                },
            }

        # --------------------  Generation delegates  -------------------- #
        def _restore_state() -> None:
            """Re-establish original prompt & history – always call this last."""
            self.system_prompt = original_system_prompt
            self.chat_history = original_chat_history

        # --------------------  streaming / non‑streaming  --------------- #
        if stream:

            def _safe_stream(gen: Generator[str, None, None]) -> Generator[str, None, None]:
                try:
                    for tok in gen:
                        yield tok
                finally:
                    _restore_state()

            raw_gen = self.generate_stream(
                user_input,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                stop_words=stop_words_list,  # Pass processed stop_words_list
                generation_kwargs=generation_kwargs,
            )
            return _safe_stream(raw_gen)

        try:
            completion_text = self.generate(
                user_input,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                stop_words=stop_words_list,  # Pass processed stop_words_list
                generation_kwargs=generation_kwargs,
            )
            return _build_final_response(completion_text)
        finally:
            _restore_state()

    def generate_stream(
        self,
        input_data: str,
        max_new_tokens: int,
        temperature: float,
        generation_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Generator[str, None, None]:
        """
        Generate streaming text response. This method should be overridden by subclasses.
        """
        warnings.warn(
            f"{self.__class__.__name__} does not have a dedicated 'generate_stream' implementation. "
            f"Falling back to non-streaming 'generate'.",
            UserWarning,
        )
        result = self.generate(
            input_data=input_data,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            generation_kwargs=generation_kwargs,
            **kwargs,
        )
        yield result

    @abstractmethod
    def generate(
        self,
        input_data: str,
        max_new_tokens: int,
        temperature: float,
        generation_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_max_context_length(self) -> int:
        """Get the maximum context length for the model."""
        raise NotImplementedError
