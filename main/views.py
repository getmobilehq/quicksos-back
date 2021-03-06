from django.forms import model_to_dict
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import EscalateSerializer, AgencySerializer, IssueSerializer, MessageSerializer
from drf_yasg.utils import swagger_auto_schema
from .models import Agency, Issue, Message, Question, User
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAdmin, IsAdminOrReadOnly, IsAgent, IsAgentOrAdmin, IsEscalator
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from .helpers.check_agency import validate_responders




@swagger_auto_schema("post", request_body=MessageSerializer())
@api_view(["POST"])
@authentication_classes([JWTAuthentication, TokenAuthentication])
@permission_classes([IsAgentOrAdmin])
def add_message(request):
    
    if request.method == "POST":
        serializer = MessageSerializer(data=request.data)

        if serializer.is_valid():
    
            if serializer.validated_data.get("provider") == "call":
                agencies_ = serializer.validated_data.get("agencies")
                if validate_responders(agencies_):
                    
                    serializer.save()
            else:
    
                serializer.save()
            
            
            
            return Response({"message":"success"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error":serializer.errors,"message":"failed"}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAgentOrAdmin])
def get_message(request):        
    if request.method == "GET":
        
        date = request.GET.get("filterDate")
        
        messages = Message.objects.filter(is_active=True)
        
        if date:
            messages = messages.filter(date_created__date=date)
            
        serializer = MessageSerializer(messages, many=True)
        data = {"message":"success",
                "data":serializer.data}
        
        return Response(data,status=status.HTTP_200_OK)
    
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAgent])
def pending_message(request):        
    if request.method == "GET":
        date = request.GET.get("filterDate")
        
        messages = Message.objects.filter(is_active=True, status = "pending")
        
        
        
        if date:
            messages = messages.filter(date_created__date=date)
            
        serializer = MessageSerializer(messages, many=True)
        data = {"message":"success",
                "data":serializer.data}
        
        return Response(data,status=status.HTTP_200_OK)
    
