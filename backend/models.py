from typing import Dict, List, Any, Optional
from pydantic import BaseModel

# Модели данных для запросов и ответов API

class DrugInfo(BaseModel):
    """Информация о препарате (исследуемый или референтный)."""
    drug_name: str
    active_substance: str
    dosage_form: str
    dosage: str
    route: str = "per os"  # путь введения

class DesignRequest(BaseModel):
    """Запрос на получение вариантов дизайна."""
    drug_info: DrugInfo
    intake_condition: str  # "натощак" или "после еды"
    preferred_design: Optional[str] = None

class DesignOption(BaseModel):
    """Один вариант дизайна исследования."""
    name: str
    description: str
    rationale: str          # обоснование
    parameters: Dict[str, Any]

class SampleSizeRequest(BaseModel):
    """Запрос на расчёт размера выборки."""
    cv_intra: float
    expected_ratio: float = 0.95
    alpha: float = 0.05
    power: float = 0.8
    design: str

class SampleSizeResult(BaseModel):
    """Результат расчёта размера выборки."""
    n_subjects: int
    n_dropout: int
    n_screened: int
    assumptions: Dict[str, Any]

class InclusionCriteriaRequest(BaseModel):
    """Запрос на генерацию критериев включения/исключения."""
    drug_info: DrugInfo
    population: str = "здоровые добровольцы"
    age_range: List[int] = [18, 45]
    bmi_range: List[float] = [18.5, 30.0]

class InclusionCriteriaResult(BaseModel):
    """Сгенерированные критерии."""
    inclusion: List[str]
    exclusion: List[str]
    rationale: str

class ValidationRequest(BaseModel):
    """Запрос на проверку соответствия требованиям."""
    design: Dict[str, Any]
    sample_size: Dict[str, Any]
    criteria: Dict[str, Any]

class ValidationResult(BaseModel):
    """Результат проверки."""
    compliant: bool
    risks: List[str]
    warnings: List[str]
    references: List[str]

class SynopsisRequest(BaseModel):
    """Запрос на финальную генерацию синопсиса (плоский словарь строк)."""
    variables: Dict[str, str]