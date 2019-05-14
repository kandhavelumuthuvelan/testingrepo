from pymongo import MongoClient
import configparser
from pprint import pprint
import os.path,subprocess
from subprocess import STDOUT,PIPE
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from bson.objectid import ObjectId
import json
from datetime import datetime,timedelta ,date
import time


config = configparser.ConfigParser()
config.read('ConfigFile.properties')
securitykey=config.get('securitySection', 'key')
host=config.get('DatabaseSection', 'dbhost')
port=config.get('DatabaseSection', 'dbport')
username=config.get('DatabaseSection', 'dbusername')
password=config.get('DatabaseSection', 'dbpassword')
dbname=config.get('DatabaseSection', 'dbname')
connectionstring="mongodb://"+username+":"+password+"@"+host+":"+port+"/"+dbname


client = MongoClient(connectionstring)
db=client.dashboarddb
# Issue the serverStatus command and print the results
serverStatusResult=db.command("serverStatus")
connection=""
repoid=""

def compile_java(java_file):
    cmd = 'javac -cp org-apache-commons-codec.jar; patdecryptor.java'
    try:
        subprocess.check_call(cmd,shell = True)
    except subprocess.CalledProcessError:
        print("Error")

def execute_java(java_file,securitykey,pat ):
    java_class,ext = os.path.splitext(java_file)
    cmd = ['java','-cp', 'org-apache-commons-codec.jar;',java_class,pat,securitykey]
    proc = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    stdout,stderr = proc.communicate()
    return stdout

def vsts_connector(personalaccesstoken,organizationurl):
    #pprint(personalaccesstoken)
    global connection
    credentials = BasicAuthentication('', personalaccesstoken)
    connection = Connection(base_url=organizationurl, creds=credentials)
    #get_all_commits_from_azure(connection)
    #pprint(connection)

def get_repositoryid(project_name,repository_name):
    global repoid
    git_client = connection.clients.get_git_client()
    repos = git_client.get_repositories(project_name)
    for repo in repos:
        if(repo.name==repository_name):
            repoid=repo.id
	
def get_all_commits_from_azure(branch,collectorItemId):
    git_client = connection.clients.get_git_client()
    since=(datetime.now()- timedelta(minutes=1000)).strftime("%m/%d/%Y %H:%M:%S")
    commits = git_client.get_all_commits(repoid,branch,since)
    #commits = git_client.get_all_commits("mytrack")
    #print(commits[0].author.date )
    for commit in commits:
        #pprint((datetime.now()- timedelta(minutes=30)).strftime("%d/%m/%Y %H:%M:%S"))
         pprint((datetime.now()- timedelta(minutes=30)).strftime("%m/%d/%Y %H:%M:%S"))
        #pprint((datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        #pprint(commit.__dict__)
       #pprint(commit.author.date)
       #pprint(unixtime = time.mktime(commit.author.date))
        #dt = datetime(2019, 3, 28, 9, 51, 19)
        #dt=commit.author.date
        #pprint(datetime.fromtimestamp(1557137251602))
        #pprint(time.mktime(dt.timetuple()) * 1000 + dt.microsecond/1000)
        #parse_data_from_commit(commit,collectorItemId,branch)
		
 
def get_pull_request_from_azure(project_name,collectorItemId,organizationurl,reponame,branch):
    git_client = connection.clients.get_git_client()
    pullrequests = git_client.get_pull_requests_by_project_alone(project_name)
    for pullrequest in pullrequests:
        #pprint(pullrequest.created_by.__dict__)
        parse_data_from_pull_request(pullrequest,collectorItemId,organizationurl,reponame,branch)
		
