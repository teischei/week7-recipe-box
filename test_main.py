from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_create_and_get_recipe():
    r = client.post(
        "/recipes",
        json={"title": "Pancakes", "ingredients": ["flour", "milk"], "tags": ["breakfast"]},
    )
    assert r.status_code == 200
    rid = r.json()["id"]
    r2 = client.get(f"/recipes/{rid}")
    assert r2.status_code == 200
    assert r2.json()["title"] == "Pancakes"
    assert r2.json()["tags"] == ["breakfast"]


def test_list_recipes():
    client.post("/recipes", json={"title": "Toast"})
    r = client.get("/recipes")
    assert r.status_code == 200
    assert any(rec["title"] == "Toast" for rec in r.json())


def test_list_recipes_by_tag():
    breakfast = client.post(
        "/recipes",
        json={"title": "Week 7 Pancakes", "tags": ["week7-breakfast"]},
    )
    dinner = client.post(
        "/recipes",
        json={"title": "Week 7 Pasta", "tags": ["week7-dinner"]},
    )

    r = client.get("/recipes?tag=week7-breakfast")

    assert r.status_code == 200
    recipe_ids = [recipe["id"] for recipe in r.json()]
    assert breakfast.json()["id"] in recipe_ids
    assert dinner.json()["id"] not in recipe_ids


def test_unknown_recipe_404():
    r = client.get("/recipes/99999")
    assert r.status_code == 404


def test_shopping_list_merges_unique_ingredients():
    first = client.post(
        "/recipes",
        json={"title": "Pancakes", "ingredients": ["flour", "milk", "eggs"]},
    )
    second = client.post(
        "/recipes",
        json={"title": "French toast", "ingredients": ["bread", "milk", "eggs"]},
    )

    r = client.get(
        "/shopping-list",
        params={"ids": f"{first.json()['id']},{second.json()['id']},{first.json()['id']},99999"},
    )

    assert r.status_code == 200
    assert r.json() == {"ingredients": ["flour", "milk", "eggs", "bread"]}


def test_shopping_list_rejects_non_numeric_ids():
    r = client.get("/shopping-list", params={"ids": "one,two"})
    assert r.status_code == 422
