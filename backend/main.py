from datetime import datetime
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient

app = FastAPI()

# Enable CORS for Vercel / Localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Replace with MongoDB Atlas URI if deployed
db = client["school_erp"]

class LoginRequest(BaseModel):
    email: str
    password: str

class AttendancePayload(BaseModel):
    rollNo: str
    studentName: str
    status: str
    date: str
    parentPhone: str = "+919876543210"

@app.post("/token")
async def login(data: LoginRequest, request: Request):
    user_email = data.email.strip().lower()
    
    # 1. Determine role & assign corresponding Indian student/staff credentials
    role = "STUDENT"
    full_name = "Ramu Varma"
    
    if "admin" in user_email or user_email == "admin@school.com":
        role = "ADMIN"
        full_name = "Rajesh Sharma (Admin / CEO)"
    elif "t-501" in user_email or user_email == "teacher@school.com":
        role = "TEACHER"
        full_name = "Dr. Sunita Deshmukh"
    elif "p-101" in user_email or user_email == "parent@school.com":
        role = "PARENT"
        full_name = "Kishore Varma"
    elif user_email in ["101", "student@school.com", "ramu"]:
        role = "STUDENT"
        full_name = "Ramu Varma"
    elif user_email in ["102", "raju"]:
        role = "STUDENT"
        full_name = "Raju Badhavath"
    elif user_email in ["103", "manideep"]:
        role = "STUDENT"
        full_name = "Manideep Rao"
    else:
        role = "STUDENT"
        full_name = f"Student ({data.email.upper()})"

    # 2. Store Login Details in MongoDB 'login_history' collection
    login_record = {
        "id": f"LOG-{int(datetime.utcnow().timestamp())}",
        "user_identifier": data.email,
        "full_name": full_name,
        "role": role,
        "login_time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "client_ip": request.client.host if request.client else "127.0.0.1",
        "user_agent": request.headers.get("user-agent", "Unknown"),
        "status": "SUCCESS"
    }
    
    # Insert record into MongoDB
    try:
        db.login_history.insert_one(login_record)
        print(f"Logged into database: {login_record}")
    except Exception as e:
        print(f"Database write error: {e}")

    # 3. Return session token and details
    return {
        "access_token": f"jwt-session-token-{role.lower()}-{int(datetime.utcnow().timestamp())}",
        "token_type": "bearer",
        "role": role,
        "full_name": full_name,
        "email": data.email
    }

@app.get("/api/login-history")
async def get_login_history():
    try:
        logs = list(db.login_history.find({}, {"_id": 0}).sort("login_time", -1).limit(50))
        return logs
    except Exception as e:
        return []

@app.post("/api/attendance")
async def record_attendance(data: AttendancePayload):
    try:
        db.attendance.insert_one(data.dict())
        return {"status": "success", "message": "Attendance recorded in database"}
    except Exception as e:
        return {"status": "error", "message": str(e)}