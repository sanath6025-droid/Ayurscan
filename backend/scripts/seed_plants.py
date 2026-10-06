#!/usr/bin/env python3
"""
Seed script for AyurScan plants database.
Loads plants.json, connects to MongoDB, creates indexes, and inserts records
without creating duplicates. Handles connection errors cleanly.
"""
import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError, PyMongoError

# Locate directories
SCRIPT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = SCRIPT_DIR.parent
ROOT_DIR = BACKEND_DIR.parent

# Load environment variables
env_path = BACKEND_DIR / ".env"
if not env_path.exists():
    env_path = ROOT_DIR / ".env"
load_dotenv(dotenv_path=env_path)

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "ayurscan")

DATA_FILE = BACKEND_DIR / "data" / "plants.json"

def seed_database():
    print("=" * 60)
    print("AyurScan Plant Database Seeder")
    print("=" * 60)

    if not DATA_FILE.exists():
        print(f"Error: Plant data file not found at {DATA_FILE}")
        sys.exit(1)

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            plants_data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error parsing plants.json: {e}")
            sys.exit(1)

    print(f"Loaded {len(plants_data)} plants from {DATA_FILE.name}")
    print(f"Connecting to MongoDB at: {MONGODB_URI}")

    try:
        # 5 second timeout to handle offline/missing MongoDB gracefully
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        # Verify connection
        client.admin.command("ping")
        print("Connected to MongoDB successfully.")
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        print("\n" + "!" * 60)
        print("Unable to connect to MongoDB server.")
        print(f"Connection URI: {MONGODB_URI}")
        print("Ensure MongoDB is running locally or provide a valid MONGODB_URI in backend/.env")
        print(f"Details: {e}")
        print("!" * 60)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected connection error: {e}")
        sys.exit(1)

    try:
        db = client[DATABASE_NAME]
        plants_collection = db["plants"]

        # Create indexes
        print("Ensuring indexes on scientific_name, common_name, and ayurvedic_name...")
        plants_collection.create_index("scientific_name", unique=True)
        plants_collection.create_index("common_name")
        plants_collection.create_index("ayurvedic_name")

        inserted_count = 0
        updated_count = 0

        for plant in plants_data:
            scientific_name = plant.get("scientific_name")
            if not scientific_name:
                continue

            res = plants_collection.update_one(
                {"scientific_name": scientific_name},
                {"$set": plant},
                upsert=True
            )
            if res.upserted_id is not None:
                inserted_count += 1
            else:
                updated_count += 1

        print("\n------------------------------------------------------------")
        print(f"Inserted: {inserted_count} new plants")
        print(f"Updated:  {updated_count} existing plants")
        print(f"Total:    {inserted_count + updated_count} plants cataloged")
        print("Database seeding completed successfully.")
        print("------------------------------------------------------------\n")

    except PyMongoError as pe:
        print(f"MongoDB Operation Error during seeding: {pe}")
        sys.exit(1)
    finally:
        client.close()

if __name__ == "__main__":
    seed_database()
