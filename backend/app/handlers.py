from .database import database
from typing import Dict, Any, List, Union

async def select(query: str, values: Dict[str, Any] = None, fetch_all: bool = False) -> Union[Dict, List[Dict], None]:
    if not database.is_connected:
        await database.connect()
    
    try:
        if fetch_all:
            result = await database.fetch_all(query=query, values=values)
        else:
            result = await database.fetch_one(query=query, values=values)
        return result
    except Exception as e:
        return None

async def update(query: str, values: Dict[str, Any]) -> bool:
    if not database.is_connected:
        await database.connect()
    
    try:
        await database.execute(query=query, values=values)
        return True
    except Exception as e:
        return False

async def delete(query: str, values: Dict[str, Any]) -> bool:
    if not database.is_connected:
        await database.connect()
    
    try:
        await database.execute(query=query, values=values)
        return True
    except Exception as e:
        print(f"Database delete error: {e}")
        return False
