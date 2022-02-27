from typing import Coroutine
import uvicorn
from pydantic import BaseSettings
from fastapi import FastAPI, Request, Response, HTTPException

class Settings(BaseSettings):
	group_id: int
	confirmation_response: str

	class Config:
		env_file = '.env'

settings = Settings()
app = FastAPI()

def confirmation(req_body: Coroutine):
	if req_body['group_id'] == settings.group_id:
		return Response(content=settings.confirmation_response, media_type='application/json')

	return HTTPException(status_code=400, detail='Invalid group id')

@app.post('/main')
async def auth(req: Request):
	req_body = await req.json()

	return {
		'confirmation': confirmation(req_body)
	}.get(req_body['type'], False)

if __name__ == "__main__":
	uvicorn.run('main:app', port=5000, reload=True)