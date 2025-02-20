
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS564 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

"""
Escapes quotes inside text
"""
def escape_and_wrap(value):
    if value is None:
        return '""'  # Treat None as an empty string
    return f'"{value.replace("\"", "\"\"")}"'


"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file,seenUsers,seenCategories,seenItemCategory):
    with open(json_file, 'r') as f:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file
        with open("Items.dat", "a") as item_file, \
            open("Users.dat", "a") as user_file, \
            open("Bids.dat", "a") as bids_file, \
            open("Categories.dat", "a") as categories_file, \
            open("ItemCategory.dat", "a") as item_category_file:

            for item in items:
                ### Process Item Data ###
                itemID = item['ItemID']
                name = escape_and_wrap(item.get("Name", ""))
                currently = transformDollar(item['Currently'])
                buy_price = transformDollar(item.get('Buy_Price', None))
                first_bid = transformDollar(item['First_Bid'])
                number_of_bids = item['Number_of_Bids']
                started = transformDttm(item['Started'])
                ends = transformDttm(item['Ends'])
                description = escape_and_wrap(item['Description'])
                sellerID = escape_and_wrap(item['Seller']['UserID'])

                item_file.write(f"{itemID}|{name}|{currently}|{buy_price}|{first_bid}|{number_of_bids}|{started}|{ends}|{description}|{sellerID}\n")

                ### Process User(Seller) Data ###
                sellerRating = item['Seller']['Rating']
                sellerLocation = escape_and_wrap(item.get("Location", ""))
                sellerCountry = escape_and_wrap(item.get("Country", ""))

                if sellerID not in seenUsers:
                    user_file.write(f"{sellerID}|{sellerRating}|{sellerLocation}|{sellerCountry}\n")
                    seenUsers.add(sellerID)

                ### Process Bids Data ###
                if 'Bids' in item and item['Bids'] is not None:
                    for bid in item['Bids']:
                        bidder = bid['Bid']['Bidder']
                        bidderID = escape_and_wrap(bidder['UserID'])
                        time = transformDttm(bid['Bid']['Time'])
                        amount = transformDollar(bid['Bid']['Amount'])
                        
                        bids_file.write(f"{itemID}|{bidderID}|{time}|{amount}\n")
                        
                        # Also add the bidder to Users.dat (avoid duplicates separately)
                        bidder_rating = bidder['Rating']
                        bidder_location = escape_and_wrap(bidder.get("Location", ""))
                        bidder_country = escape_and_wrap(bidder.get("Country", ""))

                        if bidderID not in seenUsers:
                            user_file.write(f"{bidderID}|{bidder_rating}|{bidder_location}|{bidder_country}\n")
                            seenUsers.add(bidderID)

                ### Process Categories Data ###
                for category in item['Category']:
                    hashRes = hash((itemID,category))
                    if category not in seenCategories:
                        categories_file.write(f"{escape_and_wrap(category)}\n")
                        seenCategories.add(category)
                    if hashRes not in seenItemCategory:
                        item_category_file.write(f"{itemID}|{escape_and_wrap(category)}\n")
                        seenItemCategory.add(hashRes)



"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    seenUsers = set()
    seenCategories = set()
    seenItemCategory = set()
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f,seenUsers,seenCategories,seenItemCategory)
            print ("Success parsing " + f)

if __name__ == '__main__':
    main(sys.argv)
