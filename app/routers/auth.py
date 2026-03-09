from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.session import get_db
from ..models.user import User
from ..schemas.user import UserCreate, UserLogin
from ..core.security import hash_password, verify_password

router = APIRouter()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    print("register")
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        full_name=user.full_name,
        email=user.email,
        nomber = "",
        hashed_password= user.password ##hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    db_user = db.query(User).filter(User.email == new_user.email).first()
    print("user_id app ********** ", db_user.id)
    return { "message": "User created successfully",
             "user_id": db_user.id,
             "email": db_user.email,      
             "full_name": db_user.full_name
           }


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    print("login app")
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    ##if not verify_password(user.password, db_user.hashed_password):
    if user.password == db_user.hashed_password:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    return {
        "message": "Login successful",
        "user_id": db_user.id,
        "email": db_user.email,      
        "full_name": db_user.full_name
    }