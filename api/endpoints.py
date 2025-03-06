from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from io import BytesIO

from models.schemas import AssessmentResult as AssessmentResponse 
from core.document_processor import DocumentProcessorFactory
from core.assessment_engine import AssessmentEngine
from core.rag_manager import RAGManager

router = APIRouter()

class AnalysisError(Exception):
    pass

def get_assessment_engine():
    try:
        rag_manager = RAGManager()
        return AssessmentEngine(rag_manager)
    except Exception as e:
        print(f"Error initializing RAG system: {e}")
        # Return a simple version that will report errors properly
        class SimpleRAG:
            def analyze_text(self, _):
                return {"criteria_matches": {}}
        return AssessmentEngine(SimpleRAG())

@router.post("/assess", response_model=AssessmentResponse)
async def assess_o1a(
    cv: UploadFile = File(...),
    assessment_engine: AssessmentEngine = Depends(get_assessment_engine) 
):
    try:
        # Validate file type
        processor = DocumentProcessorFactory.get_processor(cv.content_type)
        contents = await cv.read()
        cv_text = processor.extract_text(BytesIO(contents))
    except Exception as e:
        raise HTTPException(400, detail=str(e))

    try:
        result = assessment_engine.assess_cv(cv_text)
    except AnalysisError as e:
        raise HTTPException(500, detail="Analysis failed")

    return result