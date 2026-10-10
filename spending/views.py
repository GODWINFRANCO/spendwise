from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework import permissions

from spending.serializers import SignupSerializer,Expenseserializer
from spending.models import Expense
# Create your views here.

class Signupview(APIView):
    def post(self,request):
        form_data=request.data
        serializer_instance=SignupSerializer(data=form_data)

        if serializer_instance.is_valid():
            cleaned_data=serializer_instance.validated_data
            qs=User.objects.create_user(**cleaned_data)

            serializer_instance=SignupSerializer(qs)
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)

class GetMeView(APIView):

    authentication_classes=[authentication.BasicAuthentication]

    permission_classes =[permissions.IsAuthenticated]

    def get(self,request):

        auth_user = request.user
        instance =User.objects.get(username=auth_user)
        serializer_instance = SignupSerializer(instance)

        return Response(data=serializer_instance.data)

class ExpenseListCreateView(APIView):

    authentication_classes=[authentication.BasicAuthentication]
    
    permission_classes =[permissions.IsAuthenticated]

    def get(self,request):

        instance = Expense.objects.filter(owner=request.user)

        serializer_instance = Expenseserializer(instance,many=True)

        return Response(data=serializer_instance.data)

    def post(self,request):

        form_data = request.data

        serializer_instance = Expenseserializer(data = form_data)

        if serializer_instance.is_valid():

            serializer_instance.save(owner=request.user)

            return Response(data=serializer_instance.data)
        
        else:
            
            return Response(data=serializer_instance.errors)
            
class ExpenseRetrieveUpdateDeleteView(APIView):

    authentication_classes=[authentication.BasicAuthentication]
        
    permission_classes =[permissions.IsAuthenticated]

    def get(self,request,pk=None):
        
        instance = get_object_or_404(Expense,id=pk)

        serializer_instance = Expenseserializer(instance)

        return Response(data=serializer_instance.data)

    def put(self, request, pk=None):
        
        instance = get_object_or_404(Expense, id=pk)

        form_data = request.data

        serializer_instance = Expenseserializer(instance,data=form_data)
        
        if serializer_instance.is_valid():
            
            serializer_instance.save()
            
            return Response(data=serializer_instance.data)
        
        else:
            
            return Response(data=serializer_instance.errors)
        
    def delete(self,request,pk=None):

        instance = get_object_or_404(Expense,id=pk)

        instance.delete()

        return Response(data={"message":"deleted"})