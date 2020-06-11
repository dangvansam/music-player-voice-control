from youtube_search import YoutubeSearch 
import json
import random
import string

# results = YoutubeSearch("im lang", max_results=5).to_json()
# results = json.loads(results)
# #print(results)
# results = results["videos"]
# print(results)
# list_title = [e["title"] for e in results]
# print(list_title)

def next_keyword(list_title):
    new_keys = []
    exts = [" ", "nhạc", "cover", "music", "remix"]
    for t in list_title:
        t2 = t.translate(string.punctuation)
        #print(t2.split("-"))
        if "|" in t2:
            for e in t2.split("|"):
                if len(e.split(" ")) > 1:
                    new_keys.append(e.strip())
        else:
            for e in t2.split("-"):
                if len(e.split(" ")) > 1:
                    new_keys.append(e.strip())
    print(new_keys)
    random.shuffle(new_keys)
    print(new_keys)
    next_key = random.choice(exts) + random.choice(new_keys)
    print(next_key)
    return next_key
#next_keyword(list_title)