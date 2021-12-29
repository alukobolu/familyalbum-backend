# Create your views here.
from typing_extensions import IntVar
from django.db.models.query_utils import Q
from django.http.response import HttpResponse
from accounts.models import Account
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Files, Albums ,DeletedList,FavoriteList
from rest_framework.pagination import PageNumberPagination
from .serializers import FilesSerializer,AlbumSerializer,RenameAlbumSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
# Create your views here.


#Pagination default
paginator = PageNumberPagination()
paginator.page_size = 20


def try_and_catch(function):
    def wrap(self,request, *args, **kwargs):
        try:
            return function(self,request, *args, **kwargs)
        except:
            data ={}
            data["Error"]     = "Sorry something went wrong"
            return Response(data=data)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def album_access_validation(request,instance):
    if instance.blacklist == True:
        validation = False
        message = f"{instance.name} is Locked at the moment"
        return validation,message 
    else:
        members = instance.members.all()
        if request.user in members:
            if instance.deleted == True:
                validation = False
                message = f"{instance.name} is Deleted"
            else:
                validation = True
                message = "Good to go"
            return validation,message 
        else:
            validation = False
            message = f"No access to {instance.name}"
            return validation,message 

class file_upload(APIView):
    permission_classes = [IsAuthenticated] # User has to be logged in 
    userid  = None

    def getting_album(self,albumids,request):
        valid_albums = []
        messages = []
        self.userid = request.user
        if albumids =="":
            return True,valid_albums
        for albumid in albumids:
            album = Albums.objects.get(album_id=albumid)
            validation,message = album_access_validation(request,album)
            if validation == True:
                valid_albums.append(album)
            else:
                messages.append(message)

        if valid_albums == []:
            return False,message
        else:
            return True,valid_albums

    def upload_function(self,request,albums,searchtags):
        data={}
        form = FilesSerializer(request.POST, request.FILES)
        if form.is_valid():
            filemax = 50
            sizemax = 500
            if len(request.FILES.getlist('files')) > filemax:
                data["Error"]   = "You uploaded too much files"
            else:
                for f in request.FILES.getlist('file') : # For Loop to enable a uploading of multiple files 
                    instance                    = Files()
                    instance.filename           = str(f)
                    instance.file               = f     
                        
                    instance.fileSize           = f.size
                    instance.fileExtension      = str(f).split('.')[-1]
                    instance.filetype           = f.content_type
                    instance.user               = self.userid
                    instance.search_tag         = searchtags

                    instance.save()

                    if albums !=[]:
                        for album in albums: 
                            instance.album.add(album)     

                    data["error"] = None
                    if instance.fileSize > sizemax*1048576 :
                        data["error"] = instance.filename+" is too large"
                   
                    if data["error"] is None:
                        instance.save()

                if data["error"] is None:
                    data["success"]  = "Uploaded sucessfully"
                       
            return data
        return form.errors
    @try_and_catch
    def post(self, request):
        album_id_list  = request.POST['album']
        album_ids = album_id_list.split(",")
        searchtags = request.POST['searchtags']
    
        validation,result = self.getting_album(album_ids,request)  
        if validation ==False:
            data ={}
            data["Error"] = result
            return Response(data=data)
        else:
            data = self.upload_function(request,result,searchtags)
            return Response(data=data)
        
# Class to view all documents uploaded by a particular user
class view_all_files(APIView):
    permission_classes = [IsAuthenticated] # User has to be logged in
    context = []

    def get_all_items(self,instance):
        for f in instance:
            data ={} 
            data["file_id"]   = str(f.file_id)
            data["name"]      = str(f.filename)
            data["size"]      = str(f.fileSize)
            data["type"]      = str(f.filetype)   
            data["searchtag"] = str(f.search_tag) 
            data["favourites"]= f.favourite
            data["URL"]        = f.file.url
            self.context.append(data)

    #@try_and_catch
    def get(self,request,albumid):
        self.context = []
         
        album = Albums.objects.get(album_id=albumid)
        validation,message = album_access_validation(request,album)
        if validation == True:
            instance  = Files.objects.filter(deleted=False, album=album).distinct().order_by('-date_posted')
        else:
            data ={}
            data["Error"]     = message
            return Response(data=data)
        
        self.get_all_items(instance)
        
        context = paginator.paginate_queryset(self.context, request)
        page_response = paginator.get_paginated_response(context)
        return page_response

