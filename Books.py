import requests
import xml.etree.ElementTree as ET
import xmltodict
import pprint
import json
from database_bookshelf import *


class Book ():
    def __init__ (self):
        self.id = ''
        self. title = ''
        self.author = ''
        self.genres = []
        self.year_published = ''
        self.average_rating = 0
        self.user_rating = 0
        self.index = 0
        self.tags = []
        self.notes = ''

#which result is the book
    def set_index (self, x):
        self.index = x

    def set_stats (self, data):
        #print(data)
        self.average_rating = (data["GoodreadsResponse"]['search']['results']['work'][self.index]['average_rating'])
        # try:
        #     self.year_published = (key["GoodreadsResponse"]['search']['results']['work'][self.index]['original_publication_year']['#text'])
        # except KeyError:
        #    self.year_published = "none"
        #if user wants notes
        self.title = (data["GoodreadsResponse"]['search']['results']['work'][self.index]['best_book']['title'])
        self.author = (data["GoodreadsResponse"]['search']['results']['work'][self.index]['best_book']['author']['name'])
        self.id = (data["GoodreadsResponse"]['search']['results']['work'][self.index]['best_book']['id']['#text'])


    #add notes to book, think it will overide when new is added
    def add_note (self, note, conn, cur):
        self.notes = str(note)
        self.notes = self.notes + " -" + str(note)
        insert_notes(self.notes,self.id,conn,cur)
        #print(self.notes)

    def add_tags(self, tag):
        self.tags.append(str(tag))

    def add_genres(self, genre):
        self.genre.append(" -" + str(genre))



    def format_genres(self):
        string = ''
        for item in (self.genres) :
            string.__add__(" " + str(item))
        return string


    def format_tags(self):
        string = ''
        for item in (self.tags) :
            string.__add__(" " + str(item))
        return string




