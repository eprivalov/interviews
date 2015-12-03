#-*-coding: utf-8 -*-
__author__ = "eprivalov"
import threading
import urllib, urllib2
import time
from Queue import Queue

class AsyncWebPageClient(object):
    """
Результат задания представляет собой модуль написанный на языке Python 2.7
(разрешается использовать любые библиотеки из стандартного pip репозитория).
В модуле необходимо реализовать класс AsyncWebPageClient, конструктор которого
принимает количество потоков, которые будут выполнять задачи, при этом должно
присутствовать значение по умолчанию.
Класс AsyncWebPageClient должен содержать метод get_pages который принимает коллекцию
url для загрузки и возвращает словарь (список словарей) содержащий код ответа, url
запроса и контент в формате:
{'status_code': <status code>, 'url': <url>, 'content': <content>}
Если во время запроса или обработки его результатов происходит ошибка url не должен
теряться, и функция должна также возвратить словарь только код ответа должен стать -1 и
в словарь добавляется объект исключения. Формат словаря в случае ошибки:
{ 'status_code': -1, 'err': <error object>, 'url': <url>}
"""

    THREADS = 1
    URL_COLLECTION = ('http://google.com/',
                      'http://yandex.ru/',
                      'http://vk.com/',
                      'http://gooogle.com/asda/'
                      )
    QUEUE = Queue()
    LOCK = threading.RLock()

    RESULT = []

    def __init__(self, *args, **kwargs):
        if "input_threads" in kwargs:
            self.enter_threads = kwargs["input_threads"]
        else:
            self.enter_threads = self.THREADS
        try:
            print self.get_page(self.URL_COLLECTION)
        except RuntimeWarning:
            pass

    def get_page(self, url_collection):
        a = time.time()
        if len(url_collection) > 1:
            for i in url_collection:
                print i
                self.QUEUE.put(i)
            print "pushed"
            for _ in xrange(self.enter_threads):
                thread_ = threading.Thread(target=self.main_function())
                thread_.start()
                print thread_
            while threading.active_count() > 1:
                time.sleep(1)
        b = time.time()
        print b-a
        return self.RESULT

    def main_function(self):
        while True:
            try:
                target_link = self.QUEUE.get_nowait()
            except Exception:
                return
            self.RESULT.append(self.create_dict(target_link))

    def create_dict(self, item):
        if self.check_page_status(item) == 200:
            return dict(status_code=200, url=item, content=self.get_page_content(item))
        else:
            return dict(status_code=-1, url=item, err=self.check_page_status(item))

    def get_page_content(self, url):
        return urllib.urlopen(url).read().decode("UTF-8", "replace")

    def check_page_status(self, url_page):
        return urllib.urlopen(url_page).getcode()

if __name__ == "__main__":
    AsyncWebPageClient(input_threads=1)
