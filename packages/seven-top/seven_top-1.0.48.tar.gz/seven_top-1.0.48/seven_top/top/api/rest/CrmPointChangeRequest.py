'''
Created by auto_sdk on 2019.08.06
'''
from seven_top.top.api.base import RestApi
class CrmPointChangeRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.account_date = None
		self.activity_id = None
		self.activity_name = None
		self.buyer_nick = None
		self.change_type = None
		self.mix_nick = None
		self.open_id = None
		self.opt_type = None
		self.quantity = None
		self.remark = None
		self.request_id = None

	def getapiname(self):
		return 'taobao.crm.point.change'
