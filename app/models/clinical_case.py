from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, ARRAY, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.base import Base

class ClinicalCase(Base):
    __tablename__ = "clinical_cases"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", backref="clinical_cases")

    age = Column(Integer)
    gender = Column(String)
    country = Column(String)

    marital_status = Column(String)
    is_pregnant = Column(Boolean)
    
    symptoms = Column(ARRAY(String))
    symptoms_duration = Column(String)
    
    smoking_exposure = Column(ARRAY(String))
    ex_smoker_duration = Column(String)
    
    cough_details = Column(JSONB, default={
                    "dry_cough": False,
                    "productive_cough": False,
                    "worse_at_night": False,
                    "worse_in_morning": False,
                    "continuous_all_day": False,
                    "hemoptysis": False,
                    "choking_episodes": False,
                    "post_nasal_drip": False
                })
    
    sputum_color = Column(String)
    
    medical_history = Column(ARRAY(String))
    family_history = Column(ARRAY(String))
    surgery_details = Column(String)
    
    additional_notes = Column(Text)
    
    breath_audio_path = Column(String)
    cough_audio_path = Column(String)
    
    final_diagnosis = Column(String)
    confidence = Column(String)   # Low / Medium / High
    supporting_evidence = Column(ARRAY(Text))
    
    ai_model = Column(String, nullable=True)   # llama3 / gpt / etc
    ai_version = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())


'''
   dry_cough = Column(Boolean)
    productive_cough = Column(Boolean)
    worse_at_night = Column(Boolean)
    worse_in_morning = Column(Boolean)
    continuous_all_day = Column(Boolean)
    hemoptysis = Column(Boolean)
    choking_episodes = Column(Boolean)
    post_nasal_drip = Column(Boolean)
    
'''