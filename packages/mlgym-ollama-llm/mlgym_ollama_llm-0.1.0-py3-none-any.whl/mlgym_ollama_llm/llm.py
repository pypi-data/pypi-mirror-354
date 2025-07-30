from typing import List, Any, Optional
from llama_index.core.llms import (
    LLM,
    LLMMetadata,
    ChatMessage,
    MessageRole,
    ChatResponse,
    CompletionResponse
)
from llama_index.core.llms.callbacks import CallbackManager
from ollama import Client

class MLGymOllamaLLM(LLM):
    def __init__(
        self,
        model: str,
        base_url: str,
        api_key: str,
        request_timeout: float = 360.0,
        callback_manager: Optional[CallbackManager] = None,
    ):
        super().__init__(callback_manager=callback_manager)
        self._model = model
        self._client = Client(
            host=base_url,
            timeout=request_timeout,
            headers={
                "api-key": api_key
            }
        )

    def chat(self, messages: List[ChatMessage], **kwargs: Any) -> ChatResponse:
        ollama_messages = [
            {"role": msg.role.value, "content": msg.content}
            for msg in messages
        ]
        result = self._client.chat(
            model=self._model,
            messages=ollama_messages,
            **kwargs
        )
        message = result["message"]
        return ChatResponse(
            message=ChatMessage(
                role=MessageRole(message["role"]),
                content=message["content"]
            ),
            raw=result,
        )

    def complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        result = self._client.generate(
            model=self._model,
            prompt=prompt,
            **kwargs
        )
        return CompletionResponse(text=result["response"], raw=result)

    def stream_chat(self, messages: List[ChatMessage], **kwargs: Any):
        raise NotImplementedError("stream_chat not implemented")

    def stream_complete(self, prompt: str, **kwargs: Any):
        raise NotImplementedError("stream_complete not implemented")

    async def achat(self, messages: List[ChatMessage], **kwargs: Any):
        raise NotImplementedError("achat not implemented")

    async def acomplete(self, prompt: str, **kwargs: Any):
        raise NotImplementedError("acomplete not implemented")

    async def astream_chat(self, messages: List[ChatMessage], **kwargs: Any):
        raise NotImplementedError("astream_chat not implemented")

    async def astream_complete(self, prompt: str, **kwargs: Any):
        raise NotImplementedError("astream_complete not implemented")

    @property
    def metadata(self) -> LLMMetadata:
        return LLMMetadata(
            context_window=4096,
            num_output=256,
            is_chat_model=True,
            is_function_calling_model=False,
            model_name=self._model,
        )