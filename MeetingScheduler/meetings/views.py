from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from .models import clients, Meeting,Owner
import threading
import random


#  Send email verification
def send_verification_email(name, email, verification_code):
    subject = 'Account Verification Code'
    message = f"""
Dear {name},

Thank you for signing up with Accounting and Tax Services!

To complete your registration, please use the verification code below:

🔐 Verification Code: {verification_code}

If you didn't request this, please ignore this email.

Regards,  
Team Accounting and Tax Services
"""
    send_mail(
        subject=subject,
        message=message,
        from_email='projectdjango069@gmail.com',
        recipient_list=[email],
        fail_silently=False,
    )


#  Signup View
def signup(request):
    if request.method == 'POST':
        if 'code' in request.POST:
            entered_code = request.POST['code']
            session_code = request.session.get('verification_code')

            if entered_code == session_code:
                name = request.session.get('temp_name')
                email = request.session.get('temp_email')
                password = request.session.get('temp_password')
                code = session_code

                clients.objects.create(name=name, email=email, password=password, code=code)

                for key in ['verification_code', 'temp_name', 'temp_email', 'temp_password']:
                    request.session.pop(key, None)

                messages.success(request, "Signup successful! Please login.")
                return redirect('login')
            else:
                return render(request, 'Signup.html', {
                    'show_code_input': True,
                    'message': 'Invalid verification code!',
                    'name': request.session.get('temp_name'),
                    'email': request.session.get('temp_email')
                })

        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        verification_code = str(random.randint(100000, 999999))

        request.session['temp_name'] = name
        request.session['temp_email'] = email
        request.session['temp_password'] = password
        request.session['verification_code'] = verification_code

        threading.Thread(target=send_verification_email, args=(name, email, verification_code)).start()

        return render(request, 'Signup.html', {
            'show_code_input': True,
            'message': 'Verification code sent to your email.',
            'name': name,
            'email': email
        })

    return render(request, 'Signup.html')


#  Login View

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Try Client Login First
        try:
            client = clients.objects.get(email=email)
            if client.password == password:
                request.session['client_id'] = client.id
                request.session['client_name'] = client.name
                return redirect('dashboard')
            else:
                messages.error(request, 'Incorrect password.')
                return render(request, 'login.html')
        except clients.DoesNotExist:
            pass  # Not a client, check owner

        # Try Owner Login
        try:
            owner = Owner.objects.get(email=email)
            if owner.password == password:
                request.session['owner_id'] = owner.id
                request.session['owner_name'] = owner.name
                return redirect('meeting_status')
            else:
                messages.error(request, 'Incorrect password.')
        except Owner.DoesNotExist:
            messages.error(request, 'Email not registered.')

    return render(request, 'login.html')




#  Logout View
@login_required(login_url='/login/')
def logout(request):
    request.session.flush()
    return redirect('login')


#  Dashboard
def dashboard(request):
    if 'client_id' not in request.session:
        return redirect('login')  # Prevents redirect loop
    return render(request, 'dashboard.html')



#  Book Meeting (Client)
def book_meeting(request):
    if request.method == 'POST':
        client_id = request.session.get('client_id')
        if not client_id:
            return redirect('login')

        client = clients.objects.get(id=client_id)

        #  Step 1: Get an existing owner
        owner = Owner.objects.first()
        if not owner:
            messages.error(request, "No owner found to assign the meeting.")
            return redirect('dashboard')

        #  Step 2: Collect meeting data
        reg_no = request.POST['reg_no']
        meeting_type = request.POST['meeting_type']
        date = request.POST['date']
        time = request.POST['time']
        print("OWNER:", owner)  # Debug print
        print("OWNER ID:", owner.id)
        #  Step 3: Create meeting with owner
        Meeting.objects.create(
            client=client,
            owner=owner,
            reg_no=reg_no,
            meeting_type=meeting_type,
            date=date,
            time=time
        )

        messages.success(request, "Meeting booked successfully.")
        return redirect('dashboard')

    return render(request, 'book_meeting.html')
 
#  Show All Meetings (Manager/Owner)
def meeting_status(request):
    if 'owner_id' not in request.session:
        return redirect('login')

    owner_id = request.session['owner_id']
    meetings = Meeting.objects.filter(owner_id=owner_id)

    return render(request, 'meeting_status.html', {'meetings': meetings})