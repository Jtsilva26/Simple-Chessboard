from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from app1.forms import ChessForm, JoinForm, LoginForm
from app1.models import Board
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
# Create your views here.
def home(request):
    if(Board.objects.all().count() == 0):
        newGame(request)
    page_data={"rows":[], "chess_form":ChessForm}
    # If there are is no Board model data, or if the user pressed the new game
    # button, create a new game in the Board model

    # if (Board.objects.all().count() == 0) or \
    # (request.method == 'POST' and 'new_game' in request.POST):

    if(Board.objects.filter(user=request.user).count() == 0) or (request.method == 'POST' and 'new_game' in request.POST):
        newGame(request)
    elif (request.method == 'POST'):
        chess_form = ChessForm(request.POST)
        if (chess_form.is_valid()):
            start = chess_form.cleaned_data["start"]
            end = chess_form.cleaned_data["end"]

            #Force update ...workaround the fact that django does not
            #support multi-field primary keys
            # Board(user=request.user, location=end, value=Board.objects.get(name=start).value).save()
            # Board(user=request.user, location=start, value="&nbsp").save()
            # Board.objects.filter(user=request.user, location=end, value="&nbsp").delete()
            # Board.objects.filter(user=request.user, location=start, value=Board.objects.get(name=start).value).delete()
            Board.objects.filter(user=request.user, location=end).update(value=Board.objects.filter(user=request.user).get(location=start).value)
            Board.objects.filter(user=request.user, location=start).update(value = '&nbsp')
        else:
            page_data["chess_form"] = chess_form

    for row in range(8,0,-1):
        row_data = {}
        for col in ['a','b','c','d','e','f','g','h']:
            id = "{}{}".format(col, row)
            try:
                # record = Board.objects.get(name=id)
                record = Board.objects.get(user=request.user, location=id)
                row_data[id] = record.value
            except Board.DoesNotExist:
                row_data[id] = 0
        page_data.get("rows").append(row_data)
    return render(request,'app1/home.html',page_data)

def newGame(request):
    page_data = {
     "rows": [
     {"a8": "&#9820", "b8": "&#9822", "c8": "&#9821", "d8": "&#9819", "e8": "&#9818", "f8": "&#9821", "g8": "&#9822", "h8": "&#9820"},
     {"a7": "&#9823", "b7": "&#9823", "c7": "&#9823", "d7": "&#9823", "e7": "&#9823", "f7": "&#9823", "g7": "&#9823", "h7": "&#9823"},
     {"a6": "&nbsp", "b6": "&nbsp", "c6": "&nbsp", "d6": "&nbsp", "e6": "&nbsp", "f6": "&nbsp", "g6": "&nbsp", "h6": "&nbsp"},
     {"a5": "&nbsp", "b5": "&nbsp", "c5": "&nbsp", "d5": "&nbsp", "e5": "&nbsp", "f5": "&nbsp", "g5": "&nbsp", "h5": "&nbsp"},
     {"a4": "&nbsp", "b4": "&nbsp", "c4": "&nbsp", "d4": "&nbsp", "e4": "&nbsp", "f4": "&nbsp", "g4": "&nbsp", "h4": "&nbsp"},
     {"a3": "&nbsp", "b3": "&nbsp", "c3": "&nbsp", "d3": "&nbsp", "e3": "&nbsp", "f3": "&nbsp", "g3": "&nbsp", "h3": "&nbsp"},
     {"a2": "&#9817", "b2": "&#9817", "c2": "&#9817", "d2": "&#9817", "e2": "&#9817", "f2": "&#9817", "g2": "&#9817", "h2": "&#9817"},
     {"a1": "&#9814", "b1": "&#9816", "c1": "&#9815", "d1": "&#9813", "e1": "&#9812", "f1": "&#9815", "g1": "&#9816", "h1": "&#9814"}
     ]
    }
    #Delete all board board model objects (records)
    # Board.objects.all().delete()
    Board.objects.filter(user=request.user).delete()

    #Populate board model objects from page_data
    for row in page_data.get("rows"):
        for location,value in row.items():
            Board(user=request.user, location=location, value=value).save()

def join(request):
    if (request.method == "POST"):
        join_form = JoinForm(request.POST)
        if (join_form.is_valid()):
            # Save form data to DB
            user = join_form.save()
            # Encrypt the password
            user.set_password(user.password)
            # Save encrypted password to DB
            user.save()
            # Success! Redirect to home page.
            return redirect("/")
        else:
             # Form invalid, print errors to console
             page_data = { "join_form": join_form }
             return render(request, 'app1/join.html', page_data)
    else:
         join_form = JoinForm()
         page_data = { "join_form": join_form }
         return render(request, 'app1/join.html', page_data)

def user_login(request):
    if (request.method == 'POST'):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
             # First get the username and password supplied
             username = login_form.cleaned_data["username"]
             password = login_form.cleaned_data["password"]
             # Django's built-in authentication function:
             user = authenticate(username=username, password=password)
             # If we have a user
             if user:
                 #Check it the account is active
                 if user.is_active:
                     # Log the user in.
                     login(request,user)
                     # Send the user back to homepage
                     return redirect("/")
                 else:
                     # If account is not active:
                     return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return render(request, 'app1/login.html', {"login_form": LoginForm})
    else:
        #Nothing has been provided for username or password.
        return render(request, 'app1/login.html', {"login_form": LoginForm})

def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return redirect("/")

@login_required(login_url='/login/')
def historyOfChess(request):
    return render(request, 'app1/historyOfChess.html')

@login_required(login_url='/login/')
def chessPieceSummary(request):
    return render(request, 'app1/chessPieceSummary.html')

@login_required(login_url='/login/')
def about(request):
    return render(request, 'app1/about.html')
