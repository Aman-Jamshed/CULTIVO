from django.urls import path, include
from .import views



urlpatterns = [
    path('', views.home, name="home"),
    path('question', views.question, name="question"),
    path('allques', views.allques, name="allquestions"),
    path('question/<str:pk>', views.showques, name="showquestions"),
    path('question/<str:pk>/edit', views.editques, name="editquestion"),
    path('question/<str:pk>/delete', views.deleteques, name="deletequestion"),
    path('crop/', views.crop_recommend, name="crop_recommend"),
    path('crop/crop-predict', views.crop_prediction, name="crop_prediction"),
    path('register/', views.registerPage, name="register"),
    path('profile/', views.userPage, name="userPage"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

]
