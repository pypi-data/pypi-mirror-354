from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

from src.text2sql.utils.ai import parse_ai_uri


def test_ai_uri():
    samples = [
        "llm+openai://gpt-4:32k@sk-123@https://api.openai.com/v1",
        "EMBEDDING+OLLAMA://mxbai-embed@127.0.0.1:11434",
        "LLM+OPENAI://gpt-3.5@321@https://api.openai.com/v1",
        "llm+openai://COMMON:abc123@http://etz.paic.com.cn/a/b/c"
    ]
    for s in samples:
        print(parse_ai_uri(s))

    api = parse_ai_uri("llm+openai://qwen2.5:0.5b@123@http://localhost:11434/v1")

    llm = ChatOpenAI(
        model_name=api.model,
        openai_api_base=api.api_uri,
        openai_api_key=api.api_key
    )
    print(llm.invoke("hi").content)

    api = parse_ai_uri("llm+ollama://qwen2.5:0.5b@123@http://localhost:11434")

    llm = ChatOllama(
        model=api.model,
        base_url=api.api_uri,
        api_key=api.api_key
    )
    print(llm.invoke("hi").content)