@api_view(["GET", "PUT", "DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAgent])
def message_detail(request, message_id):
    try:
        obj = Message.objects.get(id=message_id, is_active=True)
    except Message.DoesNotExist:
        errors = {
                "message":"failed",
                "errors": f'Message with id {message_id} not found'
                }
        return Response(errors, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer =MessageSerializer(obj)
        data = {
                "message":"success",
                "data":serializer.data
                }
            
        return Response(data, status=status.HTTP_200_OK)
        
    
    elif request.method == 'PUT':
        serializer = MessageSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = {
                "message":"success",
                "data":serializer.data
                }
            
            return Response(data, status=status.HTTP_202_ACCEPTED)
        else:
            errors = {
                "message":"failed",
                "errors":serializer.errors
                }
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        obj.delete()
        data = {
                "message":"success"
                }
            
        return Response(data, status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema("post", request_body=AgencySerializer())
@api_view(["GET", "POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminOrReadOnly])
def agencies(request):
    
    if request.method == "GET":
        agency = Agency.objects.filter(is_active=True)
        serializer = AgencySerializer(agency, many=True)
        data = {"message":"success",
                "data":serializer.data}
        
        return Response(data,status=status.HTTP_200_OK)
    
    elif request.method == "POST":
        serializer = AgencySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            return Response({"message":"success"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error":serializer.errors,"message":"failed"}, status=status.HTTP_400_BAD_REQUEST)
         
    
    
    
@api_view(["GET", "PUT", "DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdmin])
def agency_detail(request, agency_id):
    try:
        obj = Agency.objects.get(id=agency_id, is_active=True)
    except Agency.DoesNotExist:
        errors = {
                "message":"failed",
                "errors": f'Agency with id {agency_id} not found'
                }
        return Response(errors, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer =AgencySerializer(obj)
        data = {
                "message":"success",
                "data":serializer.data
                }
            
        return Response(data, status=status.HTTP_200_OK)
        
    
    elif request.method == 'PUT':
        serializer = AgencySerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = {
                "message":"success",
                "data":serializer.data
                }
            
            return Response(data, status=status.HTTP_202_ACCEPTED)
        else:
            errors = {
                "message":"failed",
                "errors":serializer.errors
                }
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        obj.delete()
        data = {
                "message":"success"
                }
            
        return Response(data, status=status.HTTP_204_NO_CONTENT)
    


@swagger_auto_schema("post", request_body=EscalateSerializer())
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAgent])
def escalate(request, message_id):
    try:
        obj = Message.objects.get(id=message_id, is_active=True, status="pending")
    
        
    except Message.DoesNotExist:
        errors = {
                "message":"failed",
                "errors": f'Message with id {message_id} not found or has been escalated'
                }
        return Response(errors, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "POST":
        
        serializer = EscalateSerializer(data=request.data)
        
        if serializer.is_valid():
            agencies_ = serializer.validated_data.get('agencies')
            
            #check all the agencies to be escalated to, if any does not have an escalator, raise an error.
            if validate_responders(agencies_):
                    
                obj.agencies.set(agencies_)
                # print(request.user)
                obj.agent = request.user
                obj.status= "escalated"
                obj.date_escalated = timezone.now()
                
                obj.save()
            
                return Response({"message":"successful"}, status=status.HTTP_201_CREATED)
        else:
            errors = {
                "message":"failed",
                "errors":serializer.errors
                }
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsEscalator])
def escalated_message(request):        
    if request.method == "GET":
        date = request.GET.get("filterDate")
                
        messages = Message.objects.filter(is_active=True, status="escalated",agencies=request.user.agency )
        
        if date:
            messages = messages.filter(date_escalated__date=date)
            
        serializer = MessageSerializer(messages, many=True)
        data = {"message":"success",
                "data":serializer.data}
        
        return Response(data,status=status.HTTP_200_OK)
    
    

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def message_report(request, message_id):        
    if request.method == "GET":
        try:
            message = Message.objects.get(is_active=True, id=message_id)
            msg_serializer = MessageSerializer(message)
            data_ = {"message_data":msg_serializer.data,
                "responder_reports":[{
                    "first_responder": model_to_dict(case.responder,exclude=
                                                 ['password',
                                                  'groups',
                                                  'user_permissions',
                                                  'agency',
                                                  'last_login']),
                    "agency":model_to_dict(case.responder.agency),
                    "escalator_note": case.escalator_note, 
                    "responder_status":case.status, 
                    'reports':case.report_detail,
                    "assigned_date" : case.date_created,
                    } for case in message.assigned.all()],
                     }
            
            data = {"message":"success",
                    "data":data_}
            
            return Response(data,status=status.HTTP_200_OK)
        except Message.DoesNotExist:
            errors = {
                    "message":"failed",
                    "errors": f'Message not found'
                    }
            return Response(errors, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAgent])
def mark_as_emergency(request, message_id):        
    if request.method == "GET":
        try:
            message = Message.objects.get(is_active=True, id=message_id)
            message.is_emergency=True
            message.save()
            
            data = {"message":"success"
                    }
            
            return Response(data,status=status.HTTP_200_OK)
        except Message.DoesNotExist:
            errors = {
                    "message":"failed",
                    "errors": f'Message not found'
                    }
            return Response(errors, status=status.HTTP_404_NOT_FOUND)
        
        
        
        
# =========== CRUD QUESTIONS, ISSUES AND RESPONSES ================
@swagger_auto_schema("post", request_body=IssueSerializer())
@api_view(["GET", "POST"])
@authentication_classes([JWTAuthentication, TokenAuthentication])
@permission_classes([IsAdminOrReadOnly])
def issues(request):
    
    if request.method == "GET":
        issue = Issue.objects.filter(is_active=True)
        serializer = IssueSerializer(issue, many=True)
        data = {"message":"success",
                "data":serializer.data}
        
        return Response(data,status=status.HTTP_200_OK)
    
    elif request.method == "POST":
        serializer = IssueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            return Response({"message":"success"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error":serializer.errors,"message":"failed"}, status=status.HTTP_400_BAD_REQUEST)
         
    
    
    
@api_view(["GET", "PUT", "DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdmin])
def issue_detail(request, issue_id):
    try:
        obj = Issue.objects.get(id=issue_id, is_active=True)
    except Issue.DoesNotExist:
        errors = {
                "message":"failed",
                "errors": f'Issue with id {issue_id} not found'
                }
        return Response(errors, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer =IssueSerializer(obj)
        data = {
                "message":"success",
                "data":serializer.data
                }
            
        return Response(data, status=status.HTTP_200_OK)
        
    
    elif request.method == 'PUT':
        serializer = IssueSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = {
                "message":"success",
                "data":serializer.data
                }
            
            return Response(data, status=status.HTTP_202_ACCEPTED)
        else:
            errors = {
                "message":"failed",
                "errors":serializer.errors
                }
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        obj.delete()
        data = {
                "message":"success"
                }
            
        return Response(data, status=status.HTTP_204_NO_CONTENT)
    
    
@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdmin])
def question_detail(request, question_id):
    try:
        obj = Question.objects.get(id=question_id, is_active=True)
    except Question.DoesNotExist:
        errors = {
                "message":"failed",
                "errors": f'Question with id {question_id} not found'
                }
        return Response(errors, status=status.HTTP_404_NOT_FOUND)
    
    # if request.method == 'GET':
    #     serializer =IssueSerializer(obj)
    #     data = {
    #             "message":"success",
    #             "data":serializer.data
    #             }
            
    #     return Response(data, status=status.HTTP_200_OK)
        
    
    # elif request.method == 'PUT':
    #     serializer = IssueSerializer(obj, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         data = {
    #             "message":"success",
    #             "data":serializer.data
    #             }
            
    #         return Response(data, status=status.HTTP_202_ACCEPTED)
    #     else:
    #         errors = {
    #             "message":"failed",
    #             "errors":serializer.errors
    #             }
    #         return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        
    if request.method == 'DELETE':
        obj.delete()
        data = {
                "message":"success"
                }
            
        return Response(data, status=status.HTTP_204_NO_CONTENT)