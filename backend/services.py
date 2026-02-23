import httpx
from fastapi import HTTPException
from typing import List

from backend.config import AI_SERVICE_URL
from backend.models import (
    DrugInfo, DesignOption,
    SampleSizeRequest, SampleSizeResult,
    InclusionCriteriaRequest, InclusionCriteriaResult,
    ValidationRequest, ValidationResult
)

# ------------------ Клиент для внешнего ИИ-сервиса ------------------

async def call_ai_service(endpoint: str, payload: dict) -> dict:
    """
    Асинхронно вызывает внешний ИИ-сервис по указанному эндпоинту.

    Аргументы:
        endpoint: путь к методу (например, "/generate-criteria")
        payload: данные запроса в виде словаря

    Возвращает:
        ответ сервиса в виде словаря (JSON)

    Исключения:
        HTTPException 503, если сервис недоступен или произошла ошибка.
    """
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(
                f"{AI_SERVICE_URL}{endpoint}",
                json=payload,
                timeout=30.0
            )
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"AI service unavailable: {e}")

# ------------------ Генерация дизайна ------------------

def generate_design_options(drug: DrugInfo, condition: str) -> List[DesignOption]:
    """
    Генерирует список возможных дизайнов исследования на основе информации о препарате
    и условиях приёма. В текущей версии возвращает фиксированные варианты (заглушка).

    Аргументы:
        drug: информация о препарате (объект DrugInfo)
        condition: режим приёма ("натощак" или "после еды")

    Возвращает:
        список объектов DesignOption
    """
    # Здесь может быть вызов ИИ или более сложная логика
    return [
        DesignOption(
            name="2x2 crossover",
            description="Двухпериодный перекрестный дизайн",
            rationale="Стандартный дизайн для изучения биоэквивалентности",
            parameters={"periods": 2, "sequences": 2, "washout": "≥5 half-lives"}
        ),
        DesignOption(
            name="replicate crossover",
            description="Репликативный перекрестный дизайн (4 периода)",
            rationale="Используется для высоковариабельных препаратов",
            parameters={"periods": 4, "sequences": 2, "washout": "≥5 half-lives"}
        )
    ]

# ------------------ Расчёт размера выборки ------------------

def calculate_sample_size(request: SampleSizeRequest) -> SampleSizeResult:
    """
    Рассчитывает необходимый размер выборки для исследования биоэквивалентности
    методом TOST (двусторонний t-критерий). В текущей версии возвращает
    фиксированные значения (заглушка).

    Аргументы:
        request: объект SampleSizeRequest с параметрами расчёта

    Возвращает:
        объект SampleSizeResult с результатами
    """
    # Здесь должен быть вызов статистической библиотеки (например, statsmodels)
    base_n = 24
    dropout = int(base_n * 0.15)
    screened = int(base_n * 1.2)
    return SampleSizeResult(
        n_subjects=base_n,
        n_dropout=dropout,
        n_screened=screened,
        assumptions={
            "cv_intra": request.cv_intra,
            "expected_ratio": request.expected_ratio,
            "alpha": request.alpha,
            "power": request.power,
            "design": request.design
        }
    )

# ------------------ Генерация критериев включения/исключения ------------------

async def generate_inclusion_criteria(request: InclusionCriteriaRequest) -> InclusionCriteriaResult:
    """
    Генерирует списки критериев включения и исключения.
    Сначала пытается вызвать внешний ИИ-сервис, в случае неудачи
    возвращает шаблонные критерии (заглушка).

    Аргументы:
        request: объект InclusionCriteriaRequest с данными

    Возвращает:
        объект InclusionCriteriaResult
    """
    try:
        # Пытаемся получить данные от ИИ
        ai_result = await call_ai_service("/generate-criteria", request.dict())
        return InclusionCriteriaResult(**ai_result)
    except:
        # Заглушка на случай ошибки
        return InclusionCriteriaResult(
            inclusion=[
                f"Мужчины и женщины в возрасте от {request.age_range[0]} до {request.age_range[1]} лет",
                f"ИМТ от {request.bmi_range[0]} до {request.bmi_range[1]} кг/м²",
                "Отсутствие клинически значимых отклонений",
                "Подписанное информированное согласие"
            ],
            exclusion=[
                "Наличие хронических заболеваний",
                "Приём любых лекарств за 30 дней до скрининга",
                f"Гиперчувствительность к {request.drug_info.active_substance}",
                "Беременность или лактация"
            ],
            rationale="Критерии разработаны на основе типовых требований."
        )

# ------------------ Валидация данных ------------------

def validate_design(request: ValidationRequest) -> ValidationResult:
    """
    Проверяет собранные данные на соответствие регуляторным требованиям
    (например, Решение 85). Выявляет потенциальные риски.

    Аргументы:
        request: объект ValidationRequest с данными о дизайне, выборке и критериях

    Возвращает:
        объект ValidationResult с результатами проверки
    """
    risks = []
    if request.design.get("name") == "2x2 crossover" and request.sample_size.get("n_subjects", 0) < 12:
        risks.append("Недостаточный размер выборки для 2x2 дизайна")
    return ValidationResult(
        compliant=len(risks) == 0,
        risks=risks,
        warnings=["Необходимо проверить отмывочный период"],
        references=["Решение Совета ЕЭК №85", "ICH E9"]
    )