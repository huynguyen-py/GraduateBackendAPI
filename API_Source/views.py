from django.db.models import Count
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib import auth
from django.shortcuts import get_object_or_404
from .models import User
from rest_framework.response import Response
from .serializers import UserSerializer, EmailVertificationSerializer, LoginSerializers
from rest_framework.generics import GenericAPIView
from rest_framework import status, views, generics
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import operator


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveUpdate(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_url_kwarg = 'email_user'
    lookup_field = 'email'
    queryset = User.objects.all()
    # def get_queryset(self):
    #     return User.objects.filter(id=self.request.user.id)



@api_view()
@permission_classes([permissions.IsAuthenticated, ])
def getTop3author(request):
    user_ = User.objects.all().annotate(Count('Followed', distinct=True))
    user_serializer = UserSerializer(user_[:3], many=True)
    return Response({'data': user_serializer.data})


@api_view()
@permission_classes([permissions.IsAuthenticated,])
def user_follow_user(request):
    user_ = get_object_or_404(User, email=request.query_params['email_user'])
    if user_.Followed.filter(email=request.user).exists():
        user_.Followed.remove(request.user)
        return Response({'data': "unfollowed"})
    else:
        user_.Followed.add(request.user)
        return Response({'data': "followed"})


class RegisterView(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()

            user_data = serializer.data
            user = User.objects.get(email=user_data['email'])
            token = RefreshToken.for_user(user).access_token

            current_site = get_current_site(request).domain
            relativeLink = reverse('email-verify')
            absurl = 'http://' + current_site + relativeLink + "?token=" + str(token)
            email_body = "Hi " + user.username + "\nPlease use link bellow to verify your email, by domain:\n" + absurl
            email_body += "\n Thank you for register!"
            data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Verify your Email'}
            Util.send_email(data)
            return Response({'data':serializer.data,'message': 'Register successful! Please verify in your email.'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmail(views.APIView):
    serializer_class = EmailVertificationSerializer

    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY
                                           , description='views for verify email user'
                                           , type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            # payload = jwt.decode(token, settings.SECRET_KEY)
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified=True
                user.save()
            return Response({'email': "Successfully activated"}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': identifier}, status=status.HTTP_400_BAD_REQUEST)


class LoginApiView(generics.GenericAPIView):
    serializer_class = LoginSerializers

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = auth.authenticate(
                request,
                email=request.data['email'],
                password=request.data['password']
            )
            if user:
                refresh = user.tokens()
                data = {
                    'refresh_token': str(refresh['refresh']),
                    'access_token': str(refresh['access']),
                    'access_expires': int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()),
                    'refresh_expires': int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()),
                    'usermail': user.email,
                }
                return Response(data, status=status.HTTP_200_OK)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)

            return Response({
                'error_message': 'Email or password is incorrect!',
                'error_code': 400
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'error_messages': serializer.errors,
            'error_code': 400
        }, status=status.HTTP_400_BAD_REQUEST)