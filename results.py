#/usr/bin/python

import json
import sys
import re
import subprocess
import os.path
from pprint import pprint

reload(sys)
sys.setdefaultencoding('utf-8')

def decodeJSONFiles( filenames ):
    #need to parse data line by line because of json object on each line
    #as a whole its not valid JSON
    content = {}
    for f in filenames:
        with open(f) as file:
            lists = []
            for line in file:
                lists.append(json.loads(line))
        content[f] = lists

    return content

def findMatches(content):
    #use these data structures to add listings and products
    results_obj = {}
    listings = []
    results = []
    count = 0

    print "finding matches........."

    #for each prouct add product name to the results_obj dictionary
    for prod in content['products.txt']:
        results_obj['product_name'] = prod['product_name']

        #look at each listing
        for listing in content['listings.txt']:

            #if the manufacturer is the same for both product and listing we can continue
            if listing.get('manufacturer').lower() ==  prod.get('manufacturer').lower():

                #use regex to find only the model in the listing title and ignore case
                #putting this here because there is always a model associated with the product
                mregex = '\\b' + prod.get('model')+ '\\b'
                searchmodel = re.search(mregex,listing.get('title'), re.M|re.I)

                #family entry in dictionary is not always present so check to see if there
                if prod.get('family') != None:

                    #if it is then use regex to find only the family in the listing title and ignore case
                    fregex = '\\b' + prod.get('family')+ '\\b'
                    searchfamily = re.search(fregex,listing.get('title'), re.M|re.I)

                    #if both family and model are found, this is defintely the listing we are looking for
                    if searchmodel and searchfamily:
                        listings.append(listing)

                #if there isnt a family we will just look for the model
                elif searchmodel:
                    listings.append(listing)

        #as long as we found a listing we will add it to the final data structure to be printed
        if len(listings) > 0:

            #create listings entry in dictionary and add the array of listings to it
            #already has product name and we just need to add the listings entry now
            results_obj["listings"] = listings
            results.append(results_obj)

            #clear the dictionary and listing list for next iteration
            results_obj = {}
            listings = []


    return results

def printToJSON(results):
    print "printing to JSON File........."
    output = 'results.txt'

    #if results.txt is already there delete it
    if os.path.exists('./' + output):
        subprocess.call("rm " + output, shell=True)

    #write JSON to file
    for result in results:
        var = open('results.txt', 'a')
        #use ensure_ascii to allow foriegn languages to appear normally in .txt
        var.write(json.dumps(result,ensure_ascii=False))
        var.write("\n")

def main():
    filenames = ['products.txt','listings.txt']
    decoded_content = decodeJSONFiles( filenames )
    results = findMatches(decoded_content)
    printToJSON(results)


main()
