from pydantic import BaseModel, Field


# ============================================================
# PATIENT / INTAKE
# ============================================================

class IntakeResult(BaseModel):
    age: int | None = None
    gender: str | None = None

    symptoms: list[str] = Field(default_factory=list)
    duration: str | None = None
    progression: str | None = None

    medical_history: list[str] = Field(default_factory=list)
    medications: list[str] = Field(default_factory=list)
    observations: list[str] = Field(default_factory=list)

    missing_information: list[str] = Field(default_factory=list)


# ============================================================
# CLINICAL AGENT
# ============================================================

class ClinicalResult(BaseModel):
    findings: list[str]
    risk_categories: list[str]
    relevant_factors: list[str]
    possible_conditions: list[str]
    supporting_observations: list[str]
    uncertainty: str
    additional_information_needed: list[str]
    rag_query: str


# ============================================================
# TREND ENGINE / P2
# ============================================================

class MetricTrend(BaseModel):
    metric: str
    direction: str
    absolute_change: float | None = None
    percentage_change: float | None = None
    baseline_deviation: float | None = None
    monotonic_deterioration: bool = False


class TrendResult(BaseModel):
    status: str
    trends: list[MetricTrend] = Field(default_factory=list)
    deterioration_detected: bool
    missing_observations: list[str] = Field(default_factory=list)


# ============================================================
# SAFETY ENGINE / P2
# ============================================================

class SafetyResult(BaseModel):
    status: str

    triggered_rules: list[str] = Field(
        default_factory=list
    )

    missing_required_data: list[str] = Field(
        default_factory=list
    )

    safety_findings: list[str] = Field(
        default_factory=list
    )

    rationale: list[str] = Field(
        default_factory=list
    )


# ============================================================
# RAG / EVIDENCE / P3
# ============================================================

class EvidenceItem(BaseModel):
    source: str
    page_or_section: str
    relevance_score: float
    text: str


class EvidenceResult(BaseModel):
    status: str

    evidence: list[EvidenceItem] = Field(
        default_factory=list
    )

    supported_considerations: list[str] = Field(
        default_factory=list
    )

    conflicting_evidence: list[str] = Field(
        default_factory=list
    )


# ============================================================
# INFORMATION REQUEST
# ============================================================

class InformationRequest(BaseModel):
    questions: list[str] = Field(default_factory=list)
    reason: str


# ============================================================
# CARE COORDINATOR
# ============================================================

class CoordinatorInput(BaseModel):
    patient: IntakeResult
    clinical: ClinicalResult
    evidence: EvidenceResult
    trend: TrendResult
    safety: SafetyResult


class CoordinatorResult(BaseModel):
    status: str
    information_request: InformationRequest | None = None

    final_assessment: str

    key_findings: list[str] = Field(
        default_factory=list
    )

    evidence_summary: list[str] = Field(
        default_factory=list
    )

    trend_summary: list[str] = Field(
        default_factory=list
    )

    safety_status: str

    uncertainty: str