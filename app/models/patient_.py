from pydantic import BaseModel
from typing import List, Dict, Optional

class PatientForm(BaseModel):
    # Step 1
    country: str
    age: str
    gender: str
    marital_status: str
    is_pregnant: bool

    # Step 2
    smoking_exposure: List[str]
    ex_smoker_duration: Optional[str]

    # Step 3
    main_symptoms: List[str]
    symptoms_duration: str

    # Step 4
    cough_details: Dict[str, bool]
    sputum_color: str

    # Step 5
    past_medical_history: List[str]
    surgery_details: Optional[str]

    # Step 6
    family_history: List[str]

    # Step 7
    cough_audio_path: Optional[str]
    breath_audio_path: Optional[str]

    additional_notes: Optional[str]
