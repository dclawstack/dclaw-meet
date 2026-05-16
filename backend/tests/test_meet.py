import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    response = await client.get("/health/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    payload = {"email": "alice@example.com", "full_name": "Alice Smith", "avatar_url": None}
    response = await client.post("/api/v1/users", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "alice@example.com"
    assert data["full_name"] == "Alice Smith"
    assert "id" in data

    # Duplicate email should fail
    response = await client.post("/api/v1/users", json=payload)
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_list_users(client: AsyncClient):
    # Seed a user first
    await client.post("/api/v1/users", json={"email": "bob@example.com", "full_name": "Bob Jones"})
    response = await client.get("/api/v1/users")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert len(data["items"]) >= 1


@pytest.mark.asyncio
async def test_get_user(client: AsyncClient):
    create_resp = await client.post("/api/v1/users", json={"email": "carol@example.com", "full_name": "Carol"})
    uid = create_resp.json()["id"]
    response = await client.get(f"/api/v1/users/{uid}")
    assert response.status_code == 200
    assert response.json()["id"] == uid


@pytest.mark.asyncio
async def test_get_user_not_found(client: AsyncClient):
    response = await client.get("/api/v1/users/12345678-1234-1234-1234-123456789abc")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_user(client: AsyncClient):
    create_resp = await client.post("/api/v1/users", json={"email": "dan@example.com", "full_name": "Dan"})
    uid = create_resp.json()["id"]
    response = await client.put(f"/api/v1/users/{uid}", json={"full_name": "Dan Updated"})
    assert response.status_code == 200
    assert response.json()["full_name"] == "Dan Updated"


@pytest.mark.asyncio
async def test_delete_user(client: AsyncClient):
    create_resp = await client.post("/api/v1/users", json={"email": "eve@example.com", "full_name": "Eve"})
    uid = create_resp.json()["id"]
    response = await client.delete(f"/api/v1/users/{uid}")
    assert response.status_code == 204
    get_resp = await client.get(f"/api/v1/users/{uid}")
    assert get_resp.status_code == 404


# ── Rooms ─────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_room(client: AsyncClient):
    user_resp = await client.post("/api/v1/users", json={"email": "roomhost@example.com", "full_name": "Room Host"})
    host_id = user_resp.json()["id"]
    payload = {"name": "Standup", "slug": "daily-standup", "host_id": host_id, "settings": {}}
    response = await client.post("/api/v1/rooms", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Standup"
    assert data["slug"] == "daily-standup"

    # Duplicate slug should fail
    response = await client.post("/api/v1/rooms", json=payload)
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_list_rooms(client: AsyncClient):
    user_resp = await client.post("/api/v1/users", json={"email": "host2@example.com", "full_name": "Host2"})
    host_id = user_resp.json()["id"]
    await client.post("/api/v1/rooms", json={"name": "Room A", "slug": "room-a", "host_id": host_id})
    response = await client.get("/api/v1/rooms")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1


@pytest.mark.asyncio
async def test_get_room(client: AsyncClient):
    user_resp = await client.post("/api/v1/users", json={"email": "host3@example.com", "full_name": "Host3"})
    host_id = user_resp.json()["id"]
    create_resp = await client.post("/api/v1/rooms", json={"name": "Room B", "slug": "room-b", "host_id": host_id})
    rid = create_resp.json()["id"]
    response = await client.get(f"/api/v1/rooms/{rid}")
    assert response.status_code == 200
    assert response.json()["id"] == rid


@pytest.mark.asyncio
async def test_update_room(client: AsyncClient):
    user_resp = await client.post("/api/v1/users", json={"email": "host4@example.com", "full_name": "Host4"})
    host_id = user_resp.json()["id"]
    create_resp = await client.post("/api/v1/rooms", json={"name": "Room C", "slug": "room-c", "host_id": host_id})
    rid = create_resp.json()["id"]
    response = await client.put(f"/api/v1/rooms/{rid}", json={"name": "Room C Updated"})
    assert response.status_code == 200
    assert response.json()["name"] == "Room C Updated"


@pytest.mark.asyncio
async def test_delete_room(client: AsyncClient):
    user_resp = await client.post("/api/v1/users", json={"email": "host5@example.com", "full_name": "Host5"})
    host_id = user_resp.json()["id"]
    create_resp = await client.post("/api/v1/rooms", json={"name": "Room D", "slug": "room-d", "host_id": host_id})
    rid = create_resp.json()["id"]
    response = await client.delete(f"/api/v1/rooms/{rid}")
    assert response.status_code == 204
    get_resp = await client.get(f"/api/v1/rooms/{rid}")
    assert get_resp.status_code == 404


# ── Meetings ──────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_meeting(client: AsyncClient):
    user_resp = await client.post("/api/v1/users", json={"email": "mhost@example.com", "full_name": "M Host"})
    host_id = user_resp.json()["id"]
    room_resp = await client.post("/api/v1/rooms", json={"name": "Conf", "slug": "conf-1", "host_id": host_id})
    room_id = room_resp.json()["id"]
    payload = {"title": "Sprint Planning", "room_id": room_id, "status": "scheduled"}
    response = await client.post("/api/v1/meetings", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Sprint Planning"
    assert data["room_id"] == room_id


@pytest.mark.asyncio
async def test_list_meetings(client: AsyncClient):
    user_resp = await client.post("/api/v1/users", json={"email": "mhost2@example.com", "full_name": "M Host2"})
    host_id = user_resp.json()["id"]
    room_resp = await client.post("/api/v1/rooms", json={"name": "Conf2", "slug": "conf-2", "host_id": host_id})
    room_id = room_resp.json()["id"]
    await client.post("/api/v1/meetings", json={"title": "Meeting A", "room_id": room_id})
    response = await client.get("/api/v1/meetings")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1


@pytest.mark.asyncio
async def test_filter_meetings_by_status(client: AsyncClient):
    user_resp = await client.post("/api/v1/users", json={"email": "mhost3@example.com", "full_name": "M Host3"})
    host_id = user_resp.json()["id"]
    room_resp = await client.post("/api/v1/rooms", json={"name": "Conf3", "slug": "conf-3", "host_id": host_id})
    room_id = room_resp.json()["id"]
    await client.post("/api/v1/meetings", json={"title": "Live Meeting", "room_id": room_id, "status": "live"})
    response = await client.get("/api/v1/meetings?status=live")
    assert response.status_code == 200
    data = response.json()
    assert all(m["status"] == "live" for m in data["items"])


@pytest.mark.asyncio
async def test_get_meeting(client: AsyncClient):
    user_resp = await client.post("/api/v1/users", json={"email": "mhost4@example.com", "full_name": "M Host4"})
    host_id = user_resp.json()["id"]
    room_resp = await client.post("/api/v1/rooms", json={"name": "Conf4", "slug": "conf-4", "host_id": host_id})
    room_id = room_resp.json()["id"]
    create_resp = await client.post("/api/v1/meetings", json={"title": "Retro", "room_id": room_id})
    mid = create_resp.json()["id"]
    response = await client.get(f"/api/v1/meetings/{mid}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == mid
    assert "participants" in data
    assert "action_items" in data


@pytest.mark.asyncio
async def test_update_meeting(client: AsyncClient):
    user_resp = await client.post("/api/v1/users", json={"email": "mhost5@example.com", "full_name": "M Host5"})
    host_id = user_resp.json()["id"]
    room_resp = await client.post("/api/v1/rooms", json={"name": "Conf5", "slug": "conf-5", "host_id": host_id})
    room_id = room_resp.json()["id"]
    create_resp = await client.post("/api/v1/meetings", json={"title": "Review", "room_id": room_id})
    mid = create_resp.json()["id"]
    response = await client.put(f"/api/v1/meetings/{mid}", json={"status": "ended"})
    assert response.status_code == 200
    assert response.json()["status"] == "ended"


@pytest.mark.asyncio
async def test_delete_meeting(client: AsyncClient):
    user_resp = await client.post("/api/v1/users", json={"email": "mhost6@example.com", "full_name": "M Host6"})
    host_id = user_resp.json()["id"]
    room_resp = await client.post("/api/v1/rooms", json={"name": "Conf6", "slug": "conf-6", "host_id": host_id})
    room_id = room_resp.json()["id"]
    create_resp = await client.post("/api/v1/meetings", json={"title": "Grooming", "room_id": room_id})
    mid = create_resp.json()["id"]
    response = await client.delete(f"/api/v1/meetings/{mid}")
    assert response.status_code == 204
    get_resp = await client.get(f"/api/v1/meetings/{mid}")
    assert get_resp.status_code == 404


# ── Dashboard ─────────────────────────────────────────

@pytest.mark.asyncio
async def test_dashboard_stats(client: AsyncClient):
    response = await client.get("/api/v1/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert "total_meetings" in data
    assert "total_rooms" in data
    assert "total_participants" in data
    assert "open_action_items" in data
