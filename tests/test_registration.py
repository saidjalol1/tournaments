import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_register_player():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # tournament adding 
        response = await client.post("/tournaments", json={
            "name": "Test Cup",
            "max_players": 2,
            "start_at": "2025-06-01T15:00:00Z"
        })
        assert response.status_code == 201
        tournament = response.json()

        # player registration
        response = await client.post(f"/tournaments/{tournament['id']}/register", json={
            "name": "John Doe",
            "email": "john@example.com"
        })
        assert response.status_code == 201

        # same email regitering 
        response = await client.post(f"/tournaments/{tournament['id']}/register", json={
            "name": "John Smith",
            "email": "john@example.com"
        })
        assert response.status_code == 400
