# ==================== backend/routers.py ====================
from io import BytesIO
from pathlib import Path
from typing import Dict, List, Optional
from pydantic import BaseModel
import re  

from fastapi import APIRouter, Response, HTTPException, Request
from docx import Document

# =====================================================
# ВЫБЕРИТЕ НУЖНЫЙ МОДУЛЬ (должен совпадать с выбранным в llm_integration.py)
# =====================================================
#from backend import llm_functions as llm_module          # реальные функции
from backend import llm_functions_mock as llm_module   # мок-функции
# =====================================================

from backend.models import (
    DesignRequest, DesignOption,
    SampleSizeRequest, SampleSizeResult,
    InclusionCriteriaRequest, InclusionCriteriaResult,
    ValidationRequest, ValidationResult,
    SynopsisRequest
)
from backend.services import (
    generate_design_options,
    calculate_sample_size,
    generate_inclusion_criteria,
    validate_design
)
from backend.utils import replace_placeholders_in_doc
from backend.llm_integration import run_llm_sequence
import asyncio
from functools import partial

router = APIRouter()

# ==================== МОДЕЛИ ====================
class LLMSynopsisRequest(BaseModel):
    protocol_id: Optional[str] = None
    sponsor_name: Optional[str] = None
    study_center: Optional[str] = None
    bioanalytical_lab_name: Optional[str] = None
    drug_name: Optional[str] = None
    active_substance: str
    gender_allowed: Optional[str] = None
    prior_study_exclusion_months: Optional[str] = None
    dosage_form: str
    dosage: str
    
    additional_vars: Optional[Dict[str, str]] = {}

# ------------------ Дизайн исследования ------------------
@router.post("/api/design/options", response_model=List[DesignOption])
async def get_design_options(request: DesignRequest):
    options = generate_design_options(request.drug_info, request.intake_condition)
    return options

# ------------------ Расчёт размера выборки ------------------
@router.post("/api/sample-size/calculate", response_model=SampleSizeResult)
async def calculate_sample_size_endpoint(request: SampleSizeRequest):
    return calculate_sample_size(request)

# ------------------ Генерация критериев включения/исключения ------------------
# ТЕПЕРЬ ЭТОТ ЭНДПОИНТ ГЕНЕРИРУЕТ СИНОПСИС (docx)
@router.post("/api/inclusion-criteria/generate", response_model=None)
async def generate_criteria_endpoint(request: LLMSynopsisRequest):
    user_vars = request.dict(exclude_unset=True)
    
    user_vars.pop("active_substance", None)
    user_vars.pop("dosage_form", None)
    user_vars.pop("dosage", None)

    loop = asyncio.get_event_loop()
    func = partial(
        run_llm_sequence,
        active_substance=request.active_substance,
        dosage_form=request.dosage_form,
        dosage=request.dosage,
        user_vars=user_vars
    )
    llm_vars = await loop.run_in_executor(None, func)

    all_vars = llm_vars
    template_path = Path(__file__).parent / "template.docx"
    if not template_path.exists():
        raise HTTPException(status_code=500, detail="Файл template.docx не найден")
    doc = Document(str(template_path))
    replace_placeholders_in_doc(doc, all_vars)
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    protocol_id = all_vars.get("protocol_id", "synopsis")
    filename = f"synopsis_{protocol_id}.docx"
    return Response(
        content=buffer.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

# ------------------ Валидация ------------------
@router.post("/api/validate", response_model=ValidationResult)
async def validate_endpoint(request: ValidationRequest):
    return validate_design(request)

# ------------------ Генерация синопсиса с LLM ------------------

@router.post("/api/synopsis/generate-with-llm", response_model=InclusionCriteriaResult)
async def generate_synopsis_with_llm(request: InclusionCriteriaRequest):
    return await generate_inclusion_criteria(request)

# ------------------ Старый эндпоинт для обратной совместимости ------------------
@router.post("/generate", response_model=None)
@router.get("/generate", response_model=None)
async def generate_synopsis_legacy(request: Request):

    if request.method == "GET":
        variables = dict(request.query_params)
    else:
        try:
            variables = await request.json()
        except Exception:
            variables = {}
    variables = {k: str(v) for k, v in variables.items() if v is not None}

    
    active_substance = variables.get("active_substance", "ибупрофен")
    dosage_form = variables.get("dosage_form", "таблетки")
    dosage = variables.get("dosage", "200 мг")

    
    user_vars = variables.copy()
    user_vars.pop("active_substance", None)
    user_vars.pop("dosage_form", None)
    user_vars.pop("dosage", None)

    
    loop = asyncio.get_event_loop()
    func = partial(
        run_llm_sequence,
        active_substance=active_substance,
        dosage_form=dosage_form,
        dosage=dosage,
        user_vars=user_vars
    )
    llm_vars = await loop.run_in_executor(None, func)

    all_vars = llm_vars
    template_path = Path(__file__).parent / "template.docx"
    if not template_path.exists():
        raise HTTPException(status_code=500, detail="Файл template.docx не найден")
    doc = Document(str(template_path))
    replace_placeholders_in_doc(doc, all_vars)
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    protocol_id = all_vars.get("protocol_id", "synopsis")
    filename = f"synopsis_{protocol_id}.docx"
    return Response(
        content=buffer.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

# ------------------ test ------------------
@router.post("/api/test")
async def get_test(city: str):
    test = llm_module.test_query(city)
    return test