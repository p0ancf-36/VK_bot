import random
import json
from typing import TYPE_CHECKING
from fastapi import Response
from sqlalchemy import text

from db.sql_req import get_response, save_new_phrase

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
	if "payload" in req_body['object']['message']:
		return await action(req_body, vk_api, session)

	message_text: str = req_body['object']['message']['text']
	sender_id = req_body['object']['message']['from_id']

	replies: str = await get_response(session, message_text.lower())

	if message_text.find("/") != -1:
		question, answer = message_text.split("/")
		await save_new_phrase(session, question, answer)
		return Response("OK", media_type="application/json")

	if len(replies) == 0:
		vk_api.messages.send(
			user_id = sender_id,
			message = "Извните я вас не понимаю. Позвать кожаного мешка?",
			random_id = random.randint(0, 2**31),
			v=5.131
		)
		vk_api.messages.send(
			user_id = sender_id,
			message = "Напишите в формате \"вопрос/ответ\", чтобы я это запомнил.",
			random_id = random.randint(0, 2**31),
			v=5.131
		)

	for reply in replies:
		vk_api.messages.send(
			user_id = sender_id,
			message = f"{reply.answer}",
			random_id = random.randint(0, 2**31),
			v=5.131
		)
	
	return Response("OK", media_type="application/json")

async def action(req_body, vk_api: 'API', session: 'AsyncSession'):
	payload = req_body['object']['message']['payload']

	if payload == '{"command":"start"}':
		return await start(req_body, vk_api)
	if payload == '{"command":"friends"}':
		return await add_user(session, req_body, vk_api, "friends")
	if payload == '{"command":"classmates"}':
		return await add_user(session, req_body, vk_api, "classmates")
	if payload == '{"command":"programmers"}':
		return await add_user(session, req_body, vk_api, "programmers")

async def start(req_body, vk_api: 'API'):
	sender_id = req_body['object']['message']['from_id']

	reply = "Выберите группу интересов."
	keyboard = {
		"one_time": True,
		"buttons": [
			[
				{
					"action": {
						"type": "text",
						"payload": '{"command": "friends"}',
						"label": "Друзья"
					},
					"color": "primary"
				},
				{
					"action": {
						"type": "text",
						"payload": '{"command": "classmates"}',
						"label": "Одноклассники"
					},
					"color": "primary"
				},
				{
					"action": {
						"type": "text",
						"payload": '{"command": "programmers"}',
						"label": "Программисты"
					},
					"color": "primary"
				},
			]
		]
	}

	vk_api.messages.send(
		user_id = sender_id,
		message = f"{reply}",
		keyboard=json.dumps(keyboard),
		random_id = random.randint(0, 2**31),
		v=5.131
	)

	return Response("OK", media_type="application/json")

async def add_user(session: 'AsyncSession', req_body, vk_api: 'API', group_name):
	sql_text = text(f"SELECT id FROM users ORDER BY id DESC")
	response = (await session.execute(sql_text)).all()

	last_id = 0
	if len(response) != 0:
		last_id = response[0].id

	sql_text = text(f"SELECT id FROM groups WHERE name = '{group_name}'")
	response = (await session.execute(sql_text)).all()
	group_id = response[0].id

	chat_id = req_body['object']['message']['from_id']

	sql_text = text(f"SELECT id FROM users WHERE chat_id = {chat_id} and group_id = {group_id}")
	response = (await session.execute(sql_text)).all()
	if len(response) != 0:
		vk_api.messages.send(
			user_id = chat_id,
			message = "Вы уже подписаны на эту группу!",
			random_id = random.randint(0, 2**31),
			v=5.131
		)
	else:
		sql_text = text(f"INSERT INTO users VALUES ({last_id+1}, {chat_id}, {group_id})")
		response = (await session.execute(sql_text))
		await session.commit()
		vk_api.messages.send(
			user_id = chat_id,
			message = f"Вы была подписаны на группу {group_name}!",
			random_id = random.randint(0, 2**31),
			v=5.131
		)

	return Response("OK", media_type="application/json")