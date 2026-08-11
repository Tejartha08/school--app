from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure

# MongoDB Atlas Connection
MONGO_URI = "mongodb+srv://2210030379_db_user:SchoolERP2026Test@school-erp.lmhnl8z.mongodb.net/schoolERP?appName=School-ERP"

try:
    print("🔄 Connecting to MongoDB Atlas...")

    client = MongoClient(
        MONGO_URI,
        serverSelectionTimeoutMS=10000
    )

    # Test MongoDB connection
    client.admin.command("ping")

    print("✅ MongoDB Connected Successfully")

    # Select database
    db = client["schoolERP"]

    print("✅ Database selected:", db.name)

    # Show collections
    collections = db.list_collection_names()

    print("📁 Existing collections:")

    if collections:
        for collection in collections:
            print("   -", collection)
    else:
        print("   No collections found yet.")

    client.close()

    print("✅ MongoDB connection closed successfully")

except OperationFailure as e:
    print("❌ MongoDB Authentication Failed")
    print("Please check the MongoDB username and password.")
    print("Error:", e)

except ServerSelectionTimeoutError as e:
    print("❌ Could not connect to MongoDB Atlas")
    print("Check Network Access / IP Address in MongoDB Atlas.")
    print("Error:", e)

except Exception as e:
    print("❌ MongoDB Connection Failed")
    print("Error:", e)