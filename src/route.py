import random
import pymongo
import string
import datetime

class Route:
	def __init__(self,path=[],distance=0,exhausted=0,item=''):
		self.path = path
		self.distance = distance
		self.exhausted = exhausted
		self.biddingProcess = "Incomplete"
		self.item = item
		self.measure = 'loaves'
		self.daysToExp = 0
		self.initiated = datetime.datetime.utcnow()



	###########################################
	### Post-procesing 	                    ###
	###  					                ###
	### Once route is found, adjust attrib- ###
	### utes and insert into database. 		###
	###  					                ###
	###########################################
	def ConstructFields(self):
		client = pymongo.MongoClient("mongodb+srv://wnuelle:QwakkleSmakkle#!#@cluster0-gqwgd.mongodb.net/test?retryWrites=true&w=majority")
		ID_list = client.test.routes.distinct('id')
		while True:
			key = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
			if key not in ID_list:
				self.routeID = key
				break
		self.length = len(self.path)
		self.currentFee = 0
		self.total_weight = 0
		self.distance = round(self.distance,2)
		return 'Yo'

	def ConstructDetails(self,client,FB,FP):

		def Merge(dict1, dict2): 
			res = {**dict1, **dict2} 
			return res

		def get_info(ID,FB,FP):
			print(FB)
			print(FP)
			if str(ID)[0] == str(1):
				return {'Food bank name':FB.at[ID,'fp_name'],'Safe Address':str(FB.at[ID,'city']) + ', ' + str(FB.at[ID,'state']) + ', ' + str(FB.at[ID,'zc']),'Address': str(FB.at[ID,'address']) + ' ' + str(FB.at[ID,'city'] + ' ' + str(FB.at[ID,'state'] + ' ' + str(FB.at[ID,'zc']))),'Type':self.item,'Quantity':FB.at[ID,self.item],'Contact name':str(FB.at[ID,'first_name'])+ ' ' +str(FB.at[ID,'last_name']),'Email':FB.at[ID,'email'],'Phone':FB.at[ID,'phone_number']}
			else:
				return {'Supplier name':FP.at[ID,'fp_name'],'Safe Address':str(FP.at[ID,'city']) + ', ' + str(FP.at[ID,'state']) + ', ' + str(FP.at[ID,'zc']),'Address': str(FP.at[ID,'address']) + ' ' + str(FP.at[ID,'city'] + ' ' + str(FP.at[ID,'state'] + ' ' + str(FP.at[ID,'zc']))),'Type':self.item,'Quantity':FP.at[ID,self.item],'Contact name':str(FP.at[ID,'first_name'])+ ' ' +str(FP.at[ID,'last_name']),'Email':FP.at[ID,'email'],'Phone':FP.at[ID,'phone_number']}
		
		### (!!!) NEED TO FIX QUANTITIES SENT TO EACH FOOD BANK (ADJUST to maximum of food supply (see SupplyBreakdown function))
		run = self.ConstructFields()

		meta = {'id':self.routeID,'Item':self.item,'Total quantity':self.exhausted,'Current Fee':self.currentFee,'Route length':self.length,'Total distance':str(self.distance) + ' miles','Courier selection':self.biddingProcess}
		path_info = {str(i):get_info(self.path[i],FB,FP) for i in range(len(self.path))}
		input_dictionary = Merge(meta,path_info)

		client.test.routes.insert(input_dictionary)

	#def GetVolunteers():

	#def SupplyBreakdown(FB,FP,value):


