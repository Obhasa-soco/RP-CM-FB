import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class FirebaseDB:
    def __init__(self, service_account_key_path="/home/soco/Projects/Claw_machine_firebase/serviceAccountKey.json"):
        # Initialize Firebase app
        self._initialize_firestore(service_account_key_path)
        # Initialize Firestore database
        self.db = firestore.client()

    def _initialize_firestore(self, service_account_key_path):
        # Path to your Firebase private key JSON file
        cred = credentials.Certificate(service_account_key_path)
        firebase_admin.initialize_app(cred)

    def find_and_delete_by_id(self, collection_name, document_id):
        # Secret Code
        SECRET = os.getenv("THIS_IS_SECRET")
        # Reference the document by ID
        doc_ref = self.db.collection(collection_name).document(document_id)
        
        # Fetch the document
        doc = doc_ref.get()

        if doc.exists and document_id != SECRET:
            # Delete the document
            doc_ref.delete()
            print(f"Document with ID {document_id} has been deleted.")
            return True
        elif doc.exists and document_id == SECRET:
            print("Super User$$")
            return True
        else:
            # print(False)  # Print False if the document does not exist
            return False

    def add_data(self, barcode, status):
        # Collection Name
        COLLECTION = os.getenv("THIS_IS_COLLECTION")
        # Reference to the Firestore collection (you can change the collection name)
        doc_ref = self.db.collection(COLLECTION).document(barcode)

        # Add data to Firestore
        doc_ref.set({
            'Barcode': barcode,
            'Status': status
        })
