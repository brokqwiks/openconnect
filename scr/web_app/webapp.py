import time
from fastapi import FastAPI, WebSocket, Response, Request, Query, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
import webbrowser
from pydantic import BaseModel
import requests
import json

app = FastAPI()

class Connection(BaseModel):
    appUrl: str
    address: str
    timestamp: str



@app.get('/')
def root():
    return True

@app.get('/connection', response_class=HTMLResponse)
def connect(responce: Response):
    with open('templates/webapp.html', 'r', encoding='utf-8') as file:
        return file.read()

wallet_url = "127.0.0.2:8000"

@app.get('/connection/{connection_hash}')
def connection(responce: Response, request: Request, connection_hash):
    request_data = request.query_params
    if request_data['connect'] != None:
        if request_data['connect']:
            responce.set_cookie(key="OpenConnection", value=connection_hash)
            connection_data = requests.get(f"http://{wallet_url}/connection/{connection_hash}/info")
            connection_data.raise_for_status()
            connection_info = connection_data.json()
            responce.set_cookie(key="OpenAddress", value=connection_info['address'])
            return "Connect"
        else:
            return "Connection error"

@app.get('/connection/{connection_hash}/info')
def connection_info(connection_hash: str, request: Request):
    if connection_hash == request.cookies.get('OpenConnection'):
        try:
            response = requests.get(f"http://{wallet_url}/connection/{connection_hash}/info")
            response.raise_for_status()
            connection_info = response.json()
            return connection_info
        except requests.RequestException as e:
            return f"Error: {e}"

@app.get('/connection/{connection_hash}/delete')
def connection_delete(connection_hash: str, request: Request, responce: Response):
    if connection_hash == request.cookies.get('OpenConnection'):
        response = requests.delete(f"http://{wallet_url}/connection/{connection_hash}")
        response.raise_for_status()
        connection_delete_info = response.json()
        responce.delete_cookie(key="OpenConnection")
        responce.delete_cookie(key="OpenAddress")
        return connection_delete_info
