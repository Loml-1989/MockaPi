MockaPi is a API tool for anyone who wants to generate mock data for any reason.

Framework: FastAPI
Lib for Generation: Faker
Validation: Pydantic
Server: Uvicorn

GET Endpoints: `/users`, `/products`, `/cards`, `/companies`, `/crypto`, `/colors`, and `/jobs`.

POST Endpoints: `/gen`

`/gen` is for dynamic data generation.
It requires API key.

Header Key: `x-api-key`
Key: `eyelawview`

How to run it locally?!?!
- clone the repo
- install the requirements.txt using `pip install -r requirements.txt` command
- start the server using `uvicorn main:app --reload`
- nevigate to http://127.0.0.1:8000/docs