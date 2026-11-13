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


def test_scale_recipe_ingredients():
    recipe = client.post(
        "/recipes",
        json={
            "title": "Soup",
            "ingredients": ["200 g tomatoes", "1 cup broth"],
            "tags": ["dinner"],
        },
    )

    r = client.get(f"/recipes/{recipe.json()['id']}/scaled?factor=2")

    assert r.status_code == 200
    assert r.json()["id"] == recipe.json()["id"]
    assert r.json()["title"] == "Soup"
    assert r.json()["tags"] == ["dinner"]
    assert r.json()["ingredients"] == ["400 g tomatoes", "2 cup broth"]


def test_scale_unknown_recipe_404():
    r = client.get("/recipes/99999/scaled?factor=2")
    assert r.status_code == 404


def test_scale_recipe_rejects_zero_factor():
    recipe = client.post("/recipes", json={"title": "Rice", "ingredients": ["1 cup rice"]})

    r = client.get(f"/recipes/{recipe.json()['id']}/scaled?factor=0")

    assert r.status_code == 422


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
