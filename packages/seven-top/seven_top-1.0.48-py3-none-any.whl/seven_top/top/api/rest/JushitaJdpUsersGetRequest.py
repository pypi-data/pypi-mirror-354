'''
Created by auto_sdk on 2022.09.20
'''
from seven_top.top.api.base import RestApi
class JushitaJdpUsersGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.end_modified = None
		self.page_no = None
		self.page_size = None
		self.start_modified = None
		self.target_appkey = None
		self.user_id = None

	def getapiname(self):
		return 'taobao.jushita.jdp.users.get'
