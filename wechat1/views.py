# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import (TextMessage,VoiceMessage,ImageMessage,VideoMessage,LinkMessage,LocationMessage,EventMessage)
#from wechat_sdk.context.framework.django import DatabaseContextStore

# instantiation WechatBasic
wechat_instance =WechatBasic(
	token='gymbed',
	appid='wxab99513ecc320726',
	appsecret='e50b922614c004089038b31f79f075f0'
)

def index(request):
	if request.method == 'GET':
		signature = request.GET.get('signature')
		timestamp = request.GET.get('timestamp')
		nonce     = request.GET.get('nonce')

		if  not wechat_instance.check_signature(
				signature=signature,timestamp=timestamp,nonce=nonce):
			return HttpResponseBadRequest('Verify Failed')
	        return HttpResponse( request.GET.get('echostr',''),content_type="text/plain")

	try:
		wechat_instance.parse_data(data=request.body)
	except ParseError:
		return HttpResponseBadRequest('Invaild XML Data')

	#get the parse message from wechat
	message =wechat_instance.get_message()
	
	response=wechat_instance.response_text(
		content=(
			' mbed OS智能安防测试系统'
			))
	if isinstance(message,TextMessage):
		content=message.content.strip()
		if content=="开门":
			reply_text=('正在开锁，请稍等')
		elif content=="关门":
			reply_text=('正在锁门，请稍等')
		elif content.endswith("2"):
			reply_text="haha"
		response=wechat_instance.response_text(content=reply_text)	
	return HttpResponse(response,content_type='application/xml')

def save(request):
	tempture=request.GET.get('p1'),
	HttpResponse(tempture)
	return HttpResponse(tempture)


