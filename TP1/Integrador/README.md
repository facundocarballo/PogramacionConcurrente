# Dangerous Cipher

At the University, we have worked with synchronization and communication mechanisms of process to creates programs with concurrency.

We had the freedom to choose our own project, as long as we applied some synchronization and communication mechanisms.

We decided to create an Encryptor/Decryptor app using only a key.

Using the AES algorithm, we develop a CLI app that allows you to encrypt and decrypt files using a key.

## How it works?
![Dangerous Cipher Diagram](https://i.ibb.co/80RQLf6/Dangerous-Cipher.png)

The server is running on the background waiting for some client request.

### Encrypt Process
When the client request for **encrypt** a folder, the server will iterate all the folder looking for subfolders inside of it. If the main folder have subfolders there, the server will launch a thread for each subfolder finded, with the same function (some recursive technique).

Everytime the function find a file, will encrypt that file and will update the cipher file, where will be all the cipher text of all those files encrypted.

### Decrypt Process
When the client request for **decrypt** a file, the server will open the cipher file and will try to recover it with the key that the user provides to the server.

Here the server use only one thread to make this request.

## Where is implemented?
📁 folder
> This folder is an example folder for encrypt and decrypt some data.

📄 client.py
> This file contains all the code to run a client to encrypt or decrypt data.

📄 M5.ipynb
> Description of all project (in Spanish), how it's works and how run it. With examples.

📄 server.py
> This file contains all the code to run a server who will be the responsible to handle the decryption and encryption of the files.