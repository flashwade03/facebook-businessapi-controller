import sys, os, json
from facebook_business import FacebookSession
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from fb_api import *

class FacebookAccountManager :
   
    keydata = []
    apis = {}
    adaccounts = {}

    def __init__(self):
        cwd = os.getcwd()
        keyfilepath = cwd+'/fb_account.json'
        with open(keyfilepath) as f:
            self.keydata = json.load(f)
        print 'finished load fb_account.json key file\n'

    def get_key_data(self):
        #print str(self.keydata)
        return self.keydata
 
    
    def create_api(self, appname):
        if appname in self.apis:
            print 'You already made instance.'
            return self.apis[appname]
        else:
            for key in self.keydata:
                if key['app_name'] == appname:
                    if key['business_key']['app_secret'] != None and key['business_key']['user_access_token'] != None and key['business_key']['account_id'] != None and key['business_key']['app_id'] != None:
                        api = API(key['business_key']['app_id'], key['business_key']['app_secret'], key['business_key']['user_access_token']) 
                        self.apis[appname] = api
                        return api
                    else :
                        print appname + " has invalid key!!!"
                        return None
        
        print appname + " is invalid appname"
        return None
    
    def get_api(self, appname):
        if (appname in self.apis) == False:
            target_api = self.create_api(appname)
        else:
            target_api = self.apis[appname]

        return target_api

    def get_adaccount(self, appname):
        if appname in self.adaccounts:
            return acaccount[appname]

        target_api = None
        if (appname in self.apis) == False:
            target_api = self.create_api(appname)
        else:
            target_api = self.apis[appname]
        
        accountid = None
        for key in self.keydata:
            if key['app_name'] == appname:
                accountid = key['business_key']['account_id']

        account = AdAccount(fbid = 'act_'+accountid, api = target_api.api)
        self.adaccounts[appname] = account
        print account
        return account
            

