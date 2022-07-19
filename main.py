import requests

base_url = "https://qyapi.weixin.qq.com/cgi-bin/"


def get_access_token(corpid, corpsecret):
	url = f"{base_url}gettoken?corpid={corpid}&corpsecret={corpsecret}"
	res = requests.get(url)
	return res.json()["access_token"]


def get_external_group_list(access_token):
	url = f"{base_url}externalcontact/groupchat/list?access_token={access_token}"
	data = {
		"limit": 10,
	}
	res = requests.post(url, json=data)
	return res.json()


def get_external_group(access_token, chat_id):
	url = f"{base_url}externalcontact/groupchat/get?access_token={access_token}"
	data = {
		"chat_id": chat_id,
		"need_name": 1,
	}
	res = requests.post(url, json=data)
	return res.json()


def send_msg_to_external_group(access_token, chat_id, msg):
	url = f"{base_url}appchat/send?access_token={access_token}&debug=1"
	data = {
		"chat_id": chat_id,
		"msgtype": "text",
		"text": {
			"content": msg,
		},
	}
	res = requests.post(url, json=data)
	print(f"send msg to external group: {res.json()}")
	return res.json()


if __name__ == '__main__':
	corpid = "ww0aa0efcebb56a94d"
	corpsecret = "vrCfbb3CnBkBEIddbdaqirgLOt8hBfvXJx1BBRBBJaQ"
	access_token = get_access_token(corpid, corpsecret)
	print(f"access_token: {access_token}")
	group_list = get_external_group_list(access_token)
	print(f"group_list: {group_list}")
	# group_chat_id = "wrYG5OBwAA39To9q1UJmRqAjui4EzNdg"
	# group_info = get_external_group(access_token, group_chat_id)
	# print(f"group_info: {group_info}")
	# send_msg_to_external_group(access_token, group_chat_id, "hello")
