'''
Created by auto_sdk on 2025.05.09
'''
from top.api.base import RestApi
class OpencrmSignatureVerifySubmitRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.signature_request = None

	def getapiname(self):
		return 'taobao.opencrm.signature.verify.submit'
