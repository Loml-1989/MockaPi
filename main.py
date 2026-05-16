from fastapi import FastAPI, Query
from faker import Faker
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()
fake = Faker()

class CustomRequest(BaseModel):
    fields: List[str]
    count: Optional[int] = 1

@app.get("/")
def root():
    return {
        "message": "Welcum to MockaPi.",
        "status": "Online n working.",
        "docs_url": "/docs"
    }

@app.get("/users")
def get_users(count: int = Query(default=5, le=100)):
    """Generates a list of fake user profiles."""
    users = []
    for _ in range(count):
        users.append({
            "id": fake.uuid4(),
            "name": fake.name(),
            "email": fake.email(),
            "address": fake.city()
        })
    return {"count": count, "data": users}

@app.get("/products")
def get_products(count: int = Query(default=5, le=100)):
    products = []
    for _ in range(count):
        products.append({
            "product_id": fake.ean(),
            "name": fake.catch_phrase(),
            "price": fake.random_number(digits=2),
            "category": fake.word(),
            "description": fake.sentence()
        })
    return {"count": count, "data": products}

@app.get("/cards")
def get_cards(count: int = Query(default=5, le=100)):
    cards = []
    for _ in range(count):
        cards.append({
            "card_number": fake.credit_card_number(),
            "card_cvv": fake.credit_card_security_code(),
            "card_expiration_date": fake.credit_card_expire(),
            "card_provider": fake.credit_card_provider(),
            "card_holder": fake.name(),
            "card_holder_address": fake.address()
        })
    return {"count": count, "data": cards}

@app.post("/gen")
def gen(request: CustomRequest):
    results = []
    for _ in range(request.count):
        item = {}
        for field in request.fields:
            try:
                item[field] = getattr(fake, field)()
            except AttributeError:
                item[field] = "Field not supported"
        results.append(item)
    return{"data": results}
