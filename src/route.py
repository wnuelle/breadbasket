import random
import pymongo
import string

class Route:
	def __init__(self,path=[],distance=0,exhausted=0,item=''):
		self.routeID = 1 #''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)])
		self.path = path
		self.distance = distance
		self.exhausted = exhausted
		self.biddingProcess = "Incomplete"
		self.item = item
	
	def ConstructDetails(self,client,FB,FP):

		def Merge(dict1, dict2): 
			res = {**dict1, **dict2} 
			return res

		def get_info(ID,FB,FP):
			if str(ID)[0] == str(1):
				return {'Food bank name':FB.at[ID,'fp_name'],'Address': str(FB.at[ID,'address']) + ' ' + str(FB.at[ID,'city'] + ' ' + str(FB.at[ID,'state'] + ' ' + str(FB.at[ID,'zc']))),'Type':self.item,'Quantity':FB.at[ID,self.item],'Contact name':str(FB.at[ID,'first_name'])+ ' ' +str(FB.at[ID,'last_name']),'Email':FB.at[ID,'email'],'Phone':FB.at[ID,'phone_number']}
			else:
				return {'Supplier name':FP.at[ID,'fp_name'],'Address': str(FP.at[ID,'address']) + ' ' + str(FP.at[ID,'city'] + ' ' + str(FP.at[ID,'state'] + ' ' + str(FP.at[ID,'zc']))),'Type':self.item,'Quantity':FP.at[ID,self.item],'Contact name':str(FP.at[ID,'first_name'])+ ' ' +str(FP.at[ID,'last_name']),'Email':FP.at[ID,'email'],'Phone':FP.at[ID,'phone_number']}
		
		### NEED TO FIX QUANTITIES SENT TO EACH FOOD BANK (ADJUST to maximum of food supply (see SupplyBreakdown function))
		meta = {'id':self.routeID,'Item':self.item,'Total quantity':self.exhausted,'Total distance':str(self.distance) + ' miles','Courier selection':self.biddingProcess}
		path_info = {str(i):get_info(self.path[i],FB,FP) for i in range(len(self.path))}
		input_dictionary = Merge(meta,path_info)

		client.test.routes.insert(input_dictionary)

	#def GetVolunteers():

	#def SupplyBreakdown(FB,FP,value):


