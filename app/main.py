from fastapi import FastAPI, Depends, HTTPException
from database import engine, Base, get_db
import models
from datetime import datetime
from sqlalchemy.orm import Session
from typing import Optional
from auth import get_api_key
from schemas import (
    ApprovalDecision,
    ApprovalRequestCreate,
    ApprovalRequestResponse,
    ApprovalHistoryResponse
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Approval Request API",
)


@app.get("/")
def root():
    return {"message": "API running"}


@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post(
    "/approval-requests",
    response_model=ApprovalRequestResponse
)
def create_request(
    request: ApprovalRequestCreate,
    db: Session = Depends(get_db)
):
    new_request = models.ApprovalRequest(
        title=request.title,
        description=request.description,
        request_type=request.request_type,
        requester_name=request.requester_name,
        requester_email=request.requester_email,
        approver_name=request.approver_name,
        approver_email=request.approver_email,
        priority=request.priority
    ) 

    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    history = models.ApprovalHistory(
        request_id=new_request.id,
        old_status="PENDING",
        new_status="PENDING",
        action="CREATED",
        performed_by_name=new_request.requester_name,
        performed_by_email=new_request.requester_email,
        comment="Request created"
    )

    db.add(history)
    db.commit()

    return new_request

@app.get(
    "/approval-requests",
     response_model=list[ApprovalRequestResponse]

)
def get_requests(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    request_type: Optional[str] = None,
    requester_email: Optional[str] = None,
    approver_email: Optional[str] = None,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
    
):
     query = db.query(models.ApprovalRequest)

     if status:
        query = query.filter(
            models.ApprovalRequest.status == status
        )

     if priority:
        query = query.filter(
            models.ApprovalRequest.priority == priority
        )

     if request_type:
        query = query.filter(
            models.ApprovalRequest.request_type == request_type
        )

     if requester_email:
        query = query.filter(
            models.ApprovalRequest.requester_email == requester_email
        )

     if approver_email:
        query = query.filter(
            models.ApprovalRequest.approver_email == approver_email
        )

     requests = query.all()
     return requests

@app.get(
    "/approval-requests/{request_id}",
    response_model=ApprovalRequestResponse
)
def get_request_by_id(
    request_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    request = (
        db.query(models.ApprovalRequest)
        .filter(models.ApprovalRequest.id == request_id)
        .first()
    )

    if not request:
        raise HTTPException(
            status_code=404,
            detail="Request not found"
        )

    return request
    
@app.put(
    "/approval-requests/{request_id}/approve",
    response_model=ApprovalRequestResponse
)
def approve_request(
    request_id: int,
    decision: ApprovalDecision,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    request = (
        db.query(models.ApprovalRequest)
        .filter(models.ApprovalRequest.id == request_id)
        .first()
    )

    if not request:
        raise HTTPException(
            status_code=404,
            detail="request not found"
        )
    
    if request.status != "PENDING":
        raise HTTPException(
            status_code=400,
            detail="only pending requests can be approved"
        )
    
   

    old_status = request.status

    request.status = "APPROVED"
    request.decision_comment = decision.decision_comment
    request.decision_at = datetime.utcnow()

    history = models.ApprovalHistory(
        request_id=request.id,
        old_status=old_status,
        new_status="APPROVED",
        action="APPROVED",
        performed_by_name=request.approver_name,
        performed_by_email=request.approver_email,
        comment=decision.decision_comment
    )

    db.add(history)

    db.commit()
    db.refresh(request)

    return request

@app.put(
    "/approval-requests/{request_id}/cancel",
    response_model=ApprovalRequestResponse
)
def cancel_request(
    request_id: int,
    decision: ApprovalDecision,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    request = (
        db.query(models.ApprovalRequest)
        .filter(models.ApprovalRequest.id == request_id)
        .first()
    )

    if not request:
        raise HTTPException(
            status_code=404,
            detail="request not found"
        )

    if request.status != "PENDING":
        raise HTTPException(
            status_code=400,
            detail="only pending requests can be cancelled"
        )

    old_status = request.status

    request.status = "CANCELLED"
    request.decision_comment = decision.decision_comment
    request.decision_at = datetime.utcnow()

    history = models.ApprovalHistory(
        request_id=request.id,
        old_status=old_status,
        new_status="CANCELLED",
        action="CANCELLED",
        performed_by_name=request.approver_name,
        performed_by_email=request.approver_email,
        comment=decision.decision_comment
    )

    db.add(history)

    db.commit()
    db.refresh(request)

    return request

@app.put(
    "/approval-requests/{request_id}/reject",
    response_model=ApprovalRequestResponse
)
def reject_request(
    request_id: int,
    decision: ApprovalDecision,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    request = (
        db.query(models.ApprovalRequest)
        .filter(models.ApprovalRequest.id == request_id)
        .first()
    )

    if not request:
        raise HTTPException(
            status_code=404,
            detail="request not found"
        )
    
    if request.status != "PENDING":
        raise HTTPException(
            status_code=400,
            detail="only pending requests can be cancelled"
        )

    old_status = request.status

    request.status = "REJECTED"
    request.decision_comment = decision.decision_comment
    request.decision_at = datetime.utcnow()

    history = models.ApprovalHistory(
        request_id=request.id,
        old_status=old_status,
        new_status="REJECTED",
        action="REJECTED",
        performed_by_name=request.approver_name,
        performed_by_email=request.approver_email,
        comment=decision.decision_comment
    )

    db.add(history)

    db.commit()
    db.refresh(request)

    return request

@app.get(
    "/approval-requests/{request_id}/history",
    response_model=list[ApprovalHistoryResponse]
)
def get_request_history(
    request_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    history = (
        db.query(models.ApprovalHistory)
        .filter(models.ApprovalHistory.request_id == request_id)
        .all()
    )

    return history

@app.get("/dashboard/summary")
def dashboard_summary(
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    total_requests = (
        db.query(models.ApprovalRequest)
        .count()
    )

    pending_requests = (
        db.query(models.ApprovalRequest)
        .filter(models.ApprovalRequest.status == "PENDING")
        .count()
    )

    approved_requests = (
        db.query(models.ApprovalRequest)
        .filter(models.ApprovalRequest.status == "APPROVED")
        .count()
    )

    rejected_requests = (
        db.query(models.ApprovalRequest)
        .filter(models.ApprovalRequest.status == "REJECTED")
        .count()
    )

    cancelled_requests = (
        db.query(models.ApprovalRequest)
        .filter(models.ApprovalRequest.status == "CANCELLED")
        .count()
    )

    return {
        "total_requests": total_requests,
        "pending_requests": pending_requests,
        "approved_requests": approved_requests,
        "rejected_requests": rejected_requests,
        "cancelled_requests": cancelled_requests
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8080,
        reload=True
    )