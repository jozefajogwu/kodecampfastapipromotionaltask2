from fastapi import FastAPI, Query, Path, Body
from pydantic import BaseModel, Field, EmailStr

app = FastAPI()

# Task 1: Basic Query Parameters
@app.get("/items/")
async def get_items(name: str, category: str, price: float):
    return {"name": name, "category": category, "price": price}

# Task 2: Query Parameters with Default Values and Optional Fields
@app.get("/search/")
async def search_items(query: str, page: int = 1, size: int = 10):
    return {"query": query, "page": page, "size": size}

# Task 3: Request Body with Nested Pydantic Models
class Address(BaseModel):
    street: str
    city: str
    zip: str

class User(BaseModel):
    name: str
    email: EmailStr
    address: Address

@app.post("/users/")
async def create_user(user: User):
    return user

# Task 4: Query Parameters with String Validations
@app.get("/validate/")
async def validate_username(
    username: str = Query(
        ...,
        min_length=3,
        max_length=50,
        regex="^[a-zA-Z0-9_]+$"
    )
):
    return {"username": username, "validation": "passed"}

# Task 5: Combined Parameters and Validations
class Report(BaseModel):
    title: str = Field(..., min_length=3)
    content: str = Field(..., min_length=10)

@app.post("/reports/{report_id}")
async def create_report(
    report_id: int = Path(..., gt=0),
    start_date: str = Query(...),
    end_date: str = Query(...),
    report: Report = Body(...)
):
    return {
        "report_id": report_id,
        "start_date": start_date,
        "end_date": end_date,
        "report": report
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