# Class to view a particular document , specified using the document doc_id 
class view_one_file(APIView):
    #permission_classes = [IsAuthenticated] # User has to be logged in
    @try_and_catch
    def get(self,request,fileid):
        data ={}
        instance    = Files.objects.get(file_id=fileid)
        album    = Albums.objects.get(album_id=instance.album.album_id)
        validation,message = album_access_validation(request,album)
        if validation == True:
            
            data["file_id"]    = str(instance.file_id)
            data["name"]       = str(instance.filename)
            data["size"]       = str(instance.fileSize)
            data["time"]       = instance.time
            data["extention"]  = str(instance.fileExtension)
            data["type"]       = str(instance.filetype)
            data["favourites"] = instance.favourite
            data["deleted"]    = instance.deleted
            data["URL"]        = instance.files.url
        else:
            data["Error"]      = message
        return Response(data=data)

# Class to delete a particular document , specified using the document doc_id 
# Class to also restore a particular document , specified using the document doc_id if file has been deleted before
# Documents are not actually deleted but are added to DeletedList Model and deleted field in DocmentFile will be set to True
class delete_file(APIView):
    permission_classes = [IsAuthenticated] # User has to be logged in
   
    def remove_from_deleted_list(self,file):
        data={}
        instance            = DeletedList.objects.get(file=file)
        if instance.permanent_delete == False:
            file.deleted       = False #    Setting Deleted field in DocumentFile to False
            instance.delete() # Removing document from deleteList

            file.save()
            data["recovered"]     = "Recovered"
            data["success"]     = "Successfully removed document from your deleted list"
        else:
            data["Error"]     = "This item does not exist"
        return data

    def delete_document(self,request,file):
        data={}
        file.deleted    = True #    Setting Deleted field in DocumentFile to True
        file.save()

        instanceDelete = DeletedList()
        instanceDelete.files    = file
        instanceDelete.user     = request.user
        instanceDelete.filetype = file.filetype
        instanceDelete.save()

        if FavoriteList.objects.filter(files=file).exists()==True: # Checking if the document that is to be deleted exist in the favoriteList
            data = self.remove_from_favourites(file)
        data["deleted"]     = "Deleted"
        data["success"]     = "Successfully Deleted document "
        return data
        
    def remove_from_favourites(self, file):
        data = {}
        instanceFav            = FavoriteList.objects.get(file=file)
        instanceFav.delete() #    Delete the document from favouriteList 
        file.favourite = False
        file.save()
        data["success_fav"]     = "Successfully Deleted document and removed from favourites"
        return data


    @try_and_catch
    def post(self, request):
        data ={}
        fileid          = request.POST['file_id']
        file            = Files.objects.get(doc_id=fileid, user=request.user)

        if DeletedList.objects.filter(file=file).exists()==True: # Checking if File is has already been deleted (if the file exist in the deletedList table) 
            data =   self.remove_from_deleted_list(file)
        else: # if Document has not been deleted before
            data = self.delete_document(request,file)
        return Response(data=data)
        
# Class to Favourite a particular document , specified using the document doc_id  
# Class to also Unfavourite a particular document , specified using the document doc_id if file has been favourited before
class favourite_file(APIView):
    permission_classes = [IsAuthenticated] # User has to be logged in
    def removed_from_favourites_list(self,fav):
        data={}
        instance            = FavoriteList.objects.get(files=fav)
        fav.favourite       = False #    Setting Favourite field in DocumentFile to False
        instance.delete() # Removing document from FavouriteList

        fav.save()
        data["removed"]     = "Removed"
        data["success"]     = "Successfully removed document from your favourite"
        return data

    def favourite_a_document(self,request,fav):
        data={}
        instance            = FavoriteList()
        instance.user       = request.user
        instance.files      = fav
        instance.filetype   = fav.filetype
        fav.favourite       = True
        instance.save()
        fav.save()
        data["added"]     = "Added"
        data["success"]     = "Successfully made document your favourite"
        return data

    @try_and_catch
    def post(self, request):
        data ={}
        fileid          = request.POST['file_id']
        fav             = Files.objects.get(file_id=fileid, user=request.user, deleted=False)
    
        if FavoriteList.objects.filter(files=fav).exists()==True: # Checking if File is has already been favourited (if the file exist in the FavouriteList table) 
            data = self.removed_from_favourites_list(fav)
        else:   # if Document has not been favourited before
            data = self.favourite_a_document(request,fav)
        return Response(data=data)\

