
#!/usr/bin/env python 
#-*-encoding:utf-8-*-

'''
Created on Mar 23, 2017

@author: bingo
'''



import logging
import color
'''
# using metaclass to solve this problem, but failed
class Setlogger(type):
    def __new__(meta, classname, supers, attrdict):
        attrdict['setLogger'](classname)
        return type.__new__(meta, classname, supers, attrdict)

'''

class superLogger(object):

#    __metaclass__ = Setlogger


    def __init__(self, logFileName, logLevel, loggerName):
        self.logFileName = logFileName
        self.logLevel = logLevel
        self.logger = logging.getLogger(loggerName)    
        #set log level for logger objector

        self.logger.setLevel(self.logLevel)
        # create the handler objector
        self.fh = logging.FileHandler(self.logFileName)
        self.sh = logging.StreamHandler()
        #set level for handler objector
        self.fh.setLevel(self.logLevel)
        self.sh.setLevel(self.logLevel)
        #set format for handler objector
        self.formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        self.fh.setFormatter(self.formatter)
        self.sh.setFormatter(self.formatter)
        #add handlers to logger object
        self.logger.addHandler(self.fh)
        self.logger.addHandler(self.sh)

    
#    # create this function is order to auto run setLogger function, derector function with parameters
#    def autoSet(self):
#        self.setLogger()
#        def derector(func):        
#            def wrapper(*args, **kargs):                               #function parameter transfer 
#                return func(*args, **kargs)
#            return wrapper       

    def autoSet(self):
        self.setLogger()
  
    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warn(self, message):
        message = color.y("[%s]" % color.B(message))
        self.logger.warn(message)

    def error(self, message):
        message = color.r("[%s]" % color.B(message))
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)        

class Logger(superLogger):
      def __init__(self, loghome, loggerName):
          super(Logger, self).__init__(loghome, logging.DEBUG, loggerName)

if __name__ == "__main__":
    log = Logger(__name__)
    log.debug("this is not a big problem")
    log.info("this is a question")
    log.info("this is a question")
    
