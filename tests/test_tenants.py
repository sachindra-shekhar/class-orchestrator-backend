def test_tenant_crud_flow(client):
    create = client.post("/api/v1/tenants", json={"name": "Acme", "email": "acme@example.com"})
    assert create.status_code == 201
    tenant = create.json()
    assert tenant["status"] == "active"

    list_resp = client.get("/api/v1/tenants")
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 1

    tenant_id = tenant["id"]
    get_resp = client.get(f"/api/v1/tenants/{tenant_id}")
    assert get_resp.status_code == 200

    update_resp = client.put(f"/api/v1/tenants/{tenant_id}", json={"status": "inactive"})
    assert update_resp.status_code == 200
    assert update_resp.json()["status"] == "inactive"

    del_resp = client.delete(f"/api/v1/tenants/{tenant_id}")
    assert del_resp.status_code == 204

    missing = client.get(f"/api/v1/tenants/{tenant_id}")
    assert missing.status_code == 404
