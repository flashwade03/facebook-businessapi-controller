import sys, os, queue, time
from facebook_business import FacebookSession
from facebook_business.api import FacebookAdsApi
from functools import partial
from facebook_business.adobjects.adset import AdSet

class API:

    api = None
    object_queue = None
    successevent_queue = None
    failevent_queue = None

    batch = None

    class request_bundle:
        element = None
        success_callback = None
        failure_callback = None
        mode = None
        def __init__(self, target, m, success = None, failure = None):
            self.element = target
            self.mode = m
            self.success_callback = success
            self.failure_callback = failure

    def __init__(self, clientid, appsecret, token):
        session = FacebookSession(
                clientid,
                appsecret,
                token
        )
        self.api = FacebookAdsApi(session)
        self.object_queue = queue.Queue()
        self.batch = self.api.new_batch()

    class RemoteMode:
        CREATE = 0
        UPDATE = 1
        DELETE = 2
        
    def remote_create(self, target, success_event = None, failure_event = None):
        obj = API.request_bundle(target, API.RemoteMode.CREATE, success_event, failure_event)
        self.object_queue.put(obj)

    def remote_update(self, target, success_event = None, failure_event = None):
        obj = API.request_bundle(target, API.RemoteMode.UPDATE, success_event, failure_event)
        self.object_queue.put(obj)

    def remote_delete(self, target, success_event = None, failure_event = None):
        obj = API.request_bundle(target, API.RemoteMode.DELETE, success_event, failure_event)
        self.object_queue.put(obj)

    def execute(self):
        #time.sleep(300)
        totalcount = self.object_queue.qsize()
        currentcount = 0
        finished = False

        while not finished:
            for i in range(0, 30):
                if self.object_queue.qsize() == 0:
                    break;
                
                obj = self.object_queue.get()
                item = obj.element
                mode = obj.mode
                success_event = obj.success_callback
                fail_event = obj.failure_callback

                if mode == API.RemoteMode.CREATE:
                    item.remote_create(batch = self.batch, success=success_event ,failure= fail_event)
                elif mode == API.RemoteMode.UPDATE:
                    item.remote_update(batch = self.batch, success=success_event, failure = fail_event)
                elif mode == API.RemoteMode.DELETE:
                    item.remote_delete(batch = self.batch, success = success_event, failure = fail_event)
                currentcount = currentcount+1

            print 'Processing... : '+str(currentcount)+'/'+str(totalcount)
            self.batch.execute()
            self.batch = self.api.new_batch()
            if self.object_queue.qsize() == 0:
                print 'Finish work'
                finished = True
            else:
                print 'Wait 5min for next work'
                time.sleep(600)


