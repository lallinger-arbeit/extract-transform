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

    local_path=os.path.expanduser("~/tmp")
    local_file_name =data["name"]+"_" + str(uuid.uuid4()) + ".csv"
    full_path_to_file =os.path.join(local_path, local_file_name)

    csv=data["name"]+","+str(data["count"])+","+data["meta"]
    f = open(full_path_to_file,  'w')
    f.write(csv)
    f.close()

    block_blob_service.create_blob_from_path(container_name, local_file_name, full_path_to_file)
    os.remove(full_path_to_file)
    return "Uploaded blob "+local_file_name+" to landing zone\n"


@app.route('/', methods=['PUT','POST'])
def receive():
    return extract_transform(request.get_json())

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(8080))