# Class to view all favourited documents ,favourited by a particular user
class view_all_favourites(APIView):
    permission_classes = [IsAuthenticated] # User has to be logged in
    context =[]

    def get_all_files(self,instance):
        for f in instance: # For Loop to view each file that was favourited by a user
            if f.file != None:    
                data = {}
                data["file_id"]  = str(f.file.file_id)
                data["name"]   = str(f.file.filename)
                data["size"]   = str(f.file.fileSize)
                data["type"]   = str(f.file.filetype)
                data["favourites"]= f.file.favourite
                data["URL"]        = f.file.file.url
                       
                self.context.append(data) 
    @try_and_catch
    def get(self,request):
        self.context = []
        instance  = FavoriteList.objects.filter(user=request.user).order_by('-id')
        self.get_all_files(instance)
       
        context = paginator.paginate_queryset(self.context, request)
        return paginator.get_paginated_response(context)

# Class to view all Deleted documents ,Deleted by a particular user
class view_all_deleted(APIView):
    permission_classes = [IsAuthenticated] # User has to be logged in
    context = []
    def get_all_deleted_list(self,request,instance):
        for f in instance: # For Loop to view each file that was Deleted by a user
            data = {}
            data["doc_id"]  = str(f.file.file_id)
            data["name"]   = str(f.file.filename)
            data["size"]   = str(f.file.fileSize)
            data["type"]   = str(f.file.filetype)
            data["favourites"]= f.file.favourite
            data["URL"]        = f.file.file.url
            self.context.append(data)       

    def get(self,request):
        self.context = []
        instance  = DeletedList.objects.filter(user=request.user,delete_root=True,permanent_delete=False).order_by('-id')
        self.get_all_deleted_list(request,instance)

        context = paginator.paginate_queryset(self.context, request)
        return paginator.get_paginated_response(context)

class search_file(APIView):
    permission_classes = [IsAuthenticated] # User has to be logged in 
    context = []
    
    def get_files(self,file):
        count = 0
        for f in file:   
            data ={} 
            data["file_id"]  = str(f.file_id)
            data["name"]   = str(f.filename)
            data["size"]   = str(f.fileSize)
            data["type"]   = str(f.filetype)
            data["favourites"]= f.favourite
            data["private"]= f.private
            data['deleted'] = f.deleted
            data["URL"]        = f.files.url
            count = count + 1
            self.context.append(data)

    @try_and_catch
    def post(self,request):
        keys = request.POST['keys']
        albumid = request.POST['albumid']
        album = Albums.objects.filter(album_id=albumid,members=request.user).distinct()
        queries = keys.split(" ")
        self.context = []
        for key in queries: 
            file = Files.objects.filter(Q(album=album),Q(deleted=False),Q(search_tag__icontains=key)|Q(filename__icontains=key)).distinct()
            self.get_files(file)
       
        context = paginator.paginate_queryset(self.context, request)
        return paginator.get_paginated_response(context)

class TestView(APIView):
    def get(self,request,format=None):
        print("Yup it worked")
        return Response("Yh this is going to be dope",status=200)

# Create folder
class create_album(APIView):
    permission_classes = [IsAuthenticated] # User has to be logged in 

    @try_and_catch
    def post(self, request):   
        context = {}     
        name            = request.POST['name']
        description     = request.POST['description']
        members         = request.POST['members']
        private         = request.POST['private']

        special_characters = "/\|*<>?;"
        if any(c in special_characters for c in name):
            context["fail"]  = "Invalid Folder Name "
            return Response(data=context)
        else: 
            form = AlbumSerializer(request.POST, request.FILES)
            if form.is_valid():     
                instance                    = Albums()
                instance.name               = name
                instance.description        = description
                instance.album_image        = request.FILES.get('album_image')
                instance.private            =  private
                instance.user            =  request.user
                instance.save()
                instance.admins.add(request.user)
                edit_members.adding_members(self,members,instance)
                context['success'] ="successful"
                return Response(data=context)
            return form.errors

