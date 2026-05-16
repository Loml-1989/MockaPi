from fastapi import FastAPI, Query, Header, HTTPException
from faker import Faker
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI()
fake = Faker()

SECRET_API_KEY = "eyelawview"

class CustomRequest(BaseModel):
    fields: List[str] = Field(..., min_length=1)
    count: Optional[int] = Field(default=1, ge=1, le=10)

def get_pageination(page: int, count: int):
    return {"current_page": page, "item_per_page": count}

@app.get("/")
def root():
    return {
        "message": "Welcum to MockaPi.",
        "status": "Online n working.",
        "docs_url": "/docs"
    }

@app.get("/users")
def get_users(count: int = Query(default=5, le=100), page: int = Query(default=1, ge=1)):
    users = []
    for _ in range(count):
        users.append({
            "id": fake.uuid4(),
            "name": fake.name(),
            "email": fake.email(),
            "address": fake.city()
        })
    return {"pagination": get_pageination(page, count), "data": users}

@app.get("/products")
def get_products(count: int = Query(default=5, le=100), page: int = Query(default=1, ge=1)):
    products = []
    for _ in range(count):
        products.append({
            "product_id": fake.ean(),
            "name": fake.catch_phrase(),
            "price": f"${fake.random_number(digits=2)}.{fake.random_number(digits=2)}",
            "category": fake.word(),
            "description": fake.sentence()
        })
    return {"pagination": get_pageination(page, count), "data": products}

@app.get("/cards")
def get_cards(count: int = Query(default=5, le=100), page: int = Query(default=1, ge=1)):
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
    return {"pagination": get_pageination(page, count), "data": cards}

@app.get("/companies")
def get_companies(count: int = Query(default=5, le=100), page: int = Query(default=1, ge=1)):
    companies = []
    for _ in range(count):
        companies.append({
            "name": fake.company(),
            "email": fake.company_email(),
            "address": fake.address(),
            "number": fake.phone_number()
        })
    return {"pagination": get_pageination(page, count), "data": companies}


@app.get("/crypto")
def get_crypto(page: int = Query(default=1, ge=1), count: int = Query(default=5, ge=1, le=100)):
    crypto = []
    for _ in range(count):
        crypto.append({
            "coin": fake.cryptocurrency_name(),
            "code": fake.cryptocurrency_code(),
            "wallet_address": f"0x{fake.sha256()[:40]}"
        })
    return {"pagination": get_pageination(page, count), "data": crypto}

@app.get("/colors")
def get_colors(page: int = Query(default=1, ge=1), count: int = Query(default=5, ge=1, le=100)):
    colors = []
    for _ in range(count):
        colors.append({
            "color_name": fake.color_name(),
            "color_value": fake.hex_color()
        })
    return {"pagination": get_pageination(page, count), "data": colors}

@app.get("/jobs")
def get_jobs(page: int = Query(default=1, ge=1), count: int = Query(default=5, ge=1, le=100)):
    jobs = []
    for _ in range(count):
        jobs.append({
            "job_title": fake.job(),
            "company": fake.company()
        })
    return {"pagination": get_pageination(page, count), "data": jobs}

@app.post("/gen")
def gen(request: CustomRequest, x_api_key: str = Header(None, description="its da API key")):
    
    if not x_api_key:
        raise HTTPException(status_code = 401, detail = "Missing API Key.")
    if x_api_key != SECRET_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key.")
    
    results = []
    for _ in range(request.count):
        item = {}
        for field in request.fields:
            try:
                item[field] = getattr(fake, field)()
            except AttributeError:
                # Proper error message instead of crashing
                item[field] = f"ERROR: '{field}' is not a valid parameter."
        results.append(item)
    return {"data": results}