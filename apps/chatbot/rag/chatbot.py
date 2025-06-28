from langchain_core.messages import AIMessage, HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph
from langchain.chains import create_retrieval_chain
from .llm import get_openai_llm, get_local_llm
from .vector_db import VectorDB
from .contextual_retriever import ContextualRetriever
from .qa_chain import QuestionAnsweringChain
from .state_manager import StateManager
from .standardize import preprocess_text

class Chatbot:
    def __init__(self):
        self.llm = get_openai_llm(model_name="gpt-4.1")
        # self.local_llm = get_local_llm()     
        self.vector_db = VectorDB() 
        self.retriever = self.vector_db.get_compressed_retriever(search_kwargs={"k": 6})  
        self.contextual_retriever = ContextualRetriever(self.llm, self.retriever).get_history_aware_retriever()
        self.qa_chain = QuestionAnsweringChain(self.llm).create_qa_chain()
        self.rag_chain = create_retrieval_chain(self.contextual_retriever, self.qa_chain)
        self.memory = MemorySaver()

    def call_model(self, state: StateManager):
        state["input"] = preprocess_text(state["input"])
        response = self.rag_chain.invoke(state)
        
        return {
            "chat_history": [
                HumanMessage(state["input"]),
                AIMessage(response["answer"]),
            ],
            "context": response["context"],
            "answer": response["answer"],
        }

        
    def setup_workflow(self):        
        self.workflow = StateGraph(state_schema=StateManager)
        self.workflow.add_edge(START, "model")
        self.workflow.add_node("model", self.call_model)
        self.app = self.workflow.compile(checkpointer=self.memory)
        return self.app


    def ask(self, question: str, config: dict):
        
        state = {
            "input": question,
            "chat_history": [],
            "context": "",
            "answer": "",
        }
        
        result = self.app.invoke(state, config=config)
        
        return {"answer": result["answer"], "documents": result["context"]}

if __name__ == "__main__":
    # Khởi tạo chatbot
    chatbot = Chatbot()
    
    # Thiết lập workflow
    app = chatbot.setup_workflow()
    
    # Cấu hình cho session
    config = {"configurable": {"thread_id": "test_session_1"}}
    
    print("Chatbot đã sẵn sàng! Gõ 'quit' để thoát.\n")
    
    while True:
        # Nhập câu hỏi từ người dùng
        question = input("Bạn: ")
        
        # Kiểm tra điều kiện thoát
        if question.lower() in ['exit', 'quit', 'thoát']:
            print("Tạm biệt!")
            break
            
        if question.strip() == "":
            continue
            
        try:
            # Gọi chatbot để trả lời
            print("Bot đang suy nghĩ...")
            answer = chatbot.ask(question, config)
            print(f"Bot: {answer}\n")
            
        except Exception as e:
            print(f"Lỗi: {e}\n")
            import traceback
            print(traceback.format_exc())
