from pydantic import BaseModel, EmailStr, ConfigDict
from enum import Enum
from typing import Optional
from datetime import datetime

class RequestType(str, Enum):
    LEAVE = "LEAVE"
    DEPLOYMENT = "DEPLOYMENT"
    EXPENSE = "EXPENSE"
    ACCESS = "ACCESS"
    DOCUMENT_REVIEW = "DOCUMENT_REVIEW"
    OTHER = "OTHER"

class Priority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class Status(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"

class ApprovalRequestCreate(BaseModel):
    title: str
    description: str
    request_type: RequestType
    requester_name: str
    requester_email: EmailStr
    approver_name: str
    approver_email: EmailStr
    priority: Priority

class ApprovalRequestResponse(BaseModel):
    id: int
    title: str
    description: str
    request_type: RequestType
    requester_name: str
    requester_email: EmailStr
    approver_name: str
    approver_email: EmailStr
    #approver_role: str
    priority: Priority
    status: Status
    decision_comment: str | None = None
    created_at: datetime
    updated_at: datetime
    decision_at: datetime | None = None

class ApprovalDecision(BaseModel):
    decision_comment: str

class ApprovalHistoryResponse(BaseModel):
    id: int
    request_id: int
    old_status: Status
    new_status: Status
    action: str
    performed_by_name: str
    performed_by_email: str
    comment: str
    created_at: datetime
    
    class Config:
        orm_mode = True


