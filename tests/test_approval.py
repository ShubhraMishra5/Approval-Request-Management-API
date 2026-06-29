from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

HEADERS = {
    "api-key": "secret-api-key"
}


def test_health_check():

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_request_success():

    payload = {
        "title": "Laptop Request",
        "description": "Need laptop for development",
        "request_type": "OTHER",
        "requester_name": "Shubhra",
        "requester_email": "Shubhra@test.com",
        "approver_name": "Akshay",
        "approver_email": "Akshay@test.com",
        "priority": "HIGH"
    }

    response = client.post(
        "/approval-requests",
        json=payload,
        headers=HEADERS
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Laptop Request"
    assert data["status"] == "PENDING"


def test_get_requests_success():

    response = client.get(
        "/approval-requests",
        headers=HEADERS
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_invalid_api_key():

    response = client.get(
        "/approval-requests",
        headers={
            "api-key": "wrong-key"
        }
    )

    assert response.status_code == 401


def test_missing_api_key():

    response = client.get(
        "/approval-requests"
    )

    assert response.status_code == 401


def test_request_not_found():

    response = client.get(
        "/approval-requests/999999",
        headers=HEADERS
    )

    assert response.status_code == 404


def test_approve_request_success():

    payload = {
        "title": "VPN Access",
        "description": "Need VPN access",
        "request_type": "ACCESS",
        "requester_name": "Ishita",
        "requester_email": "Ishita@test.com",
        "approver_name": "Security Lead",
        "approver_email": "security@test.com",
        "priority": "MEDIUM"
    }

    create_response = client.post(
        "/approval-requests",
        json=payload,
        headers=HEADERS
    )

    request_id = create_response.json()["id"]

    approve_response = client.put(
        f"/approval-requests/{request_id}/approve",
        json={
            "decision_comment": "Approved"
        },
        headers=HEADERS
    )

    assert approve_response.status_code == 200

    data = approve_response.json()

    assert data["status"] == "APPROVED"


def test_reject_request_success():

    payload = {
        "title": "Software Access",
        "description": "Need software access",
        "request_type": "OTHER",
        "requester_name": "Mina",
        "requester_email": "Mina@test.com",
        "approver_name": "IT Lead",
        "approver_email": "it@test.com",
        "priority": "LOW"
    }

    create_response = client.post(
        "/approval-requests",
        json=payload,
        headers=HEADERS
    )

    request_id = create_response.json()["id"]

    reject_response = client.put(
        f"/approval-requests/{request_id}/reject",
        json={
            "decision_comment": "Rejected"
        },
        headers=HEADERS
    )

    assert reject_response.status_code == 200

    data = reject_response.json()

    assert data["status"] == "REJECTED"


def test_dashboard_summary():

    response = client.get(
        "/dashboard/summary",
        headers=HEADERS
    )

    assert response.status_code == 200

    data = response.json()

    assert "total_requests" in data
    assert "pending_requests" in data
    assert "approved_requests" in data
    assert "rejected_requests" in data
    assert "cancelled_requests" in data