from pymongo import MongoClient
from pymongo.encryption_options import AutoEncryptionOpts
from bson.binary import Binary, UUID_SUBTYPE
import base64

MONGO_URI = "youtr_mongodb_connection_string_here"
KEY_VAULT_NAMESPACE = "encryption.__keyVault"

CRYPT_SHARED_LIB_PATH = r"crypt_file\mongo_crypt_v1.dll" # Update with your actual path

with open("master-key.txt", "rb") as f:
    local_master_key = f.read()

kms_providers = {"local": {"key": local_master_key}}

dek_base64 = "......" # Replace with your actual base64 DEK string
data_key_id = Binary(base64.b64decode(dek_base64), UUID_SUBTYPE)



patient_schema = {
    f"{PATIENT_DB}.{PATIENT_COLL}": {
        "bsonType": "object",
        "encryptMetadata": {
            "keyId": [data_key_id],
        },
        "properties": {
            "ssn": {
                "encrypt": {
                    "bsonType": "string",
                    "algorithm": "AEAD_AES_256_CBC_HMAC_SHA_512-Random"
                }
            },
            "email": {
                "encrypt": {
                    "bsonType": "string",
                    "algorithm": "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic"
                }
            }
        }
    }
}


extra_options = {"crypt_shared_lib_path": CRYPT_SHARED_LIB_PATH}

fle_opts = AutoEncryptionOpts(
    kms_providers=kms_providers,
    key_vault_namespace=KEY_VAULT_NAMESPACE,
    schema_map=patient_schema,
    **extra_options
)

secure_client = MongoClient(MONGO_URI, auto_encryption_opts=fle_opts)
patient_coll = secure_client["db"]["collection"]

test_doc = {"ssn": "123-45-6789", "email": "test@example.com", "name": "Prakash1"}
patient_coll.insert_one(test_doc)


regular_client = MongoClient(MONGO_URI)
print("\n Stored in DB (encrypted):")
print(regular_client["db"]["collection"].find_one({"_id": "P001"}))



print("\n Decrypted with secure client:")
print(patient_coll.find_one({"_id": "P001"}))


