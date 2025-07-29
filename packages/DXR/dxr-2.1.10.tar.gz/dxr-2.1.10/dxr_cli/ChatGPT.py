"""
A simple wrapper for the official ChatGPT API
"""
import argparse
import json
import os
import sys
from typing import NoReturn

import requests
import tiktoken

from .utils import create_completer
from .utils import create_session
from .utils import get_input
import openai

ENGINE = os.environ.get("GPT_ENGINE") or "gpt-3.5-turbo"


class Chatbot:
    """
    Official ChatGPT API
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = None,
        engine: str = None,
        proxy: str = None,
        max_tokens: int = 4095,
        temperature: float = 0.5,
        top_p: float = 1.0,
        reply_count: int = 1,
        system_prompt: str = "You are ChatGPT, a large language model trained by OpenAI. Respond conversationally",
    ) -> None:
        """
        Initialize Chatbot with API key (from https://platform.openai.com/account/api-keys)
        """
        self.engine = engine or ENGINE
        self.session = requests.Session()
        self.api_key = api_key
        openai.api_key = self.api_key
        if base_url is not None:
            openai.api_base = base_url + 'v1'
        self.proxy = proxy
        if self.proxy:
            proxies = {
                "http": self.proxy,
                "https": self.proxy,
            }
            self.session.proxies = proxies
        self.conversation: dict = {
            "default": [
                {
                    "role": "system",
                    "content": system_prompt,
                },
            ],
        }
        self.system_prompt = system_prompt
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.reply_count = reply_count

        if self.get_token_count("default") > self.max_tokens:
            raise Exception("System prompt is too long")

    def add_to_conversation(
        self,
        message: str,
        role: str,
        convo_id: str = "default",
    ) -> None:
        """
        Add a message to the conversation
        """
        self.conversation[convo_id].append({"role": role, "content": message})

    def __truncate_conversation(self, convo_id: str = "default") -> None:
        """
        Truncate the conversation
        """
        while True:
            if (
                self.get_token_count(convo_id) > self.max_tokens
                and len(self.conversation[convo_id]) > 1
            ):
                # Don't remove the first message
                self.conversation[convo_id].pop(1)
            else:
                break

    # https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb
    def get_token_count(self, convo_id: str = "default") -> int:
        """
        Get token count
        """
        if self.engine not in ["gpt-3.5-turbo", "gpt-3.5-turbo-0301", 'gpt-4-0314', 'gpt-4']:
            raise NotImplementedError("Unsupported engine {self.engine}")

        encoding = tiktoken.encoding_for_model(self.engine)

        num_tokens = 0
        for message in self.conversation[convo_id]:
            # every message follows <im_start>{role/name}\n{content}<im_end>\n
            num_tokens += 4
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += -1  # role is always required and always 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant
        return num_tokens

    def get_max_tokens(self, convo_id: str) -> int:
        """
        Get max tokens
        """
        return 4000 - self.get_token_count(convo_id)

    def ask_stream(
        self,
        prompt: str,
        role: str = "user",
        convo_id: str = "default",
        **kwargs,
    ) -> str:
        """
        Ask a question
        """
        # Make conversation if it doesn't exist
        if convo_id not in self.conversation:
            self.reset(convo_id=convo_id, system_prompt=self.system_prompt)
        self.add_to_conversation(prompt, "user", convo_id=convo_id)
        self.__truncate_conversation(convo_id=convo_id)
        response = openai.ChatCompletion.create(
            model=self.engine,
            messages=self.conversation[convo_id],
            temperature=kwargs.get("temperature", self.temperature),
            top_p=kwargs.get("top_p", self.top_p),
            n=kwargs.get("n", self.reply_count),
            stream=True,
            user=role,
        )  
        response_role: str = None
        full_response: str = ""
        for resp in response:
            choices = resp.get("choices")
            if not choices:
                continue
            delta = choices[0].get("delta")
            if not delta:
                continue
            if "role" in delta:
                response_role = delta["role"]
            else:
                response_role = "assistant"
            if "content" in delta:
                content = delta["content"]
                full_response += content
                yield content
        self.add_to_conversation(full_response, response_role, convo_id=convo_id)

    def ask(
        self,
        prompt: str,
        role: str = "user",
        convo_id: str = "default",
        **kwargs,
    ) -> str:
        """
        Non-streaming ask
        """
        response = self.ask_stream(
            prompt=prompt,
            role=role,
            convo_id=convo_id,
            **kwargs,
        )
        full_response: str = "".join(response)
        return full_response

    def rollback(self, n: int = 1, convo_id: str = "default") -> None:
        """
        Rollback the conversation
        """
        for _ in range(n):
            self.conversation[convo_id].pop()

    def reset(self, convo_id: str = "default", system_prompt: str = None) -> None:
        """
        Reset the conversation
        """
        self.conversation[convo_id] = [
            {"role": "system", "content": system_prompt or self.system_prompt},
        ]

    def save(self, file: str, *convo_ids: str) -> bool:
        """
        Save the conversation to a JSON file
        """
        try:
            with open(file, "w", encoding="utf-8") as f:
                if convo_ids:
                    json.dump({k: self.conversation[k] for k in convo_ids}, f, indent=2)
                else:
                    for convo_id in self.conversation:
                        system_message = self.conversation[convo_id][0]
                        # 只保留50条对话，但是必须要保留系统的第一条消息
                        self.conversation[convo_id] = self.conversation[convo_id][-50:]
                        self.conversation[convo_id][0] = system_message
                    json.dump(self.conversation, f, indent=2)
        except (FileNotFoundError, KeyError):
            return False
        return True
        # print(f"Error: {file} could not be created")

    def load(self, file: str, *convo_ids: str) -> bool:
        """
        Load the conversation from a JSON  file
        """
        try:
            with open(file, encoding="utf-8") as f:
                if convo_ids:
                    convos = json.load(f)
                    self.conversation.update({k: convos[k] for k in convo_ids})
                else:
                    self.conversation = json.load(f)
        except (FileNotFoundError, KeyError, json.decoder.JSONDecodeError):
            return False
        return True
    
    def voice_2_text(self, file):
        # 判断file是文件还是文件的字符串，如果是文件的字符串，就转换成文件
        if isinstance(file, str):
            file = open(file, 'rb')
        response = openai.Audio.transcribe('whisper-1', file)
        return response['text']