from collections import Counter
import sqlite3
import time

from flask import Flask, request, g, render_template, redirect, url_for, jsonify, abort
from flask import session as login_session

app = Flask(__name__)
app.config.from_object(__name__)

#TODO: MAX_PAGE and MAX_POST
MAX_POST = 100000
MAX_PAGE = (MAX_POST - 1)/9 + 1


def connect_to_database():
    return sqlite3.connect('search_engine_demo.db')

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = connect_to_database()
    return db

@app.route('/', methods=['post', 'get'])
def index():
    rows = select_query("""SELECT count(*), MIN(id), MAX(id)
                              FROM posts""",
                           [])
    print rows
    # TODO: submit the post request and save the name and email to the database
    return render_template("index.html")

@app.route('/advertiser')
def advertiser():
    return render_template("advertiser.html")

@app.route('/influencer')
def influencer():
    return render_template("influencer.html")

@app.route('/page/<int:page_number>')
def page(page_number):
    if page_number >= 1 and page_number <= MAX_PAGE:
        min_idx = 9*(page_number-1) + 1
        max_idx = 9*(page_number)
        pervious_page = (page_number - 1) if page_number != 1 else 1
        next_page = (page_number + 1) if page_number != MAX_PAGE else MAX_PAGE

        #query the posts based on the page_number
        posts = select_query("""SELECT * 
                                FROM posts
                                WHERE id >= ?
                                AND id <= ?""",
                             [min_idx, max_idx])

        #TODO: test out posts after database created
        #print posts, sidojfds

        #TODO: modify the html after its created
        return render_template("page.html", posts=posts,
                               pervious_page=pervious_page,
                               next_page=next_page)
    else:
        return redirect(url_for('page', page_number=1))

    
@app.route('/post/<int:post_id>')
def post(post_id):
    if post_id >= 1 and post_id <= MAX_POST:
        back_to_page = (product_id - 1)/9 + 1
        pervious_post = (post_id - 1) if post_id != 1 else 1
        next_post = (post_id + 1) if post_id != MAX_POST else MAX_POST

        #query the results based on the post_id
        results = select_query("""SELECT * 
                                  FROM results
                                  WHERE post_id >= ?""",
                               [post_id])

        #TODO: test out results after database created
        print results, sidojfds

        #TODO: modify the html after its created
        return render_template("post.html", results=results,
                               back_to_page=back_to_page,
                               pervious_post=pervious_post,
                               next_post=next_post)
    else:
        return redirect(url_for('post', post_id=1))
    

@app.route('/dynamic', methods=['GET', 'POST'])
def dynamic():
    if request.method == 'POST':
        #TODO: send request to search engine api and display result
        pass
    else:
        #TODO: display empty layout with a field asking for an image URL
        pass
        #return render_template("dynamic.html")


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def select_query(query, args=()):
    cur = get_db().execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows

def insert_query(query, args=()):
    conn = get_db()
    conn.execute(query, args)
    conn.commit()

if __name__ == '__main__':
    app.secret_key = 'osjfodiasjoIHUUYoihiuGhiUYgUTf%^^7Y9*hOIlBgCHFyTFu&%T'
    app.run(threaded=True)

