import random
import shutil
import string

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from routers.schemas import PostBase, PostDisplay, UserAuth
from db.db_post import Session
from db.database import get_db
from db import db_post
from typing import List
from auth.oauth2 import get_current_user

router = APIRouter(
    prefix='/post',
    tags=['post']
)

image_url_types = ['absolute','relative']


@router.post('', response_model=PostDisplay)
def create(request: PostBase, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    if not request.image_url_type in image_url_types:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Parameter image_url_type can take values 'absolute' or 'relative'.")
    return db_post.create(db, request)


@router.get('/all', response_model=List[PostDisplay])
def posts(db: Session = Depends(get_db)):
    return db_post.get_all(db)


@router.post('/image')
def upload_image(image: UploadFile = File(...), current_user: UserAuth = Depends(get_current_user)):
    # generating a unique filename to store image in local
    letter = string.ascii_letters
    rand_str = ''.join(random.choice(letter) for i in range(6))
    new = f'_{rand_str}.'
    filename = new.join(image.filename.rsplit('.', 1))
    path = f'images/{filename}'

    # opening file and copying the uploaded image
    with open(path, 'w+b') as buffer:
        shutil.copyfileobj(image.file, buffer)

    return {'filename': path}
