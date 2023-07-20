from fastapi import FastAPI, Response, APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..model import Post
from ..schema import CreatePost, PostResponse
from ..routers import oauth2

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.get('/', response_model=List[PostResponse])
def posts(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user), limit: int = 10, skip:int =0):
    post = db.query(Post).limit(limit).offset(skip).all()
    return post


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: CreatePost, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    new_post = Post(owner_id=user_id.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get('/{id}', response_model=PostResponse)
def get_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not such id exist")

    return post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    post = db.query(Post).filter(Post.id == id).first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with it {id} does not exist")

    if post.owner_id != int (user_id.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized to perform requested action")

    db.delete(post)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=PostResponse)
def update_post(id: int, post: CreatePost, db:Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):

    updated_post = db.query(Post).filter(Post.id == id).first()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with it {id} does not exist")

    if updated_post.owner_id != int(user_id.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized to perform requested action")


    updated_post.title = post.title
    updated_post.content = post.content
    db.commit()

    response = {
        "id": updated_post.id,
        "title": updated_post.title,
        "content": updated_post.content,
        "published": updated_post.published,
        "created_at": updated_post.created_at
    }

    return updated_post

