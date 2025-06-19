from django.shortcuts import render, redirect
from .models import clients
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.core.mail import send_mail
import random
import threading
from django.contrib.auth.decorators import login_required

def send_verification_email(email, verification_code):
    send_mail(
        subject='Your Student Signup Verification Code',
        message=f'Your verification code is: {verification_code}',
        from_email='your_email@gmail.com',
        recipient_list=[email],
        fail_silently=False,
    )

def signup(request):
    if request.method == 'POST':
        # STEP 2: Verify code
        if 'code' in request.POST:
            entered_code = request.POST['code']
            session_code = request.session.get('verification_code')

            if entered_code == session_code:
                # Code correct, create student
                name = request.session.get('temp_name')
                email = request.session.get('temp_email')
                password = request.session.get('temp_password')
                code = request.session.get('verification_code')

                clients.objects.create(name=name, email=email, password=password, code=code)

                # Clear temp session data
                for key in ['verification_code', 'temp_name', 'temp_email', 'temp_password']:
                    request.session.pop(key, None)

                messages.success(request, "Signup successful! Please login.")
                return redirect('login')
            else:
                return render(request, 'signup_here.html', {
                    'show_code_input': True,
                    'message': 'Invalid verification code!',
                    'name': request.session.get('temp_name'),
                    'email': request.session.get('temp_email')
                })

        # STEP 1: Initial form submission
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']

        verification_code = str(random.randint(100000, 999999))

        request.session['temp_name'] = name
        request.session['temp_email'] = email
        request.session['temp_password'] = password
        request.session['verification_code'] = verification_code

        threading.Thread(target=send_verification_email, args=(email, verification_code)).start()

        return render(request, 'signup.html', {
            'show_code_input': True,
            'message': 'Verification code sent to your email.',
            'name': name,
            'email': email
        })

    return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            client = clients.objects.get(email=email)
            if client.password == password:
                # Save login state in session
                request.session['client_id'] = client.id
                request.session['client_name'] = client.name
                return redirect('dashboard')  # Redirect to a dashboard or homepage
            else:
                messages.error(request, 'Incorrect password.')
        except clients.DoesNotExist:
            messages.error(request, 'Email not registered.')

    return render(request, 'login.html')



@login_required(login_url='/login/')
def logout(request):
    request.session.flush()
    return redirect('login')