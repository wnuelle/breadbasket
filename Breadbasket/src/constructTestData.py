import pandas as pd
import numpy as np
import requests


def LatLong(addr,city,state):
	URL = f'https://maps.googleapis.com/maps/api/geocode/json?address={addr}+{city}+{state}&key=*YOURKEYHERE*'
	resp = requests.get(URL).json()
	return resp['results'][0]['geometry']['location']

### Data objects
# Food bank DB
data = [[100000,'Happy Valley Food Bank','41865 N Mill Creek Rd','Wadsworth','IL',60083,4,True,0,0,0,0],
		[100001,'Arnett Farms Relief Center','1306 N Cedar Lake Rd','Round Lake Beach','IL',60073,1.5,True,0,0,0,0],
		[100002,'Dinky Doink Food Bank','161 N Seymour Ave','Mundelein','IL',60060,8,True,0,0,0,0],
		[100003,'Breakthrough Fresh Market','3334 W Carroll Ave', 'Chicago','IL',60624,1.8,True,1200,0,0,1000],
		[100004,'Marillac House Food Pantry', '2859 Jackson Blvd','Chicago','IL',60612,2.3,True,0,12000,8071,0],
		[100005,'Pilsen Food Pantry','1850 S Throop St','Chicago','IL',60608,3.5,True,0,0,10006,1500],
		[100006,'Casa Catalina','4537 S Ashland Ave','Chicago','IL',60609,1.1,True,0,7411,0,4313]]

FB = pd.DataFrame(data,columns = ['FBID','Food+Bank+Name','Address','City','State','ZIP','Over+Capacity+By','Accepts Produce','starch:pasta','starch:bread','grain:rice','fruit:tomatoes'])

#Food processor DB
data = [[200000,'Decatur Dairy','W1668 County Hwy F','Brodhead','WI',53520,True,0,0,0,0],
		[200001,'Peanut plant','1107 River St','Belleville','WI',53508,True,0,0,0,0],
		[200002,'Tomato King','1825 Willow Rd','Northfield','IL',60093,True,0,0,0,10000],
		[200003,'Rice King','110 W Bartlett Ave','Bartlett','IL',60103,True,0,0,20000,0],
		[200004,'Bread Master','1825 Willow Rd','Northfield','IL',60093,True,0,5000,0,0]
		]

FP = pd.DataFrame(data,columns = ['FPID','Food+Processor+Name','Address','City','State','ZIP','Forklift','starch:pasta','starch:bread','grain:rice','fruit:tomatoes'])

### Check cases

# ROUTE: Tomato King -> Casa Catalina -> Pilsen Food Pantry -> Breakthrough fresh market
# ROUTE: Rice King -> Marillac Food Pantry -> Pilsen Food Pantry
# ROUTE: Bread Master -> Marillac Food Pantry -> Casa Catalina

FB['latlong'] = np.vectorize(LatLong)(FB['Address'],FB['City'],FB['State'])
FB['lat'] = FB['latlong'].apply(lambda x: list(x.values())[0])
FB['long'] = FB['latlong'].apply(lambda x: list(x.values())[1])
FB.drop(columns=['latlong'],inplace=True)

FP['latlong'] = np.vectorize(LatLong)(FP['Address'],FP['City'],FP['State'])
FP['lat'] = FP['latlong'].apply(lambda x: list(x.values())[0])
FP['long'] = FP['latlong'].apply(lambda x: list(x.values())[1])
FP.drop(columns=['latlong'],inplace=True)

print(FB.to_csv('testdata/Food+Banks.csv'))
print(FP.to_csv('testdata/Food+Processors.csv'))