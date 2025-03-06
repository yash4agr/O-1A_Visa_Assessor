from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import Embeddings
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from together import Together

from pathlib import Path
from typing import List
import os
import re

from config.prompts import ANALYSIS_PROMPT
from config.settings import settings

class TogetherEmbeddings(Embeddings):
    """Wrapper for Together AI embeddings."""
    
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.client = Together()
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents using Together API."""
        embeddings = []
        # Process in batches to avoid API limits
        for text in texts:
            response = self.client.embeddings.create(
                model=self.model_name,
                input=text,
            )
            embeddings.append(response.data[0].embedding)
        return embeddings
    
    def embed_query(self, text: str) -> List[float]:
        """Embed a query using Together API."""
        response = self.client.embeddings.create(
            model=self.model_name,
            input=text,
        )
        return response.data[0].embedding

class RAGManager:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap
        )
        
        self.embeddings = TogetherEmbeddings(
            model_name=settings.embedding_model
        )
        self.vectorstore = self._initialize_vectorstore()
        
        self.llm = ChatOpenAI(
            model=settings.llm_model,
            openai_api_key=os.environ.get("TOGETHER_API_KEY"),
            openai_api_base="https://api.together.xyz/v1"
        )
        self.qa_chain = self._create_qa_chain()

    def _initialize_vectorstore(self):
        # Load and process knowledge documents
        documents = self._load_knowledge_documents()
        texts = self.text_splitter.split_documents(documents)
        return FAISS.from_documents(texts, self.embeddings)

    def _load_knowledge_documents(self):
        knowledge_path = Path(settings.knowledge_dir)
        if not knowledge_path.exists():
            raise FileNotFoundError(f"Knowledge directory not found: {settings.knowledge_dir}")
        
        # Load different file types
        loaders = {
            "*.pdf": DirectoryLoader(settings.knowledge_dir, glob="**/*.pdf", loader_cls=PyPDFLoader),
            "*.txt": DirectoryLoader(settings.knowledge_dir, glob="**/*.txt", loader_cls=TextLoader),
            "*.docx": DirectoryLoader(settings.knowledge_dir, glob="**/*.docx", loader_cls=Docx2txtLoader)
        }
        
        documents = []
        for loader in loaders.values():
            try:
                documents.extend(loader.load())
            except Exception as e:
                print(f"Error loading documents: {e}")
        
        return documents

    def _create_qa_chain(self):
        return RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(
                search_kwargs={"k": settings.search_k}
            )
        )

    def analyze_text(self, text: str) -> dict:
        text = self._preprocess_text(text)
        result = self.qa_chain.invoke({
            "query": ANALYSIS_PROMPT.format(context=text)
        })
        return self._parse_response(result["result"])

    def _preprocess_text(self, text: str) -> str:
        """Preprocess text for consistency across file formats."""
        
        
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r'(\w+)-\s+(\w+)', r'\1\2', text)
        
        return text

    def _parse_response(self, response: str) -> dict:
        import json
        
        try:
            # Find JSON content
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                result = json.loads(json_str)
                
                # Filter out empty or "None"
                if "criteria_matches" in result:
                    for criterion, matches in list(result["criteria_matches"].items()):
                        result["criteria_matches"][criterion] = [
                            match for match in matches 
                            if match.get("evidence") and match.get("evidence").lower() != "none"
                        ]
                        
                        # Remove empty criteria lists
                        if not result["criteria_matches"][criterion]:
                            del result["criteria_matches"][criterion]
                
                return result
            return json.loads(response)
        except json.JSONDecodeError as e:
            # Fallback to a minimal structure if parsing fails
            print(f"Error parsing LLM response: {e}")
            return {
                "criteria_matches": {},
                "error": "Failed to parse LLM response"
            }