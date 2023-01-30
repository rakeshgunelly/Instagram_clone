from fastapi import APIRouter, Depends, HTTPException, status
from routers.schemas import PostBase, PostDisplay
from db.db_post import Session
from db.database import get_db
from db import db_post


router = APIRouter(
    prefix='/post',
    tags=['post']
)

image_url_types = ['absolute','relative']

@router.post('', response_model=PostDisplay)
def create(request: PostBase, db: Session = Depends(get_db)):
    if not request.image_url_type in image_url_types:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Parameter image_url_type can take values 'absolute' or 'relative'.")
    return db_post.create(db, request)
