from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import text

async def get_response(session: AsyncSession, req: str):
	sql_text = text(f"SELECT answer FROM phrases WHERE phrase = '{req}'")
	response = await session.execute(sql_text)
	await session.commit()
	return response.all()

async def save_new_phrase(session: AsyncSession, question: str, answer: str):
	sql_text = text("SELECT id FROM phrases ORDER BY id DESC")
	response = await session.execute(sql_text)
	last_id = response.all()[0].id
	sql_text = text(f"INSERT INTO phrases VALUES ({last_id+1}, '{question}', '{answer}')")
	await session.execute(sql_text)
	await session.commit()
	return True
