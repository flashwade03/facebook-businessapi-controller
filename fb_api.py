import sys, os, queue, time
from facebook_business import FacebookSession
from facebook_business.api import FacebookAdsApi
from functools import partial

class API:

    api = None
    object_queue = None
    mode_queue = None
    self.batch = None

    def __init__(self, clientid, appsecret, token):
        session = FacebookSession(
                clientid,
                appsecret,
                token
        )
        self.api = FacebookAdsApi(session)
        self.object_queue = queue.Queue()
        self.mode_queue = queue.Queue()
        self.batch = self.api.new_batch()

    class RemoteMode:
        CREATE = 0
        UPDATE = 1
        DELETE = 2
        
    def remote_create(self, obj):
        self.object_queue.put(obj)
        self.mode_queue(API.RemoteMode.CREATE)

    def remote_update(self, obj):
        self.object_queue.put(obj)
        self.mode_queue(API.RemoteMode.UPDATE)

    def remote_delete(self, obj):
        self.object_queue.put(obj)
        self.mode_queue(API.RemoteMode.DELETE)
    
    def execute(self):
        totalcount = object_queue.size()
        finished = False

        while not finished:
            for i in range(0, 50):
                if object_queue.size() == 0:
                    break;
                
                item = self.object_queue.get()
                mode = self.mode_queue.get()
                if mode == 0:
                    item.remote_create(batch = self.batch)
                elif mode == 1:
                    item.remote_update(batch = self.batch)
                elif mode == 2:
                    item.remote_delete(batch = self.batch)

            self.batch.execute()
            if object_queue.size() == 0:
                finished = True
            else:
                time.sleep(300)
