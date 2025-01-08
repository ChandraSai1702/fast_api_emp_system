from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from backend.database import SessionLocal, engine
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing_extensions import Annotated
from backend.models import Employee , Base
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Histogram, Gauge
from fastapi.responses import JSONResponse
from prometheus_client import generate_latest, REGISTRY

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)


# Prometheus monitoring setup
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

# Prometheus metrics
employee_created_counter = Counter("employee_created", "Number of employees created")
employee_deleted_counter = Counter("employee_deleted", "Number of employees deleted")
employee_updated_counter = Counter("employee_updated", "Number of employees updated")
employee_creation_duration_histogram = Histogram(
    "employee_creation_duration_seconds", "Duration of employee creation requests", buckets=[0.1, 0.5, 1, 2, 5]
)
http_requests_duration_histogram = Histogram(
    "http_requests_duration_seconds", "Duration of HTTP requests", buckets=[0.1, 0.5, 1, 2, 5]
)
active_users_gauge = Gauge("active_users", "Number of active users in the system")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# Function to update active_users gauge based on the database count
def update_active_users_gauge(db: db_dependency):
    active_count = db.query(Employee).count()
    active_users_gauge.set(active_count)

# Call this function at the start and after each employee action
# update_active_users_gauge(db)

class EmployeeCreate(BaseModel):
    emp_name : str = Field(min_length=3, max_length=25)
    position : str
    department: str
    email: str

class EmployeeUpdate(BaseModel):
    emp_name : str = Field(min_length=3, max_length=25)
    position : str
    department : str
    email : str

class EmployeeResponse(BaseModel):
    emp_id : int
    emp_name : str
    position : str
    department : str
    email : str 

    class Config:
        orm_mode = True
        model_config = {"from_attributes": True}

# to create a new employee
@app.post("/employee/", status_code=status.HTTP_201_CREATED, response_model=EmployeeResponse)
async def create_a_employee(db: db_dependency, create_employee: EmployeeCreate):
    employee_model = Employee(**create_employee.model_dump())
    db.add(employee_model)
    db.commit()
    db.refresh(employee_model)
    employee_created_counter.inc()
    # active_users_gauge.inc()
    update_active_users_gauge(db) 
    return employee_model

# to get all employees
@app.get("/employee/", status_code=status.HTTP_200_OK, response_model=List[EmployeeResponse])
async def read_all_employees(db: db_dependency):
    return db.query(Employee).all()

# to update an employee
@app.put("/employee/{emp_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_a_emp(db: db_dependency, emp_id: int, update_employee: EmployeeUpdate):
    update_emp = db.query(Employee).filter(Employee.emp_id == emp_id).first()
    if update_emp is None:
        raise HTTPException(status_code=404, detail='employee not found.')

    update_emp.emp_name = update_employee.emp_name
    update_emp.position = update_employee.position
    update_emp.department = update_employee.department
    update_emp.email = update_employee.email

    db.commit()
    db.refresh(update_emp)
    employee_updated_counter.inc() 
    return update_emp

# to get an employee by id
@app.get("/employee/{emp_id}", status_code=status.HTTP_200_OK, response_model=EmployeeResponse)
async def read_by_id(db: db_dependency, emp_id: int):
    employee = db.query(Employee).filter(Employee.emp_id == emp_id).first()
    if employee is None:
        raise HTTPException(status_code=404, detail='employee not found')
    return employee

# to delete an employee
@app.delete("/employee/{emp_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_by_id(db: db_dependency, emp_id: int):
    employee = db.query(Employee).filter(Employee.emp_id == emp_id).delete()
    if employee is None:
        raise HTTPException(status_code=404, detail='employee not found')
    db.commit()
    employee_deleted_counter.inc() 
    # active_users_gauge.dec()
    update_active_users_gauge(db)

#custom metrics endpoint
@app.get("/metrics", status_code=status.HTTP_200_OK)
async def custom_metrics():
    metrics_data ={
        "employees_created": employee_created_counter._value.get(),
        "employees_deleted": employee_deleted_counter._value.get(),
        "employees_updated": employee_updated_counter._value.get(),
        "employee_creation_duration": employee_creation_duration_histogram._buckets.get(),
        "active_users": active_users_gauge._value.get(),
        "http_request_duration": http_requests_duration_histogram._buckets.get()
    }

    return JSONResponse(content=metrics_data)

