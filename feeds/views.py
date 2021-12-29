from django.shortcuts import render
from accounts.models import Account
from rest_framework.response import Response
from rest_framework.views import APIView
from albums.models import Files, Albums 
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from albums.views import try_and_catch,album_access_validation
from .models import Posts,Comments,DeletedFeeds

#Pagination default
paginator = PageNumberPagination()
paginator.page_size = 20


# Create your views here.
class posting(APIView):
    permission_classes = [IsAuthenticated] # User has to be logged in

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


    def posting_function(self,request,albums):
        data={}  
        type = request.POST['type']
        if type != 'TEXT':
            file = Files.objects.get(file_id=request.POST['file'])
        else:
            file = None

        for album in albums:
            instance = Posts()
            instance.user = request.user
            instance.type = type
            instance.album = album
            instance.content_file = file
            instance.content_text = request.POST['text']
            instance.save()
        data["success"]  = "Posted sucessfully"
        return data

    @try_and_catch
    def post(self,request):
        album_id_list  = request.POST['album']
        album_ids = album_id_list.split(",")
        validation,result = self.getting_album(album_ids,request)  
        if validation ==False:
            data ={}
            data["Error"] = result
            return Response(data=data)
        else:
            data = self.posting_function(request,result)
            return Response(data=data)

class commenting(APIView):
    permission_classes = [IsAuthenticated] # User has to be logged in

    @try_and_catch
    def post(self,request):
        post = Posts.objects.get(post_id=request.POST['post'])

        root_id = request.POST['root']
        if root_id != 'none':
            root = Comments.objects.get(comment_id=root_id)
        else:
            root = None

        type = request.POST['type']
        if type != 'TEXT':
            file = Files.objects.get(file_id=request.POST['file'])
        else:
            file = None

        instance = Comments()
        instance.root_id = root
        instance.post = post
        instance.user = request.user
        instance.type = type
        instance.content_file = file
        instance.content_text = request.POST['text']
        instance.save()
        data = {}
        data["success"]  = "Commented sucessfully"
        return Response(data=data)

class view_feed(APIView):
    permission_classes = [IsAuthenticated] # User has to be logged in
    context = []

    def get_all_items(self,instance):
        for f in instance:
            data ={} 
            data["post_id"]   = str(f.post_id)
            data["type"]      = str(f.type)
            if f.type == 'IMAGE':
                data["image"]      = f.content_file.file.url   
            elif f.type == 'AUDIO':
                data["audio"]      = f.content_file.file.url 
            elif  f.type == 'VIDEO':
                data["video"]      = f.content_file.file.url 
            data["text"]      = f.content_text 
            data["date_created"]= f.date_created
            self.context.append(data)

    @try_and_catch
    def get(self,request,albumid):
        self.context = []
         
        album = Albums.objects.get(album_id=albumid)
        validation,message = album_access_validation(request,album)
        if validation == True:
            instance  = Posts.objects.filter(deleted=False, album=album).order_by('-date_created')
        else:
            data ={}
            data["Error"]     = message
            return Response(data=data)
        self.get_all_items(instance)
        
        context = paginator.paginate_queryset(self.context, request)
        page_response = paginator.get_paginated_response(context)
        return page_response

class view_post(APIView):
    permission_classes = [IsAuthenticated] # User has to be logged in

    def get_all_items(self,instance):
        data ={}
        data["post_id"]   = str(instance.post_id)
        data["type"]      = str(instance.type)
        if instance.type == 'IMAGE':
            data["image"]      = instance.content_file.file.url   
        elif instance.type == 'AUDIO':
            data["audio"]      = instance.content_file.file.url 
        elif  instance.type == 'VIDEO':
            data["video"]      = instance.content_file.file.url 
        data["text"]      = instance.content_text 
        data["date_created"]= instance.date_created 
        return data

    @try_and_catch
    def get(self,request,postid):
        data ={}
        instance    = Posts.objects.get(post_id=postid)
        album   = Albums.objects.get(album_id=instance.album.album_id)
        validation,message = album_access_validation(request,album)
        if validation == True:
            data = self.get_all_items(instance)
        else:
            data["Error"]      = message
        return Response(data=data)

