from os import times
import requests,json
token = 'secret_t47Ax0NiCcbGVmhHMdF5p2gxtjFEkKAtQtBsAI8hwlh'
databaseID = '968d78a76a24476c9d7d0de83a1d38df'
headers={"Authorization": "Bearer " + token, "Notion-Version": "2021-05-13"}

def getDatabase(token = token,dabaseID = databaseID):
    url = f"https://api.notion.com/v1/databases/{databaseID}/query"#字符串为页面id
    res = requests.request('POST',url=url,headers=headers)
    data = res.json()
    with open('./db.json','w',encoding='utf8') as f:
        json.dump(data,f,ensure_ascii=False)

def postData(title,author,url,des,token=token,databaseID = databaseID,headers=headers):
    requests.request("POST",
    "https://api.notion.com/v1/pages",
    json={
        "parent": {"type": "database_id", "database_id": databaseID},
        "properties": {
            "url": {"url": url},
            "Title": {"title": [{"type": "text", "text": {"content": title}}]},
            "Describition": {"rich_text": [{"type": "text", "text": {"content": des}}]},
            "Author": {"rich_text": [{"type": "text", "text": {"content": author}}]},

            #"url": {"rich_text": [{"type": "url", "url": {"content": url}}]},
        },
        "children": [
            {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "text": [{"type": "text", "text": {"content": des}}],
            }
            }
        ]
    },
    headers={"Authorization": "Bearer " + token, "Notion-Version": "2021-05-13"},
    )

#getDatabase()


postData("testxt","safdsfdsaf","https://www.url.com","111111111111111")