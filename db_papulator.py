import sqlite3
import json
import random

# connect to database
conn = sqlite3.connect('search_engine_demo.db')
cur = conn.cursor()

##with open("FIN_JSON_celebrity.json", 'r') as f:
##    data = json.load(f)
##
##    count = 1
##    for post in data["data"]:
##        if len(post['search_result']) != 0:
##            any_result_inserted = False
##            for result in post['search_result']:
##                any_field_empty = False
##                for i in result:
##                    if not result[i]:
##                        any_field_empty = True
##                        break
##
##                
##                cur.execute("""INSERT INTO results
##                               (post_id, image_url, seller_url,
##                               seller_name, item_name, price)
##                               VALUES (?, ?, ?, ?, ?, ?)""",
##                            [count, post['look']['image'], post['look']['url']])
##                
##            cur.execute("""INSERT INTO posts
##                           (id, main_image_url, source_url)
##                           VALUES (?,?)""",
##                        [count, post['look']['image'], post['look']['url']])
            

with open("FIN_JSON_tumblr_celebrity.json", 'r') as f:
    data = json.load(f)
    count = 1
    
    for post in data["data"]:

        main_image_url = post['image_url']
        source_url = post['blog_url']
        tags = ",".join(post['tags'])
        Image_name = post['blog_name']

        cur.execute("""INSERT INTO posts
                       (id, main_image_url, source_url,
                       tags, Image_name)
                       VALUES (?, ?, ?, ?, ?)""",
                    [count, main_image_url, source_url,
                     tags, Image_name])
            
        post_result = []
        for results in post['search_result']:
            for result in results:
                post_result.append(result)

        if len(post_result) > 9:
            for i in random.sample(post_result, 9):
                if type(i['reference_image_links']) == list:
                    image_url = i['reference_image_links'][0]
                else:
                    image_url = i['reference_image_links']
                seller_url = i['url']
                seller_name = i['seller']
                item_name = i['itemName']
                if type(i['price']) == list:
                    price = i['price'][0]
                else:
                    price = i['price']
                
                cur.execute("""INSERT INTO results
                               (post_id, image_url, seller_url,
                               seller_name, item_name, price)
                               VALUES (?, ?, ?, ?, ?, ?)""",
                            [count, image_url, seller_url,
                             seller_name, item_name, price])
        else:
            for i in post_result:
                if type(i['reference_image_links']) == list:
                    image_url = i['reference_image_links'][0]
                else:
                    image_url = i['reference_image_links']
                seller_url = i['url']
                seller_name = i['seller']
                item_name = i['itemName']
                if type(i['price']) == list:
                    price = i['price'][0]
                else:
                    price = i['price']
                
                cur.execute("""INSERT INTO results
                               (post_id, image_url, seller_url,
                               seller_name, item_name, price)
                               VALUES (?, ?, ?, ?, ?, ?)""",
                            [count, image_url, seller_url,
                             seller_name, item_name, price])
        count += 1


conn.commit()
conn.close()
