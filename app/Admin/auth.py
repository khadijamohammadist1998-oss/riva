# admin/auth.py
from sqladmin.authentication import AuthenticationBackend
from fastapi import Request
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal
from models.admin_user import AdminUser

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        db: Session = SessionLocal()
        admin = db.query(AdminUser).filter(AdminUser.username == username).first()

        if not admin:
            return False

        ##if not pwd_context.verify(password, admin.password_hash):
        if admin.password_hash != password:
            return False

        request.session.update({"admin_id": admin.id})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        return request.session.get("admin_id") is not None