class view_comments(APIView):
    permission_classes = [IsAuthenticated] # User has to be logged in
    context = []

    def get_all_items(self,instance):
        for f in instance:
            data ={} 
            data["comment_id"]   = str(f.comment_id)
            if f.root_id != None:
                data["reply_to"]   = str(f.root_id.user.username)
            data["user"]      = str(f.user.username)   
            data["type"]      = str(f.type)
            if f.type == 'IMAGE':
                data["image"]      = f.content_file.file.url   
            elif f.type == 'AUDIO':
                data["audio"]      = f.content_file.file.url 
            elif  f.type == 'VIDEO':
                data["video"]      = f.content_file.file.url 
            data["text"]      = f.content_text 
            data["date_created"]= f.date_created
            self.context.append(data)

    @try_and_catch
    def get(self,request,postid):
        self.context = []
         
        instance    = Posts.objects.get(post_id=postid)
        album   = Albums.objects.get(album_id=instance.album.album_id)
        validation,message = album_access_validation(request,album)
        if validation == True:
            instance1  = Comments.objects.filter(deleted=False, post=instance).order_by('-date_created')
        else:
            data ={}
            data["Error"]     = message
            return Response(data=data)
        self.get_all_items(instance1)
        
        context = paginator.paginate_queryset(self.context, request)
        page_response = paginator.get_paginated_response(context)
        return page_response

class delete_post(APIView):
    permission_classes = [IsAuthenticated] # User has to be logged in

    def delete(self,request,post):
        data={}
        post.deleted    = True #    Setting Deleted field in DocumentFile to True
        post.save()

        instanceDelete = DeletedFeeds()
        instanceDelete.post    = post
        instanceDelete.user     = request.user
        instanceDelete.save()

        data["deleted"]     = "Deleted"
        data["success"]     = "Successfully Deleted "
        return data

    def recover(self,post):
        data={}
        instance            = DeletedFeeds.objects.get(post=post)
        if instance.permanent_delete == False:
            post.deleted       = False #    Setting Deleted field in DocumentFile to False
            instance.delete() # Removing document from deleteList

            post.save()
            data["recovered"]     = "Recovered"
            data["success"]     = "Successfully recovered"
        else:
            data["Error"]     = "This item does not exist"
        return data

    @try_and_catch
    def post(self,request):
        data ={}
        postid          = request.POST['post_id']
        post            = Posts.objects.get(post_id=postid, user=request.user)

        if DeletedFeeds.objects.filter(post=post).exists()==True: # Checking if File is has already been deleted (if the file exist in the deletedList table) 
            data =   self.recover(post)
        else: # if Document has not been deleted before
            data = self.delete(request,post)
        return Response(data=data)

class delete_comment(APIView):
    permission_classes = [IsAuthenticated] # User has to be logged in

    def delete(self,request,comment):
        data={}
        comment.deleted    = True #    Setting Deleted field in DocumentFile to True
        comment.save()

        instanceDelete = DeletedFeeds()
        instanceDelete.comment    = comment
        instanceDelete.user     = request.user
        instanceDelete.save()

        data["deleted"]     = "Deleted"
        data["success"]     = "Successfully Deleted "
        return data

    def recover(self,comment):
        data={}
        instance            = DeletedFeeds.objects.get(comment=comment)
        if instance.permanent_delete == False:
            comment.deleted       = False #    Setting Deleted field in DocumentFile to False
            instance.delete() # Removing document from deleteList

            comment.save()
            data["recovered"]     = "Recovered"
            data["success"]     = "Successfully recovered"
        else:
            data["Error"]     = "This item does not exist"
        return data

    @try_and_catch
    def post(self,request):
        data ={}
        commentid          = request.POST['comment_id']
        comment            = Comments.objects.get(comment_id=commentid, user=request.user)

        if DeletedFeeds.objects.filter(comment=comment).exists()==True: # Checking if File is has already been deleted (if the file exist in the deletedList table) 
            data =   self.recover(comment)
        else: # if Document has not been deleted before
            data = self.delete(request,comment)
        return Response(data=data)