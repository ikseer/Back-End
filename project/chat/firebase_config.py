import base64
import json

import firebase_admin
from decouple import config
from firebase_admin import credentials

firebase_adminsdk_json = base64.b64decode(config('FIREBASE_ADMINSDK_JSON'))
firebase_adminsdk_dict = json.loads(firebase_adminsdk_json)


cred = credentials.Certificate(firebase_adminsdk_dict)
firebase_admin.initialize_app(cred)
