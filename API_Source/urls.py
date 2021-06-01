from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RegisterView, VerifyEmail, LoginApiView, UserRetrieveUpdate, user_follow_user, getTop3author

# router = DefaultRouter()
# router.register(r'', UserViewSet, basename='users')

urlpatterns = [
    # path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginApiView.as_view(), name="login"),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    path('follow/', user_follow_user, name="user_follow_user"),
    path('top_author/', getTop3author, name="top_3_author"),
    path('<str:email_user>/', UserRetrieveUpdate.as_view(), name="retrieve-update"),
]
