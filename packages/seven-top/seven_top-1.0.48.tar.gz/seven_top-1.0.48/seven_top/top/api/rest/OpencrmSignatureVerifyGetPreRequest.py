'''
Created by auto_sdk on 2025.05.09
'''
from top.api.base import RestApi
class OpencrmSignatureVerifyGetPreRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)

	def getapiname(self):
		return 'taobao.opencrm.signature.verify.get.pre'
