from collections import Counter
import sqlite3
import time
import os
import base64
import requests
from requests import Request, Session
import json

from flask import Flask, request, g, render_template, redirect, url_for, jsonify, abort
from flask import session as login_session

app = Flask(__name__)
app.config.from_object(__name__)


def connect_to_database():
    return sqlite3.connect(os.path.join(app.root_path,
                                        'search_engine_demo.db'))

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = connect_to_database()
    return db

@app.route('/', methods=['POST', 'GET'])
def index():
    rows = select_query("""SELECT count(*), MIN(id), MAX(id)
                              FROM feedback""",
                           [])
    print rows
    # submit the post request and save the name and email to the database
    if request.method == 'POST':
        name = request.form['register-form-name']
        email = request.form['register-form-email']

        insert_query("""INSERT INTO stay_updated (name, email)
                        VALUES (?, ?)""",
                      [name, email])
    return render_template("index.html")

@app.route('/advertiser', methods=['POST', 'GET'])
def advertiser():
    if request.method == 'POST':
        name = request.form['register-form-name']
        company = request.form['register-form-company']
        email = request.form['register-form-email']
        phone = request.form['register-form-phone']
        message = request.form['template-contactform-message']
        
        insert_query("""INSERT INTO advertiser
                        (name, company, email, phone, message)
                        VALUES (?, ?, ?, ?, ?)""",
                      [name, company, email, phone, message])
        
    return render_template("advertiser.html")

@app.route('/influencer', methods=['POST', 'GET'])
def influencer():
    if request.method == 'POST':
        tumblr_id = request.form['register-form-name']
        email = request.form['register-form-email']

        insert_query("""INSERT INTO influencer (tumblr_id, email)
                        VALUES (?, ?)""",
                      [tumblr_id, email])
    return render_template("influencer.html")
    
@app.route('/post/<int:post_id>')
def post(post_id):
    MAX_POST = select_query("""SELECT MAX(id)
                           FROM posts""",
                           [])[0][0]
    print MAX_POST
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
        tags2 = tags.replace('#',",")
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
        description = []
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
            for j in tmp:
                description.append('%s at %s'%(j[5], j[6]))

        #limit the length of results to be the min_results_length
        for i in xrange(len(segmented_images)):
            results[i] = results[i][:min_results_length]

        #process the description
        if len(description) != 0:
            description = "Shop for " + ", ".join(description) + '.'

        #process tags2
        if len(tags2) > 1:
            tags2 = " - Shopping for " + tags2
        else:
            tags2 = ''

        #create the template filled with data
        return render_template("post.html", id1=post_id - 1,
                               id2=post_id + 1,
                               main_image_url=main_image_url,
                               source_url=source_url,
                               tags=tags,
                               image_name=image_name,
                               segmented_images=segmented_images,
                               results=results,
                               description=description,
                               tags2=tags2)
    elif post_id < 1:
        return redirect(url_for('post', post_id=1))
    else:
        return redirect(url_for('post', post_id=MAX_POST))
    
@app.route('/legal')
def legal():
    return render_template("legal.html")

@app.route('/feedback', methods=['POST', 'GET'])
def feedback():
    if request.method == 'POST':
        name = request.form['template-contactform-name']
        email = request.form['template-contactform-email']
        message = request.form['template-contactform-message']
        
        insert_query("""INSERT INTO feedback
                        (name, email, message)
                        VALUES (?, ?, ?)""",
                      [name, email, message])
        
    return render_template("feedback.html")

@app.route('/api/tfsearch', methods=['POST'])
def api_tfsearch():
    
    if request.method == 'POST':
        image = ''
        if "segmented_image" in request.form:
            image = request.form['segmented_image']
        elif "main_image" in request.form:
            image = request.form['main_image']

        if image:
            response = requests.get(image)
            api_input = {"img64":base64.b64encode(response.content)}
            s = Session()
            req = Request('POST', "http://www.gofindapi.com:3000/searchapi",
                          data=json.dumps(api_input), headers={'Content-Type':"application/json"})
            prepped = req.prepare()
            resp = s.send(prepped)
            
            return resp.content

        else:
            return 'Error: no main_image and/or segmented_image!'

