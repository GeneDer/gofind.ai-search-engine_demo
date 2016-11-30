import sqlite3
import json

# connect to database
conn = sqlite3.connect('search_engine_demo.db')
cur = conn.cursor()

with open("FIN_JSON_celebrity.json", 'r') as f:
    data = json.load(f)

    count = 1
    for post in data["data"]:
        if len(post['search_result']) != 0:
            any_result_inserted = False
            for result in post['search_result']:
                any_field_empty = False
                for i in result:
                    if not result[i]:
                        any_field_empty = True
                        break

                
                cur.execute("""INSERT INTO results
                               (post_id, image_url, seller_url,
                               seller_name, item_name, price)
                               VALUES (?, ?, ?, ?, ?, ?)""",
                            [count, post['look']['image'], post['look']['url']])
                
            cur.execute("""INSERT INTO posts
                           (id, main_image_url, source_url)
                           VALUES (?,?)""",
                        [count, post['look']['image'], post['look']['url']])
            
            


conn.commit()
conn.close()
