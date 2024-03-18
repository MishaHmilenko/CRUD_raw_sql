from fastapi import APIRouter, HTTPException

from src.db.main import create_tables, drop_tables

router = APIRouter(prefix='/tasks', tags=['tasks'])


@router.get('/initdb')
async def initdb():
    try:
        create_tables()
        return {'message': 'Tables created!'}
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f'Error {e}'
        )


@router.delete('/delete-tables')
async def delete_tables():
    try:
        drop_tables()
        return {'message': 'Tables dropped!'}
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f'Error {e}'
        )