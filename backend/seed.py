import models, auth, database

# Recreate tables
models.Base.metadata.drop_all(bind=database.engine)
models.Base.metadata.create_all(bind=database.engine)

db = database.SessionLocal()

users = [
    {"email": "2210030379cse@gmail.com", "password": "123", "full_name": "Teja Student", "role": "STUDENT"},
    {"email": "teacher@school.com", "password": "123", "full_name": "Sarah Teacher", "role": "TEACHER"},
    {"email": "parent@school.com", "password": "123", "full_name": "Parent User", "role": "PARENT"},
    {"email": "admin@school.com", "password": "123", "full_name": "System Admin", "role": "ADMIN"},
]

for user_data in users:
    hashed_pwd = auth.get_password_hash(user_data["password"])
    user = models.User(
        email=user_data["email"],
        hashed_password=hashed_pwd,
        full_name=user_data["full_name"],
        role=user_data["role"]
    )
    db.add(user)

db.commit()
db.close()
print("Database seeded successfully! All passwords are set to '123'")