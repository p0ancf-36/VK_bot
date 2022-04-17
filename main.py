import random
import uvicorn
import vk

from pydantic import BaseSettings
from fastapi import FastAPI, Request, Response, HTTPException, Depends
from fastapi.responses import HTMLResponse

from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import text

from common.reply import reply_to_message

class Settings(BaseSettings):
	group_id: int
	confirmation_response: str
	vk_token: str
	sqlite_config: str

	class Config:
		env_file = '.env'

settings = Settings()

vk_session = vk.Session(access_token = settings.vk_token)
vk_api = vk.API(vk_session)

engine = create_async_engine(
	settings.sqlite_config,
	echo=True
)
async_session = sessionmaker(
	engine,
	class_=AsyncSession,
	expire_on_commit=False
)

async def get_session() -> AsyncSession:
	async with async_session() as session:
		yield session

app = FastAPI()

async def confirmation(**kwargs):
	req_body = kwargs['req_body']
	if req_body['group_id'] == settings.group_id:
		return Response(content=settings.confirmation_response, media_type='application/json')

	return HTTPException(status_code=400, detail='Invalid group id')

@app.post('/main')
async def auth(req: Request, session: AsyncSession = Depends(get_session)):
	req_body = await req.json()

	response = await {
		'confirmation': confirmation,
		'message_new': reply_to_message
	}.get(req_body['type'], lambda **kwargs: False)(req_body=req_body, vk_api=vk_api, session=session)
	return response

@app.get('/admin', response_class=HTMLResponse)
async def admin():
	file = open('./frontend/admin.html')
	return file.read()

@app.post('/send/{group_id}')
async def send(group_id, message, session: AsyncSession = Depends(get_session)):
	print(message)

	sql_text = text(f"SELECT chat_id FROM users WHERE group_id = {group_id}")
	response = (await session.execute(sql_text)).all()

	for i in response:
		vk_api.messages.send(
			user_id = i,
			message = message,
			random_id = random.randint(0, 2**31),
			v=5.131
		)

if __name__ == "__main__":
	uvicorn.run('main:app', port=5000, reload=True)