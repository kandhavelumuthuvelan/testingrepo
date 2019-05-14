from pymongo import MongoClient
from random import randint
from bson.objectid import ObjectId
#Step 1: Connect to MongoDB - Note: Change connection string as needed
client = MongoClient(port=27017)
db=client.dashboarddb
online=True ;
enabled=True ;
#Step 2: Create sample data
business = {
		'_class' : 'com.capitalone.dashboard.model.Commit',
        'collectorItemId' : ObjectId('5cd90784e4b0a831d490f2d5'),
        'timestamp' : 1557137251602,
        'firstEverCommit' : False,
		'scmUrl' : 'https://dev.azure.com/kandhavelumuthuvelan1',
		'scmBranch' : "master",
		'scmRevisionNumber' : "392959ea56d9481d4c5b865d7057b0e40e3e5d63",
		'scmCommitLog' : "first commit",
		'scmAuthor' : "kandhavelu",
		'scmAuthorLogin': "kandhavelumuthuvelan",
		'scmParentRevisionNumbers':[],
		'scmCommitTimestamp': 1557119961000,
		'numberOfChanges' : 1,
		'type': 'New'
    }
#Step 3: Insert business object directly into MongoDB via isnert_one
result=db.commits .insert_one(business)
#Step 4: Print to the console the ObjectID of the new document
print('Collector {0}'.format(result))
#Step 5: Tell us that you are done
print('finished creating 500 business reviews')