from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .forms import RegistrationForm
from .models import user

# Create your views here.
def home(request):
    return render(request,'home.html')

def login(request):
    return render(request,'login.html')

@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! You can now login.')
            return redirect('login')
        else:
            # Pass form with errors back to template
            return render(request, 'register.html', {'form': form})
    else:
        form = RegistrationForm()
        return render(request, 'register.html', {'form': form})

def admin_dashboard(request):
    return render(request,'admin.html')

def user_dashboard(request):
    return render(request,'dashboard.html')

def view_contracts(request):
    return render(request,'viewContracts.html')

def upload_contract(request):
    return render(request,'uploadContract.html')

def send_complaint(request):
    return render(request,'complaint.html')

def feedback(request):
    return render(request,'feedback.html')