# -*- coding: utf-8 -*-
# @Time        : 2022/7/19 11:37
# @File        : DailyPractice.py
# @Description : None
# ----------------------------------------------
# ☆ ☆ ☆ ☆ ☆ ☆ ☆ 
# >>> Author    : Alex
# >>> Mail      : liu_zhao_feng_alex@163.com
# >>> Github    : https://github.com/koking0
# >>> Blog      : https://alex007.blog.csdn.net/
# ☆ ☆ ☆ ☆ ☆ ☆ ☆
import time

import requests
from wechatpy.enterprise import WeChatClient

corpid = "ww0aa0efcebb56a94d"
corpsecret = "vrCfbb3CnBkBEIddbdaqirgLOt8hBfvXJx1BBRBBJaQ"


def get_daily_practice(date):
	# 获取今天每日一题
	practice_url = "http://127.0.0.1:11111/problem/getByConditions"
	data = {"gmtCreate": date}
	# 发送请求
	response = requests.post(practice_url, json=data)
	# 获取返回的数据
	data = response.json()
	return data["body"]["dataList"]


def get_rank():
	rank_url = "http://127.0.0.1:11111/blog/ranking"
	data = {}
	response = requests.post(rank_url, json=data)
	data = response.json()
	return data["body"]["dataInfo"]["users"]


if __name__ == '__main__':
	# 获取今天的日期，格式为yyyy-mm-dd
	today = time.strftime("%Y-%m-%d", time.localtime())
	practice = get_daily_practice(today)
	# 获取每日一题排名
	rank = get_rank()
	# 消息推送模板
	msg = f"早上好呀 everybody，今天是{today}，我们来做个每日一题吧！\n\n"
	for p in practice:
		msg += f"{p['problemLevel']}等级题目：{p['title']}，题目链接：{p['link']}\n"
	msg += "\n做完题目记得写一篇博客总结哦，博客链接提交到工作室官网每日一题栏目。"
	msg += "\n官网每日一题栏目：http://www.matrix-studio.top/#/problems\n\n"
	msg += "今天每日一题榜单：\n"
	for idx, r in enumerate(rank[:3]):
		msg += f"No {idx + 1}. {r['user']['username']}，提交{r['count']}篇博客\n"
	msg += "\n是兄弟，来卷我！"
	# 创建企业微信客户端
	client = WeChatClient(corpid, corpsecret)
	group_chat_id = "wrYG5OBwAAaWueDpiyRoytK-Br3qfw9g"
	template = {
		"chat_type": "group",
		"chat_id": group_chat_id,
		"sender": "LiuZhaoFeng",
		"msgtype": "text",
		"text": {
			"content": msg,
		},
	}
	try:
		result = client.external_contact.add_msg_template(template=template)
		# 无效或无法发送的external_userid列表
		fail_list = result["fail_list"]
		# 企业群发消息的id，可用于获取群发消息发送结果
		msgid = result["msgid"]
	except Exception as err:
		# 接口调用失败
		print(err)
