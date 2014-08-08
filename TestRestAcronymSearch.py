"""
   Use this Test script to test JSON Rest API Validation.
   Author: Lava B
"""

"""
Test Comand: python TestRestAcronymSearch.py --short_acronym HMM --long_acronym_count 5
"""

#!/usr/bin/env python

import sys
import argparse
import datetime
import RestAcronymSearch

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='JSON Short Acronym to Long Acronym Convertor')
    parser.add_argument('--short_acronym', dest='shortAcronym', help='Please enter Short Acronym for JSON Dictionary Lookup')
    parser.add_argument('--long_acronym_count', dest='acronymCount', help='Please enter Long Acronym Search Count')
    parser.add_argument('--start_time', dest='startTime', default='None', help='Optional Start Time(UTC) for Acronym Lookup.')
    parser.add_argument('--end_time', dest='endTime', default='None', help='Optional End Time(UTC) for Acronym Lookup.')

    args = parser.parse_args()

    print("In Main Received Arguments and Validating")

    if (args.shortAcronym == None):
        parser.print_help()
        sys.exit(-1)

    print("In Test Main Calling GetLongAcronymForms for getting Long Acronyms")

    AcronymList = RestAcronymSearch.GetLongAcronymForms(args.shortAcronym, args.acronymCount, args.startTime, args.endTime)

    print("\n\nTest Printing Returning List of Long Acronyms\n")
    print(AcronymList)

    while len(AcronymList) > 0:
        astr = AcronymList[0]
        del AcronymList[0]
        print(astr)

    print("\n\nTest End of Printing Returning List of Long Acronyms\n")

    print(AcronymList)
    print("In Main End of Testing")
#if


