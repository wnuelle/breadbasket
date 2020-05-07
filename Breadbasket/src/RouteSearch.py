import pandas as pd
import numpy as np
import requests
import googlemaps
import itertools
import route
from datetime import datetime


FOOD = ['starch:pasta','starch:bread','grain:rice','fruit:tomatoes']

def GetDistanceByAddr(id1,id2,FB,FP):
	if str(id1)[0] == str(2):
		URL = f"https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={FP.at[id1,'Address']}{FP.at[id1,'City']}{FP.at[id1,'State']}&destinations={FB.at[id2,'Address']}{FB.at[id2,'City']}{FB.at[id2,'State']}&key=*YOURKEYHERE*"
		resp = requests.get(URL).json()
		return resp['rows'][0]['elements'][0]['distance']['value']
	else:
		### Google Maps API
		URL = f"https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={FB.at[id1,'Address']}{FB.at[id1,'City']}{FB.at[id1,'State']}&destinations={FB.at[id2,'Address']}{FB.at[id2,'City']}{FB.at[id2,'State']}&key=*YOURKEYHERE*"
		resp = requests.get(URL).json()
		return resp['rows'][0]['elements'][0]['distance']['value']

def ConditionCheck():
	## travel time won't endanger the quality of the good being carried
	## no more than x stops for the driver to make ??
	## supplies are exhausted (or near exhausted: we can talk about this condition)
	## all recipients get their food before it goes bad
	return 0

def Search(value,FB,FP,source,item):

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
			rte.ConstructDetails(FB,FP)

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

def __main__():

	### Prepare FB db
	FB = pd.read_csv('testdata/Food+Banks.csv').set_index('FBID') ### To be replaced by calls to database
	FB.drop(columns=['Unnamed: 0'],inplace=True)
	cols = FB[FOOD].columns
	bt = FB[FOOD].apply(lambda x: x > 0)
	FB['Demand'] = bt.apply(lambda x: list(cols[x.values]), axis=1)

	### Prepare FP db
	FP = pd.read_csv('testdata/Food+Processors.csv').set_index('FPID') ## To be replaced by calls to database
	FP.drop(columns=['Unnamed: 0'],inplace=True)
	cols = FP[FOOD].columns
	bt = FP[FOOD].apply(lambda x: x > 0)
	FP['Supply'] = bt.apply(lambda x: list(cols[x.values]), axis=1)

	print(FB)
	print(FP)

	for index,row in FP.iterrows(): ## iterrows is usually a bad solution, but I couldn't think of a way to vectorize and we're not performance constrained
		if len(row['Supply'])>0:
			for item in row['Supply']: ## This looks like it adds a bunch of time complexity, but it will typically be either 1 or 2 values
				value = FP.at[index,item]
				result = Search(value,FB,FP,index,item)
				if result != None:
					print(result.path)

				### GOAL: zero the Supply of items out
		else:
			FP.drop(index,inplace=True)

__main__()

"""
RankMatrix = pd.DataFrame(columns=list(df1['FBID']))
RankMatrix['FPID'] = df2['FPID']
RankMatrix = RankMatrix.set_index('FPID')
"""
