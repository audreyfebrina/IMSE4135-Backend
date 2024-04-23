import os
from pathlib import Path
from dotenv import load_dotenv

from fastapi import FastAPI


import motor.motor_asyncio


# Load project environment
dotenv_path = Path(".env")
load_dotenv(dotenv_path=dotenv_path)

app = FastAPI(
    title="IMSE4135",
    summary="Backend for IMSE4135 project.",
)

mongodb_uri = str(os.getenv("MONGODB_URI"))


# Create a shared database connection
client = motor.motor_asyncio.AsyncIOMotorClient(mongodb_uri)
db = client.test_db
bag_collection = db.get_collection("bags")
box_collection = db.get_collection("boxes")
officer_collection = db.get_collection("officers")
prisoner_collection = db.get_collection("prisoners")
shelf_collection = db.get_collection("shelves")

# Include the shelf routes
from routes.shelf import shelf_router
from routes.bag import bag_router
from routes.box import box_router
from routes.officer import officer_router
from routes.prisoner import prisoner_router

app.include_router(shelf_router)
app.include_router(bag_router)
app.include_router(box_router)
app.include_router(officer_router)
app.include_router(prisoner_router)
