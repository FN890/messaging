### Install

Environment used: Ubuntu 22.04.4 LTS.

```
cd messaging

python3 -m venv env
source env/bin/activate

pip install -r requirements.txt

python manage.py runserver

```

### Admin Page

On the admin page users and messages can be viewed and modified without using curl.

username: admin
password admin
url: http://127.0.0.1:8000/admin/

### Get users.
```
curl -X GET "http://127.0.0.1:8000/api/v1/get-users/"
```

### Post user.
```
curl -X POST "http://127.0.0.1:8000/api/v1/post-users/" -H "Content-Type: application/json" -d '{"username": "<user_name>"}'
```

### Delete user. Note: will delete all sent and received messages.
```
curl -X DELETE "http://127.0.0.1:8000/api/v1/delete-users/?user_id=<user_id>"
```

### Get new messages by last upate. Example last_update: 2024-04-21T11:43:09.335413Z (Coordinated Universal Time)
```
curl -X GET "http://127.0.0.1:8000/api/v1/get-messages/<user_id>/<last_update>/"
```

### Get messages by indices.
```
curl -X GET "http://127.0.0.1:8000/api/v1/get-messages/<user_id>/<start_index>/<end_index>/"
```

### Post message. Note: Both the sender and recipient must exist.
```
curl -X POST "http://127.0.0.1:8000/api/v1/post-message/" -H "Content-Type: application/json" -d '{"sender": <user_id>, "recipient": <user_id>, "message": "This is a message."}'
```

### Delete one or several messages.
```
curl -X DELETE "http://127.0.0.1:8000/api/v1/delete-messages/?message_ids=1&message_ids=<message_id>&message_ids=<message_id>"
```
