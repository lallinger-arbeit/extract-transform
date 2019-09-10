import os, uuid, sys

from flask import Flask
from flask import request
from azure.storage.blob import BlockBlobService, PublicAccess

app = Flask(__name__)


def extract_transform(data):
    user=os.environ['STORAGE_USERNAME']
    password=os.environ['STORAGE_PASSWORD']
    container_name ='landingzone'
    
    block_blob_service = BlockBlobService(account_name=user, account_key=password)

    blobname =data["name"]+"_" + str(uuid.uuid4()) + ".csv"
    csv=data["name"]+","+str(data["count"])+","+data["meta"]
    block_blob_service.create_blob_from_text(container_name, blobname, csv)

    return "Uploaded blob "+blobname+" to landing zone\n"


@app.route('/', methods=['PUT','POST'])
def receive():
    return extract_transform(request.get_json())

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(8080))