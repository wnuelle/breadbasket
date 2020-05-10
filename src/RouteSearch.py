import pandas as pd
import numpy as np
import requests
import googlemaps
import itertools
import route
from datetime import datetime
import pymongo


FOOD = ['starch:pasta','starch:bread','grain:rice','fruit:tomatoes']

def GetDistanceByAddr(id1,id2,FB,FP):
	if str(id1)[0] == str(2):
		URL = f"https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={FP.at[id1,'address']}{FP.at[id1,'city']}{FP.at[id1,'state']}&destinations={FB.at[id2,'address']}{FB.at[id2,'city']}{FB.at[id2,'state']}&key=AIzaSyBR4VBHFKox9cvzeCdR2gojPGcGD6ij5vE"
		resp = requests.get(URL).json()
		return resp['rows'][0]['elements'][0]['distance']['value']
	else:
		### Google Maps API
		URL = f"https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={FB.at[id1,'address']}{FB.at[id1,'city']}{FB.at[id1,'state']}&destinations={FB.at[id2,'address']}{FB.at[id2,'city']}{FB.at[id2,'state']}&key=AIzaSyBR4VBHFKox9cvzeCdR2gojPGcGD6ij5vE"
		resp = requests.get(URL).json()
		return resp['rows'][0]['elements'][0]['distance']['value']

def ConditionCheck():
	## travel time won't endanger the quality of the good being carried
	## no more than x stops for the driver to make ??
	## supplies are exhausted (or near exhausted: we can talk about this condition)
	## all recipients get their food before it goes bad
	return 0

def Search(client,value,FB,FP,source,item):

	#def heuristic(id1,id2):
		#Need to determine some heuristic for the Completion Conditions

	eligible_banks = FB[FB[item]>0][item]
	OL = {} #Open list
	CL = {} #Closed list

	rte = route.Route(path=[source],item=item)
	OL[rte] = rte.distance

	while len(OL) > 0:
		s = datetime.utcnow()
		rte = min(OL,key=OL.get)
		del OL[min(OL,key=OL.get)]

		if rte.exhausted >= value: ##Eventually condition check
			## Call route address book etc...
			print('Found!')
			rte.ConstructDetails(client,FB,FP)
			print(rte.path)
			return rte
		else:
			neighbors = list(set(eligible_banks.index) - set(rte.path))
			for end in neighbors:

				exhausted = rte.exhausted
				exhausted += FB.at[end,item]
				distance = rte.distance
				distance += GetDistanceByAddr(rte.path[len(rte.path)-1],end,FB,FP)/1609.

				path = rte.path.copy() + [end]

				new_rte = route.Route(path=path,distance=distance,exhausted=exhausted,item=item)
				OL[new_rte] = new_rte.distance
		e = datetime.utcnow()
		print(e-s)
	return None

def PATHFINDER():
	
	client = pymongo.MongoClient()

	print("Suppliers")
	print("---------")
	print()
	print()
	suppliers = client.test.suppliers
	FP = pd.DataFrame(list(suppliers.find()))
	cols = FP[FOOD].columns
	for F in FOOD:
		FP[F] = FP[F].astype(float)
	bt = FP[FOOD].apply(lambda x: x > 0)
	FP['Supply'] = bt.apply(lambda x: list(cols[x.values]), axis=1)
	FP.set_index('FPID',inplace=True)
	print(FP)


	print("Food banks")
	print("---------")
	print()
	print()
	banks = client.test.banks
	FB = pd.DataFrame(list(banks.find()))
	cols = FB[FOOD].columns
	for F in FOOD:
		FB[F] = FB[F].astype(float)
	bt = FB[FOOD].apply(lambda x: x > 0)
	FB['Demand'] = bt.apply(lambda x: list(cols[x.values]), axis=1)
	FB.set_index('FBID',inplace=True)
	print(FB)

	for index,row in FP.iterrows(): ## iterrows is usually a bad solution, but I couldn't think of a way to vectorize and we're not performance constrained
		if len(row['Supply'])>0:
			for item in row['Supply']: ## This looks like it adds a bunch of time complexity, but it will typically be either 1 or 2 values
				value = FP.at[index,item]
				result = Search(client,value,FB,FP,index,item)
				if result != None:
					print(result.path)

				### GOAL: zero the Supply of items out
		else:
			FP.drop(index,inplace=True)

PATHFINDER()