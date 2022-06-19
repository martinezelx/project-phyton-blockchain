# Blockchain project in python whit proof of work consensous.

## Tech stack
- IDE: PyCharm 2022.1.2 (Community Edition)
- Python 3.10
- Python packages 
     - datetime
     - hashlib
     - json
     - requests
     - uuid
     - flask
     - urllib.parse
     - flask_ngrok

## Prerequisites to test/run the application
- Python 3.10 env

## Packages explanation
- datetime: The datetime module provides classes to manipulate dates and times. Although the implementation allows arithmetic operations with dates and times, its main objective is to be able to extract fields efficiently for later manipulation or formatting.

- hashlib: This module implements a common interface to different hashing algorithms and secure message digests. Included are the FIPS secure hashing algorithms SHA1, SHA224, SHA226, SHA384, and SHA512 (defined in FIPS 180-2) as well as the RSA MD5 algorithm (defined in Internet RFC 1321). The terms "secure hash" and "message digest" are interchangeable. The oldest algorithms were called message digests. The modern term is secure hash.

- json: JSON stands for JavaScript Object Notation. JSON is a lightweight data format used for data exchange between several different languages. It is easy for humans to read and easily parsed by machines.

- flask: Flask is a micro web framework written in Python. It is classified as a microframework because it does not require any particular tools or libraries. It has no database abstraction layer, form validation, or any other components where pre-existing third-party libraries provide common functions. However, Flask does support extensions that can add features to your application as if they were implemented in Flask itself. There are extensions for object-relational mappers, form validation, payload handling, various open authentication technologies, and various tools related to the common framework.

- flask-ngrok: An easy way to demo Flask applications from your machine. It makes your Flask applications running on localhost available on the Internet through the excellent ngrok tool.

- requests: Requests is an HTTP library for the Python programming language. The goal of the project is to make HTTP requests simpler and more human-friendly. The current version is 2.26.0. Applications are released under the Apache 2.0 License.

- uuid: This module provides immutable UUID objects (the UUID class) and the uuid1(), uuid3(), uuid4(), uuid5() functions to generate version 1, 3, 4 and 5 UUIDs like it is specified in RFC 4122.
If all you want is a unique ID, you should probably call uuid1() or uuid4(). Note that uuid1() can compromise privacy as it creates a UUID that contains the computer's network address. uuid4() creates a random UUID.

- urllib.parse: This module defines a standard interface to split Uniform Resource Locator (URL) strings into components (addressing scheme, network location, path, etc.), to recombine the components into a URL string, and to convert a "relative URL" to an absolute URL given a "base URL". The module has been designed to conform to the Internet RFC on Uniform Relative Resource Locators. Supports the following URL schemes: *file, ftp, gopher, hdl, http, https, imap, mailto, mms, news, nntp, prospero, rsync, rtsp, rtspu, sftp, shttp, sip, sips, snews, svn, svn+ssh, telnet, wait, ws, wss*.

## Run the application
1. Clone the repository
2. In the cloned folder repository, run the following command: ```blockchain.py```
3. Find the direction in python console to execute requests: ```Running on htttp://160a-85-31-131-19.ngrok.io```

## Available endpoints
- GET 
     - /is_valid 
     - /get_chain
     - /mine_block
     - /replace_chain
- POST 
     - /connect_node
     - /add_tx

### Examples to call the endpoints
You can use the HTTP client of your choice to call the endpoints. In the next examples I will use Postman to perform the requests.

#### Check if blockchain is valid
- `GET http://160a-85-31-131-19.ngrok.io/is_valid`
```json
{
    "message": "OK 200 - blockchain is valid :)"
}
```
in case of the endpoint returns a 500 error, the response will be
```json
{
    "message": "ERROR 500 - blockchain not valid :("
}
```

#### Get the actual chain, in firts execution will be mined the genesis block
- `GET http://160a-85-31-131-19.ngrok.io/get_chain`
```json
{
    "chain": [
        {
            "index": 1,
            "previous_hash": "0",
            "proof": 1,
            "timestamp": "2022-06-19 15:11:52.370477",
            "transactions": []
        }
    ],
    "length": 1
}
```

#### Mine block
- `GET http://160a-85-31-131-19.ngrok.io/mine_block`
```json
{
    "index": 2,
    "message": "Congrats for the new block bro!",
    "previous_hash": "456d2e5ec72c986e0f1df55ef56969ea4a187fa0a47e631854bd1e34a47c45fa",
    "proof": 533,
    "timestamp": "2022-06-19 15:20:36.523789",
    "transactions": [
        {
            "amount": 10,
            "receiver": "Martinez",
            "sender": "0fe9adafc8aa4319987156b493cfd2ca"
        }
    ]
}
```

#### Replace the chain if its neccesary
- `GET http://160a-85-31-131-19.ngrok.io/replace_chain`
```json
{
    "actual_chain": [
        {
            "index": 1,
            "previous_hash": "0",
            "proof": 1,
            "timestamp": "2022-06-19 15:11:52.370477",
            "transactions": []
        },
        {
            "index": 2,
            "previous_hash": "456d2e5ec72c986e0f1df55ef56969ea4a187fa0a47e631854bd1e34a47c45fa",
            "proof": 533,
            "timestamp": "2022-06-19 15:20:36.523789",
            "transactions": [
                {
                    "amount": 10,
                    "receiver": "Martinez",
                    "sender": "0fe9adafc8aa4319987156b493cfd2ca"
                }
            ]
        }
    ],
    "message": "All nodes are synchronized, not replaced"
}
```
returns the entire chain and a message for verify if chain is synchronized or not

#### Add nodes to blockchain
- `POST http://160a-85-31-131-19.ngrok.io/connect_node`
```json
{
    "nodes": [
        "http://192.168.1.131:5002",
        "http://192.168.1.131:5003"
    ]
}
```

response:
```json
{
    "message": "Nodes add to blockchain: ['http://160a-85-31-131-20.ngrok.io', 'http://160a-85-31-131-21.ngrok.io']",
    "total_nodes": [
        "160a-85-31-131-20.ngrok.io",
        "160a-85-31-131-21.ngrok.io"
    ]
}
```




