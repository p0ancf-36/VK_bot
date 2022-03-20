import random
from typing import TYPE_CHECKING
from fastapi import Response

from db.sql_req import get_response

if TYPE_CHECKING:
	from vk import API
	from sqlalchemy.ext.asyncio.session import AsyncSession

# def echo_message(answer):
# 	def echo(req_body, vk_api):
# 		sender_id = req_body['object']['message']['from_id']
# 		for i in answer:
# 			vk_api.messages.send(
# 				user_id = sender_id,
# 				message = f"{i}",
# 				random_id = random.randint(0, 2**31),
# 				v=5.131
# 			)
	
# 	if type(answer) == str: answer = [answer]
# 	return echo

# echo_messages = {
# 	"Привет" : echo_message("И тебе привет"),
# 	"Как дела?": echo_message(["Хорошо", "А как у тебя?"])
# }

async def reply_to_message(req_body, vk_api: 'API', session: 'AsyncSession'):
	message_text: str = req_body['object']['message']['text']
	sender_id = req_body['object']['message']['from_id']

	replies = await get_response(session, message_text)
	for reply in replies:
		vk_api.messages.send(
			user_id = sender_id,
			message = f"{reply.answer}",
			random_id = random.randint(0, 2**31),
			v=5.131
		)
	
	return Response("OK", media_type="application/json")