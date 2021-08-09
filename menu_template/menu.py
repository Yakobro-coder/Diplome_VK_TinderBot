import json

menu = {
    "one_time": True,
    "buttons": [
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"1\"}",
                "label": "Для себя!"
            },
            "color": "positive"
        }]
    ]
}


menu = json.dumps(menu, ensure_ascii=False).encode('utf-8')
menu = str(menu.decode('utf-8'))
