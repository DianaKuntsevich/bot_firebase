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


    def get_collection(self, collection_id): # получить коллекцию
        return [doc.to_dict() for doc in self.db_client.collection(collection_id).get()]


    def get_document(self, collection_id, document_id):  #получить документ
        return self.db_client.collection(collection_id).document(document_id).get().to_dict()

    def set_document(self, collection_id, document_id, data): # добавить запись
        self.db_client.collection(collection_id).document(document_id).set(data, merge=True)


db = FirestoreClient()
# data = db.get_collection('keyboard_name')
# for i in data:
#     print(i.to_dict())




# db = FirestoreClient()
# to_wright = {
#     "keyboard_name": "engine"
# }
# db.set_document('keyboard_name', 'engine', to_wright)