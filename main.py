from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, field_validator, computed_field, Field, EmailStr
from fastapi.middleware.cors import CORSMiddleware
import json

app =  FastAPI() 

#CORS -> CROSS ORIGIN RESOURCE SHARING 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"]
)


@app.get('/') #ENDPOINT 
def greet():
    return{"Hello, It's Mou"}

@app.get('/hello')
def hello():
    return{"This is Hello page"}

#HELPER FUNCTION
def load_data():
    with open("students.json",'r')as file:
        return json.load(file)

def save_data(data):
    with open("students.json","w") as file:
        json.dump(data, file, indent=4) #indent=4 keeps the file readable

@app.get('/student')
def student():
    return load_data()

#students_id -> this is our path parameter.
@app.get("/students/{student_id}") #/student/S001
def get_id(
    student_id:str = Path(...,description="The Id of the student",
    examples=["S001"])
    ): #student_id = S001
    data = load_data()
    if student_id not in data:
        raise HTTPException(
            status_code=404,
            detail=f"Students with Id '{student_id}' not found"
        )
    return data[student_id]#data[S001]

#QUERY PARAMETERS
#http://127.0.0.1:8000/filter?course=Python
@app.get('/filter')
def filter_student(
    course:str = Query(
        None, 
        description = "show only students in this course", 
        examples = ["Python"])): #course = python
    data = load_data()

    if course is None:
        return data
    
    filtered = {}
    for student_id , info in data.items():
        if info["course"].lower() == course.lower():
            filtered[student_id] = info

    return filtered

# http://127.0.0.1:8000/sort?sort_by=marks,age,name&order=asc,desc

SORT_FIELDS = ["marks","age","name"]
SORT_ORDER = ["asc","desc"]

@app.get('/sort')
def sort_students(
    sort_by : str = Query(None, description = "Sort by marks, name, age", examples = ["marks"]),
    order : str = Query("asc", description = "asc or desc", examples = ["asc","desc"])
    ):

    if sort_by not in SORT_FIELDS:
        raise HTTPException(
            status_code = 404,
            detail = f"Invalid sort_by '{sort_by}, Choose from {SORT_FIELDS}"
        )

    if order not in SORT_ORDER:
            raise HTTPException(
                status_code = 404,
                detail = f"Invalid order '{order}, Choose from {SORT_ORDER}"
        )

    data = load_data()

    #step-1 Turn the dictionary into a list, putting the ID inside each student
    student = []
    for student_id, info in data.items():
        info["id"] = student_id
        student.append(info)

    #Step-2 Sort the list by the choosen field
    reverse = (order=="desc")
    sorted_students = sorted(student, key=lambda s:s[sort_by], reverse=reverse)

    return sorted_students

#PAGINATION
#http://127.0.0.1:8000/paginate?page=1&limit=2
#page -> which page you want
#limit -> how many students(records) on one page
#Formula:
#start = (page - 1) * limit
#end = start + limit
@app.get("/paginate")
def paginate_student(
    page:int = Query(1, ge=1, description="Which page you want (start from 1)"), 
    limit:int = Query(2, ge=1, le=100, description="How many students on one page(1 to 100)")):
    data = load_data()

    #Turn the dictionary into a list, putting the ID inside each student
    student = []
    for student_id , info in data.items():
        info['id'] = student_id
        student.append(info)

    start = (page-1)*limit
    end = start+limit

    page_student = student[start : end]
    total_students = len(student)

    return{
        "page" : page,
        "limit" : limit,
        "total_students" : total_students,
        "students" : page_student
    }


#REQUEST BODY
#POST -> data comes in the BODY (a JSON Object sent with the request)
#When a function argument is a Pydantic Model, FastAPI reads it from the body and validates automatically, Bad Data -> 422

class Student(BaseModel):
    id      : str = Field(..., examples=["S001"])
    name    : str = Field(..., min_length=2, max_length=50)
    age     : int = Field(..., gt=0, le=100)
    course  : str = Field(..., max_length=50)
    marks   : int = Field(..., ge=0, le=100)
    email   : EmailStr

    #Custom Rule : Name must contain only letters and spaces
    @field_validator("name")#name=Kabir singh
    @classmethod
    def check_name(cls, value):
        if not value.replace(" ", "").isalpha():
            raise ValueError("Name must contain only letters and spaces")
        
        return value.title()

    @computed_field
    @property
    def grade(self) -> str:
        if self.marks >= 90:
            return "A+"
        elif self.marks >= 80:
            return "A"
        elif self.marks >= 70:
            return "B"
        elif self.marks >= 60:
            return "C"
        else:
            return "F"

@app.post('/create', status_code = 201)
def create_student(student: Student):
    data = load_data()

    if student.id in data:
        raise HTTPException(
            status_code = 400,
            detail = f"Student with ID '{student.id}' already exists"
            )

    data[student.id] = student.model_dump(exclude={"id","grade"})
    save_data(data)

    return {"message":"Student created Successfully","student":student}



class StudentUpdate(BaseModel):
    name    : str | None = Field(None, min_length=2, max_length=50)
    age     : int | None = Field(None, gt=0, lt=100)
    course  : str | None = Field(None, max_length=50)
    marks   : int | None = Field(None, ge=0, le=100)
    email   : EmailStr | None = None

@app.put("/update/{student_id}")
def update_student(
    student_update : StudentUpdate,
    student_id : str = Path(..., description = "The Id of the student",examples=["S001"])
    ):
    data = load_data()

    if student_id not in data:
        raise HTTPException(
            status_code=404,
            detail=f"Student with Id '{student_id}' not found"
        )

    #STEP1 : The student as it is right now.
    existing = data[student_id]

    #STEP2 : ONLY the fields the client actually sent
    update = student_update.model_dump(exclude_unset=True)
 
    #STEP3: COPY the new value on the top of old one.
    for key, value in update.items():
        existing[key] = value

    #STEP4: Check the final student again
    student = Student(id=student_id, **existing)

    data[student_id] = student.model_dump(exclude=["id", "grade"])
    save_data(data)

    return {"Message": "Student Updated Successfully", "student":student}


@app.delete('/delete/{student_id}')
def delete_student(
    student_id : str = Path(..., description="The Id of the student", examples=["S001"])
    ):
    data = load_data()

    if student_id not in data:
        raise HTTPException(
            status_code = 404,
            detail = f"Student with id '{student_id}' not found"
        )

    del data[student_id]
    save_data(data)

    return{"message": f"Student '{student_id}' delete successfully"}
