from sqlalchemy.orm.session import Session
from routers.schemas import PostBase
from db.models import DbPost
import datetime
from fastapi import HTTPException,status


def create(db: Session, request: PostBase):
    new_post = DbPost(
        image_url=request.image_url,
        image_url_type=request.image_url_type,
        caption=request.caption,
        timestamp=datetime.datetime.now(),
        user_id=request.creator_id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


def get_all(db: Session):
    return db.query(DbPost).all()


def delete(db: Session, postid: int, current_user_id: int):
    post = db.query(DbPost).filter(DbPost.id == postid).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with post id: {postid} is not found')
    if post.user_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Only post user can delete the post')

    db.delete(post)
    db.commit()
    return 'ok'
