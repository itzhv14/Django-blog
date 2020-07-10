from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required


# Create your views here.
def register(request):
	if (request.method == 'POST'):
		form = UserRegisterForm(request.POST)
		# request.POST to pass the typed data to form
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f"Your account has been created, Please Login!")
			return redirect('login')
		else:
			print("adasdas")
	else:
		form = UserRegisterForm()
		print("eeeerrrorrrr")
	return render (request, 'users/register.html', {'form': form})


@login_required
def profile(request):
	if (request.method == 'POST'):
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		# request.POST to pass the typed data to form
		# instance is added to populate the form with the previous data
		# request.FILES for file data i.e. image is to be uploaded
		if p_form.is_valid() and u_form.is_valid():
			p_form.save()
			u_form.save()
			messages.success(request, f"Your profile has been updated!")
			return redirect('profile')
			
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)

	context = {
		'u_form': u_form,
		'p_form': p_form
	}
	return render(request, 'users/profile.html', context)








# for flashing messeges after login and logout

from django.contrib.auth.signals import user_logged_out, user_logged_in 
from django.dispatch import receiver

@receiver(user_logged_out)
def on_user_logged_out(sender, request, user, **kwargs):
    if user:
        msg = f'You have securely logged out {user.username}. Thank you for visiting.'
    else:
        msg = 'You have securely logged out. Thank you for visiting.'
    messages.add_message(request, messages.INFO, msg)

@receiver(user_logged_in)
def on_user_logged_in(sender, request, user, **kwargs):
    if user:
        msg = f'You have successfully logged in as {user.username}.'
    else:
        msg = 'You have successfully logged in.'
    messages.add_message(request, messages.SUCCESS, msg)