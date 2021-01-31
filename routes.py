import sqlite3
from flask import Flask, render_template, redirect, url_for
from flask import request, jsonify
from flask import g
import os

from forms import *
from Methods import *
from Books import *
from database_bookshelf import *

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d



@app.route('/')  # at end point '/' - end point is last thing on url
def home():  # <h1></h1> are tags for biggest heading and <p> tags are for a paragraph
    return render_template('base.html', title='Home Page', par='Welcome to my Bookshelf!')


@app.route('/all', methods=['GET','POST'])
def api_all():
    conn = sqlite3.connect('bookbase.db')
    # let connetion object know to use dict_factory function to return item as dictonary instead of list
    conn.row_factory = dict_factory  # row factoru returns special object that is easier to work with than tuple (dictonary)
    cur = conn.cursor()
    cur.execute('SELECT * FROM bookbase;')
    r = cur.fetchall()
    return render_template('data.html', title='All Books', books=r, par = request.args.get('par'), id = request.args.get('id'))


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404






"""show results of searching goodreads for a book"""


@app.route('/results', methods=('GET', 'POST'))
def book_selection():
    conn = sqlite3.connect('bookbase.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    try:
        title = str((request.args.get('titleText')))
        booklist = search(title)
        num_results = booklist[0]
        data = booklist[1]
        temp_case = show_options(num_results, data)
        # make dict into list
        books = selection_list_maker(temp_case)
        # print(temp_case[object].title())
        select_book = ChooseBook(request.form)
        # populate slection list
        select_book.books.choices = books



        # if book has been selected
        if (request.method == 'POST'):
            # get id
            chosen_id = (select_book.books.data)
            # search db for id to check for duplicates
            same_book = search_by_id(chosen_id, conn, cur)
            #if there isn't a duplicate book
            if (same_book == None):
                for object in temp_case:
                    book = temp_case[object]
                    # find book with matching id and add to database
                    if (str(book.id) == str(chosen_id)):
                        cover = getCover(book.id)
                        url = getUrl(book.id)
                        add_book(book,cover,url, conn, cur)
                        return redirect(url_for('add_notes', ID=chosen_id))
            return redirect(url_for('api_all', title='error',
                                    par ='You have already entered that book (hilighted in blue)', id = chosen_id))
        # else render template showing book options
        return render_template('show_options.html',
                               title='Searching...',
                               header="Searching Goodreads for: " + title,
                               form=select_book)
    except:
        print('something went wrong')
    finally:
        return redirect(url_for('home'))


"""Search for a book"""
@app.route('/new', methods=('GET', 'POST'))
def search_GR():
    myform = BookSearchForm(request.form)
    if (request.method == 'POST'):
        title = myform.title._value()

        return redirect(url_for('book_selection', titleText=title))  # send title to selection page

    return render_template('new_book.html',
                           title='Search',
                           par='Enter a book to search GR for!',
                           form=myform)

"""Allow user to insert note"""
@app.route('/create', methods=('Get', 'POST'))
def add_notes():
    conn = sqlite3.connect('bookbase.db')
    # let connetion object know to use dict_factory function to return item as dictonary instead of list
    conn.row_factory = dict_factory  # row factoru returns special object that is easier to work with than tuple (dictonary)
    cur = conn.cursor()

    # request.form retrieves values from form once posted
    id = str((request.args.get('ID')))
    myform = AddNote(request.form)
    if (request.method == 'POST'):
        text = myform.body._value()
        insert_notes(id,text,conn,cur)

        # current_book.add_note(str(notes))

        return redirect(url_for('api_all'))

    return render_template('add_note.html',
                           form=myform)

@app.route('/delete', methods=('Get', 'POST'))
def _delete_book():
    conn = sqlite3.connect('bookbase.db')
    conn.row_factory = dict_factory  # row factoru returns special object that is easier to work with than tuple (dictonary)
    cur = conn.cursor()
    id='27188596'
    #id = str((request.args.get('ID')))
    delete_book(id,conn,cur)
    return redirect(url_for('api_all'))


if __name__ == '__main__':
    app.run()
