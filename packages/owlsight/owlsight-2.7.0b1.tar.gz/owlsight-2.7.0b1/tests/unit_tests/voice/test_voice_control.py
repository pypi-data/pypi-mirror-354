import pytest
from unittest.mock import Mock, patch
import queue
import importlib.util

# Check if required dependencies are installed
realtimestt_installed = importlib.util.find_spec("RealtimeSTT") is not None
faster_whisper_installed = importlib.util.find_spec("faster_whisper") is not None

if not realtimestt_installed or not faster_whisper_installed:
    missing_deps = []
    if not realtimestt_installed:
        missing_deps.append("RealtimeSTT")
    if not faster_whisper_installed:
        missing_deps.append("faster-whisper")
    pytest.skip(f"{', '.join(missing_deps)} not installed. Skipping voice control tests.", allow_module_level=True)

from owlsight.voice.voice_control import VoiceControl


@pytest.fixture(autouse=True)
def mock_audio_recorder():
    """Mock AudioToTextRecorder to prevent actual multiprocessing during tests."""
    with patch("RealtimeSTT.AudioToTextRecorder") as mock_recorder:
        # Create a mock instance that will be returned when AudioToTextRecorder is instantiated
        mock_instance = Mock()
        mock_recorder.return_value = mock_instance

        # Mock the shutdown method
        mock_instance.shutdown = Mock()

        yield mock_instance


@pytest.fixture
def voice_control():
    """Create a VoiceControl instance with mocked queues and callback."""
    vc = VoiceControl(
        word_to_key_map={"left": "left", "right": "right", "select all": ["ctrl", "a"], "delete": "delete"},
        word_to_word_map={"exit": "exit()", "print": "print()"},
        debug=True,
    )

    # Mock the queues
    vc.key_press_queue = Mock(spec=queue.Queue)
    vc.typing_queue = Mock(spec=queue.Queue)

    # Mock the callback
    vc.on_command_processed = Mock()

    # Cleanup function
    def cleanup():
        # Signal threads to stop
        vc._stop_event.set()

        # Properly shutdown the recorder
        if vc.recorder:
            vc.recorder.shutdown()

        # Put None in queues to signal threads to exit
        vc.key_press_queue.put(None)
        vc.typing_queue.put(None)

        # Wait for threads to finish with longer timeouts
        if vc.key_press_thread.is_alive():
            vc.key_press_thread.join(timeout=5)
        if vc.typing_thread.is_alive():
            vc.typing_thread.join(timeout=5)
        if vc.voice_thread and vc.voice_thread.is_alive():
            vc.voice_thread.join(timeout=5)

    # Register cleanup with pytest
    yield vc
    cleanup()


@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        # Basic word transformations
        ("exit", "exit()"),
        ("print", "print()"),
        # With punctuation
        ("exit.", "exit()"),
        ("exit!", "exit()"),
        # Mixed case
        ("EXIT", "exit()"),
        ("ExIt", "exit()"),
        # In a sentence
        ("I want to exit.", "I want to exit()"),
        # Multiple words
        ("exit print", "exit() print()"),
    ],
)
def test_word_transformations(voice_control, input_text, expected_output):
    """Test various word transformation scenarios."""
    voice_control._process_text(input_text)
    voice_control.typing_queue.put.assert_called_once_with(expected_output)


# # Test commands
# @pytest.mark.parametrize("input_text, expected_commands", [
#     ("left", [("left", "left")]),
#     ("select all", [("select all", ["ctrl", "a"])]),
# ])
# def test_commands(voice_control, input_text, expected_commands):
#     """Test command recognition and key press queueing."""
#     voice_control._process_text(input_text)

#     expected_calls = [call(key) for _, key in expected_commands]
#     voice_control.key_press_queue.put.assert_has_calls(expected_calls)
#     assert voice_control.key_press_queue.put.call_count == len(expected_commands)

#     expected_callback_calls = [call(word, key) for word, key in expected_commands]
#     voice_control.on_command_processed.assert_has_calls(expected_callback_calls)
#     assert voice_control.on_command_processed.call_count == len(expected_commands)
