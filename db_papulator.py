import sqlite3
import json

# connect to database
conn = sqlite3.connect('main_images.db')
cur = conn.cursor()

with open("outfitidentifier.json", 'r') as f:
    data = json.load(f)
    for i in data:
        cur.execute("""INSERT INTO main_images
                       (main_image_url, source_url)
                       VALUES (?,?)""",
                    [i['main_image_url'], i['source_link']])


conn.commit()
conn.close()
