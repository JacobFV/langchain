from __future__ import annotations

from typing import Any, Coroutine, List, Optional

from langchain.callbacks.manager import (
    AsyncCallbackManagerForLLMRun,
    CallbackManagerForLLMRun,
)
from langchain.chat_models.base import BaseChatModel, SimpleChatModel
from langchain.llms.base import BaseLanguageModel
from langchain.schema import BaseMessage, ChatResult
from langchain.utils import serialize_msgs


class ChatModelFacade(SimpleChatModel):
    llm: BaseLanguageModel

    def _call(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
    ) -> str:
        if isinstance(self.llm, BaseChatModel):
            return self.llm(messages, stop=stop).content
        elif isinstance(self.llm, BaseLanguageModel):
            return self.llm(serialize_msgs(messages), stop=stop)
        else:
            raise ValueError(
                f"Invalid llm type: {type(self.llm)}. Must be a chat model or language model."
            )

    @classmethod
    def of(cls, llm):
        if isinstance(llm, BaseChatModel):
            return llm
        elif isinstance(llm, BaseLanguageModel):
            return cls(llm=llm)
        else:
            raise ValueError(
                f"Invalid llm type: {type(llm)}. Must be a chat model or language model."
            )

    def _agenerate(
        self,
        messages: List[BaseMessage],
        stop: List[str] | None = None,
        run_manager: AsyncCallbackManagerForLLMRun | None = None,
    ) -> Coroutine[Any, Any, ChatResult]:
        return super()._agenerate(messages, stop, run_manager)

    @property
    def _llm_type(self) -> str:
        return "chat_model_facade"
