from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Sum
from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework import permissions


from spending.serializers import SignupSerializer,Expenseserializer
from spending.models import Expense
from spending.permissions import IsOwner
from spending.ai_service import get_budget_plan
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

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes =[permissions.IsAuthenticated]

    def get(self,request):

        auth_user = request.user

        instance =User.objects.get(username=auth_user)

        serializer_instance = SignupSerializer(instance)

        return Response(data=serializer_instance.data)

class ExpenseListCreateView(APIView):

    authentication_classes=[authentication.TokenAuthentication]
    
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

    authentication_classes=[authentication.TokenAuthentication]
        
    #permission_classes =[permissions.IsAuthenticated]

    permission_classes = [IsOwner]

    def get(self,request,pk=None):
        
        instance = get_object_or_404(Expense,id=pk)

        self.check_object_permissions(request,instance)

        serializer_instance = Expenseserializer(instance)

        return Response(data=serializer_instance.data)

    def put(self, request, pk=None):
        
        instance = get_object_or_404(Expense, id=pk)

        self.check_object_permissions(request,instance)

        form_data = request.data

        serializer_instance = Expenseserializer(instance,data=form_data)
        
        if serializer_instance.is_valid():
            
            serializer_instance.save()
            
            return Response(data=serializer_instance.data)
        
        else:
            
            return Response(data=serializer_instance.errors)
        
    def delete(self,request,pk=None):

        instance = get_object_or_404(Expense,id=pk)

        self.check_object_permissions(request,instance)

        instance.delete()

        return Response(data={"message":"deleted"})

class ExpenseSummaryView(APIView):

    authentication_classes=[authentication.TokenAuthentication]
        
    permission_classes =[permissions.IsAuthenticated]

    def get(self,request):

        response_data = {
            "todays_total":0
                         }

        current_date = datetime.now().today()

        current_month = datetime.now().month

        current_year = datetime.now().year

        #monthly summary

        monthly_transaction = Expense.objects.filter(owner=request.user,created_at__month=current_month,created_at__year=current_year)

        if monthly_transaction:

            monthly_total = monthly_transaction.values("amount").aggregate(total=Sum("amount")).get("total")

            response_data["monthly_total"] = monthly_total

        #todays summary

        today_transaction = Expense.objects.filter(owner=request.user,created_at__date=current_date)

        if today_transaction:

            todays_total = today_transaction.values("amount").aggregate(total=Sum("amount")).get("total")

            category_summary = today_transaction.values("category").annotate(total=Sum("amount"))

            response_data["todays_total"]=todays_total

            response_data["category_summary"]=category_summary

        return Response(data=response_data)

class BudgetPlanView(APIView):

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):

        user=request.user

        current_month = datetime.now().month

        current_year = datetime.now().year

        response_data = {
                    "monthly_total":0
                                 }

        monthly_transaction = Expense.objects.filter(owner=request.user,created_at__month=current_month,created_at__year=current_year)

        if monthly_transaction:

            monthly_total = monthly_transaction.values("amount").aggregate(total=Sum("amount")).get("total")

            category_summary = monthly_transaction.values("category").annotate(total=Sum("amount"))

            response_data["monthly_total"]=monthly_total
            
            response_data["category_summary"]=category_summary

            budget_plan = get_budget_plan(response_data)

            response_data["plan"]=budget_plan
            
            return Response(data=response_data)