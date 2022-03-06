import random

def reply_to_message(req_body, vk_api):
	sender_id = req_body['object']['message']['from_id']
	message_text = req_body['object']['message']['text']
	if message_text == 'hello':
		reply = "hello"
		vk_api.messages.send(
			user_id = sender_id,
			message = reply,
			random_id = random.randint(0, 2**31),
			v=5.131
		)