@app.route('/tfsearch', methods=['POST', 'GET'])
def tfsearch():
    if request.method == 'POST':
        image = ''
        segmented_image = ''
        main_image = ''
        if "segmented_image" in request.form:
            image = request.form['segmented_image']
        elif "main_image" in request.form:
            image = request.form['main_image']

        main_image = request.form['main_image']
        segmented_image = request.form['segmented_image']

        
        if image:
            response = requests.get(image)
            api_input = {"img64":base64.b64encode(response.content)}
            s = Session()
            req = Request('POST', "http://www.gofindapi.com:3000/searchapi",
                          data=json.dumps(api_input),
                          headers={'Content-Type':"application/json"})
            prepped = req.prepare()
            resp = s.send(prepped)
            
            api_output = json.loads(resp.content)
            if 'data' in api_output:
                return render_template("tfsearch.html",
                                       page_title="TF Search",
                                       main_image_url=main_image,
                                       segmented_image=segmented_image,
                                       results=[api_output['data']])
            else:
                return render_template("tfsearch.html",
                                       page_title="TF Search",
                                       main_image_url=main_image,
                                       segmented_image=segmented_image,
                                       results=[])

        else:
            return 'Error: no main_image and/or segmented_image!'
    else:
        return render_template("tfsearch.html",
                               page_title="TF Search",
                               results=[])
        
@app.route('/post_search', methods=['POST', 'GET'])
def post_search():
    if request.method == 'POST':
        image = ''
        segmented_image = ''
        main_image = ''
        if "segmented_image" in request.form:
            image = request.form['segmented_image']
        elif "main_image" in request.form:
            image = request.form['main_image']

        main_image = request.form['main_image']
        segmented_image = request.form['segmented_image']

        
        if image:
            response = requests.get(image)
            api_input = {"img64":base64.b64encode(response.content)}
            s = Session()
            req = Request('POST', "http://www.gofindapi.com:3000/searchapi",
                          data=json.dumps(api_input), headers={'Content-Type':"application/json"})
            prepped = req.prepare()
            resp = s.send(prepped)
            
            api_output = json.loads(resp.content)
            if 'data' in api_output:
                #insert into database
                post_id = select_query("""SELECT MAX(id)
                           FROM posts""",
                           [])[0][0] + 1
                insert_query("""INSERT INTO posts
                                (id, main_image_url, source_url,
                                tags, image_name)
                                VALUES (?, ?, ?, ?, ?)""",
                             [post_id, main_image, main_image,
                              " ", " "])
                segm_id = select_query("""SELECT MAX(id)
                           FROM segmented""",
                           [])[0][0] + 1
                insert_query("""INSERT INTO segmented
                                (id, segmented_image_url, post_id)
                                VALUES (?, ?, ?)""",
                             [segm_id, segmented_image, post_id])
                for result in api_output['data']:
                    image_url = result['reference_image_links'][0]
                    seller_url = result['url']
                    seller_name = result['seller']
                    item_name = result['itemName']
                    if type(result['price']) == list:
                        price = result['price'][0]
                    else:
                        price = result['price']

                    insert_query("""INSERT INTO results
                                   (segmented_id, image_url, seller_url,
                                   seller_name, item_name, price)
                                   VALUES (?, ?, ?, ?, ?, ?)""",
                                [segm_id, image_url, seller_url,
                                 seller_name, item_name, price])
                
                return redirect(url_for('post', post_id=post_id))
            else:
                return render_template("tfsearch.html",
                                       main_image_url=main_image,
                                       segmented_image=segmented_image,
                                       results=[])

        else:
            return 'Error: no main_image and/or segmented_image!'
    else:
        return render_template("tfsearch.html",
                               page_title="Post Search Result",
                               results=[])    

@app.route('/google9c8e70e78888c82b.html')
def googleVerify():
    return render_template("google9c8e70e78888c82b.html")

@app.route('/sitemap.xml')
def sitemap():
    return render_template("sitemap.xml")

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

