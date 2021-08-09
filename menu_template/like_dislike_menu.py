import json

like_dis_menu = {
    "one_time": True,
    "buttons": [
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"1\"}",
                "label": "Like!"
            },
            "color": "positive"
        },
        {
            "action": {
                "type": "text",
                "payload": "{\"button\": \"2\"}",
                "label": "Dislike!"
            },
            "color": "negative"
        }
        ],
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"1\"}",
                "label": "Заново"
            },
            "color": "primary"
        }]
    ]
}


like_dis_menu = json.dumps(like_dis_menu, ensure_ascii=False).encode('utf-8')
like_dis_menu = str(like_dis_menu.decode('utf-8'))
