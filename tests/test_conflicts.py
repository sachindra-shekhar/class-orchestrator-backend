def test_occurrence_conflict_returns_409(client):
    tenant = client.post("/api/v1/tenants", json={"name": "Acme", "email": "x@example.com"}).json()
    tenant_id = tenant["id"]

    cls = client.post(f"/api/v1/tenants/{tenant_id}/classes", json={"name": "Math"}).json()
    class_id = cls["id"]

    body = {
        "classId": class_id,
        "startTime": "2026-05-01T10:00:00Z",
        "endTime": "2026-05-01T11:00:00Z",
    }
    first = client.post(f"/api/v1/tenants/{tenant_id}/classes/{class_id}/occurrences", json=body)
    assert first.status_code == 201

    conflict = client.post(
        f"/api/v1/tenants/{tenant_id}/classes/{class_id}/occurrences",
        json={
            "classId": class_id,
            "startTime": "2026-05-01T10:30:00Z",
            "endTime": "2026-05-01T11:30:00Z",
        },
    )
    assert conflict.status_code == 409
    assert conflict.json()["code"] == "SCHEDULE_CONFLICT"
