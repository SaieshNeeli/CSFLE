from pymongo import MongoClient, ASCENDING

# Updated connection string with retryWrites and w=majority
connection_string = "your_mongodb_connection_string_here"
key_vault_db = "encryption"
key_vault_coll = "__keyVault"
key_vault_namespace = f"{key_vault_db}.{key_vault_coll}"

# Add connection timeout and server selection timeout
client_options = {
    "connectTimeoutMS": 10000,  # 10 seconds
    "serverSelectionTimeoutMS": 5000,  # 5 seconds
    "retryWrites": True,
    "w": "majority"
}

try:
    print("Attempting to connect to MongoDB Atlas...")
    key_vault_client = MongoClient(connection_string, **client_options)
    
    # Test the connection
    key_vault_client.admin.command('ping')
    print("✅ Successfully connected to MongoDB Atlas")
    
    # List all databases (for debugging)
    print("\nAvailable databases:")
    for db in key_vault_client.list_database_names():
        print(f"- {db}")
    
    # Create the key vault collection if it doesn't exist
    if key_vault_db not in key_vault_client.list_database_names():
        print(f"\nCreating database: {key_vault_db}")
        key_vault_client[key_vault_db].create_collection(key_vault_coll)
    
    # Create unique index for keyAltNames
    print(f"\nCreating index on {key_vault_namespace}...")
    key_vault_client[key_vault_db][key_vault_coll].create_index(
        [("keyAltNames", ASCENDING)],
        unique=True,
        partialFilterExpression={"keyAltNames": {"$exists": True}},
    )
    print("✅ Key vault index created successfully")

except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nTroubleshooting steps:")
    print("1. Check your internet connection")
    print("2. Verify the MongoDB Atlas connection string is correct")
    print("3. Ensure your IP is whitelisted in MongoDB Atlas")
    print("4. Try connecting with MongoDB Compass to verify the connection")