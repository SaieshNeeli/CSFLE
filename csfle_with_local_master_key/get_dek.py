import base64
from bson.codec_options import CodecOptions
from bson.binary import STANDARD
from pymongo import MongoClient
from pymongo.encryption import ClientEncryption

# --- your MongoDB connection string ---
connection_string = "your_mongodb_connection_string_here"

# --- read your local master key ---
path = "./master-key.txt" # path to your local master key file
with open(path, "rb") as f:
    local_master_key = f.read()

# --- define KMS provider ---
kms_providers = {"local": {"key": local_master_key}}

# --- define key vault namespace ---
key_vault_namespace = "encryption.__keyVault"

# --- connect to MongoDB ---
client = MongoClient(connection_string)

# --- create ClientEncryption object ---
client_encryption = ClientEncryption(
    kms_providers,
    key_vault_namespace,
    client,
    CodecOptions(uuid_representation=STANDARD),
)

# --- create a Data Encryption Key ---
data_key_id = client_encryption.create_data_key("local", key_alt_names=["demo-data-key"])
base_64_data_key_id = base64.b64encode(data_key_id)
print("DataKeyId [base64]:", base_64_data_key_id.decode())
