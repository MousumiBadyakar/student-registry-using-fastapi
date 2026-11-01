# 📘 Student Registry — FastAPI & Streamlit

A full-stack Student Registry application built using **FastAPI, Python, Streamlit, HTML, CSS, and JavaScript**. It provides an interactive dashboard to manage student records with CRUD operations, data validation, filtering, sorting, and pagination.

## 🚀 Live Demo

- **Streamlit Application:** [Student Registry](https://student-registry-using-fastapi-ztsmwhdqtfbdrqczqitdfq.streamlit.app/)
- **FastAPI Backend:** [Render API](https://student-registry-using-fastapi.onrender.com)
- **API Documentation:** [Swagger UI](https://student-registry-using-fastapi.onrender.com/docs)

## ✨ Features

- **Student Management:** Create, view, update, and delete student records.
- **Data Validation:** Validate student details using Pydantic.
- **Search Students:** Find student records using their unique student ID.
- **Filtering:** Filter student records by course.
- **Sorting:** Sort records using different fields and ordering options.
- **Pagination:** Navigate through student records efficiently.
- **Dashboard Analytics:** View student statistics, class average, grade distribution, and other insights.
- **Interactive UI:** Clean and responsive Streamlit dashboard.
- **REST API:** Backend endpoints built using FastAPI.
- **Data Persistence:** Store student records using JSON file-based storage.

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| Backend | Python, FastAPI |
| Frontend | Streamlit, HTML, CSS, JavaScript |
| Data Validation | Pydantic |
| Data Handling | Pandas |
| Data Visualization | Altair |
| API Communication | REST APIs, Requests |
| Storage | JSON |
| Backend Deployment | Render |
| Frontend Deployment | Streamlit Community Cloud |
| Version Control | Git & GitHub |

## 🏗️ Project Architecture

```text
Student-Registry/
│
├── app.py                  # Streamlit frontend
├── main.py                 # FastAPI backend
├── requirements.txt        # Project dependencies
├── students.json           # Student records
├── .gitignore
│
└── web/
    ├── index.html          # HTML frontend
    ├── style.css           # CSS styling
    └── app.js              # JavaScript functionality
```

### Application Workflow

1. Users interact with the Streamlit dashboard.
2. Streamlit sends HTTP requests to the FastAPI backend.
3. FastAPI processes requests and validates incoming data.
4. Student records are managed through JSON-based storage.
5. API responses are displayed on the Streamlit dashboard.

## 🔗 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/student` | Retrieve all students |
| GET | `/paginate` | Retrieve paginated student records |
| GET | `/filter` | Filter students by course |
| GET | `/sort` | Sort student records |
| GET | `/students/{id}` | Retrieve a student by ID |
| POST | `/create` | Create a new student |
| PUT | `/update/{id}` | Update student details |
| DELETE | `/delete/{id}` | Delete a student |

Explore and test all endpoints through the [FastAPI Swagger Documentation](https://student-registry-using-fastapi.onrender.com/docs).

## 💻 Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/MousumiBadyakar/student-registry-using-fastapi.git
```

### 2. Navigate to the Project Directory

```bash
cd student-registry-using-fastapi
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

**Windows:**
```bash
venv\Scripts\activate
```

**Linux / macOS:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Start the FastAPI Backend

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### 6. Run the Streamlit Frontend

Open another terminal and run:

```bash
streamlit run app.py
```

The Streamlit application will open in your browser.

**Note:** When running locally, the Streamlit API base URL should be `http://127.0.0.1:8000`. When using the deployed application, it should point to the Render backend URL.

## ☁️ Deployment

The application is deployed using two platforms:

- **Backend — Render:** Hosts the FastAPI application and exposes REST API endpoints.
- **Frontend — Streamlit Community Cloud:** Hosts the interactive Streamlit dashboard.

The Streamlit frontend communicates with the deployed FastAPI backend through its public API URL.

## 🎯 Learning Outcomes

Through this project, I explored:

- Building RESTful APIs using FastAPI.
- Implementing CRUD operations.
- Validating request data using Pydantic.
- Connecting a frontend application with a backend API.
- Working with JSON-based data storage.
- Implementing filtering, sorting, and pagination.
- Building interactive dashboards using Streamlit.
- Deploying full-stack Python applications.

## 👩‍💻 Author

**Mousumi Badyakar**