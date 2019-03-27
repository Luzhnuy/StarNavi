from django.urls import include, path
from . import views


urlpatterns=[
    path('users/',views.UserList.as_view(),name="user_list"),
    path('user/<int:pk>/',views.UserDetali.as_view(),name="user_detali"),
    path('user-create/',views.UserCreate.as_view(),name='user_create'),
    path('auth/', include('rest_framework.urls', namespace='rest_framework'))
]