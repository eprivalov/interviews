__author__ = "eprivalov"
import threading


class AsyncWebPageClient(object):

    THREADS = 1

    def __init__(self, enter_threads):
        self.enter_threads = enter_threads

    def get_page(self):
        pass

if __name__ == "__main__":
    AsyncWebPageClient(enter_threads=2)
