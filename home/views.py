from django.shortcuts import render
from rest_framework.decorators import api_view,action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets,status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import authenticate
from django.core.paginator import Paginator

from home.models import Person
from home.serializers import PeopleSerializer,LoginSerializer,RegisterSerializer
from rest_framework.authentication import TokenAuthentication, BasicAuthentication

class LoginAPI(APIView):

    def post(self,request):
        data = request.data
        serializer = LoginSerializer(data = data)
        if not serializer.is_valid():
            return Response(
                {
                    'status': False,
                    'Message': serializer.errors,
                 } ,status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(username = serializer.data['username'],password = serializer.data['password'])

        if not user:
            return Response(
                {
                    'status': False,
                    'Message': "Invalid username or password",
                 } ,status.HTTP_400_BAD_REQUEST
            )
        token = Token.objects.get_or_create(user=user)

        return Response({'status': True,'message': 'Logged in Successfully','token':str(token)},status.HTTP_201_CREATED)
        

class RegisterAPI(APIView):

    def post(self,request):
        data = request.data
        serializer = RegisterSerializer(data=data)

        if not serializer.is_valid():
            return Response(
                {
                    'status': False,
                    'Message': serializer.errors,
                 } ,status.HTTP_400_BAD_REQUEST
            )
        serializer.save()

        return Response({'status': True, 'Message': "User Created"},status.HTTP_201_CREATED)

@api_view(['GET','POST','PUT'])
def index(request):
    courses = {
        'course_name': 'Python',
        'learn': ['flask', 'Django', 'Tornado', 'FastApi'],
        'course_provider': 'Scaler'
    }
    if request.method == 'GET':
        print(request.GET.get('search'))
        print("GET request")
        return Response(courses)
    elif request.method == 'POST':
        data = request.data
        print("********")
        print(data)
        print("********")
        print("POST request")
        return Response(courses)
    elif request.method == 'PUT':
        print("PUT request")
        return Response(courses)

@api_view(['POST'])
def login(request):
    data  = request.data
    serializer = LoginSerializer(data = data)

    if serializer.is_valid():
        data = serializer.data
        print(data)
        return Response({'message': 'Sucess'})

    return Response(serializer.errors)

#CRUD Operations using the Serializer class.
class PersonAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self,request):
        try:
            print(request.user)
            #query to get all the queryset of Person
            obj = Person.objects.all()
            page = request.GET.get('page',1)
            page_size = 3
            paginator = Paginator(obj,page_size)
            #to serialize all the queryset and as there were more than one objects in queryset so  we pass many = True
            serializer = PeopleSerializer(paginator.page(page),many=True)
            #return the seialized data
            return Response(serializer.data)
        except Exception as e:
            return Response({'status':False,
                             'message':'Invalid Page'})


    def post(self, request):
        #take data from frontend
        data = request.data
        serializer = PeopleSerializer(data = data)
        #check if the serializer data is valid and return
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        #return error if any
        return Response(serializer.errors)
    
    def patch(self, request):
        #request the data from the user
        data = request.data
        #query to get the queryset
        obj  = Person.objects.get(id = data['id']) 
        #serializer to update the data Partially 
        serializer = PeopleSerializer(obj,data = data,partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        #return error if any
        return Response(serializer.errors)

    def put(self, request):
        #request the data from the user
        data = request.data
        serializer = PeopleSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        #return error if any
        return Response(serializer.errors)
    
    def delete(self, request):
        #request the data from the user
        data =  request.data
        #query to get the queryset
        obj = Person.objects.get(id = data['id'])
        #Delete  the data 
        obj.delete()
        return Response({'message': 'Pesron Deleted'})


#CRUD Operations in Rest Framework GET POST PUT PATCH DELETE
@api_view(['GET','POST','PUT','PATCH','DELETE'])
def person(request):
    if request.method == 'GET':
        #query to get all the queryset of Person
        obj = Person.objects.all()
        #to serialize all the queryset and as there were more than one objects in queryset so  we pass many = True
        serializer = PeopleSerializer(obj,many=True)
        #return the seialized data
        return Response(serializer.data)
    
    elif request.method == 'POST':
        #take data from frontend
        data = request.data
        serializer = PeopleSerializer(data = data)
        #check if the serializer data is valid and return
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        #return error if any
        return Response(serializer.errors)
    
    elif request.method == 'PUT':
        #request the data from the user
        data = request.data
        serializer = PeopleSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        #return error if any
        return Response(serializer.errors)
    
    elif request.method == 'PATCH':
        #request the data from the user
        data = request.data
        #query to get the queryset
        obj  = Person.objects.get(id = data['id']) 
        #serializer to update the data Partially 
        serializer = PeopleSerializer(obj,data = data,partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        #return error if any
        return Response(serializer.errors)
    
    else:
        #request the data from the user
        data =  request.data
        #query to get the queryset
        obj = Person.objects.get(id = data['id'])
        #Delete  the data 
        obj.delete()
        return Response({'message': 'Pesron Deleted'})

#The ModelViewSet class is capable of handling all the CRUD api so it makes the developers task easy. 
class PeopleViewSet(viewsets.ModelViewSet):
    serializer_class = PeopleSerializer
    queryset = Person.objects.all()

    def list(self,request):
        search = request.GET.get('search')
        queryset = self.queryset
        if search:
            queryset = queryset.filter(name__startswith=search)
        serializer = PeopleSerializer(queryset,many = True)
        return Response({'data':serializer.data},status = status.HTTP_200_OK)
    
    @action(detail = True,methods = ['POST'])
    def sent_an_email(self,request,pk):
        obj = Person.objects.get(pk=pk)
        serializer = PeopleSerializer(obj)
        return Response(
            {
                "status": True,
                "message":"Mail sent successfully",
                "data": serializer.data
            }
        ) 
