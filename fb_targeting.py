import os, sys
from fb_accountmanager import *
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign as AdCampaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.targeting import Targeting
from fb_api import *

fb = FacebookAccountManager()
'''
adaccount = fb.get_adaccount('block')
campaigns = adaccount.get_campaigns(fields = [AdCampaign.Field.name, AdCampaign.Field.status])
for campaign in campaigns:
    if campaign[AdCampaign.Field.status] == 'ACTIVE':
        adsets = campaign.get_ad_sets(fields=[AdSet.Field.name, AdSet.Field.targeting])
        for adset in adsets:
            print adset[AdSet.Field.targeting][Targeting.Field.user_os]
            
'''

def changeosversion(app):
    appname = app
    adaccount = fb.get_adaccount(appname)
    my_api = fb.get_api(appname)
    campaigns = adaccount.get_campaigns(fields=[AdCampaign.Field.status])
    updatecount = 0
    for campaign in campaigns:
        if campaign[AdCampaign.Field.status] == 'ACTIVE':
            adsets = campaign.get_ad_sets(fields=[AdSet.Field.name, AdSet.Field.targeting, AdSet.Field.status])
            for adset in adsets:
                def callback_update_success(response, my_adset=None):
                    print(
                        "Update target OS %s successfully."
                        % my_adset[AdSet.Field.name]
                    )


                callback_update_success = partial(
                    callback_update_success,
                    my_adset = adset,
                )

                def callback_update_failure(response, my_adset=None):
                    print(
                        "FAILED to update target os %s."
                        % my_adset[AdSet.Field.name]
                    )
                    raise response.error()

                callback_update_failure = partial(
                    callback_update_failure,
                    my_adset = adset
                )

                if adset[AdSet.Field.status] == 'ACTIVE':
                    print adset[AdSet.Field.name]
                    if 'user_os' not in adset[AdSet.Field.targeting].keys():
                        continue
                    current_os = adset[AdSet.Field.targeting][Targeting.Field.user_os][0]
                    elements = current_os.split('_')
                    if len(elements) < 5:
                        print 'Invalid version format : ' + current_os
                        continue
                    platform = elements[0]
                    version = elements[2]
                    if str(platform) == 'Android':
                        if float(version) >= 5.0:
                            print 'Already changed : ' + str(version)
                            continue
                        else:
                            adset[AdSet.Field.targeting][Targeting.Field.user_os] = ['5.0']
                            print 'change to version : '+str(adset[AdSet.Field.targeting][Targeting.Field.user_os])
                            updatecount = updatecount+1
                            my_api.remote_update(adset, callback_update_success, callback_update_failure)
                    elif str(platform) == 'iOS':
                        if float(version) >= 9.0:
                            print 'Already changed : ' + str(version)
                            continue
                        else:
                            adset[AdSet.Field.targeting][Targeting.Field.user_os] = ['9.0']
                            print 'change to version : '+str(adset[AdSet.Field.targeting][Targeting.Field.user_os])
                            updatecount = updatecount+1
                            my_api.remote_update(adset, callback_update_success, callback_update_failure)
                    else:
                        print 'Invalid OS Type : '+str(platform)
                        continue

    if updatecount > 0:
        my_api.execute()       

def runfbmodule(start):
    #time.sleep(300)
    startpoint = int(start)
    currentpoint = startpoint
    keydata = fb.get_key_data()
    for i in range(0, 5):
        currentaccountname = 'BitMango_'+str(currentpoint).zfill(2)
        for key in keydata:
            if key['business_key']['account_name'] == currentaccountname:
                print currentaccountname
                appname = key['app_name']
                changeosversion(appname)
                time.sleep(600)
                break
        currentpoint = currentpoint + 1

def main():
    startpoint = int(sys.argv[1])
    runfbmodule(startpoint)

if __name__ == "__main__":
    sys.exit(main())


