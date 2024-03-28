import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class FirestoreClient:
    def __init__(self):
        self.config = 'key.json'
        self.db_client = self.get_client(self.config)

    @staticmethod
    def get_client(config):
        cred = credentials.Certificate(config)
        firebase_admin.initialize_app(cred)
        return firestore.client()


    def get_collection(self, collection_id):
        return self.db_client.collection(collection_id).get()


    def get_document(self, collection_id, document_id):
        return self.db_client.collection(collection_id).document(document_id).get().to_dict()

    def set_document(self, collection_id, document_id, data):
        self.db_client.collection(collection_id).document(document_id).set(data, merge=True)


# db = FirestoreClient()
# to_wright = {
#     'lesson': 'math'
# }
# db.set_document('Person', 'teacher', to_wright)
# data = db.get_document('Person', 'Students')
#  for i in data:
#     print(i)