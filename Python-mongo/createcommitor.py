from pymongo import MongoClient
from random import randint
#Step 1: Connect to MongoDB - Note: Change connection string as needed
client = MongoClient(port=27017)
db=client.dashboarddb
online=True ;
enabled=True ;
#Step 2: Create sample data
business = {
		'_class' : 'com.capitalone.dashboard.model.Collector',
        'name' : 'Azure Devops',
        'collectorType' : 'SCM',
        'enabled' : enabled,
		'online' : online,
		'errors' : [],
		'uniqueFields' : 
			
			{
			
			
			'branch' : " ",
			'url' : " ",
			
			}
			,
		'allFields' : 
			{
			
			'password' : " ",
			'personalAccessToken': " ",
			'branch' : " ",
			'userID' : " ",
			'url' : " ",
			
			}
			,
		'lastExecuted' : 1557377071736,
		'searchFields' :
		[
		 'description' 
		]
    }
#Step 3: Insert business object directly into MongoDB via isnert_one
result=db.collectors.insert_one(business)
#Step 4: Print to the console the ObjectID of the new document
print('Collector {0}'.format(result))
#Step 5: Tell us that you are done
print('finished creating 500 business reviews')