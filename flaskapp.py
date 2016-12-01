from collections import Counter
import sqlite3
import time
import os

from flask import Flask, request, g, render_template, redirect, url_for, jsonify, abort
from flask import session as login_session

app = Flask(__name__)
app.config.from_object(__name__)

MAX_POST = 6889
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
        image_name = post[0][4]

        #query the segmented_images based on the post_id
        segmented_images = select_query("""SELECT *
                                           FROM segmented
                                           WHERE post_id = ?""",
                                        [post_id])

        #limit showing at most 3 segmented_images
        if len(segmented_images) > 3:
            segmented_images = segmented_images[:3]

        #query results based on each segmented_images
        results = []
        min_results_length = 10
        for i in segmented_images:
            tmp = select_query("""SELECT * 
                                  FROM results
                                  WHERE segmented_id = ?""",
                               [i[0]])
            results.append(tmp)
            if len(tmp) < min_results_length:
                min_results_length = len(tmp)

        #limit the length of results to be the min_results_length
        for i in xrange(len(segmented_images)):
            results[i] = results[i][:min_results_length]
                

        #create the template filled with data
        return render_template("post.html", main_image_url=main_image_url,
                               source_url=source_url,
                               tags=tags,
                               image_name=image_name,
                               segmented_images=segmented_images,
                               results=results)
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

