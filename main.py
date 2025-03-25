from fastapi import FastAPI
from pydantic import BaseModel
from agents import course_generator

app = FastAPI()

class CourseRequest(BaseModel):
    brief: str
    target_audience: str

@app.post("/generate-course/")
def generate_course(request: CourseRequest):
    """API to generate a structured course from a brief description."""
    return course_generator(request.brief, request.target_audience)