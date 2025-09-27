from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BlogSerializer
from .models import Blog
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication 
from rest_framework.response import Response
from .models import Blog
from django.db.models import Q
from django.core.paginator import Paginator 
# Create your views here.

class PublicBlog(APIView):
    def get(self,request):
        try:
            blogs=Blog.objects.all().order_by('?') #For randomness in fetching for Public API fetching blogs.
            if request.GET.get('search'):
                search=request.GET.get('search')
                blogs=blogs.filter(Q(title__icontains=search)|Q(content__icontains=search)) 

            page_number=request.GET.get('page',1)
            paginator=Paginator(blogs,5)       

            serializer=BlogSerializer(paginator.page(page_number),many=True)

            return Response({
                'data':serializer.data,
                'message':'Blogs fetched successfully.'
            },status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({
                'message':'Something went wrong or invalid page'
            },status=status.HTTP_404_NOT_FOUND)


class BlogView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]            
    def post(self,request):
        try:
            data=request.data
            data['user']=request.user.id #Assigning user field of blog object
            serializer=BlogSerializer(data=data)  
            if not serializer.is_valid():
                return Response({'data':serializer.errors,'message':'Invalid entries'},status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()

            
            
            
            return Response({'data':serializer.data,'message':'Blog posted successfully'},status=status.HTTP_201_CREATED)
        
        except Exception as e:
            print(e)
            return Response({'message':'To post blog you must be logged in first'},status=status.HTTP_401_UNAUTHORIZED)
        
    def get(self,request):
        try:
            blogs=Blog.objects.filter(user=request.user) #Filter the blogs by the currently logged in user
            if request.GET.get('search'):    
                search=request.GET.get('search')
                blogs = blogs.filter(Q(title__icontains=search)|Q(content__icontains=search)) #If there is a search query, search the blogs according to the query
            serializer=BlogSerializer(blogs,many=True)

            


            return Response({'data':serializer.data,'message':'Blogs fetched successfully'}, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({'data':{},'message':'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)
        

    def patch(self,request):
        try:
            data=request.data
            blog=Blog.objects.filter(uid=data.get('uid'))

            if not blog.exists():
                return Response({
                    'data':{},
                    'message':'Invalid blog uid' 
                },status=status.HTTP_404_NOT_FOUND)
            if request.user != blog[0].user:
                return Response({
                    'data':{},
                    'message':"You are not authorized to update this blog "
                },status=status.HTTP_401_UNAUTHORIZED)  
            
            serializer=BlogSerializer(blog[0],data=data,partial=True) #Call Serializer to validate the sent data, partial=True says that all fields are not necessary and that's okay. 

            if not serializer.is_valid():        
                return Response({
                    'data':serializer.errors,
                    'message':'Invalid entries'
                },status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()

            return Response({
                'data':serializer.data,
                'message':'Blog patched successfully'
            },status=status.HTTP_200_OK)


        except Exception as e:
            print(f"Error occured while updating blog -> {e}")
            return Response({
                'data': {},
                'message': 'An unexpected error occurred during the blog update.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self,request):
        try:
            data=request.data 
            uid=data.get('uid')
            if not uid:
                return Response({
                    'data':{},
                    'message':'UID is required'
                },status=status.HTTP_400_BAD_REQUEST)
            blog=Blog.objects.get(uid=data.get('uid'))
            
            
            if request.user != blog.user:
                return Response({
                    'data':{},
                    'message':'You are not authorized to do this'

                },status=status.HTTP_401_UNAUTHORIZED)
            
            blog.delete()
            return Response({
                    'data':{},
                    'message':'Blog deleted successfully'
            },status=status.HTTP_200_OK)
            

        except Exception as e:  
            print(e)
            return Response({
                'data':{},
                'message':'Something went wrong'
            },status=status.HTTP_400_BAD_REQUEST) 
    


