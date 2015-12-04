#-*-coding: utf-8 -*-
__author__ = "eprivalov"
import threading
import urllib, urllib2
import time
from Queue import Queue


class AsyncWebPageClient(object):

    THREADS = 10
    RESULT = []

    def __init__(self, *args, **kwargs):
        self.Queue = Queue()
        if "threads" in kwargs:
            self.threads = kwargs["threads"]
        else:
            self.threads = self.THREADS

        for _ in xrange(self.threads):
            thread_ = threading.Thread(target=self.get_page_content)
            thread_.setDaemon(True)
            thread_.start()

    def get_page(self, url_collection):
        current_queue = Queue()
        for url in url_collection:
            self.Queue.put((url, current_queue))
        collection_length = len(url_collection)
        if collection_length > 1:
            for item in range(collection_length):
                status, url, data = current_queue.get()
                if status == 200:
                    self.RESULT.append(dict(status_code=status, url=url, content=data))
                else:
                    self.RESULT.append(dict(status_code=-1, url=url, err=data))
            return self.RESULT

        #elif collection_length == 1:
        #    status, url, data = current_queue.get()
        #    if status == 200:
        #        self.RESULT.append(dict(status_code=status, url=url, content=data))
        #    else:
        #        self.RESULT.append(dict(status_code=-1, url=url, err=data))
        #    return self.RESULT
        #else:
        #    return "Collection is empty, please enter filled collection at least by one item."

    def get_page_content(self):
        while 1:
            url, Queue = self.Queue.get()
            try:
                self.page = urllib.urlopen(url)
                if self.page.getcode() == 200:
                    Queue.put((200, url, self.page.read()))
                    #self.page.close()
                else:
                    Queue.put(('-1', url, self.page.getcode()))
                self.page.close()
            except BaseException, e:
                self.page.close()




url_collection = ('http://facebook.com/groups/insydiaofficial/',
                  'http://google.com/asdas/',
                  )
a = time.time()
print AsyncWebPageClient(threads=2).get_page(url_collection)
print time.time() - a