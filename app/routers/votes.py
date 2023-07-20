from fastapi import FastAPI, APIRouter, status, HTTPException, Depends, Response
from sqlalchemy.orm import Session
from ..schema import Vote
from ..database import get_db
from ..model import Votes, Post
from . oauth2 import get_current_user

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: Vote, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):

    post = db.query(Post).filter(Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no such post exist")

    vote_query = db.query(Votes).filter(Votes.post_id == vote.post_id, Votes.user_id==user_id.id).first()

    if (vote.dir == 1):
        if vote_query:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {user_id.id} has alredy voted on post {vote.post_id}")
        new_vote = Votes(
            post_id = vote.post_id,
            user_id = user_id.id
        )
        db.add(new_vote)
        db.commit()
        return {"message": "you have successfully voted for the post."}
    else:
        if not vote_query:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote does not exist")

        db.delete(vote_query)
        db.commit()

        return {"message": "successfully deleted vote"}