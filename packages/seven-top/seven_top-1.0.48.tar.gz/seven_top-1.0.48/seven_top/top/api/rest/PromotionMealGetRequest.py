'''
Created by auto_sdk on 2018.11.10
'''
from seven_top.top.api.base import RestApi
class PromotionMealGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.meal_id = None
		self.status = None

	def getapiname(self):
		return 'taobao.promotion.meal.get'
