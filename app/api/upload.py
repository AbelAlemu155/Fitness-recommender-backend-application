from datetime import datetime

from flask import request, jsonify, g
import base64

from app import db
from app.api import api
import uuid
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

from app.models import Post


@api.route('/createpost',methods=['POST'])
def create_post():
    title=request.get_json().get('title')
    body=request.get_json().get('body')
    bytes=request.get_json().get('bytes')
    id=None
    if len(bytes)!=0:
        id=upload_image(bytes)
    post=Post(title=title, body=body,image_url=id)

    post.author = g.current_user
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json())

#str2 is the List<int> for binary image
def upload_image(str2):

    unique_path = str(uuid.uuid4())
    unique_name=str(uuid.uuid4())

    converted_string = base64.b64encode(bytearray(str2))


    with open(unique_path+'.bin', "wb") as file:
        file.write(converted_string)



    file = open(unique_path+'.bin', 'rb')
    byte = file.read()
    file.close()

    decodeit = open(unique_name+'.jpeg', 'wb')
    decodeit.write(base64.b64decode((byte)))
    decodeit.close()
    f = drive.CreateFile({'title': str(datetime.now()),'parents': [{'id': '1e4gWQ80qsHj3_DYV4Nr6tkPj95rki5dj'}]})
    f.SetContentFile(decodeit.name)
    f.Upload()
    id=f['id']

    f = None
    return id




