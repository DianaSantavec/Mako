
class BaseLogger(object):
    
    def print(self, text=""):
        pass

    def task(self, task, identifier=None):
        pass

    def title(self, title):
        pass

    def table(self, table, has_header=True):
        pass

    def schedule(self, schedule):
        pass
