import requests
from typing import List, Dict, Any
from langchain_core.messages import BaseMessage, HumanMessage, AIMessageChunk
from setting.models_provider.base_model_provider import MaxKBBaseModel
import json

class CustomChatModel(MaxKBBaseModel):
    def __init__(self, endpoint_url: str, api_key: str, **kwargs):
        self.endpoint_url = endpoint_url
        self.api_key = api_key
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }

    @staticmethod
    def is_cache_model():
        return False

    def invoke(self, messages: List[BaseMessage], **kwargs) -> Any:
        payload = {
            "model": "claude-3-5-sonnet-20240620",
            'messages': [{'role': 'user' if isinstance(msg, HumanMessage) else 'assistant',
                         'content': msg.content} for msg in messages],
            'temperature': kwargs.get('temperature', 0.7),
            # 'max_tokens': kwargs.get('max_tokens', 800)
        }

        try:
            response = requests.post(
                f"{self.endpoint_url}/chat/completions",
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API调用失败: {str(e)}")

    def stream(self, messages: List[BaseMessage], **kwargs) -> Any:
        payload = {
            "model": "claude-3-5-sonnet-20240620",
            'messages': [{'role': 'user' if isinstance(msg, HumanMessage) else 'assistant',
                         'content': msg.content} for msg in messages],
            'temperature': kwargs.get('temperature', 0.7),
            # 'max_tokens': kwargs.get('max_tokens', 800),
            'stream': True
        }

        try:
            response = requests.post(
                f"{self.endpoint_url}/chat/completions",
                headers=self.headers,
                json=payload,
                stream=True
            )
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8').strip()
                    # 跳过空行和结束标识
                    if decoded_line == "[DONE]" or not decoded_line.startswith("data:"):
                        continue
                    # 移除 'data: ' 前缀
                    json_str = decoded_line.replace('data: ', '')
                    try:
                        data = json.loads(json_str)
                        if 'choices' in data and len(data['choices']) > 0:
                            content = data['choices'][0].get('delta', {}).get('content', '')
                            if content:
                                yield AIMessageChunk(content=content)
                    except json.JSONDecodeError as json_err:
                        # 记录无法解析的行，便于调试
                        print(f"无法解析的JSON行: {json_str}")
                        continue
        except requests.exceptions.RequestException as e:
            raise Exception(f"流式API调用失败: {str(e)}")

    @staticmethod
    def new_instance(model_type, model_name, model_credential: Dict[str, object], **model_kwargs):
        optional_params = MaxKBBaseModel.filter_optional_params(model_kwargs)
        
        custom_chat = CustomChatModel(
            model=model_name,
            endpoint_url=model_credential.get('endpoint_url'),
            api_key=model_credential.get('api_key'),
            **optional_params
        )
        return custom_chat