import pandas as pd
from pymongo import MongoClient

################ ReferenceDB insertion in Mongodb ##########
df = pd.read_csv('ReferenceDB0.csv')
client = MongoClient('localhost', 27017)
db = client['TransportRefDB92']
collection = db['Companies92']

for i in range(0, len(df)):
    print('i=', i)
    try:
        collection.insert_one({"company": {"id": i, "Name": df['company'][i].strip(), "Address": {"INBUILDING": df['INBUILDING'][i].strip(), "EXTBUILDING": df['EXTBUILDING'][i].strip(), "POILOGISTIC": df['POILOGISTIC'][i].strip(), "ZONE": df['ZONE'][i].strip(
        ), "HouseNum": df['HouseNum'][i].strip(), "RoadName": df['RoadName'][i].strip(), "POBOX": df['POBOX'][i].strip(), "zipcode": df['zipcode'][i], "city": df['city'][i].strip(), "country": df['country'][i].strip(), "ADDITIONAL": df['ADDITIONAL'][i].strip()}, "MAJDate": " "}})

    except:
        df['company'][i] = df['company'][i].decode(errors='replace')
        df['INBUILDING'][i] = df['INBUILDING'][i].decode(errors='replace')
        df['EXTBUILDING'][i] = df['EXTBUILDING'][i].decode(errors='replace')
        df['POILOGISTIC'][i] = df['POILOGISTIC'][i].decode(errors='replace')
        df['ZONE'][i] = df['ZONE'][i].decode(errors='replace')
        df['HouseNum'][i] = df['HouseNum'][i].decode(errors='replace')
        df['RoadName'][i] = df['RoadName'][i].decode(errors='replace')
        df['POBOX'][i] = df['POBOX'][i].decode(errors='replace')
        df['zipcode'][i] = str(df['zipcode'][i]).decode(errors='replace')
        df['city'][i] = df['city'][i].decode(errors='replace')
        df['country'][i] = df['country'][i].decode(errors='replace')
        df['source'][i] = df['source'][i].decode(errors='replace')
        df['ADDITIONAL'][i] = df['ADDITIONAL'][i].decode(errors='replace')
        collection.insert_one({"company": {"id": i, "Name": df['company'][i].strip(), "Address": {"INBUILDING": df['INBUILDING'][i].strip(), "EXTBUILDING": df['EXTBUILDING'][i].strip(), "POILOGISTIC": df['POILOGISTIC'][i].strip(), "ZONE": df['ZONE'][i].strip(
        ), "HouseNum": df['HouseNum'][i].strip(), "RoadName": df['RoadName'][i].strip(), "POBOX": df['POBOX'][i].strip(), "zipcode": df['zipcode'][i], "city": df['city'][i].strip(), "country": df['country'][i].strip(), "ADDITIONAL": df['ADDITIONAL'][i].strip()}, "MAJDate": " "}})

'''
import pandas as pd 
from pymongo import MongoClient

################ ReferenceDB insertion in Mongodb ##########
df=pd.read_csv('ReferenceDB0.csv')
client = MongoClient('localhost', 27017)
db = client['TransportRefDB93']
collection = db['companies93']

for i in range(0, len(df)):
        print('i=',i)
        print('cc',df['zipcode'][i])
        collection.insert_one({"company":{"id": i, "Name": df['company'][i].strip(), "Address":{"INBUILDING":df['INBUILDING'][i].strip(),"EXTBUILDING":df['EXTBUILDING'][i].strip(),"POILOGISTIC":df['POILOGISTIC'][i].strip(),"ZONE":df['ZONE'][i].strip(),"HouseNum":df['HouseNum'][i].strip(),"RoadName":df['RoadName'][i].strip(),"POBOX":df['POBOX'][i].strip(),"zipcode":str(df['zipcode'][i]),"city":df['city'][i].strip(),"country":df['country'][i].strip(), "ADDITIONAL":df['ADDITIONAL'][i].strip()}, "MAJDate": " "}})
 
'''
