# 🔐 Client-Side Field Level Encryption (CSFLE) with Local Master Key – MongoDB

This repository demonstrates a **working implementation of MongoDB Client-Side Field Level Encryption (CSFLE)** using a **local master key**.

CSFLE ensures that **sensitive fields are encrypted in the client application itself**, so MongoDB **never sees plaintext data**.

📚 Official MongoDB Documentation:  
👉 https://www.mongodb.com/docs/manual/core/csfle/

---

## 📂 Project Structure

C:
.
│ README.md
│
├── crypt_file/
│ └── mongo_crypt_v1.dll
│
└── csfle_with_local_master_key/
├── automatic_encrypt.py
├── create_key_vault.py
├── create_master_key.py
└── get_dek.py
---

## 🧠 What is CSFLE?

**Client-Side Field Level Encryption (CSFLE)** allows applications to:

- Encrypt sensitive fields **before** sending data to MongoDB
- Decrypt data **only inside the application**
- Prevent database admins, backups, and attackers from seeing plaintext

MongoDB only stores **ciphertext**.

---

## 🔑 Encryption Architecture (Simplified)

Local Master Key (96 bytes)
↓
Encrypts
↓
Data Encryption Key (DEK) → stored in MongoDB key vault
↓
Encrypts
↓
Sensitive document fields


---

## ⚠️ Important Rules

- The **local master key must be exactly 96 bytes**
- **Never regenerate the master key** after data is encrypted
- Losing the master key = **permanent data loss**
- Local master key is best for:
  - Development
  - Proof of Concept
  - Offline systems

---

## 🛠 Prerequisites

- Python 3.9+
- MongoDB 6.0+
- `pymongo` with encryption support
- MongoDB Database Tools
- Windows (for `mongo_crypt_v1.dll`)

### Install Dependencies


pip install pymongo cryptography


📁 crypt_file/ Directory
crypt_file/
└── mongo_crypt_v1.dll

▶️ Execution Order (VERY IMPORTANT)

Run the files exactly in this order:

1️⃣ create_master_key.py (RUN ONCE)

Purpose:

Generates a 96-byte local master key

Saves it to a file (example: master-key.txt)

python create_master_key.py


⚠️ Do NOT rerun this after encrypting data.

2️⃣ create_key_vault.py (RUN ONCE)

Purpose:

Creates the MongoDB key vault collection

Creates the required unique index on keyAltNames

python create_key_vault.py


This script is safe to re-run.

3️⃣ get_dek.py (RUN ONCE PER KEY)

Purpose:

Uses the local master key

Creates a Data Encryption Key (DEK)

Stores the encrypted DEK in MongoDB key vault

Prints or returns the DEK ID / keyAltName

python get_dek.py


📌 You typically create one DEK per data domain (PII, payments, etc.)

4️⃣ automatic_encrypt.py (RUN EVERY TIME)

Purpose:

Enables automatic encryption and decryption

Inserts encrypted data

Reads decrypted data transparently

python automatic_encrypt.py


MongoDB will store encrypted values, but the application will see plaintext.

🔍 How to Verify Encryption

Use a normal MongoDB client (without CSFLE):

from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
print(client.mydb.mycollection.find_one())


You should see encrypted binary values instead of plaintext.

✅ That confirms CSFLE is working.

🔐 Deterministic vs Random Encryption
Encryption Type	Use Case
Deterministic	Equality queries (find, lookup)
Random	Maximum security (no querying)
