import os
import time
from langchain_community.document_loaders import CSVLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

# === Set your Groq API Key and base ===
os.environ["OPENAI_API_KEY"] = "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"
GROQ_API_BASE = "https://api.groq.com/openai/v1"

# === Load and split CSV logs ===
csv_path = r"C:\Users\dhaks\Downloads\Katomaron\AI-Modules\face_recognition\logs.csv"
loader = CSVLoader(file_path=csv_path)
documents = loader.load()

splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
split_docs = splitter.split_documents(documents)

# === Embed using FAISS (no embeddings needed again if already persisted) ===
print("🔁 Embedding and indexing logs...")
embedding_model = ChatOpenAI(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    openai_api_key=os.environ["OPENAI_API_KEY"],
    openai_api_base=GROQ_API_BASE,
    temperature=0
)

# Since Groq does NOT support embeddings, use basic FAISS with dummy embedder for now.
from langchain.embeddings import FakeEmbeddings
embedding = FakeEmbeddings(size=1536)  # Same dim as OpenAI embeddings

vectorstore = FAISS.from_documents(split_docs, embedding)

# === RetrievalQA Setup ===
retriever = vectorstore.as_retriever()
qa_chain = RetrievalQA.from_chain_type(
    llm=embedding_model,
    chain_type="stuff",
    retriever=retriever
)

# === Chat interface ===
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