def parse_data_from_pull_request(pullrequest,collectorItemId,organizationurl,reponame,branch):
    pullrequest_creation_date=pullrequest.creation_date
    #pullrequest_timestamp=time.mktime(pullrequest_creation_date.timetuple()) * 1000 + pullrequest_creation_date.microsecond/1000
    pullrequest_timestamp=557750341000
    sourcerepo_arr=pullrequest.source_ref_name.split('/')
    targetrepo_arr=pullrequest.target_ref_name.split('/')
    business_data = {
    '_class': 'com.capitalone.dashboard.model.GitRequest',
	'scmUrl':pullrequest.repository.url,
	'scmBranch':branch,
	'scmRevisionNumber':pullrequest.last_merge_commit.commit_id,
	'scmCommitLog':pullrequest.title,
	'scmCommitTimestamp':0,
	'numberOfChanges':0,
	'orgName':organizationurl,
	'repoName':reponame,
	'sourceRepo':sourcerepo_arr[0]+'/'+sourcerepo_arr[1],
	'sourceBranch':sourcerepo_arr[2],
	'targetRepo':targetrepo_arr[0]+'/'+targetrepo_arr[1],
	'targetBranch':targetrepo_arr[2],
	'number':pullrequest.pull_request_id,
	'collectorItemId':collectorItemId,
	'updatedAt':pullrequest_timestamp,
	'createdAt':pullrequest_timestamp,
	'closedAt':pullrequest_timestamp,
	'state':pullrequest.merge_status,
	'mergedAt':pullrequest_timestamp,
	'timestamp':pullrequest_timestamp,
	'resolutiontime':0,
	'userId':pullrequest.created_by.display_name,
	'commentsUrl':'https://api.github.com/repos/kandhavelumuthuvelan/jspapplication/issues/2/comments',
	'reviewCommentsUrl':pullrequest.url,
	'comments':[
	{
	    'user':'kandhavelumuthuvelan',
		'createdAt':1557750341000,
		'updatedAt':1557750341000,
		'body':'adding new line was accepted',
		
    }],
	'reviews':[],
	'commitStatuses':[
    ],
	'headSha':'bc5e1daff2f6f37ca54e22538f1d330dbdfbaee6',
	'baseSha':'fc963beee06a757e17724f33c116bc9887c38ae2',
	'requestType':'pull',
    }
    result=db.gitrequests .insert_one(business_data)
    #Step 4: Print to the console the ObjectID of the new document
    pprint('Collector {0}'.format(result))
    #Step 5: Tell us that you are done
    pprint('finished creating 500 business reviews')
 
def parse_data_from_commit(commit,collectorItemId,branch):
    scmCommitTimestamp_fromdate=commit.committer.date
    authortimestamp_fromdate=commit.author.date
    scm_timestamp=time.mktime(scmCommitTimestamp_fromdate.timetuple()) * 1000 + scmCommitTimestamp_fromdate.microsecond/1000
    author_timestamp=time.mktime(authortimestamp_fromdate.timetuple()) * 1000 + authortimestamp_fromdate.microsecond/1000
    numberofcount=commit.change_counts['Add']+commit.change_counts['Edit']+commit.change_counts['Delete']
    business_data = {
		'_class' : 'com.capitalone.dashboard.model.Commit',
        'collectorItemId' : ObjectId(collectorItemId),
        'timestamp' : author_timestamp,
        'firstEverCommit' : False,
		'scmUrl' : commit.remote_url,
		'scmBranch' : branch,
		'scmRevisionNumber' : commit.commit_id,
		'scmCommitLog' : commit.comment,
		'scmAuthor' : commit.committer.name,
		'scmAuthorLogin': commit.author.name,
		'scmParentRevisionNumbers':[],
		'scmCommitTimestamp': scm_timestamp,
		'numberOfChanges' : numberofcount,
		'type': 'New'
    }
    result=db.commits .insert_one(business_data)
    #Step 4: Print to the console the ObjectID of the new document
    pprint('Collector {0}'.format(result))
    #Step 5: Tell us that you are done
    pprint('finished creating 500 business reviews')
    


collectors_result=db.collectors.find_one({"name": 'Azure Devops'})
collector_id=collectors_result['_id']
#pprint(collector_id)
collector_items_results=db.collector_items.find({"enabled":True, "collectorId":collector_id})
for collector_items_result in collector_items_results:
    personalaccesstoken=execute_java('patdecryptor.java',securitykey,collector_items_result['options']['personalAccessToken'])
    organizationurl=collector_items_result['options']['url']
    path_url=collector_items_result['options']['branch']
    collectorItemId=collector_items_result['_id']
    path_split_array=path_url.split('/')
    #pprint(personalaccesstoken.decode('UTF-8'))
    #pprint(organizationurl)
    #pprint(branch)
    vsts_connector(personalaccesstoken.decode('UTF-8'),organizationurl)
    get_repositoryid(path_split_array[0],path_split_array[1])
    get_all_commits_from_azure(path_split_array[2],collectorItemId)
    get_pull_request_from_azure(path_split_array[0],collectorItemId,organizationurl,path_split_array[1],path_split_array[2])