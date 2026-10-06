import os
import json
import logging
import re
from pathlib import Path
from typing import Optional, List, Dict, Any
from pymongo import MongoClient
from pymongo.errors import PyMongoError, ConnectionFailure, ServerSelectionTimeoutError

logger = logging.getLogger("ayurscan.database")

class DatabaseManager:
    def __init__(self):
        self.mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
        self.database_name = os.getenv("DATABASE_NAME", "ayurscan")
        self.client: Optional[MongoClient] = None
        self.db = None
        self.plants_collection = None
        self.is_connected = False
        self._fallback_plants: List[Dict[str, Any]] = []
        self._load_fallback_data()

    def _load_fallback_data(self):
        candidates = [
            Path(__file__).resolve().parent.parent.parent / "data" / "plants.json",
            Path(__file__).resolve().parent.parent / "data" / "plants.json",
            Path("data/plants.json").resolve(),
            Path("backend/data/plants.json").resolve(),
        ]
        data_path = next((p for p in candidates if p.exists()), None)
        if data_path:
            try:
                with open(data_path, "r", encoding="utf-8") as f:
                    self._fallback_plants = json.load(f)
                logger.info(f"Loaded {len(self._fallback_plants)} fallback plants from {data_path}")
            except Exception as e:
                logger.warning(f"Could not load fallback plants.json from {data_path}: {e}")
        else:
            logger.warning("Could not locate plants.json in any expected fallback location.")

    def connect(self):
        try:
            logger.info("Attempting connection to MongoDB...")
            self.client = MongoClient(self.mongodb_uri, serverSelectionTimeoutMS=3000)
            self.client.admin.command("ping")
            self.db = self.client[self.database_name]
            self.plants_collection = self.db["plants"]
            self.is_connected = True
            logger.info(f"Successfully connected to MongoDB database '{self.database_name}'")

            # Ensure indexes
            try:
                self.plants_collection.create_index("scientific_name", unique=True)
                self.plants_collection.create_index("common_name")
                self.plants_collection.create_index("ayurvedic_name")
            except Exception as ie:
                logger.warning(f"Index creation warning: {ie}")

        except (ConnectionFailure, ServerSelectionTimeoutError, PyMongoError) as e:
            self.is_connected = False
            self.client = None
            self.db = None
            self.plants_collection = None
            logger.warning(
                "MongoDB server is currently unavailable. Using local botanical dataset fallback. "
                "The application will continue operating smoothly."
            )
        except Exception as e:
            self.is_connected = False
            logger.warning(f"Unexpected database connection status: {e}. Fallback active.")

    def close(self):
        if self.client:
            self.client.close()
            self.is_connected = False
            logger.info("MongoDB connection closed.")

    def find_by_scientific_name(self, scientific_name: str) -> Optional[Dict[str, Any]]:
        if not scientific_name:
            return None

        clean_name = scientific_name.strip()

        if self.is_connected and self.plants_collection is not None:
            try:
                # Case-insensitive exact match
                regex = re.compile(f"^{re.escape(clean_name)}$", re.IGNORECASE)
                doc = self.plants_collection.find_one({"scientific_name": regex})
                if doc:
                    doc["_id"] = str(doc.get("_id", ""))
                    return doc

                # Fallback to prefix / contains if exact match failed
                loose_regex = re.compile(re.escape(clean_name.split()[0]), re.IGNORECASE)
                doc = self.plants_collection.find_one({"scientific_name": loose_regex})
                if doc:
                    doc["_id"] = str(doc.get("_id", ""))
                    return doc
            except Exception as e:
                logger.error("Error querying MongoDB, falling back to local dataset")

        # Fallback to in-memory dataset
        clean_lower = clean_name.lower()
        for plant in self._fallback_plants:
            sn = plant.get("scientific_name", "").lower()
            if sn == clean_lower:
                return dict(plant)

        # Partial matching in fallback
        first_token = clean_lower.split()[0] if clean_lower else ""
        for plant in self._fallback_plants:
            sn = plant.get("scientific_name", "").lower()
            if first_token and first_token in sn:
                return dict(plant)

        return None

    def search_plants(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        if not query or not query.strip():
            return []

        q = query.strip()
        results = []

        if self.is_connected and self.plants_collection is not None:
            try:
                regex = re.compile(re.escape(q), re.IGNORECASE)
                cursor = self.plants_collection.find({
                    "$or": [
                        {"common_name": regex},
                        {"scientific_name": regex},
                        {"ayurvedic_name": regex},
                        {"description": regex}
                    ]
                }).limit(limit)

                for doc in cursor:
                    doc["_id"] = str(doc.get("_id", ""))
                    results.append(doc)
                return results
            except Exception as e:
                logger.error("Error querying MongoDB search, falling back to local dataset")

        # Fallback search
        q_lower = q.lower()
        for plant in self._fallback_plants:
            cn = plant.get("common_name", "").lower()
            sn = plant.get("scientific_name", "").lower()
            an = plant.get("ayurvedic_name", "").lower()
            desc = plant.get("description", "").lower()

            if q_lower in cn or q_lower in sn or q_lower in an or q_lower in desc:
                results.append(dict(plant))
                if len(results) >= limit:
                    break

        return results

    def get_all_plants(self, skip: int = 0, limit: int = 50) -> List[Dict[str, Any]]:
        results = []
        if self.is_connected and self.plants_collection is not None:
            try:
                cursor = self.plants_collection.find().skip(skip).limit(limit)
                for doc in cursor:
                    doc["_id"] = str(doc.get("_id", ""))
                    results.append(doc)
                if results:
                    return results
            except Exception as e:
                logger.error("Error reading all plants from MongoDB, falling back")

        # Fallback
        return [dict(p) for p in self._fallback_plants[skip : skip + limit]]

# Singleton instance
db_manager = DatabaseManager()
