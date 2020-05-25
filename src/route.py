import random
import pymongo
import string
import datetime
import os

class Route:
	def __init__(self,path=[],distance=0,exhausted=0,item=''):
		self.path = path
		self.path_time = []
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
		client = pymongo.MongoClient(os.environ.get('MONGO_URI'))
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
		self.Expiration = datetime.datetime.utcnow() + datetime.timedelta(days=7)

	def ConstructDetails(self,client,FB,FP,value):

		def Merge(dict1, dict2): 
			res = {**dict1, **dict2} 
			return res

		def get_info(ID,FB,FP,delivery_amounts):
			if str(ID)[0] == str(1):
				return {'Food bank name':FB.at[ID,'fp_name'],'Safe Address':str(FB.at[ID,'city']) + ', ' + str(FB.at[ID,'state']) + ', ' + str(FB.at[ID,'zc']),'Address': str(FB.at[ID,'address']) + ' ' + str(FB.at[ID,'city'] + ' ' + str(FB.at[ID,'state'] + ' ' + str(FB.at[ID,'zc']))),'Type':self.item,'Quantity':delivery_amounts[ID],'Contact name':str(FB.at[ID,'first_name'])+ ' ' +str(FB.at[ID,'last_name']),'Email':FB.at[ID,'email'],'Phone':FB.at[ID,'phone_number']}
			else:
				return {'Supplier name':FP.at[ID,'fp_name'],'Safe Address':str(FP.at[ID,'city']) + ', ' + str(FP.at[ID,'state']) + ', ' + str(FP.at[ID,'zc']),'Address': str(FP.at[ID,'address']) + ' ' + str(FP.at[ID,'city'] + ' ' + str(FP.at[ID,'state'] + ' ' + str(FP.at[ID,'zc']))),'Type':self.item,'Quantity':FP.at[ID,self.item],'Contact name':str(FP.at[ID,'first_name'])+ ' ' +str(FP.at[ID,'last_name']),'Email':FP.at[ID,'email'],'Phone':FP.at[ID,'phone_number']}
		
		print('Constructing details...')
		### (!!!) NEED TO FIX QUANTITIES SENT TO EACH FOOD BANK (ADJUST to maximum of food supply (see SupplyBreakdown function))
		run = self.ConstructFields()
		delivery_amounts = self.SupplyBreakdown(FB,FP,value)

		meta = {'id':self.routeID,'Item':self.item,'Expiration':self.Expiration,'Total quantity':self.exhausted,'Current Fee':self.currentFee,'Route length':self.length,'Total distance':str(self.distance) + ' miles','Courier selection':self.biddingProcess}
		path_info = {str(i):get_info(self.path[i],FB,FP,delivery_amounts) for i in range(len(self.path))}
		input_dictionary = Merge(meta,path_info)

		#client.test.routes.insert(input_dictionary)

	def SupplyBreakdown(self,FB,FP,value):

		print(len(self.path))
		print(self.item)

		receipts = [id_num for id_num in self.path if id_num[:1] != str(2)]
		delivery_amounts = {bank:round(FB.at[bank,self.item]*float(value)/float(self.exhausted),1) for bank in receipts}
		return delivery_amounts
	#def GetVolunteers():



