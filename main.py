import uvicorn
import vk

from pydantic import BaseSettings
from fastapi import FastAPI, Request, Response, HTTPException

from common.reply import reply_to_message

class Settings(BaseSettings):
	group_id: int
	confirmation_response: str
	vk_token: str

	class Config:
		env_file = '.env'

settings = Settings()

vk_session = vk.Session(access_token = settings.vk_token)
vk_api = vk.API(vk_session)

app = FastAPI()

def confirmation(req_body):
	if req_body['group_id'] == settings.group_id:
		return Response(content=settings.confirmation_response, media_type='application/json')

	return HTTPException(status_code=400, detail='Invalid group id')

@app.post('/main')
async def auth(req: Request):
	req_body = await req.json()

	return {
		'confirmation': lambda: confirmation(req_body),
		'messagenew': lambda: reply_to_message(req_body, vk_api)
	}.get(req_body['type'], lambda body: False)()

if __name__ == "__main__":
	uvicorn.run('main:app', port=5000, reload=True)