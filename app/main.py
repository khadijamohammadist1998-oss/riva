from fastapi import FastAPI, Depends, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
import uuid
import shutil
import json
from pathlib import Path
from pydantic import BaseModel
from typing import List, Dict, Optional
from models.patient_ import PatientForm
from services.ai_service import analyze_patient
from services.ai_service import analyze_patient3
from sqladmin import Admin, ModelView
from database import engine
from models.clinical_case import ClinicalCase
#from models.models import DiagnosisRequest
#from admin import DiagnosisRequestAdmin
from database import get_db
from sqlalchemy.orm import Session

from db.session import engine
from Admin.admin import (UserAdmin, ClinicalCaseAdmin)
from Admin.auth import AdminAuth


print("🔥🔥🔥 THIS IS MY MAIN.PY 🔥🔥🔥")

app = FastAPI(
    title="RIVA AI Backend",
    description="Respiratory Health AI Assistant",
    version="1.0"
)

authentication_backend = AdminAuth(secret_key="SUPER_SECRET_KEY")

admin = Admin(app, engine, authentication_backend=authentication_backend)

from starlette.middleware.sessions import SessionMiddleware

app.add_middleware(SessionMiddleware,secret_key="SUPER_SECRET_KEY")

##admin.add_view(DiagnosisRequestAdmin)
admin.add_view(UserAdmin)
admin.add_view(ClinicalCaseAdmin)


import os
# Project Root
BASE_DIR = Path(__file__).resolve().parent.parent

# uploads folder in project root (NOT inside app, NOT inside venv)
UPLOAD_DIR = BASE_DIR / "uploads"
COUGH_DIR = UPLOAD_DIR / "cough"
BREATH_DIR = UPLOAD_DIR / "breath"

COUGH_DIR.mkdir(parents=True, exist_ok=True)
BREATH_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

class PatientInput(BaseModel):
    patient_json: dict
    
# API endpoint
@app.post("/analyze")
def analyze(
    patient_data: str = Form(...),
    cough_audio: UploadFile | None = File(None),
    breath_audio: UploadFile | None = File(None),
    db: Session = Depends(get_db)
):
    # =========================
    # 1️⃣ Parse patient JSON
    # =========================
    print("Received patient data from the RIVA app:")
    patient_dict = json.loads(patient_data)
    print(patient_dict)
    
    # =========================
    # 2️⃣ Save audio files
    # =========================
    cough_path = None
    breath_path = None

    if cough_audio:
        filename = f"{uuid.uuid4()}.m4a"
        absolute_path = COUGH_DIR / filename

        with open(absolute_path, "wb") as buffer:
            shutil.copyfileobj(cough_audio.file, buffer)

        # نحفظ في DB مسار نسبي فقط
        cough_path = f"uploads/cough/{filename}"

    if breath_audio:
        filename = f"{uuid.uuid4()}.m4a"
        absolute_path = BREATH_DIR / filename

        with open(absolute_path, "wb") as buffer:
            shutil.copyfileobj(breath_audio.file, buffer)

        breath_path = f"uploads/breath/{filename}"
    
    # =========================
    # 3️⃣ AI Result (Mock)
    # =========================
    ai_result = {
        "final_diagnosis": "GERD",
        "confidence": "Medium",
        "supporting_evidence": [
            "Symptoms of chest pain/tightness and heartburn are consistent with GERD.",
            "Duration of symptoms is typical for GERD.",
            "Smoking exposure may exacerbate symptoms."
        ]
    }

    # =========================
    # 4️⃣ Save to DB
    # =========================
    clinical_case_record = ClinicalCase(
        age=patient_dict.get("age"),
        gender=patient_dict.get("gender"),
        country=patient_dict.get("country"),

        marital_status=patient_dict.get("marital_status"),
        is_pregnant=patient_dict.get("is_pregnant"),

        symptoms=patient_dict.get("main_symptoms"),
        symptoms_duration=patient_dict.get("symptoms_duration"),

        smoking_exposure=patient_dict.get("smoking_exposure"),
        ex_smoker_duration=patient_dict.get("ex_smoker_duration"),

        cough_details=patient_dict.get("cough_details"),
        sputum_color=patient_dict.get("sputum_color"),

        medical_history=patient_dict.get("past_medical_history"),
        family_history=patient_dict.get("family_history"),
        surgery_details=patient_dict.get("surgery_details"),

        additional_notes=patient_dict.get("additional_notes"),

        cough_audio_path=cough_path,
        breath_audio_path=breath_path,

        final_diagnosis=ai_result["final_diagnosis"],
        confidence=ai_result["confidence"],
        supporting_evidence=ai_result["supporting_evidence"],

        ai_model="",
        ai_version="v1"
    )

    db.add(clinical_case_record)
    db.commit()
    db.refresh(clinical_case_record)

    # =========================
    # 5️⃣ Response
    # =========================
    return ai_result

## login endpoint
## POST /auth/register 
## POST /auth/login
from routers import auth

app.include_router(auth.router, prefix="/auth", tags=["Auth"])

@app.post("/analyze2")
#def analyze(patient: PatientForm):
def analyze(patient: PatientForm, db: Session = Depends(get_db)):
    print("Received patient data from the RIVA app:")
    print(patient.dict())
    # 1. Analyze the record
    # ai_result = analyze_patient3(patient.dict())
    ai_result = {
                "final_diagnosis": "GERD",
                "confidence": "Medium",
                "supporting_evidence": [
                    "Symptoms of chest pain/tightness and heartburn are consistent with gastroesophageal reflux disease (GERD).",
                    "Duration of symptoms (>1 month) is also typical for GERD.",
                    "Smoking exposure may exacerbate GERD symptoms."
                ]
                }
    print("AI RESULT****")
    print(ai_result)
    return ai_result
    # 2. save the record and the  AI result 
    '''
    record = DiagnosisRequest(
        patient_data=patient.dict(),
        final_diagnosis = ai_result.get("final_diagnosis"),
        confidence = ai_result.get("confidence"),
        supporting_evidence = ai_result.get("supporting_evidence")
    )
    
    db.add(record)
    db.commit()
    db.refresh(record)  '''




## after create folder:
## python -m venv venv

## Activating the environment:
## venv\Scripts\activate

## pip install fastapi uvicorn 
## pip install fastapi uvicorn pydantic

## play on fastapi: 
## uvicorn main:app --reload   ##  for laptob 
## uvicorn main:app --host 0.0.0.0 --port 8000 --reload   ## for real mobile 


## open 
## http://127.0.0.1:8000/docs
