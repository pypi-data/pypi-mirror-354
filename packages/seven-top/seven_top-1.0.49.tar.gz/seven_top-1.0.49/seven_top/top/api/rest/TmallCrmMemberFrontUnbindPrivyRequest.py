'''
Created by auto_sdk on 2022.09.19
'''
from seven_top.top.api.base import RestApi
class TmallCrmMemberFrontUnbindPrivyRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.ouid = None

	def getapiname(self):
		return 'tmall.crm.member.front.unbind.privy'
