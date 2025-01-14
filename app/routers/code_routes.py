from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.models.code_model import QwenCoderModel
from app.services.complexity_analyzer import ComplexityAnalyzer
from app.services.code_debug import CodeDebugger
from app.services.code_converter import CodeConverter

router = APIRouter()
model = QwenCoderModel()
analyzer = ComplexityAnalyzer()
debugger = CodeDebugger()
converter = CodeConverter()

class CodeRequest(BaseModel):
    code: str
    source_lang: Optional[str] = None
    target_lang: Optional[str] = None

@router.post("/debug")
async def debug_code(request: CodeRequest):
    try:
        debug_result = debugger.debug_code(request.code)
        return {
            "issues": debug_result.get("issues", []),
            "fixed_code": debug_result.get("fixed_code", ""),
            "summary": debug_result.get("summary", "No summary available")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in debugging: {str(e)}")

@router.post("/convert")
async def convert_code(request: CodeRequest):
    if not request.source_lang or not request.target_lang:
        raise HTTPException(status_code=400, detail="Source and target languages are required")
    try:
        result = converter.convert_code(
            request.code,
            request.source_lang,
            request.target_lang
        )
        if "error" in result:
            raise HTTPException(status_code=400, detail=result)
        return {"converted_code": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-complexity")
async def analyze_complexity(request: CodeRequest):
    try:
        analysis = analyzer.analyze_complexity(request.code)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

