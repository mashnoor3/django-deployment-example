from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
# So remember decorators are for wrapping functions.
# So now I can use the login_required decorators to wrap any view that requires user to be logged in
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'basic_app/index.html')


# Logout view should only be for when the user is logged in. So let's decorate it with the login_required decorator
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def special(request):
    return HttpResponse("You are logged in :)")

def register(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password) # Hash the password
            user.save()

            profile = profile_form.save(commit=False) #Don't commit to the database right away, otherwise may get collisions
            profile.user = user # establising the 1 to 1 relationship. Recall when we made the UserProfileInfo class, it has a 1to1 relationship with User

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic'] #key based on what I defined in the model. Similarly can get other files like this, ex PDF files for resume. Not just images.

            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)
    else:
        # So wan't a POST request. So set everything up.
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    context_dict = {'user_form':user_form, 'profile_form': profile_form, 'registered':registered}
    return render(request, 'basic_app/registrations.html', context_dict)


def user_login (request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use django's authentication fucntion. Look up, imported this.
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                # Log the user in using the imported login function
                login(request, user)
                # After logging in, send the user to someplace else. So redirect them back to homepage
                return HttpResponseRedirect(reverse('index'))
            else: #if account is not active
                return HttpResponse("ACCOUNT IS NOT ACTIVE!!!!!")

        else:
            print("Someone tried to login and failed!")
            print("Username: {} and password {}".format(username, password))
            return HttpResponse("invalid login details given")
    # Request.method was not POST, so this means the user did not actually submit anything
    else:
        return render(request, 'basic_app/login.html')
