
from datetime import date
from distutils.command.upload import upload
from sqlite3 import Timestamp
from turtle import title
from django.db import models
from django.contrib.auth.models import User




# Create your models here.
class FarmerUser(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(default="user.png", null=True, blank=True, upload_to="images/")

    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        return f'{self.user} Profile'

class Question(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    image = models.ImageField(null=True, blank=True, upload_to="images/")

    content = models.TextField()
    author = models.ForeignKey(User,null=True, on_delete=models.CASCADE)
    
    

    def __str__(self):
        return self.title + ' by ' + self.author.username





# class Solution(models.Model):
#     text= models.CharField(max_length=500, null=True)

#     question = models.ForeignKey(Question, null=True, on_delete=models.SET_NULL)
#     user = models.ForeignKey(UserModel, null=True, on_delete=models.SET_NULL)



#     date_created = models.DateTimeField(auto_now_add= True, null=True)

    
#     def __str__(self):
#         t = self.text[0:50] + "......"
#         return t

    


# name:String ,
#     image:{type:String, default:"https://source.unsplash.com/Zm2n2O7Fph4"},
#     description:String,
#     created:{type:Date,default:Date.now},
#     author:{
#         id:{
#             type:mongoose.Schema.Types.ObjectId,
#             ref:"User"
#         },
#         username:String
#     },
#     solutions: [
#       {
#          type: mongoose.Schema.Types.ObjectId,
#          ref: "Solutions"
#       }
#   ]
