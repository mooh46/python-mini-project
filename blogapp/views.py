from django.shortcuts import render
#from django.http import HttpResponse
from uuid import uuid4
import json
from django.contrib import messages
from django.shortcuts import redirect
#okay so from pathlib library i import path class which i can use in my view function to locate a folder
from pathlib import Path

from django.utils.text import slugify

from blogapp.forms import Login
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from functools import wraps

from blogapp.forms import AddArticle


# Create your views here.
def admin_required(view):
    @wraps(view)
    def wrapper(request,*args, **kwargs):
        if not request.session.get("username"):
            return redirect("blogapp:login")
        return view(request, *args, **kwargs)
    return wrapper


@admin_required
def new(request):
    if request.method == "POST":
        form = AddArticle(request.POST)
        if form.is_valid():
            artcl = {
                "title": form.cleaned_data["article_title"],
                "date": str(form.cleaned_data["publishing_date"]),
                "content": form.cleaned_data["content"],
            }
            unique_id = str(uuid4())[:8]
            with open(f"blogapp/storedFiles/{slugify(artcl['title']) + '-' + unique_id }.json", "w") as file:
                json.dump(artcl, file)
            messages.success(request, "Article Added Successfully")
            return redirect("blogapp:load")

    else:
        form = AddArticle()
    return render(request ,"blogapp/add.html", {
        "form":form,
        "action_url":reverse("blogapp:new")
    })

@admin_required
def load(request):
    artcl = []
    #path objects allow me to locate folders
    inside = Path("blogapp/storedFiles")
    # path objects come with a methods and one of the methods is iterdir() it gives me an iterable of the items inside the folder
    #it allows me to look into the file and see what folder are located in that folder/Directory?
    files = inside.iterdir()
    #after main it into an iterable and assigning it a variable we looped through the iterable
    for fyle in files:
        filename = fyle.name
        print(filename)

        #then file name holds one JSON file during each iteration/loop


        #here we open we each file and read
        with open("blogapp/storedFiles/" +filename, "r") as file:
            content = file.read()
            #converted into a python object
            content = json.loads(content)
            #addign filename into the dictionary we get back from the JSON object
            # so we can use it to access the file when  we want to edit or delete the article
            content["filename"] = filename
            #appended to the list above, we get a list of dictionaries
            artcl.append(content)





    return render(request, "blogapp/articlePage.html" ,{
        "artcl":artcl

    })


@admin_required
def edit(request,name):
    #when i press the edit button it should take me to the add HTML page
    #load the privous content
    #allow me to edit
    #then resumbit and not create a new article
    clean_name = Path(name).name
    with open("blogapp/storedFiles/" + clean_name, "r") as file:
        content  =  json.load(file)
    if request.method == "POST":
        form = AddArticle(request.POST)
        if form.is_valid():
            arti = {
                "title": form.cleaned_data["article_title"],
                "date": str(form.cleaned_data["publishing_date"]),
                "content": form.cleaned_data["content"]
            }
            with open("blogapp/storedFiles/" + clean_name, "w") as file:
                json.dump(arti,file)



            return redirect("blogapp:load")
    else :
        form = AddArticle(
            initial={
                "article_title": content["title"],
                "publishing_date": content["date"],
                "content": content["content"]
            }
        )

    return render(request, "blogapp/add.html" ,{
        "form":form,
        "action_url": reverse("blogapp:edit", kwargs={"name":clean_name}),

    })
@admin_required
def delete(request,name):

    #here we are filtering the name to avoid path reversal
    #so we are  only accepting the name at the end of the url
    clean_name = Path(name).name
    inside = Path("blogapp/storedFiles/"+clean_name)
    inside.unlink(missing_ok=False)
    messages.success(request, "Article Deleted Successfully")
    return redirect("blogapp:load")

def home(request):

    artcl = []
    #use path to get the file path
    inside = Path("blogapp/storedFiles")
    #use iterdir to get an iterable
    files =  inside.iterdir()
    #loop through the iterable and add each article to the list
    for fyle in files:
        article_file_name = fyle.name
        with open("blogapp/storedFiles/"+article_file_name,"r") as file:
            content =  file.read()
            content = json.loads(content)
            content["filename"] = article_file_name
            artcl.append(content)


    return render(request,"blogapp/HomePage.html",{"artcl":artcl})


def article(request,name):
    artcl = []
    clean_name = Path(name).name
    with open("blogapp/storedFiles/" + clean_name, "r") as file:
        data = file.read()
        fyle= json.loads(data)
        artcl.append(fyle)
        print(artcl)


    return render(request, "blogapp/articlePageGuest.html" ,{"artcl":artcl})


def login_view(request):

    if request.method == "POST":
        form = Login(request.POST)
        credentials = {
            "username": "Enter-Your-Username",
            "password": "Enter-Your-Password"
        }
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            if credentials["username"] == username and credentials["password"] == password:
                request.session["username"] = username
                return redirect("blogapp:load")
            else:
                messages.error(request, "Invalid Credentials")
                return render(request,"blogapp/login.html",{"form":form})
    else:
        form = Login()

    return render(request, "blogapp/login.html", {"form":form})

def logout_view(request):

    logout(request)
    return render(request,"blogapp/login.html",{
        "message":"Logged Out"
    })
