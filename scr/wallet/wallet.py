from fastapi import FastAPI, Response, Request, HTTPException
from fastapi.responses import RedirectResponse
import hashlib
from datetime import datetime, timezone
import requests
from pydantic import BaseModel
import sqlite3
import config

app = FastAPI()

def create_connection():
    return sqlite3.connect("../../data/database.sqlite")

# Создание таблицы, если ее нет
with create_connection() as conn:
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS connections (
            connection_hash TEXT PRIMARY KEY,
            appUrl TEXT,
            address TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()

class NewConnection(BaseModel):
    appUrl: str
    address: str
    timestamp: datetime

    class Config:
        arbitrary_types_allowed = True

@app.get("/",)
def home_page(response: Response):
    wallet_address = config.test_wallet_address
    response.set_cookie(key="address", value=wallet_address)
    return wallet_address

@app.get('/connection')
def connection(request: Request):
    open_address = request.cookies.get("address")

    new_connection = NewConnection(
        appUrl=request.query_params['appUrlConnect'],
        address=open_address,
        timestamp=datetime.now(timezone.utc)
    )

    connection_hash = hashlib.sha256(
        str(new_connection.dict()).encode()).hexdigest()

    url = f"http://{new_connection.appUrl}/connection/{connection_hash}"
    data = {
        "appUrl": new_connection.appUrl,
        "address": new_connection.address,
        "timestamp": new_connection.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        "connection_hash": connection_hash
    }

    try:
        response = requests.post(f"http://127.0.0.2:8000/connection/{connection_hash}", json=data)
        response.raise_for_status()  # Проверка на наличие ошибок HTTP
        if response.json() == {"message": "Connection saved successfully"}:
            return RedirectResponse(url=f"{url}?connect=true")
        else:
            return RedirectResponse(url=f"{url}?&connect=false")

    except requests.RequestException as e:
        return f"Error: {e}"

from fastapi import HTTPException

@app.post('/connection/{connection_hash}')
def hash_connection(connection_hash: str, new_connection: NewConnection):
    with create_connection() as conn:
        new_cursor = conn.cursor()

        try:
            if not new_connection:
                print("Invalid connection data")
                raise HTTPException(status_code=422, detail="Invalid connection data")

            new_cursor.execute(
                'SELECT * FROM connections WHERE connection_hash = ?', (connection_hash,))
            existing_connection = new_cursor.fetchone()

            if existing_connection:
                print("Connection already exists")
            else:
                new_cursor.execute('''
                    INSERT INTO connections (connection_hash, appUrl, address, timestamp)
                    VALUES (?, ?, ?, ?)
                ''', (connection_hash, new_connection.appUrl,
                    new_connection.address, str(new_connection.timestamp)))
                conn.commit()
                print("Connection saved successfully")

                return {"message": "Connection saved successfully"}

        except Exception as e:
            print(f"Error during hash_connection: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
        finally:
            new_cursor.close()


@app.get('/connection/{connection_hash}/info')
def connection_info(connection_hash: str):
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                'SELECT * FROM connections WHERE connection_hash = ?', (connection_hash,))
            existing_connection = cursor.fetchone()

            if existing_connection:
                return {
                    "appUrl": existing_connection[1],
                    "address": existing_connection[2],
                    "timestamp": existing_connection[3]
                }
            else:
                raise HTTPException(status_code=404, detail="Connection not found")

        except Exception as e:
            print(f"Error during connection_info: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
        finally:
            cursor.close()

@app.delete('/connection/{connection_hash}')
def connection_delete(connection_hash: str):
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                'SELECT * FROM connections WHERE connection_hash = ?', (connection_hash,))
            existing_connection = cursor.fetchone()

            if existing_connection:
                cursor.execute(
                    'DELETE FROM connections WHERE connection_hash = ?', (connection_hash,))
                conn.commit()
                return {"message": "Connection deleted successfully"}
            else:
                raise HTTPException(status_code=404, detail="Connection not found")

        except Exception as e:
            print(f"Error during connection_delete: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
        finally:
            cursor.close()




















