from io import BytesIO
from pathlib import Path
from typing import Dict, List

from fastapi import APIRouter, Response, HTTPException
from docx import Document

from backend.config import DEFAULTS
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

# Создаём основной роутер
router = APIRouter()

# ------------------ Дизайн исследования ------------------

@router.post("/api/design/options", response_model=List[DesignOption])
async def get_design_options(request: DesignRequest):
    """
    Возвращает список возможных дизайнов исследования на основе
    информации о препарате и условиях приёма.
    """
    options = generate_design_options(request.drug_info, request.intake_condition)
    return options

# ------------------ Расчёт размера выборки ------------------

@router.post("/api/sample-size/calculate", response_model=SampleSizeResult)
async def calculate_sample_size_endpoint(request: SampleSizeRequest):
    """
    Рассчитывает необходимый размер выборки на основе входных параметров.
    """
    return calculate_sample_size(request)

# ------------------ Генерация критериев включения/исключения ------------------

@router.post("/api/inclusion-criteria/generate", response_model=InclusionCriteriaResult)
async def generate_criteria_endpoint(request: InclusionCriteriaRequest):
    """
    Генерирует критерии включения и исключения для добровольцев.
    Может использовать ИИ или шаблонные правила.
    """
    return await generate_inclusion_criteria(request)

# ------------------ Валидация ------------------

@router.post("/api/validate", response_model=ValidationResult)
async def validate_endpoint(request: ValidationRequest):
    """
    Проверяет собранные данные на соответствие регуляторным требованиям
    и возвращает список рисков и предупреждений.
    """
    return validate_design(request)

# ------------------ Генерация синопсиса ------------------

@router.post("/api/synopsis/generate", response_class=Response)
async def generate_synopsis(request: SynopsisRequest):
    """
    Принимает плоский словарь переменных, подставляет их в шаблон template.docx
    и возвращает готовый DOCX-файл для скачивания.
    """
    all_vars = {**DEFAULTS, **request.variables}
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

@router.post("/generate", response_class=Response)
async def generate_synopsis_legacy(variables: Dict[str, str] = {}):
    """
    Старый эндпоинт для обратной совместимости. Принимает простой словарь переменных
    и возвращает DOCX-файл.
    """
    all_vars = {**DEFAULTS, **variables}
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