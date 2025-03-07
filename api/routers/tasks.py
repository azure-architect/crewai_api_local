from fastapi import APIRouter, Depends, HTTPException
from typing import List

from api.dependencies.db import get_db

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/")
async def get_all(db=Depends(get_db)):
    return {"message": "Get all tasks"}


@router.get("/{item_id}")
async def get_one(item_id: str, db=Depends(get_db)):
    return {"message": f"Get task {item_id}"}


@router.post("/")
async def create(db=Depends(get_db)):
    return {"message": "Create task"}


@router.put("/{item_id}")
async def update(item_id: str, db=Depends(get_db)):
    return {"message": f"Update task {item_id}"}


@router.delete("/{item_id}")
async def delete(item_id: str, db=Depends(get_db)):
    return {"message": f"Delete task {item_id}"}
