import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
from flask_restful import Resource,reqparse 
import uuid

cred=credentials.Certificate("./serviceAccountKey.json")
admin = firebase_admin.initialize_app(cred)
admin2 = firebase_admin.initialize_app(cred, name='covidweb')
        
class FCMService(Resource):
    def __init__(self):
        self.fcm=FCMPush()

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, location='args')
        args = parser.parse_args()
        token=args.token
        return self.fcm.subscribe(token)


class FCMPush():
    cred = credentials.Certificate("./serviceAccountKey.json")
    tokens={}
    topic='topic'
    
    def __init__(self):
        pass

    def subscribe(self, token):
        id=uuid.uuid4().hex
        self.tokens[id] = token
        messaging.subscribe_to_topic(token, self.topic)
        return {
            'id': id
        }

    def pushNotifyNewUpdate(self):
        try:
            message = messaging.Message(
                data={
                    'title': 'Cập nhật mới từ COVID19',
                    'mesage': 'Số lượng người nhiễm đã được cập nhật. Vui lòng truy cập app để xem chi tiết',
                   'action': 'notification',
                   'content': 'NEW_UPDATE'
                },
                topic=self.topic,
            )
            response = messaging.send(message)
            print('Successfully sent message:', response)
            return {
                'isOk': True
            }
        except Exception as e:
            print(e)
            return {
                'isOk': False
            }
