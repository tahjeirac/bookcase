import sqlite3
#import sql errora

#
# #add book to database later
# def add_book(book):
#     #automatically commits or rolls back (if eexception) connections
#     with conn:
#         c.execute("INSERT INTO bookcase VALUES (:title, :author, :genre, :GR_Rating,:User_Rating, :Tags, :Notes, "
#                   ":Yr_Pub)", {'title': book.title, 'author': book.author, 'genre': book.format_genres(),
#                                'GR_Rating': book.average_rating,'User_Rating' : book.user_rating,
#                                'Tags': book.format_tags(), 'Notes': book.format_notes(), 'Yr_Pub':
#                                                          book.year_published})
#
#

def add_book(book,cover,url,conn,cur):
    #automatically commits or rolls back (if eexception) connections

    if (book.average_rating == None):
        book.average_rating = 0.0
    with conn:
        cur.execute("INSERT INTO bookcase VALUES (:ID,:Cover, :Title, :Author,:GoodReads_Rating,:Notes,:URL)",
                    {'ID': book.id,'Cover':cover, 'Title': book.title,
                     'Author': book.author, 'GoodReads_Rating': book.average_rating,
                     'Notes': book.notes, 'URL': url})

#return the title and author of all books added
def get_all_ID_title_author(conn,cur):
    with conn:
        cur.execute("SELECT ID,Title, Author FROM bookcase ")
    return cur.fetchall()


def insert_notes(id,note,conn,cur):

    with conn:
        #c.execute(sql,book)
        cur.execute('''UPDATE bookcase
              SET Notes = ?
              WHERE ID = ? ''', (note, id))
        #conn.commit()

def get_notes(id,conn,cur):
    with conn:
        cur.execute("SELECT Notes FROM bookcase WHERE ID = ?", (str(id).strip(),))
    return cur.fetchall()

#be able to search for multiple paramters?, make it not a tuple?
""" selects book from database"""
def select_book(id,conn,cur):
    with conn:
        #don't use * in production, only development
        cur.execute('''SELECT *
                      FROM bookcase
                      WHERE ID = ? ''',  (str(id).strip(),))
        #return dictonary of book values
        return cur.fetchone()


def search_by_id(id,conn,cur):
    with conn:
        cur.execute("SELECT * FROM bookcase WHERE ID = ?", (str(id).strip(),))
    return cur.fetchone()

def delete_book(id,conn,cur):
    with conn:
        cur.execute("""DELETE FROM bookcase 
                        WHERE ID = ?""", (str(id).strip(),))