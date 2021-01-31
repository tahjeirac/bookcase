import requests
from flask import render_template
import os
from Books import *
from database_bookshelf import *


def create_book(dict):
    if (dict == None):
        print("That book was not found")
    elif (len(dict) == 5):
        selected = Book()
        selected.id = dict['ID']
        selected.title = dict['Title']
        selected.author = dict['Author']
        selected.average_rating = dict['GoodReads_Rating']
        selected.notes = dict['Notes']
        return selected
    else:
        return """<h1>404</h1> 
                     <p>Something Went Wrong! Please return to the home page and try again.</p>"""

#show matches of book search
def show_options(num, data):
    temp_case = {}
    if num == 0:
        #redirect
        return """<h1>404</h1> 
              <p>Something Went Wrong! Please return to the search page and try again.</p>"""

    else:
        #print out stats for all the books with title
        for x in range (0, num):
            temp_book = Book()
            temp_book.set_index(x)
            temp_book.set_stats(data)
            #add book to temp bookcase
            temp_case[x] = temp_book
    return temp_case
    #return render_template('show_options.html', title='All Books', par=str(temp_book_title))

"""search goodreads for a book"""
def search(title):
    key = os.environ.get('GoodreadsKey')
    r = requests.get(
        "https://www.goodreads.com/search/index.xml",
        params = {'key': key, 'q': str(title)},)
    # get description fr book
    r_text = r.text
    # parse text from request into json
    data = json.dumps(xmltodict.parse(r_text))
    # turn json data into python object
    data = json.loads(data)
    # get how many results have returned (max 20 now)
    num_results = int(data["GoodreadsResponse"]["search"]["results-end"])
    return [num_results, data]

def getCover (id):
    key = os.environ.get('GoodreadsKey')
    r = requests.get("https://www.goodreads.com/book/show.xml",
                    params = {'key': key, 'q': str(id)},)
    r_text = r.text
    data = json.dumps(xmltodict.parse(r_text))
    data = json.loads(data)
    print(data)
    #description = str(data[]["search"]["results-end"])
    photo_url = str(data["GoodreadsResponse"]["book"]["image_url"])

    return photo_url

def getUrl (id):
    key = os.environ.get('GoodreadsKey')
    r = requests.get(
        "https://www.goodreads.com/book/show.xml",
        params = {'key': key, 'q': str(id)},)
    r_text = r.text
    data = json.dumps(xmltodict.parse(r_text))
    data = json.loads(data)
    # description = str(data[]["search"]["results-end"])
    url = str(data["GoodreadsResponse"]["book"]["url"])
    return url

"""Turn dictonary of books into simple selection list for select list"""
def selection_list_maker(dict):
    book_choices = []
    for object in dict:
        book= dict[object]
        info = (book.title + ' by ' + book.author)
        newlist = [book.id, info]
        book_choices.append(newlist)
    return book_choices
