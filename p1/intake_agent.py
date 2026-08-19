from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field
import os

from .models import IntakeResult


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY is not set. Check your .env file."
    )

client = genai.Client(api_key=api_key)


class IntakeExtraction(BaseModel):
    age: int | None
    gender: str | None

    symptoms: list[str] = Field(default_factory=list)
    duration: str | None
    progression: str | None

    medical_history: list[str] = Field(default_factory=list)
    medications: list[str] = Field(default_factory=list)
    observations: list[str] = Field(default_factory=list)


SYSTEM_INSTRUCTION = """
You are the Intake Agent for CareSync AI.

Your job is to convert unstructured patient information into
structured patient information.

Your PRIMARY objective is FACT PRESERVATION.

Every explicit patient fact stated by the user must be captured
in the appropriate output field. Do not drop explicitly stated
information just because it is not related to the main symptom.

Extract:
- age
- gender
- symptoms
- duration
- progression
- medical history
- medications
- observations

Rules:
- Do not diagnose.
- Do not assess clinical risk.
- Do not prescribe treatment.
- Do not invent any information.
- Do not infer information that was not stated.
- Do not discard explicit background information.
- If information is not provided, use null for scalar fields
  and an empty list for list fields.
- Normalize obvious wording differences while preserving meaning.
- Do not decide what information is clinically important.
- Do not decide what the application should ask next.
- Do not create a medical questionnaire.

Medical history:
- If a user explicitly states a known or existing condition,
  place it in medical_history.
- Example: "I have hypertension."
  → medical_history = ["hypertension"]

Medications:
- If a user explicitly states that they take a medication,
  place it in medications.
- Example: "I take amlodipine."
  → medications = ["amlodipine"]

Symptoms:
- Extract every explicitly stated symptom.

Age and gender:
- Extract them only when explicitly provided.

Observations:
- Extract explicitly stated measurements or physical observations
  that do not belong in the other fields.

Return only structured JSON.
"""


def _preserve_explicit_facts(
    user_input: str,
    extracted: IntakeResult
) -> IntakeResult:
    """
    Deterministic safeguard for simple, explicitly stated
    medical-history and medication phrases.

    This is not intended to replace language understanding.
    It prevents obvious explicit facts from being lost.
    """

    text = user_input.lower()

    # Common explicit medical-history patterns.
    history_patterns = {
        "hypertension": [
            "i have hypertension",
            "i have high blood pressure",
            "history of hypertension",
            "history of high blood pressure",
            "has hypertension",
            "has high blood pressure",
        ],
        "asthma": [
            "i have asthma",
            "history of asthma",
            "has asthma",
        ],
        "diabetes": [
            "i have diabetes",
            "history of diabetes",
            "has diabetes",
        ],
    }

    for condition, patterns in history_patterns.items():
        if any(pattern in text for pattern in patterns):
            if condition not in extracted.medical_history:
                extracted.medical_history.append(condition)

    # Common explicit medication patterns.
    known_medications = [
        "amlodipine",
        "metformin",
        "insulin",
    ]

    for medication in known_medications:
        phrases = [
            f"take {medication}",
            f"takes {medication}",
            f"on {medication}",
            f"using {medication}",
            f"use {medication}",
        ]

        if any(phrase in text for phrase in phrases):
            if medication not in extracted.medications:
                extracted.medications.append(medication)

    return extracted


def run_intake_agent(
    user_input: str
) -> IntakeResult:

    if not user_input.strip():
        raise ValueError(
            "Patient input cannot be empty."
        )

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=user_input,
        system_instruction=SYSTEM_INSTRUCTION,
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": IntakeExtraction.model_json_schema()
        },
    )

    extraction = IntakeExtraction.model_validate_json(
        interaction.output_text
    )

    intake_result = IntakeResult(
        age=extraction.age,
        gender=extraction.gender,
        symptoms=extraction.symptoms,
        duration=extraction.duration,
        progression=extraction.progression,
        medical_history=extraction.medical_history,
        medications=extraction.medications,
        observations=extraction.observations,
        missing_information=[]
    )

    return _preserve_explicit_facts(
        user_input,
        intake_result
    )


if __name__ == "__main__":

    user_input = input(
        "Describe the patient's symptoms or situation: "
    )

    print("\nRunning Intake Agent...")

    intake_result = run_intake_agent(user_input)

    print("\nValidated Intake Result:")
    print(intake_result)