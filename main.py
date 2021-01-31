import requests
import xmltodict
import json
import os

#gc = client.GoodreadsClient(key, code )


#print (book.authors)
#more than 20, search by author or title,returning multiple authors, none
from Books import *
from database_bookshelf import *
from Methods import *

#create_database()
#create a temporary dictonary of books
temp_case = {}
#create a database
#select book from id search
for book in (get_all_ID_title_author()):
    book = create_book(book.id)
#what if no book can be made
    #book.add_note("hello")

#have user search for book
text = str(input("what is the NAME of the book you'd like to add"))
key = os.environ.get('GoodreadsKey')
r = requests.get(
    'https://www.goodreads.com/search/index.xml',
    params = {'key': key, 'q': text},
)

#get description fr book
#r = requests.get("https://www.goodreads.com/book/show.xml?key=VdCsnffb7Pn5bgNtb6V7uQ&id=1")
r_text = r.text
#parse text from request into json
data =json.dumps(xmltodict.parse(r_text))
#turn json data into python object
data = json.loads(data)
#get how many results have returned (max 20 now)
num_results = int(data["GoodreadsResponse"]["search"]["results-end"])


def show_options(num):
    #no book is found inform user
    if num_results == 0:
        print ("no book found, try again")
    else:
        #print out stats for all the books with title
        for x in range (0, num_results):
            temp_book = Book()
            temp_book.set_index(x)
            temp_book.set_stats(data)
            print('choice ' + str((temp_book.index + 1)) + ' is ' + str(temp_book.title) + ' by ' + str(temp_book.author)  + ' w/ a rating of ' + str(temp_book.average_rating))
            print("")
            #add book to temp bookcase
            temp_case[x] = temp_book

choice = input(("enter the book you'd like to add, press 0 for none"))

try:
    choice = int(choice)
    if choice == 0:
        print("ok")

    #not repeating? if number out of bounds
    elif not(0 <= choice <= num_results):
        print("no")
    else:
        #add chosen book to users bookcase
        current_book = (temp_case[choice-1])
        notes = input("ENTER 0 to NOT add notes; otherwise enter your notes now: ")
        if not(notes == '0'):
            current_book.add_note(str(notes))

        add_book(current_book)
        temp_case.clear()
        notes = input("ENTER your notes now: ")
        current_book.add_note(notes)

        #print(get_all_title_author())

      #quit = input("Press 1 to add another book from the list and 0 to exit")

#if not an int added
except KeyError:
    print ("something went wrong!")
