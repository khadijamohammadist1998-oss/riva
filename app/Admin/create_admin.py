# create_admin.py
from passlib.context import CryptContext
from database import SessionLocal
#from db.session import SessionLocal
from models.admin_user import AdminUser

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


db = SessionLocal()
'''
password_hash = pwd_context.hash("admin123")
print("RAW PASSWORD:", password_hash)
print("TYPE:", type(password_hash))
'''
admin = AdminUser(
    username="admin",
    email = "admin@admin.com",
    password_hash= "123" #password_hash
)

db.add(admin)
db.commit()

db.close()
print("Admin created")

## run first time ## once 
## python venv/Admin/create_admin.py