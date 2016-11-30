from collections import Counter
import sqlite3
import time
import os

from flask import Flask, request, g, render_template, redirect, url_for, jsonify, abort
from flask import session as login_session

app = Flask(__name__)
app.config.from_object(__name__)

MAX_POST = 871
MAX_PAGE = (MAX_POST - 1)/9 + 1


def connect_to_database():
    return sqlite3.connect(os.path.join(app.root_path,
                                        'search_engine_demo.db'))

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
    return redirect(url_for('index'))
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
        back_to_page = (post_id - 1)/9 + 1
        pervious_post = (post_id - 1) if post_id != 1 else 1
        next_post = (post_id + 1) if post_id != MAX_POST else MAX_POST

        #query the post based on the post_id
        post = select_query("""SELECT * 
                               FROM posts
                               WHERE id = ?""",
                            [post_id])
        main_image_url = post[0][1]
        source_url = post[0][2]
        tags = post[0][3]
        Image_name = post[0][4]
        
        #query the results based on the post_id
        results = select_query("""SELECT * 
                                  FROM results
                                  WHERE post_id = ?""",
                               [post_id])

        result_reorder = []
        tmp = []
        #TODO: test out results after database created
        for i in xrange(len(results)):
            tmp.append(results[i])
            if (i+1)%3 == 0:
                result_reorder.append(tmp)
                tmp=[]
        if tmp:
            result_reorder.append(tmp)
                

        #TODO: modify the html after its created
        return render_template("post.html", main_image_url=main_image_url,
                               source_url=source_url,
                               tags=tags,
                               Image_name=Image_name,
                               results=result_reorder)
    elif post_id < 1:
        return redirect(url_for('post', post_id=1))
    else:
        return redirect(url_for('post', post_id=MAX_POST))
    

@app.route('/dynamic', methods=['GET', 'POST'])
def dynamic():
    return redirect(url_for('index'))
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

