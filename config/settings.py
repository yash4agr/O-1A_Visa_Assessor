from pydantic_settings import BaseSettings
from typing import Dict, List, ClassVar

class Settings(BaseSettings):
    # Together AI models
    embedding_model: str = "togethercomputer/m2-bert-80M-32k-retrieval"
    llm_model: str = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"
    
    # API key for Together AI
    together_api_key: str = ""
    
    knowledge_dir: str = "knowledge_base/"
    chunk_size: int = 250
    chunk_overlap: int = 25
    search_k: int = 3
    rating_thresholds: Dict[str, float] = {
        'high': 0.85,
        'medium': 0.6,
        'low': 0.3
    }
    CRITERIA: ClassVar[List[str]] = [
        "Awards",
        "Membership",
        "Press",
        "Judging",
        "Original contribution",
        "Scholarly articles", 
        "Critical employment",
        "High remuneration"
    ]

    class Config:
        env_file = ".env"

settings = Settings()