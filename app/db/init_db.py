from db.session import engine
from db.base import Base

# import all models
from models.user import User
#from models.patient import Patient
from models.clinical_case import ClinicalCase
from models.admin_user import AdminUser
#from models.cough_details import CoughDetails
#from models.ai_result import AIResult

#def init_db():
Base.metadata.create_all(bind=engine)

# We run this file once to create  all tables
## python db/init_db.py
## python venv/db/init_db.py

'''
## first time (once)
from database import engine
from models.models import Base

Base.metadata.create_all(bind=engine)
'''