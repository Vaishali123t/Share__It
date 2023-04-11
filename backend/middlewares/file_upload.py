from werkzeug.utils import secure_filename
import os
import uuid


MIME_TYPE_MAP={
'image/png':'png',
'image/jpeg':'jpeg',
'image/jpg':'jpg',
}


def allowed_file(filename):
    ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def fileUpload(file,filename):
    if file and allowed_file(filename):
        # filename = secure_filename(file.filename)
        extension=filename.rsplit('.', 1)[1].lower()
        file_uuid=str(uuid.uuid4())+'.'+extension
        file.save(os.path.join('uploads\images',file_uuid ))
        print(f'file named {file_uuid} saved')
        return True,file_uuid
        # return redirect(url_for('download_file', name=filename))
    else:
        return False,''

