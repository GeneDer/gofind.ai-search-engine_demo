import sqlite3
import json
import urllib2

# connect to database
conn = sqlite3.connect('search_engine_demo.db')
cur = conn.cursor()

post_count = 1
segm_count = 1



with open("FIN_JSON_tumblr_celebrity.json", 'r') as f, \
     open("err_tumblr_celebrity.json", 'w') as o:
    data = json.load(f)
    
    for post in data["data"]:
        if len(post['segmented']) != len(post['search_result']):
            o.write(str(post)+'\n')
            continue

        main_image_url = post['image_url']
        source_url = post['blog_url']
        if len(post['tags']) > 0:
            tags = "#" + " #".join(post['tags'])
        else:
            tag = ' '
        image_name = post['blog_name']

        cur.execute("""INSERT INTO posts
                       (id, main_image_url, source_url,
                       tags, image_name)
                       VALUES (?, ?, ?, ?, ?)""",
                    [post_count, main_image_url, source_url,
                     tags, image_name])
            
        for i in xrange(len(post['segmented'])):
            cur.execute("""INSERT INTO segmented
                       (id, segmented_image_url, post_id)
                       VALUES (?, ?, ?)""",
                    [segm_count, post['segmented'][i], post_count])
            
            for result in post['search_result'][i]:
                image_url = result['reference_image_links'][0]
                seller_url = result['url']
                seller_name = result['seller']
                item_name = result['itemName']
                if type(result['price']) == list:
                    price = result['price'][0]
                else:
                    price = result['price']
                
                cur.execute("""INSERT INTO results
                               (segmented_id, image_url, seller_url,
                               seller_name, item_name, price)
                               VALUES (?, ?, ?, ?, ?, ?)""",
                            [segm_count, image_url, seller_url,
                             seller_name, item_name, price])

            segm_count += 1
        post_count += 1

with open("FIN_JSON_tumblr.json", 'r') as f, \
     open("err_tumblr.json", 'w') as o:
    data = json.load(f)
    
    for post in data["data"]:
        if len(post['segmented']) != len(post['search_result']):
            o.write(str(post)+'\n')
            continue

        main_image_url = post['image_url']
        source_url = urllib2.unquote(post['blog_url'])
        if len(post['tags']) > 0:
            tags = "#" + " #".join(post['tags'])
        else:
            tag = ' '
        image_name = post['blog_name_url']

        cur.execute("""INSERT INTO posts
                       (id, main_image_url, source_url,
                       tags, image_name)
                       VALUES (?, ?, ?, ?, ?)""",
                    [post_count, main_image_url, source_url,
                     tags, image_name])
            
        for i in xrange(len(post['segmented'])):
            cur.execute("""INSERT INTO segmented
                       (id, segmented_image_url, post_id)
                       VALUES (?, ?, ?)""",
                    [segm_count, post['segmented'][i], post_count])
            
            for result in post['search_result'][i]:
                image_url = result['reference_image_links'][0]
                seller_url = result['url']
                seller_name = result['seller']
                item_name = result['itemName']
                if type(result['price']) == list:
                    price = result['price'][0]
                else:
                    price = result['price']
                
                cur.execute("""INSERT INTO results
                               (segmented_id, image_url, seller_url,
                               seller_name, item_name, price)
                               VALUES (?, ?, ?, ?, ?, ?)""",
                            [segm_count, image_url, seller_url,
                             seller_name, item_name, price])

            segm_count += 1
        post_count += 1


conn.commit()
conn.close()
print "total post:", post_count
print "total segm:", segm_count
