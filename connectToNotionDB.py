from os import times
import requests,json
token = 'secret_t47Ax0NiCcbGVmhHMdF5p2gxtjFEkKAtQtBsAI8hwlh'
databaseID = 'a7420683a5824438b7b33ac87331ccf1'
headers={"Authorization": "Bearer " + token, "Notion-Version": "2021-05-13"}

def getDatabase(token = token,dabaseID = databaseID):
    url = f"https://api.notion.com/v1/databases/{databaseID}/query"#字符串为页面id
    res = requests.request('POST',url=url,headers=headers)
    data = res.json()
    with open('./db.json','w',encoding='utf8') as f:
        json.dump(data,f,ensure_ascii=False)

def postData(title,author,url,des,school,time,token=token,databaseID = databaseID,headers=headers):
    requests.request("POST",
    "https://api.notion.com/v1/pages",
    json={
        "parent": {"type": "database_id", "database_id": databaseID},
        "properties": {
            "url": {"url": url},
            "Title": {"title": [{"type": "text", "text": {"content": title}}]},
            "Describition": {"rich_text": [{"type": "text", "text": {"content": des}}]},
            "Author": {"rich_text": [{"type": "text", "text": {"content": author}}]},
            "School": {"rich_text": [{"type": "text", "text": {"content": school}}]},
            "Time": {"rich_text": [{"type": "text", "text": {"content": time}}]},
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

#
# postData("te43ereqwrw34354534545dfxt","author","https://www.url.com","11dfdfdfdfd1111111111111","school234","time:2021")