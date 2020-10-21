from django.shortcuts import redirect, render, HttpResponse
from django.contrib import messages
from .models import User, Places

# Create your views here.
def index(request):
    return render(request, "index.html")

def register(request):
    print(request.POST)
    resultFromValidator = User.objects.register_validator(request.POST)
    print(resultFromValidator)
    if len(resultFromValidator)>0:
        for key, value in resultFromValidator.items():
            messages.error(request, value)
        return redirect('/')
    
    newUser = User.objects.create(name= request.POST["name"],username = request.POST["username"], password= request.POST["pw"])
    print(newUser.id)
    request.session['loggedinID'] = newUser.id
    
    return redirect("/success")

def home(request):
    if 'loggedinID' not in request.session:
        messages.error(request, "Log in to view that page.")
        return redirect("/")
    loggedinUser = User.objects.get(id= request.session['loggedinID'])
    context = {
        'loggedinUser':loggedinUser,
        'allplaces': Places.objects.all(),
        'user_places': Places.objects.filter(others=loggedinUser)
        
    }
    return render(request, "homepage.html", context)

def logout(request):
    request.session.clear()
    return redirect("/")

def login(request):
    print(request.POST)
    resultFromValidator = User.objects.loginValidator(request.POST)
    print(resultFromValidator)
    if len(resultFromValidator)>0:
        for key, value in resultFromValidator.items():
            messages.error(request, value)
        return redirect("/")
    usernameMatch = User.objects.filter(username=request.POST['username'])
    request.session['loggedinID'] = usernameMatch[0].id
    
        
    return redirect("/success")



def add(request):

    
    return render(request, "add.html")


def create(request):
    errorMessagesFromValidator= Places.objects.CreateValidator(request.POST)
    print("PRINTING ERRORS FROM THE VALIDATOR BELOW")
    print(errorMessagesFromValidator)
    if len(errorMessagesFromValidator)> 0:
        for key, value in errorMessagesFromValidator.items():
            messages.error(request, value)
            
        return redirect("/add")
    newplace = Places.objects.create(destination=request.POST['destination'], travelstart=request.POST['datefrom'], travelend=request.POST['dateto'],plan=request.POST['plan'], uploader=User.objects.get(id=request.session['loggedinID']))
    return redirect("/success")

def showplace(request, placesid):
    context = {
        'placetoshow': Places.objects.get(id=placesid)
        
    }
    
    return render(request, "showplace.html", context)


def joinplace(request, placesid):
    
    loggedinUser = User.objects.get(id= request.session['loggedinID'])
    joined= Places.objects.get(id=placesid)
    joined.others.add(loggedinUser)

    return redirect("/success")