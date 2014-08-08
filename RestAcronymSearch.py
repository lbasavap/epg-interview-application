"""
    A client program that accesses to the Acromine REST service.
    Copyright (c) 2009, Naoaki Okazaki.

    This program issues a query (shortform "HMM") to the Acromine service,
    and prints the object returned from the service.
"""

"""
Nordstrom Requirements:

Description:

    Your task is to create an application that takes an acronym and returns the long form of that acronym using the Acromine REST service. (http://www.nactem.ac.uk/software/acromine/rest.html)

    You have to implement the following user stories:
        Accept any acronym as input Return a meaningful message when the acronym is not found at Acromine For a found acronym return a list of the possible long forms Allow the user to limit the number of long forms returned Should be written in a way that is easy to consume by a human or a computer

Rules:

    Clone this repo to your github account.
    You can choose any development language (If a compiled language, please supply a make script)
    You have to push the code on your Github account and make a pull request to with the results.

"""

#!/usr/bin/env python

import sys
import argparse
import urllib
import json
import datetime

class RestDictConst:
    class ConstError(TypeError): pass
    def __setattr__(self,name,value):
        if self.__dict__.has_key(name):
            raise self.ConstError, "Can't rebind const(%s)"%name
        self.__dict__[name]=value
sys.modules[__name__]=RestDictConst()

class RestAcronymParser():
#{
    def __init__(self, argAcronymShortForm, argStartTime, argEndTime):

        """Setup constant variables."""

        # Constants
        RestDictConst.ACRONYM_SHORT_FORM = 'NOT DEFINED'
        RestDictConst.ACRONYM_LONG_FORM = ''
        RestDictConst.ACRONYM_NOT_FOUND = 'Given Rest Short Form Acronym Not Found in Dictionary'
        RestDictConst.ACRONYM_FOUND = 'Found Requested Acronym in the Dictionary'
        RestDictConst.ACRONYM_REQUEST_TYPE = 'Manual Entry' # Request received via ManualEntry or API Request
        RestDictConst.UNKNOWN = 'unknown'
        RestDictConst.REST_DICT_URL =  ('http://www.nactem.ac.uk/software/acromine/dictionary.py')

        # Acronym Dictionary for local lookup. Search for short form in the heap dictionary, if it exists return it otherwise do a remote DB query, pull & cache.
        # This improves the performance - Key, Value pair. Where Key is the short form and Value is the return result.
        self.AcronymDictionary = {} 

        # Initialize arguments received for reference
        self.ShortAcronym = argAcronymShortForm
        self.startTime = argStartTime
        self.endTime = argEndTime

        print("In RestAcronymParser Initializer: argAcronymShortForm {}, startTime {}, and endTime {}".format(self.ShortAcronym, self.startTime, self.endTime))
    # __init__

    def PrintAcronyms(self, argAcronyms):
    #{
        # Output the object.
        for sf in argAcronyms:
            print('sf: %s' % sf[u'sf'])
            for lf in sf[u'lfs']:
                print(
                    '  lf: %(lf)s, freq: %(freq)d, since: %(since)d' % lf)
                for var in lf[u'vars']:
                    print('    lf: %(lf)s, freq: %(freq)d, since: %(since)d' % var)
    #}

    def IsShortFormFoundInDict(self):
    #{
         # print("Checking whether Dictionary has requested short acronym")
         return self.AcronymDictionary.has_key(self.ShortAcronym)
    #}

    def GetAcronymListFromDict(self):
    #{
        if (self.IsShortFormFoundInDict() is True):
        #{
            return self.AcronymDictionary[self.ShortAcronym]
        #}
        else:
        #{
            print("Failed to locate requested Acronym %s in the cache" %self.ShortAcronym)
            return "Failed"
        #}
    #}

    def InsertAcronymIntoDict(self, argAcronymList):
    #{
        if (self.IsShortFormFoundInDict() is not True):
            self.AcronymDictionary[self.ShortAcronym] = argAcronymList

        return "Success"
    #}

    def GetLongAcronymFormsForShortForms(self):
    #{
        # Validate Input
        if (self.ShortAcronym == RestDictConst.ACRONYM_SHORT_FORM):
            retVal = ("Unexpected Rest Acronym Short Form Received. Please validate Input")
            print(retVal)
            return "Failed", retVal
        #if

        if (self.IsShortFormFoundInDict() is True):
        #{
           # Return the list to the caller
           retVal = self.GetAcronymListFromDict()
           print("Found Acronym in Local Cache for Short Acronym %s" %self.ShortAcronym)
           self.PrintAcronyms(retVal)
           return "Success", retVal
        #}
        else:
        #{
           print("Given Acronym %s Not Found in Local Cache. Perform Remote JSON Query." %self.ShortAcronym)

           # Access the service through HTTP GET.
           params = urllib.urlencode({'sf': self.ShortAcronym, 'lf': RestDictConst.ACRONYM_LONG_FORM})
           fileLikeObj = urllib.urlopen( RestDictConst.REST_DICT_URL, params)

           # Convert the JSON response to the Python object.
           retVal = json.loads(fileLikeObj.read())
           print("Received JSON Objects of size %d" %len(retVal))

           if (len(retVal) is 0):
              retVal = ("%s Acronym Lookup Failed to Find in Remote REST Dictionary. Please very Acronyms" %self.ShortAcronym)
              return "Failed", retVal
           else:
              print("Found Acronym in Remote Cache for Short Acronym %s" %self.ShortAcronym)
              self.InsertAcronymIntoDict(retVal)
              self.PrintAcronyms(retVal)
              return "Success", retVal
        #}
    #} 

#} // End of Class RestAcronymParser():


global AcronymParser
AcronymParser = 'Unknown'
"""
def GetLongAcronymForms(argShortAcronym):
#{
    print("Received a request for Long Acronyms for %s" %argShortAcronym)

    if AcronymParser != 'Unknown':
        AcronymParser = RestAcronymParser(args.shortAcronym, args.startTime, args.endTime)
    AcronymParser.GetLongAcronymFormsForShortForms()
#}
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='JSON Short Acronym to Long Acronym Convertor')
    parser.add_argument('--short_acronym', dest='shortAcronym', help='Please enter Short Acronym for JSON Dictionary Lookup')
    parser.add_argument('--start_time', dest='startTime', default='None', help='Optional Start Time(UTC) for Acronym Lookup.')
    parser.add_argument('--end_time', dest='endTime', default='None', help='Optional End Time(UTC) for Acronym Lookup.')

    args = parser.parse_args()

    print("In Main Received Arguments and Validating")

    if (args.shortAcronym == None):
        parser.print_help()
        sys.exit(-1)

    print("In Main Initializing RestAcronymParser")
    AcronymParser = RestAcronymParser(args.shortAcronym, args.startTime, args.endTime)
    AcronymParser.GetLongAcronymFormsForShortForms()
    print("Unit Testing. Looking for same short name. It should find it in cache.")
    AcronymParser.GetLongAcronymFormsForShortForms()
    print("In Main End of Testing")
#if


