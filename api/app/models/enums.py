from enum import StrEnum


class ApplicationStage(StrEnum):
    SAVED = "saved"
    APPLIED = "applied"
    INTERVIEWING = "interviewing"
    OFFERED = "offered"
    REJECTED = "rejected"


class ScrapeStatus(StrEnum):
    NOT_APPLICABLE = "not_applicable"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class DocType(StrEnum):
    RESUME = "resume"
    COVER_LETTER = "cover_letter"
    OTHER = "other"


class ReminderKind(StrEnum):
    NO_RESPONSE = "no_response"
    INTERVIEW_PREP = "interview_prep"
    PUSH_NOTIFICATION = "push_notification"


class ReminderStatus(StrEnum):
    PENDING = "pending"
    DISMISSED = "dismissed"
