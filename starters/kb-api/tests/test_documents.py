import httpx
import pytest

pytestmark = pytest.mark.anyio

DOC = {
    "title": "Solid Queue",
    "path": "docs/solid_queue.md",
    "body": "Jobs live in Postgres.",
    "tags": ["jobs"],
}


async def test_create_and_read(client: httpx.AsyncClient, auth: dict[str, str]) -> None:
    created = await client.post("/documents", json=DOC, headers=auth)
    assert created.status_code == 201
    document_id = created.json()["id"]

    fetched = await client.get(f"/documents/{document_id}")
    assert fetched.status_code == 200
    assert fetched.json()["title"] == "Solid Queue"


async def test_writes_need_an_api_key(client: httpx.AsyncClient) -> None:
    response = await client.post("/documents", json=DOC)
    assert response.status_code == 401


async def test_validation_errors_are_422(client: httpx.AsyncClient, auth: dict[str, str]) -> None:
    response = await client.post("/documents", json={**DOC, "title": ""}, headers=auth)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "title"]


async def test_duplicate_path_is_409(client: httpx.AsyncClient, auth: dict[str, str]) -> None:
    await client.post("/documents", json=DOC, headers=auth)
    response = await client.post("/documents", json=DOC, headers=auth)
    assert response.status_code == 409


async def test_patch_changes_only_sent_fields(client: httpx.AsyncClient, auth: dict[str, str]) -> None:
    document_id = (await client.post("/documents", json=DOC, headers=auth)).json()["id"]
    response = await client.patch(f"/documents/{document_id}", json={"tags": ["jobs", "rails"]}, headers=auth)
    assert response.json()["tags"] == ["jobs", "rails"]
    assert response.json()["title"] == "Solid Queue"


async def test_cursor_pagination(client: httpx.AsyncClient, auth: dict[str, str]) -> None:
    for n in range(5):
        await client.post("/documents", json={**DOC, "path": f"docs/{n}.md"}, headers=auth)

    first = (await client.get("/documents", params={"limit": 2})).json()
    second = (await client.get("/documents", params={"limit": 2, "after": first["next_cursor"]})).json()
    third = (await client.get("/documents", params={"limit": 2, "after": second["next_cursor"]})).json()

    paths = [d["path"] for page in (first, second, third) for d in page["items"]]
    assert paths == [f"docs/{n}.md" for n in range(5)]
    assert third["next_cursor"] is None


async def test_missing_document_is_404(client: httpx.AsyncClient) -> None:
    assert (await client.get("/documents/999999")).status_code == 404
