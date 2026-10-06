# AyurScan — AI-Powered Ayurvedic Plant Identification & Knowledge Platform

AyurScan is a full-stack, AI-driven botanical field guide that identifies single or multiple Ayurvedic plants from uploaded photos or live camera captures using Google Gemini Vision, and cross-references each identified plant with curated traditional Ayurvedic documentation stored in MongoDB.

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Key Features](#key-features)
3. [Architecture](#architecture)
4. [Technology Stack](#technology-stack)
5. [Project Structure](#project-structure)
6. [Installation & Setup](#installation--setup)
7. [Environment Variables](#environment-variables)
8. [MongoDB Setup & Database Seeding](#mongodb-setup--database-seeding)
9. [Running the Application](#running-the-application)
10. [API Endpoints](#api-endpoints)
11. [Multi-Plant Identification & Confidence Handling](#multi-plant-identification--confidence-handling)
12. [Testing](#testing)
13. [Security Best Practices](#security-best-practices)
14. [Future YOLO & Object Detection Architecture](#future-yolo--object-detection-architecture)
15. [Medical & Educational Disclaimer](#medical--educational-disclaimer)

---

## 1. Project Overview

Traditional plant identification apps often focus exclusively on the single most prominent leaf in an image, neglecting surrounding companion flora. **AyurScan** systematically inspects the entire image to detect and classify **all visually distinguishable plants** (e.g., *Tulsi + Neem + Mint* in one frame).

Identified plants are automatically enriched with verified traditional records, including Ayurvedic and Sanskrit names, traditional uses, plant parts utilized, precautions, and warnings. If a plant in the photo is blurry, obscured, or lacks visual evidence, the system refuses to guess, providing clear diagnostic feedback while preserving successful identifications.

---

## 2. Key Features

- **Multi-Plant Recognition**: Analyzes the complete photo to recognize multiple distinct species in one pass.
- **Strict Anti-Hallucination & Confidence Threshold**:
  - Application-level threshold (`0.70`).
  - Plants with confidence $\ge 0.70$ are classified as `identified`.
  - Plants with confidence $< 0.70$ are classified as `unclear` with diagnostic advice (e.g., "Plant is partially hidden; upload a closer photo").
- **70+ Curated Ayurvedic Monographs**: Comprehensive botanical database with scientific binomials, Sanskrit names, family, traditional uses, and precautions.
- **Fast Full-Text Botanical Search**: Search plants across common names (e.g., *Tulsi*), scientific names (e.g., *Ocimum tenuiflorum*), and Sanskrit names (e.g., *Tulasi*).
- **Graceful Offline Fallback**: If MongoDB is starting up or temporarily offline, the backend seamlessly switches to its local catalog cache without downtime.
- **Zero API Key Leakage**: Google Gemini API key resides solely in the FastAPI backend environment.
- **Responsive Botanical Field Guide UI**: Editorial design system with DM Sans and Fraunces typography, live camera capture, and plant monograph modals.

---

## 3. Architecture

### Current Phase (Phase 1 — MVP)
```
User Image (Upload / Camera)
         ↓
FastAPI Backend (/api/identify)
  - Image Validation & EXIF Normalization
  - Downscaling / Optimization (Pillow)
         ↓
Google Gemini 2.5 Flash API
  - Full-image visual inspection
  - Structured JSON response schema
         ↓
Multi-Plant Results (Identified + Unclear)
         ↓
MongoDB / Botanical Catalog
  - Match by scientific_name (e.g. Ocimum tenuiflorum)
  - Retrieve Ayurvedic uses, precautions, parts
         ↓
Frontend Results UI
  - Separate cards for each identified plant
  - Diagnostic warning cards for unclear plants
```

---

## 4. Technology Stack

- **Backend**:
  - Python 3.12+
  - FastAPI & Starlette
  - Pydantic v2 (Data modeling & structured validation)
  - Google Gemini SDK (`google-genai` official SDK)
  - PyMongo & MongoDB
  - Pillow (Image optimization & EXIF normalization)
  - Uvicorn (ASGI server)
- **Frontend**:
  - Semantic HTML5 & Modern Vanilla CSS (editorial botanical design system)
  - Vanilla JavaScript (Fetch API, Canvas compression, WebRTC camera API)
- **Database**:
  - MongoDB (Curated collection `plants` with indexes on `scientific_name`, `common_name`, `ayurvedic_name`)

---

## 5. Project Structure

```
AyurScan/
│
├── frontend/
│   ├── index.html           # Home page with search engine & field notes
│   ├── identify.html        # Photo upload, camera capture & vision scanner
│   ├── result.html          # Multi-plant identification cards & monograph modal
│   ├── login.html           # Account access demo
│   ├── style.css            # Core design system tokens & shared layouts
│   ├── identify.css         # Scanner stage & upload styles
│   ├── result.css           # Multi-plant cards, summary banner, & modal styles
│   ├── login.css            # Auth layout styles
│   ├── script.js            # Live catalog search & navigation logic
│   ├── identify.js          # Camera capture, upload & API dispatch
│   ├── result.js            # Multi-plant renderer & modal controller
│   └── login.js             # Auth demo controller
│
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI application entrypoint & static mount
│   │   ├── routes/
│   │   │   ├── identify.py  # POST /api/identify
│   │   │   ├── plants.py    # GET /api/plants & GET /api/plants/{name}
│   │   │   └── search.py    # GET /api/search?q=
│   │   ├── services/
│   │   │   ├── gemini_service.py # Gemini 2.5 Flash structured vision client
│   │   │   ├── plant_service.py  # Plant data enrichment & MongoDB queries
│   │   │   └── image_service.py  # Image validation, optimization & YOLO hooks
│   │   ├── database/
│   │   │   └── mongodb.py   # MongoDB manager with seamless offline fallback
│   │   ├── models/
│   │   │   └── plant.py     # Pydantic schemas for vision & catalog records
│   │   └── utils/
│   │       └── helpers.py   # Text formatting & normalization helpers
│   ├── data/
│   │   └── plants.json      # 70 curated Ayurvedic plant records
│   ├── scripts/
│   │   ├── seed_plants.py   # Idempotent MongoDB database seeder
│   │   └── generate_plants_data.py # Dataset generator
│   ├── tests/
│   │   └── test_ayurscan.py # Automated test suite (22 unit & integration tests)
│   ├── .env.example         # Environment template
│   ├── .gitignore           # Ignores .env and virtual environments
│   └── requirements.txt     # Python dependencies
│
├── .gitignore
└── README.md
```

---

## 6. Installation & Setup

### Prerequisites
- Python 3.10+
- MongoDB (local or MongoDB Atlas connection string)
- Google Gemini API key (from [Google AI Studio](https://aistudio.google.com/))

### 1. Clone & Navigate to Backend
```bash
cd backend
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

---

## 7. Environment Variables

Create `backend/.env` based on `backend/.env.example`:

```bash
cp .env.example .env
```

Edit `backend/.env`:
```ini
# Google Gemini API Key (Backend only, never expose to frontend)
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash

# Application Confidence Threshold (0.0 to 1.0)
CONFIDENCE_THRESHOLD=0.70

# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=ayurscan

# Server Configuration
HOST=127.0.0.1
PORT=8000
CORS_ORIGINS=http://localhost:5500,http://127.0.0.1:5500,http://localhost:8000,http://127.0.0.1:8000
```

> **Security Note:** `.env` is listed in `.gitignore` and is never committed to source control.

---

## 8. MongoDB Setup & Database Seeding

1. Start your local MongoDB server or prepare your MongoDB Atlas cluster URI in `backend/.env`.
2. Run the database seed script:
```bash
python scripts/seed_plants.py
```

Expected output:
```
============================================================
AyurScan Plant Database Seeder
============================================================
Loaded 70 plants from plants.json
Connecting to MongoDB at: mongodb://localhost:27017
Connected to MongoDB successfully.
Ensuring indexes on scientific_name, common_name, and ayurvedic_name...

------------------------------------------------------------
Inserted: 70 plants
Skipped:  0 existing plants
Database seeding completed successfully.
------------------------------------------------------------
```

*Note: The script is idempotent. Running it again will skip existing plants without creating duplicate entries.*

---

## 9. Running the Application

### Option A: Unified Full-Stack Server (Recommended)
FastAPI is pre-configured to serve both API routes and static frontend files:
```bash
cd backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
Open your browser to:
👉 **http://127.0.0.1:8000/**

### Option B: Standalone Frontend
You can also run the backend on port 8000 and open the frontend via VS Code Live Server or python http server:
```bash
cd frontend
python -m http.server 5500
```
Visit **http://127.0.0.1:5500/**

---

## 10. API Endpoints

### Identification
- **`POST /api/identify`**
  - **Body**: `multipart/form-data` with `image` file.
  - **Returns**:
    ```json
    {
      "total_detected": 3,
      "identified_count": 2,
      "unclear_count": 1,
      "plants": [
        {
          "common_name": "Tulsi (Holy Basil)",
          "scientific_name": "Ocimum tenuiflorum",
          "confidence": 0.94,
          "status": "identified",
          "approximate_location": "Center Foreground",
          "ayurvedic_info": {
            "ayurvedic_name": "Tulasi",
            "family": "Lamiaceae",
            "description": "An aromatic perennial shrub...",
            "traditional_uses": ["Brewed as herbal tea...", "Home gardens..."],
            "plant_parts_used": ["Leaves", "Seeds"],
            "precautions": ["Mild blood-thinning properties..."],
            "warnings": ["Do not consume pure essential oils undiluted..."]
          }
        },
        {
          "common_name": "Neem",
          "scientific_name": "Azadirachta indica",
          "confidence": 0.91,
          "status": "identified",
          "ayurvedic_info": { "ayurvedic_name": "Nimba" }
        },
        {
          "common_name": null,
          "scientific_name": null,
          "confidence": 0.35,
          "status": "unclear",
          "reason": "Plant is partially hidden, out of focus, or lacking flowers.",
          "message": "Plant is not clearly visible. Please upload a clearer image."
        }
      ],
      "disclaimer": "This information is provided for educational purposes..."
    }
    ```

### Catalog & Search
- **`GET /api/plants`**: Returns paginated list of curated plants (`?skip=0&limit=50`).
- **`GET /api/plants/{scientific_name}`**: Returns full monograph for a specific plant.
- **`GET /api/search?q={query}`**: Searches plants by common name, scientific name, or Sanskrit name.
- **`GET /api/health`**: Health check reporting Gemini readiness, model name, and database status.

---

## 11. Multi-Plant Identification & Confidence Handling

1. **Whole-Image Vision Prompt**: Gemini 2.5 Flash is instructed with a strict system prompt to inspect all quadrants (foreground, background, periphery) and extract all distinct species.
2. **Confidence Filtering**: Every candidate is evaluated against the `CONFIDENCE_THRESHOLD` (default: `0.70`).
3. **No Hallucination Policy**: If visual characteristics are incomplete (e.g. shadowed leaf, lack of flowers, blur), status is forced to `unclear`, and names are set to `null` with a clear explanation.
4. **Non-destructive Result UI**: When 2 plants are clear and 1 is unclear, the 2 identified plants are displayed with complete Ayurvedic monographs, accompanied by an explicit warning card for the unclear plant.

---

## 12. Testing

Run the automated test suite covering all major scenarios:
```bash
cd backend
python -m unittest tests/test_ayurscan.py
```

### Scenarios Tested (22 Tests):
1. Single clear plant identification
2. Multiple clear plants (Tulsi + Neem)
3. Multiple plants with one unclear (Tulsi + Neem + Hibiscus blurry)
4. Application of confidence threshold ($< 0.70 \rightarrow \text{unclear}$)
5. Rejection of invalid, corrupted, or empty uploads
6. Automatic downscaling and JPEG optimization of large images ($>1600\text{px}$)
7. Exact and case-insensitive botanical name matching
8. Search across common, botanical, and Sanskrit names
9. Graceful fallback when plants are not yet in the database
10. Graceful offline fallback when MongoDB is unavailable
11. Future YOLO crop extraction interface

---

## 13. Security Best Practices

- **Zero Client-Side Secrets**: All Gemini API requests are initiated exclusively from the backend. The API key is never bundled in HTML, JS, or client responses.
- **Strict Input Validation**: Validates image headers, file sizes (max 15MB), and MIME types before sending to Gemini.
- **Graceful Error Masking**: Never returns raw stack traces, API keys, or database credentials to end users.
- **HTTP 429 Rate Limit Handling**: Captures Google quota limits and provides courteous user messages ("Too many requests right now. Please try again in a moment.").

---

## 14. Future YOLO & Object Detection Architecture

AyurScan is designed so that a dedicated object detection model (e.g. YOLOv8 / YOLOv11) can be introduced in Phase 2 without rewriting the frontend or core API:

```
User Image
   ↓
[Phase 2 Object Detector: YOLO]
   ↓
Identified Bounding Box Crops (Plant A crop, Plant B crop, Plant C crop)
   ↓
[Phase 1 Pipeline: ImageService.extract_plant_crops_for_future_yolo()]
   ↓
Google Gemini Identification per Crop
   ↓
MongoDB Catalog Enrichment
   ↓
Frontend Results UI
```
The extension hook is already isolated in `backend/app/services/image_service.py` (`extract_plant_crops_for_future_yolo`).

---

## 15. Medical & Educational Disclaimer

AyurScan is an educational and botanical reference guide. Traditional Ayurvedic uses documented on this platform are for cultural appreciation and educational purposes. **This platform does not provide medical advice, diagnosis, or treatment.** Always seek the advice of a qualified physician or healthcare provider regarding any medical condition or before starting any herbal regimen.
