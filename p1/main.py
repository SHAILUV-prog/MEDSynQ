from intake_agent import run_intake_agent
from clinical_agent import run_clinical_agent
from coordinator import run_coordinator

from models import (
    CoordinatorInput,
    EvidenceItem,
    EvidenceResult,
    SafetyResult,
    TrendResult,
    MetricTrend,
)


def main():

    user_input = input(
        "Describe the patient's symptoms or situation: "
    )

    # ---------------------------------------------------------
    # 1. INTAKE
    # ---------------------------------------------------------

    print("\nRunning Intake Agent...")

    intake_result = run_intake_agent(
        user_input
    )

    print("\nIntake Result:")
    print(intake_result)

    # ---------------------------------------------------------
    # 2. CLINICAL
    # ---------------------------------------------------------

    print("\nRunning Clinical Agent...")

    clinical_result = run_clinical_agent(
        intake_result
    )

    print("\nClinical Result:")
    print(clinical_result)

    # ---------------------------------------------------------
    # 3. MOCK P2 TREND RESULT
    # ---------------------------------------------------------

    trend_result = TrendResult(
        status="ANALYZED",
        trends=[
            MetricTrend(
                metric="SpO2",
                direction="decreasing",
                absolute_change=-5,
                percentage_change=-5.15,
                baseline_deviation=-5,
                monotonic_deterioration=True,
            )
        ],
        deterioration_detected=True,
        missing_observations=[],
    )

    # ---------------------------------------------------------
    # 4. MOCK P2 SAFETY RESULT
    # ---------------------------------------------------------

    safety_result = SafetyResult(
        status="URGENT",
        triggered_rules=[
            "Worsening respiratory presentation"
        ],
        missing_required_data=[],
        safety_findings=[
            "Clinical presentation requires urgent human review."
        ],
        rationale=[
            "Worsening respiratory symptoms combined with "
            "declining oxygen saturation trend."
        ],
    )

    # ---------------------------------------------------------
    # 5. MOCK P3 EVIDENCE RESULT
    # ---------------------------------------------------------

    evidence_result = EvidenceResult(
        status="EVIDENCE_FOUND",
        evidence=[
            EvidenceItem(
                source="Example Clinical Guideline",
                page_or_section="Acute respiratory assessment",
                relevance_score=0.91,
                text=(
                    "Worsening respiratory symptoms should be assessed "
                    "using current physiological measurements and "
                    "clinical examination."
                ),
            )
        ],
        supported_considerations=[
            "Acute respiratory causes require further clinical evaluation."
        ],
        conflicting_evidence=[],
    )

    # ---------------------------------------------------------
    # 6. BUILD COORDINATOR INPUT
    # ---------------------------------------------------------

    coordinator_input = CoordinatorInput(
        patient=intake_result,
        clinical=clinical_result,
        evidence=evidence_result,
        trend=trend_result,
        safety=safety_result,
    )

    # ---------------------------------------------------------
    # 7. CARE COORDINATOR
    # ---------------------------------------------------------

    print("\nRunning Care Coordinator...")

    coordinator_result = run_coordinator(
        coordinator_input
    )

    print("\nCoordinator Result:")
    print(coordinator_result)


if __name__ == "__main__":
    main()