from typing import List

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from api import floor
from database import configuration
from schema import schemas
from schema.oa2 import get_current_user

router = APIRouter(tags=["Floors"], prefix="/floor")
get_db = configuration.get_db


@router.get("/", response_model=List[schemas.ShowFloor])
def get_all_foors(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    """
    Get all blogs
    Args:
        db (Session, optional): Database session. Defaults to None.
        current_user (schemas.User, optional): Current user. Defaults to None.
    Returns:
        List[schemas.ShowBlog]: List of blogs
    """
    return floor.get_all(db)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(
    request: schemas.Floor,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    """
    Create a floor
    Args:
        request (schemas.Floor): Floor to create
        db (Session, optional): Database session. Defaults to None.
        current_user (schemas.User, optional): Current user. Defaults to None.
    Returns:
        schemas.Blog: Created blog
    """
    return floor.create(request, db)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowFloor)
def get_floor_by_id(
    id: int,
    response: Response,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    """
    Get a floor by id
    Args:
        id (int): Floor id
        response (Response): FastAPI response
        db (Session, optional): Database session. Defaults to None.
        current_user (schemas.User, optional): Current user. Defaults to None.
    Returns:
        schemas.ShowBlog: Blog
    """
    return floor.show(id, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_floor(
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    """
    Delete a floor by id
    Args:
        id (int): Blog id
        db (Session, optional): Database session. Defaults to None.
        current_user (schemas.User, optional): Current user. Defaults to None.
    Returns:
        None: None
    """
    return floor.destroy(id, db)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_blog(
    id: int,
    request: schemas.Floor,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    """
    Update a floor by id
    Args:
        id (int): Floor id
        request (schemas.Blog): Floor to update
        db (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (schemas.User, optional): Current user. Defaults to Depends(get_current_user).
    Returns:
        schemas.Blog: Updated blog
    """
    return floor.update(id, request, db)
