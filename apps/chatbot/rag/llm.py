from django.conf import settings
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from dotenv import load_dotenv

load_dotenv()

api_key = settings.OPENAI_API_KEY

def get_openai_llm(model_name: str = "gpt-4o",
                   max_tokens=528,
                   temp=0.2):
    llm = ChatOpenAI(api_key=api_key,
                     model_name=model_name,
                     max_tokens=max_tokens,
                     temperature=temp,
                     max_retries=2)
    return llm

def get_local_llm(max_tokens=528,
                  temp=0.2):
    llm = ChatOllama(model = "hf.co/Dannyissme/llama3.2_1bn_imdg_raft_v2.1.16bit:latest", 
                     temperature = temp,
                     num_predict = max_tokens)
    return llm

if __name__ == "__main__":
    llm = get_local_llm()
    messages = [
                ("system", "You are an expert assistant specializing in the International Maritime Dangerous Goods (IMDG) Code. Your primary function is to answer user questions about the IMDG Code using the provided context."),
                ("human", "What is the IMDG Code?")]
    for chunk in llm.stream(messages):
        print(chunk.text(), end="")
    # print(rs.content)