import abc
from _typeshed import Incomplete
from abc import ABC
from gllm_core.event import EventEmitter as EventEmitter
from gllm_inference.constants import ALL_EXTENSIONS as ALL_EXTENSIONS, MESSAGE_TUPLE_LENGTH as MESSAGE_TUPLE_LENGTH
from gllm_inference.schema import LMOutput as LMOutput, MultimodalContent as MultimodalContent, MultimodalOutput as MultimodalOutput, MultimodalPrompt as MultimodalPrompt, PromptRole as PromptRole, ResponseSchema as ResponseSchema, UnimodalPrompt as UnimodalPrompt
from gllm_inference.schema.model_id import ModelId as ModelId
from gllm_inference.utils import get_mime_type as get_mime_type, is_local_file_path as is_local_file_path, is_remote_file_path as is_remote_file_path, validate_string_enum as validate_string_enum
from langchain_core.tools import Tool as Tool
from typing import Any

class _Key:
    """Defines valid keys in LM invokers JSON schema."""
    ADDITIONAL_PROPERTIES: str
    ANY_OF: str
    DEFAULT: str
    PROPERTIES: str
    REQUIRED: str
    TYPE: str

class _InputType:
    """Defines valid input types in LM invokers JSON schema."""
    NULL: str

class BaseLMInvoker(ABC, metaclass=abc.ABCMeta):
    '''A base class for language model invokers used in Gen AI applications.

    The `BaseLMInvoker` class provides a framework for invoking language models with prompts and hyperparameters.
    It handles both standard and streaming invocation.

    Attributes:
        model_id (str): The model ID of the language model.
        default_hyperparameters (dict[str, Any]): Default hyperparameters for invoking the language model.
        valid_extensions_map (dict[str, set[str]]): A dictionary mapping for validating the content type of the
            multimodal inputs. They keys are the mime types (e.g. "image") and the values are the set of valid
            file extensions (e.g. {".png", ".jpg", ".jpeg"}) for the corresponding mime type.
        valid_extensions (set[str]): A set of valid file extensions for the multimodal inputs.
        tools (list[Tool] | None): Tools provided to the language model to enable tool calling.
    '''
    default_hyperparameters: Incomplete
    valid_extensions_map: Incomplete
    valid_extensions: Incomplete
    tools: Incomplete
    def __init__(self, model_id: ModelId, default_hyperparameters: dict[str, Any] | None = None, valid_extensions_map: dict[str, set[str]] | None = None, tools: list[Tool] | None = None) -> None:
        '''Initializes a new instance of the BaseLMInvoker class.

        Args:
            model_id (ModelId): The model ID of the language model.
            default_hyperparameters (dict[str, Any] | None, optional): Default hyperparameters for invoking the language
                model. Defaults to None, in which case an empty dictionary is used.
            valid_extensions_map (dict[str, set[str]] | None, optional): A dictionary mapping for validating the
                content type of the multimodal inputs. They keys are the mime types (e.g. "image") and the values
                are the set of valid file extensions for the corresponding mime type. Defaults to None.
            tools (list[Tool] | None, optional): Tools provided to the language model to enable tool calling.
                Defaults to None.
        '''
    @property
    def model_id(self) -> str:
        """The model ID of the language model.

        Returns:
            str: The model ID of the language model.
        """
    def set_tools(self, tools: list[Tool]) -> None:
        """Sets the tools for the language model.

        This method sets the tools for the language model. Any existing tools will be replaced.

        Args:
            tools (list[Tool]): The list of tools to be used.
        """
    async def invoke(self, prompt: MultimodalPrompt | UnimodalPrompt, hyperparameters: dict[str, Any] | None = None, event_emitter: EventEmitter | None = None) -> MultimodalOutput:
        """Invokes the language model with the provided prompt and hyperparameters.

        This method validates the prompt and invokes the language model with the provided prompt and hyperparameters.
        It handles both standard and streaming invocation. Streaming mode is enabled if an event emitter is provided.

        Args:
            prompt (MultimodalPrompt | UnimodalPrompt): The input prompt for the language model.
            hyperparameters (dict[str, Any] | None, optional): A dictionary of hyperparameters for the language model.
                Defaults to None, in which case the default hyperparameters are used.
            event_emitter (EventEmitter | None, optional): The event emitter for streaming tokens. If provided,
                streaming invocation is enabled. Defaults to None.

        Returns:
            MultimodalOutput: The generated response from the language model.

        Raises:
            ValueError: If the prompt is not in the correct format.
        """