class edit_members(APIView):
    permission_classes = [IsAuthenticated]
    def adding_members(self,usernames,album):
        usernames = usernames.split(",")
        if usernames !=[]:
            for username in usernames:
                user = Account.objects.get(username=username)
                album.members.add(user)
        album.save()

    def removing_members(self,usernames,album):
        usernames = usernames.split(",")
        if usernames !=[]:
            for username in usernames:
                user = Account.objects.get(username=username)
                album.members.remove(user)
            album.save()
    @try_and_catch
    def post(self,request):
        context ={}
        usernames            = request.POST['members']
        album_id             = request.POST['album_id']

        album =  Albums.objects.filter(album_id=album_id).distinct()
        if request.POST.get('remove'):
            self.removing_members(usernames,album)
        else:
            self.adding_members(usernames,album)
        context["success"]  = "sucessfully"
        return Response(data=context)

class view_all_members(APIView):   
    permission_classes = [IsAuthenticated] # User has to be logged in

    @try_and_catch
    def get(self,request,album_id):

        if Albums.objects.filter(Q(deleted=False),Q(album_id=album_id),Q(members=request.user)).distinct().exists():
            album =  Albums.objects.filter(deleted=False,album_id=album_id).distinct()
            
            data={}
            data['Album_name']  = str(album.name)
            group_members = album.members.all()
            members =[]
            for f in group_members:
                members_details={}
                if Albums.objects.filter(Q(deleted=False),Q(album_id=album_id),Q(admins=f)).distinct().exists():
                    members_details['admin']  = True
                members_details['username']  = str(f.username)
                members_details['fullname']  = str(f.fullname)
                members_details['profile_image'] = f.profile_image.url
                members.append(members_details)
            data['members'] = members
            return Response(data=data)
        else:
            data ={}
            data["Error"]     = "Sorry something went wrong"
            return Response(data=data)

# Class to view all documents uploaded by a particular user
class view_all_albums(APIView):
    permission_classes = [IsAuthenticated] # User has to be logged in
    context = []

    def get_all_albums(self,instance):
        for f in instance:           # For Loop to view each file that was uploaded by a user  
            data ={}  
            data["album_id"] = str(f.album_id)
            data["description"] = str(f.description)
            data["name"]   = str(f.name)
            data["favourite"]       = f.favourite
            data["time"]   = f.date_created
            data['deleted']     = f.deleted
            data["private"]      = f.private
            data["URL"]      = 'C:/Users/Aluko/FamilyAlbum/backend/familyalbum/'+f.album_image.url
            data["number_of_members"] = f.members.count()
            self.context.append(data)
        return 
        
    @try_and_catch
    def get(self,request):
        self.context = []
        instance = Albums.objects.filter(members=request.user, deleted=False).distinct().order_by('-id')
        self.get_all_albums(instance)

        context = paginator.paginate_queryset(self.context, request)
        page_response = paginator.get_paginated_response(context)
        return page_response
    
class rename(APIView):
    permission_classes = [IsAuthenticated] # User has to be logged in 

    @try_and_catch
    def put(self, request,id):
        context = {}  
       
        instance = Albums.objects.filter(album_id=id,deleted=False,admins = request.user).distinct()
        serializer = RenameAlbumSerializer(instance, data=request.data)
                
        if serializer.is_valid():
            serializer.save()
            context['added'] ="successfully renamed folder"
            return Response(data=context)
        else:
            context['error'] ="name is invalid."
            return Response(data=context)
        
class change_privacy(APIView):
    permission_classes = [IsAuthenticated] # User has to be logged in 
   
    @try_and_catch
    def post(self, request):   
        context = {}    

        album_id         = request.POST['album_id']
        instance                = Albums.objects.filter(album_id=album_id,members=request.user).distinct()
        
        if instance.private    == True:
            instance.private     = False   
            context["removed"]  = "Converted to Public"
        else:
            instance.private     = True
            context["added"]  = "Converted to Private"
        instance.save()
        return Response(data=context)
        
class permanent_delete(APIView):
    permission_classes = [IsAuthenticated] # User has to be logged in 
   
    def delete(self,file):
        data={}
        if file.deleted  == True: #    Setting Deleted field in FolderTable to True
            instance            = DeletedList.objects.get(file=file.id)
            instance.permanent_delete = True
            instance.save()
            data["deleted"]     = "Successfully Deleted file"
        return data

    @try_and_catch
    def post(self,request):
        file_id = request.POST['file_id']
        instance = Files.objects.get(file_id = file_id)
        data = self.delete(instance)
        
        return Response(data=data)
        