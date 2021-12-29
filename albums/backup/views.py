# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import DocumentFile, FavoriteList ,DeletedList
from rest_framework.pagination import PageNumberPagination
from .serializers import DocumentFileSerializer 
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render

# Create your views here.



#Pagination default
paginator = PageNumberPagination()
paginator.page_size = 20



# Class to upload file
class document_upload(APIView):
    permission_classes = [IsAuthenticated] # User has to be logged in 

    def post(self, request):
        form = DocumentFileSerializer(request.POST, request.FILES)
        data ={}

        if form.is_valid(): # Check if is valid in the serializer
            if len(request.FILES.getlist('files')) > 10:
                data["valid"]   = "You uploaded more than one file"
            else:
                for i, f in enumerate(request.FILES.getlist('files')): # For Loop to enable a uploading of multiple files 
                    instance                    = DocumentFile()
                    instance.filename           = str(f)
                    instance.files              = f
                    instance.fileSize           = f.size
                    instance.fileExtension      = str(f).split('.')[-1]
                    instance.filetype           = f.content_type

                    instance.user               = request.user
                    data["error"] = None
                    if instance.fileSize > 1048576*100 :
                        data["error"] = instance.filename+" is more than 500mb"


                    if data["error"] is None:
                        instance.save()
                        print("saved"+instance.filename)

                if data["error"] is None:
                    data["success"]  = "Uploaded sucessfully"
                    print(i+1)

            return Response(data=data)
        return Response(form.errors,status=status.HTTP_400_BAD_REQUEST)


# Class to view all documents uploaded by a particular user
class document_allview(APIView):
    permission_classes = [IsAuthenticated] # User has to be logged in
    def get(self,request):
        context = []
        try:
            instance  = DocumentFile.objects.filter(user=request.user, deleted=False).order_by('-id')
        except:
            data ={}
            data["Error"]     = "Sorry something when wrong"
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        
        #Pagination
        

        for f in instance:           # For Loop to view each file that was uploaded by a user
            data ={}
            data["doc_id"] = str(f.doc_id)
            data["name"]   = str(f.filename)
            data["size"]   = str(f.fileSize)
            data["type"]   = str(f.filetype)
            data["favourites"]= str(f.favourite)
            data["url"]= str(f.files)
            context.append(data)

        context = paginator.paginate_queryset(context, request)
        return paginator.get_paginated_response(context)



# Class to view a particular document , specified using the document doc_id 
class document_singleview(APIView):
    permission_classes = [IsAuthenticated] # User has to be logged in
    def get(self,request,documentid):
        data ={}
        try:
            instance    = DocumentFile.objects.get(doc_id=documentid)
        except:
            data ={}
            data["Error"]     = "Sorry something when wrong"
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        
        data["doc_id"]     = str(instance.doc_id)
        data["URL"]        = str(instance.files)
        data["name"]       = str(instance.filename)
        data["size"]       = str(instance.fileSize)
        data["time"]       = str(instance.time)
        data["extention"]  = str(instance.fileExtension)
        data["type"]       = str(instance.filetype)
        data["favourites"] = str(instance.favourite)

        data["success"]         = "Successfully Viewed document"
        return Response(data=data)



