import os
import sys
import time
from langchain_community.document_loaders import CSVLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

# === Set your Groq API Key and base ===
os.environ["OPENAI_API_KEY"] = "your-groq_api_key_here"
GROQ_API_BASE = "https://api.groq.com/openai/v1"

# ✅ Correct path to logs.csv
csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../server/logs.csv"))


# === Load and split CSV logs ===
loader = CSVLoader(file_path=csv_path)
documents = loader.load()

splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
split_docs = splitter.split_documents(documents)

# === Embed using FAISS (no embeddings needed again if already persisted) ===


embedding_model = ChatOpenAI(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    openai_api_key=os.environ["OPENAI_API_KEY"],
    openai_api_base=GROQ_API_BASE,
    temperature=0
)

# 🧠 Dummy embedder since Groq doesn't support embedding generation
from langchain.embeddings import FakeEmbeddings
embedding = FakeEmbeddings(size=1536)

vectorstore = FAISS.from_documents(split_docs, embedding)

# === RetrievalQA Setup ===
retriever = vectorstore.as_retriever()

custom_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="Answer briefly and clearly using only the information in the logs.\n\n{context}\n\nQ: {question}\nA:"
)

qa_chain = RetrievalQA.from_chain_type(
    llm=embedding_model,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=False,
    chain_type_kwargs={"prompt": custom_prompt}
)


# === CLI Mode (for Node.js call or terminal use) ===
def answer_query_cli(question):
    try:
        response = qa_chain.run(question)
        return response
    except Exception as e:
        return f"Error: {str(e)}"

# === Main execution ===
if __name__ == "__main__":
    if len(sys.argv) >= 2:
        question = sys.argv[1]
        answer = answer_query_cli(question)
        print(answer)
    else:
        # === Interactive Mode ===
        print("\n RAG Chatbot Ready. Ask questions from logs.csv like:")
        print("   • Who was the last person registered?")
        print("   • How many users are currently registered?\n")
        print("Type 'exit' to quit.\n")

        while True:
            try:
                query = input(" You: ")
                if query.strip().lower() == "exit":
                    print("Exiting. Bye!")
                    break
                response = qa_chain.run(query)
                print("Bot:", response)
            except KeyboardInterrupt:
                print("\nInterrupted. Bye!")
                break
            except Exception as e:
                print(" Error while answering:", str(e))
