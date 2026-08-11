from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, schemas, auth, database

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Database Tables
models.Base.metadata.create_all(bind=database.engine)

# 1. Register Endpoint (Allows ANY email and ANY password)
@app.post("/register", response_model=schemas.Token)
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    # Check if user already exists
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="This email is already registered.")

    # Hash the password chosen by the user
    hashed_pwd = auth.get_password_hash(user.password)

    # Save new user to database
    new_user = models.User(
        email=user.email,
        hashed_password=hashed_pwd,
        full_name=user.full_name,
        role=user.role.upper(),
        parent_id=user.parent_id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate Access Token
    token = auth.create_access_token(data={"sub": new_user.email, "role": new_user.role, "id": new_user.id})
    return {
        "access_token": token,
        "token_type": "bearer",
        "role": new_user.role,
        "full_name": new_user.full_name,
        "user_id": new_user.id
    }

# 2. Login Endpoint (Authenticates ANY created email and password)
@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.email).first()
    
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth.create_access_token(
        data={"sub": user.email, "role": user.role, "id": user.id}
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user.role,
        "full_name": user.full_name,
        "user_id": user.id
    }