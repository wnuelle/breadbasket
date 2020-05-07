from random import randint

class Route:
	def __init__(self,path=[],distance=0,exhausted=0,item=''):
		self.routeID = 1
		self.path = path
		self.distance = distance
		self.exhausted = exhausted
		self.biddingProcess = "Pre-Bidding"
		self.item = item
	
	def ConstructDetails(self,FB,FP):
		Details = {'Pick Up':{},'Drop Off':[]}
		for stop in self.path:
			if str(stop)[0] == str(1):

				#Quantity
				drops = Details['Drop Off']
				drops.append({'Name':FB.at[stop,'Food+Bank+Name'],'Address': str(FB.at[stop,'Address']) + str(FB.at[stop,'City'] + str(FB.at[stop,'State'] + str(FB.at[stop,'ZIP']))),'Type':self.item,'Quantity':FB.at[stop,item]}) ## FIX QUANTITY
			else:
				Details['Pick Up'] = {'Name':FP.at[stop,'Food+Processor+Name'],'Address': str(FP.at[stop,'Address']) + str(FP.at[stop,'City'] + str(FP.at[stop,'State'] + str(FP.at[stop,'ZIP']))),'Type':self.item,'Quantity':FP.at[stop,item]}
		return Details
	#def supply_breakdown(FB,FP,value):


