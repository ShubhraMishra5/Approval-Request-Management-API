from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from database import Base
from datetime import datetime

class ApprovalRequest(Base):
    __tablename__ = "approval_requests"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, nullable = False)
    description = Column(Text, nullable = False)
    request_type = Column(String, nullable = False) 
    requester_name = Column(String, nullable = False)
    requester_email = Column(String, nullable = False)
    approver_name = Column(String, nullable = False)
    approver_email = Column(String, nullable = False)
    #approver_role= Column(String, nullable = True)
    priority = Column(String, nullable = False )
    status = Column(String, nullable = False, default = "PENDING" )
    decision_comment = Column(Text, nullable = True)
    created_at = Column(DateTime, default = datetime.utcnow)
    updated_at = Column(DateTime, default = datetime.utcnow,onupdate = datetime.utcnow)
    decision_at = Column(DateTime, nullable = True)

class ApprovalHistory(Base):
    __tablename__ = "Approval_History"
    id = Column(Integer, primary_key=True, index = True) 
    request_id = Column(Integer, nullable= False) 
    old_status = Column(String, nullable= False)
    new_status = Column(String, nullable = False)
    action = Column(String, nullable = False)
    performed_by_name = Column(String, nullable= False)
    performed_by_email = Column(String, nullable= False)
    comment = Column(Text, nullable = False)
    created_at = Column(DateTime, default = datetime.utcnow)




