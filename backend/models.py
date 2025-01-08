from sqlalchemy import Column, Integer, String
from .database import Base

class Employee(Base):
    __tablename__ = 'emp_info'

    emp_id = Column(Integer, primary_key=True, index=True)
    emp_name = Column(String, index=True)
    position = Column(String, index=True)
    department = Column(String, index=True)
    email = Column(String, unique=True, index=True)