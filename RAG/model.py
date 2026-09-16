import warnings
warnings.filterwarnings('ignore')
from langchain.llms.base import LLM
from typing import Any, List, Optional
from openai import OpenAI
import os
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
# class RagLLM(object):
#     client: Optional[Any] = None
#     def __init__(self):
#         super().__init__()
#         self.client = OpenAI(base_url="http://localhost:11434/v1/",
#                              api_key="qwen2:72b")
#
#
#     def __call__(self, prompt : str, **kwargs: Any):
#         completion = self.client.completions.create(model="qwen2:72b",
#                                                     prompt=prompt,
#                                                     temperature=kwargs.get('temperature', 0.1),
#                                                     top_p=kwargs.get('top_p', 0.9),
#                                                     max_tokens=kwargs.get('max_tokens', 4096),
#                                                     stream=kwargs.get('stream', False))
#         if kwargs.get('stream', False):
#             return completion
#         return completion.choices[0].text
#
class RagLLM:
    def __init__(self, model="deepseek-flash"):
        api_key = "sk-4746c34cc7fa442e9015a9daffb8cab3"
        if not api_key:
            raise ValueError("请先配置 DEEPSEEK_API_KEY")

        self.client = OpenAI(
            base_url="https://api.deepseek.com",
            api_key=api_key,
        )
        self.model = model

    def __call__(self, prompt: str, **kwargs: Any):
        stream = kwargs.get("stream", False)

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=kwargs.get("temperature", 0.1),
            max_tokens=kwargs.get("max_tokens", 4096),
            stream=stream,
            # 关闭深度思考，适用于普通 RAG 问答
            extra_body={"thinking": {"type": "disabled"}},
        )

        if stream:
            return completion

        return completion.choices[0].message.content or ""

# class QwenLLM(LLM):
#     client: Optional[Any] = None
#     def __init__(self):
#         super().__init__()
#         self.client = OpenAI(base_url="http://localhost:11434/v1/",
#                              api_key="qwen2:72b")
#
#
#     def _call(self,
#               prompt : str,
#               stop: Optional[List[str]] = None,
#               run_manager: Optional[CallbackManagerForLLMRun] = None,
#               **kwargs: Any):
#         completion = self.client.completions.create(model="qwen2:72b",
#                                                     prompt=prompt,
#                                                     temperature=kwargs.get('temperature', 0.1),
#                                                     top_p=kwargs.get('top_p', 0.9),
#                                                     max_tokens=kwargs.get('max_tokens', 4096),
#                                                     stream=kwargs.get('stream', False))
#         return completion.choices[0].text
#
#     @property
#     def _llm_type(self) -> str:
#         return "rag_llm_qwen2_72b"

class QwenLLM(LLM):
    # 保留类名，让 Notebook 原来的调用代码继续可用
    client: Any = None

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.client = RagLLM()

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        options = dict(kwargs)
        options["stream"] = False
        response = self.client(prompt, **options)

        # 遵循 LangChain 传入的停止字符串
        if stop:
            positions = [
                response.find(token)
                for token in stop
                if token and token in response
            ]
            if positions:
                response = response[:min(positions)]

        return response

    @property
    def _llm_type(self) -> str:
        return "deepseek_rag_evaluator"
    

class SparkAPILLM(LLM):
    client: Optional[Any] = None
    def __init__(self):
        super().__init__()
        self.client = OpenAI(
        api_key=f"Axxxxxx", # 填写讯飞星火平台上的APIPassword
        base_url = 'https://spark-api-open.xf-yun.com/v1' # 指向讯飞星火的请求地址
    )

        
    def _call(self, 
              prompt : str, 
              stop: Optional[List[str]] = None,
              run_manager: Optional[CallbackManagerForLLMRun] = None,
              **kwargs: Any):

        
        completion = self.client.chat.completions.create(model='generalv3.5', # 使用的Spark Max的模型 spark_max_3.5
                                                    messages = [
                                                        {"role": "system", "content": ""},
                                                        {"role": "user", "content": prompt}
                                                    ],
                                                    temperature=kwargs.get('temperature', 0.1),
                                                    top_p=kwargs.get('top_p', 0.9),
                                                    max_tokens=kwargs.get('max_tokens', 4096), 
                                                    stream=kwargs.get('stream', False))
        return completion.choices[0].message.content
    
    @property
    def _llm_type(self) -> str:
        return "rag_spark_max_3.5"


class RagLLMSparkAPI(object):
    client: Optional[Any] = None
    def __init__(self):
        super().__init__()
        self.client = OpenAI(base_url="https://spark-api-open.xf-yun.com/v1", # 指向讯飞星火的请求地址
                             api_key="xxx") # 填写讯飞星火平台上的APIPassword

        
    def __call__(self, prompt : str, **kwargs: Any):
        
        messages = [
            {"role": "system", "content": ""},
            {"role": "user", "content": prompt}
        ] 
        completion = self.client.chat.completions.create(model="generalv3.5", # 使用的Spark Max的模型 spark_max_3.5
                                                    messages=messages,
                                                    temperature=kwargs.get('temperature', 0.1),
                                                    top_p=kwargs.get('top_p', 0.9),
                                                    max_tokens=kwargs.get('max_tokens', 4096), 
                                                    stream=kwargs.get('stream', False))
        if kwargs.get('stream', False):
            return completion
        return completion.choices[0].message.content
    

from langchain.embeddings.huggingface import HuggingFaceEmbeddings
class RagEmbedding(object):
    def __init__(self, model_path="./data/llm_app/embedding_models/bge-m3//", 
                 device="cpu"):
        self.embedding = HuggingFaceEmbeddings(model_name=model_path,
                                               model_kwargs={"device": "cpu"})
    def get_embedding_fun(self):
        return self.embedding