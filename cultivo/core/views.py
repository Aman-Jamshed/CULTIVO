from email import message
from multiprocessing import context
from operator import sub
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm


from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required



from .models import *
from .forms import *
import numpy as np
import pandas as pd
import requests
from .config import *
import pickle


# Authentication work  start from here.......................................

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                FarmerUser.objects.create (
                    user = user,
                    
                )
                
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account created succesfully for ' + user)
                return redirect('login')



        context = {'form': form}
        return render(request, 'register.html',context)



def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')


            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or password is incorrect')



        context = {}
        return render(request, 'login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')


#-----------------------------------------------------------------------------------------


# Loading crop recommendation model

crop_recommendation_model_path = "C:/Users/jhamshed akhtar khan/Desktop/CULTIVO/cultivo/core/model/RandomForest.pkl"
crop_recommendation_model = pickle.load(
    open(crop_recommendation_model_path, 'rb'))

# --------------------------------------------------------------------------------------

# Create your views here.
def home(request):
	return render(request, "home.html")


@login_required(login_url='login')
def userPage(request):
    user=request.user.farmeruser
    form = FarmerForm(instance=user)
    context = {'form': form}
    # print('Question: ', questions)

    if request.method == 'POST':
        form = FarmerForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Profile Updated Sucessfully!')

    return render(request, 'users.html', context)




@login_required(login_url='login')
def question(request):
    submitted = False
    author = Question(author=request.user)
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES, instance=author)
        print(form)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            return redirect('/allques')

            
        

    else:
            form = QuestionForm
            if 'submitted' in request.GET:
                submitted = True

    
    return render(request, 'ask_questions.html', {'form': form, 'submitted': submitted})
    
    

@login_required(login_url='login')
def allques(request):
    questions = Question.objects.all()
    for question in questions:
        print(question)
        question.content = str(question.content)[0:200] + '.....'



    context = {'questions': questions}

    return render(request, 'allques.html', context)   
    

	
@login_required(login_url='login')
def showques(request, pk):
    
    
    question = Question.objects.get(sno=pk)
    print(question)

    context = {'question': question}

    return render(request, 'showques.html', context)


@login_required(login_url='login')
def editques(request, pk):
        
        question = Question.objects.get(sno = pk)
        
        if request.method == 'POST':
            print(request.POST)
            title = request.POST.get('question')
            
            content = request.POST.get('description')
            question.title = title
            question.content = content
            question.save()
            
            return redirect('/allques')
            

        context = {'question': question}



        return render(request, 'edit.html', context)

@login_required(login_url='login')
def deleteques(request, pk):
            question = Question.objects.get(sno = pk)
            question.delete()
            return redirect('/allques')




def weather_fetch(city_name):
    """
    Fetch and returns the temperature and humidity of a city
    :params: city_name
    :return: temperature, humidity
    """
    api_key = weather_api_key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()

    if x["cod"] != "404":
        y = x["main"]

        temperature = round((y["temp"] - 273.15), 2)
        humidity = y["humidity"]
        return temperature, humidity
    else:
        return None


@login_required(login_url='login')
def crop_recommend(request):
    
    return render(request, 'crop.html')


@login_required(login_url='login')
def crop_prediction(request):
    print(request)

    if request.method == 'POST':
        N = int(request.POST.get('nitrogen'))
        P = int(request.POST.get('phosphorous'))
        K = int(request.POST.get('pottasium'))
        ph = float(request.POST.get('ph'))
        rainfall = float(request.POST.get('rainfall'))

        # state = request.form.get("stt")
        city = request.POST.get("city")

        if weather_fetch(city) != None:
            temperature, humidity = weather_fetch(city)
            data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
            my_prediction = crop_recommendation_model.predict(data)
            final_prediction = my_prediction[0]
            print(final_prediction)
            context = {'prediction': final_prediction}

            return render(request , 'crop_result.html', context)

        else:

            return render(request, 'try_again.html')


