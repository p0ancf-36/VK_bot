from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import text

async def get_response(session: AsyncSession, req: str):
	sql_text = text(f"SELECT answer FROM phrases WHERE phrase = '{req}'")
	response = await session.execute(sql_text)
	await session.commit()
	return response.all()