# Class to delete a particular document , specified using the document doc_id 
# Class to also restore a particular document , specified using the document doc_id if file has been deleted before
# Documents are not actually deleted but are added to DeletedList Model and deleted field in DocmentFile will be set to True
class document_delete(APIView):
    permission_classes = [IsAuthenticated] # User has to be logged in
    def post(self, request):
        data ={}
        documentid          = request.POST['doc_id']
        try:
            document            = DocumentFile.objects.get(doc_id=documentid, user=request.user)
        except:
            data ={}
            data["Error"]     = "Sorry something when wrong"
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        if DeletedList.objects.filter(files=document).exists()==True: # Checking if File is has already been deleted (if the file exist in the deletedList table) 
            instance            = DeletedList.objects.get(files=document)
            document.deleted       = False #    Setting Deleted field in DocumentFile to False
            instance.delete() # Removing document from deleteList

            document.save()
            data["success"]     = "Successfully removed document from your deleted list"
            return Response(data=data)
        else: # if Document has not been deleted before

            document.deleted    = True #    Setting Deleted field in DocumentFile to True
            document.save()

            instanceDelete = DeletedList()
            instanceDelete.files    = document
            instanceDelete.user     = request.user
            instanceDelete.filetype = document.filetype
            instanceDelete.save()


            if FavoriteList.objects.filter(files=document).exists()==True: # Checking if the document that is to be deleted exist in the favoriteList
                instanceFav            = FavoriteList.objects.get(files=document)
                instanceFav.delete() #    Delete the document from favouriteList 
                data["success"]     = "Successfully Deleted document and removed from favourites"
                return Response(data=data)

            data["success"]     = "Successfully Deleted document "
            return Response(data=data)
    


# Class to Favourite a particular document , specified using the document doc_id  
# Class to also Unfavourite a particular document , specified using the document doc_id if file has been favourited before
class document_fav(APIView):
    permission_classes = [IsAuthenticated] # User has to be logged in
    def post(self, request):
        data ={}
        documentid          = request.POST['doc_id']
        try:
            fav             = DocumentFile.objects.get(doc_id=documentid, user=request.user, deleted=False)
        except:
            data ={}
            data["Error"]   = "Sorry something when wrong"
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        if FavoriteList.objects.filter(files=fav).exists()==True: # Checking if File is has already been favourited (if the file exist in the FavouriteList table) 

            instance            = FavoriteList.objects.get(files=fav)
            fav.favourite       = False #    Setting Favourite field in DocumentFile to False
            instance.delete() # Removing document from FavouriteList

            fav.save()
            data["success"]     = "Successfully removed document from your favourite"
            return Response(data=data)
        else:   # if Document has not been favourited before
            instance            = FavoriteList()
            instance.user       = request.user
            instance.files      = fav
            instance.filetype   = fav.filetype
            fav.favourite       = True
            instance.save()
            fav.save()
            data["success"]     = "Successfully made document your favourite"
            return Response(data=data)



# Class to view all favourited documents ,favourited by a particular user
class document_allview_favourites(APIView):
    permission_classes = [IsAuthenticated] # User has to be logged in
    def get(self,request):
        context = []
        try:
            instance  = FavoriteList.objects.filter(user=request.user).order_by('-id')
        except:
            data ={}
            data["Error"]   = "Sorry something when wrong"
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        for f in instance: # For Loop to view each file that was favourited by a user
            data = {}
            data["doc_id"]  = str(f.files.doc_id)
            data["name"]   = str(f.files.filename)
            data["size"]   = str(f.files.fileSize)
            data["type"]   = str(f.files.filetype)
            data["favourites"]= str(f.files.favourite)
            context.append(data)     

        context = paginator.paginate_queryset(context, request)
        return paginator.get_paginated_response(context)



# Class to view all Deleted documents ,Deleted by a particular user
class document_allview_deleted(APIView):
    permission_classes = [IsAuthenticated] # User has to be logged in
    def get(self,request):
        context = []
        try:
            instance  = DeletedList.objects.filter(user=request.user).order_by('-id')
        except:
            data ={}
            data["Error"]   = "Sorry something when wrong"
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        for f in instance: # For Loop to view each file that was Deleted by a user
            data = {}
            data["doc_id"]  = str(f.files.doc_id)
            data["name"]   = str(f.files.filename)
            data["size"]   = str(f.files.fileSize)
            data["type"]   = str(f.files.filetype)
            data["favourites"]= str(f.files.favourite)
            context.append(data)                
            
        context = paginator.paginate_queryset(context, request)
        return paginator.get_paginated_response(context)