from dataclasses import dataclass, field

from models import ClinicalResult, SafetyResult, IntakeResult


MAX_INFORMATION_ROUNDS = 3


@dataclass
class ConversationState:
    information_round: int = 0

    asked_information: list[str] = field(
        default_factory=list
    )

    unavailable_information: list[str] = field(
        default_factory=list
    )

    additional_user_information: list[str] = field(
        default_factory=list
    )

    open_information_request_made: bool = False


def record_question(
    state: ConversationState,
    question_topic: str
) -> None:
    """Record a targeted information request."""

    if question_topic not in state.asked_information:
        state.asked_information.append(question_topic)


def record_unavailable_information(
    state: ConversationState,
    information: str
) -> None:
    """Record information the user cannot provide."""

    if information not in state.unavailable_information:
        state.unavailable_information.append(information)


def record_additional_information(
    state: ConversationState,
    information: str
) -> None:
    """Store useful information volunteered by the user."""

    if information.strip():
        state.additional_user_information.append(
            information
        )


def can_ask_again(
    state: ConversationState
) -> bool:
    """Check whether another information round is allowed."""

    return (
        state.information_round
        < MAX_INFORMATION_ROUNDS
    )


def start_information_round(
    state: ConversationState
) -> None:
    """Start the next information-gathering round."""

    if not can_ask_again(state):
        raise RuntimeError(
            "Maximum information-gathering rounds reached."
        )

    state.information_round += 1


def get_requestable_information(
    state: ConversationState,
    clinical_result: ClinicalResult,
    safety_result: SafetyResult
) -> list[str]:
    """
    Determine which information can still be requested.

    Safety requirements have priority.
    Clinical requests are advisory.
    """

    if not can_ask_again(state):
        return []

    requestable = []

    # Safety-required information gets priority.
    for item in safety_result.missing_required_data:

        if item in state.asked_information:
            continue

        if item in state.unavailable_information:
            continue

        requestable.append(item)

    # Clinical requests come after Safety requirements.
    for item in clinical_result.additional_information_needed:

        if item in state.asked_information:
            continue

        if item in state.unavailable_information:
            continue

        if item not in requestable:
            requestable.append(item)

    return requestable


def select_information_for_round(
    state: ConversationState,
    clinical_result: ClinicalResult,
    safety_result: SafetyResult,
    max_items: int = 2
) -> list[str]:
    """
    Select a small number of high-value requests.
    """

    requestable = get_requestable_information(
        state,
        clinical_result,
        safety_result
    )

    return requestable[:max_items]


def build_final_information_request(
    state: ConversationState,
    clinical_result: ClinicalResult,
    safety_result: SafetyResult
) -> list[str]:
    """
    Build the third and final information request.

    Round 3 contains:
    - at most one targeted request
    - one open-ended opportunity for additional information
    """

    if state.information_round != MAX_INFORMATION_ROUNDS - 1:
        raise ValueError(
            "Final information request must be "
            "prepared before Round 3."
        )

    requestable = get_requestable_information(
        state,
        clinical_result,
        safety_result
    )

    questions = []

    # At most one specific request.
    if requestable:
        questions.append(requestable[0])

    # Open-ended final opportunity.
    questions.append(
        "Is there anything else about the patient's symptoms, "
        "medical history, medications, recent changes, or "
        "measurements that you think may be relevant?"
    )

    state.open_information_request_made = True

    return questions


def merge_intake_results(
    existing: IntakeResult,
    new: IntakeResult
) -> IntakeResult:
    """
    Merge newly extracted information into the existing
    patient state.

    Rules:
    - New non-empty scalar values replace old values.
    - New non-empty list values are appended.
    - Empty lists do not erase existing information.
    - None scalar values do not erase existing information.
    - Duplicate list entries are not added.
    """

    merged = existing.model_copy(deep=True)

    # Scalar fields
    if new.age is not None:
        merged.age = new.age

    if new.gender is not None:
        merged.gender = new.gender

    if new.duration is not None:
        merged.duration = new.duration

    if new.progression is not None:
        merged.progression = new.progression

    # List fields
    list_fields = [
        "symptoms",
        "medical_history",
        "medications",
        "observations",
    ]

    for field_name in list_fields:

        existing_values = getattr(
            merged,
            field_name
        )

        new_values = getattr(
            new,
            field_name
        )

        for value in new_values:
            if value not in existing_values:
                existing_values.append(value)

    return merged


def process_new_patient_information(
    existing_patient: IntakeResult,
    new_information: IntakeResult
) -> IntakeResult:
    """Merge a new Intake result into the patient state."""

    return merge_intake_results(
        existing_patient,
        new_information
    )