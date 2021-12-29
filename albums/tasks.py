from __future__ import absolute_import,unicode_literals
from .models import DocumentFile
from familyalbum.celery import app

@app.task(name='upload_document', bind=True)
def upload_document(self,request,f,folder,inshared,userid,associd):
    try:
        instance = DocumentFile()
        instance.filename           = str(f)
        instance.files              = f
            
        instance.folder             = folder
        instance.fileSize           = f.size
        instance.fileExtension      = str(f).split('.')[-1]
        instance.filetype           = f.content_type

        instance.inshared           = inshared
        instance.user               = userid
        instance.assoc_id           = associd
        
        if f.content_type[:5] =="image":
            instance.display_image.save(str(f),f) 
        
        if self.temp_doc_id != "":
            instance.temp_doc_id        = self.temp_doc_id
            instance.Uploaded_from      ="INBOX"
        instance.save()
    except:
        pass