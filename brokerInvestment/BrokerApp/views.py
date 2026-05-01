

from django.http import HttpResponse,JsonResponse
# from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.db.models import Q, F, Sum
import random, time, datetime, requests
from decimal import Decimal, InvalidOperation
from django.contrib.auth.hashers import make_password, check_password
from django.db import transaction
from . models import *

# for emails
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# Create your views here.

# deffine speruser function
def is_superuser(user):
    return user.is_superuser

# redirect user if not superuser
def CheckUser(view_func):
    decorated_view_funt= user_passes_test(
        is_superuser,
        login_url='dashboard',
        redirect_field_name=None
    )(view_func)
    return decorated_view_funt
    # user = request.user
    # if user.is_superuser:
    #     pass
    # return redirect('dashboard')

# for sending function
def SendMail(user):
    name = user
    email = user.email
    sender = 'sender@gmail.com'
    html_content = render_to_string(
        'extends/mail.html',
        {
            'name': name,
            'email': 'africeuros@gmail.com',
        }
    )
    message = EmailMultiAlternatives(
        subject = "Password Resting",
        body = html_content,
        from_email = sender,
        to = [f'{email}']
    )
    message.attach_alternative(html_content, 'text/html')
    message.send(fail_silently=False)

# sending otp code to the user email
def OTP(user):
    # for generation login otp code
    code = str(random.randint(0, 999999)).zfill(6)
    OTPCode.objects.create(
        otp=code,
        receiver=user
    )
    print('login code is', code)
    name = user
    email = user.email
    sender = 'sender@gmail.com'
    html_content = render_to_string(
        'extends/login-otp-mail.html',
        {
            'name': name,
            'email': 'africeuros@gmail.com',
            'code': code,
        }
    )
    message = EmailMultiAlternatives(
        subject = "Password Resting",
        body = html_content,
        from_email = sender,
        to = [f'{email}']
    )
    message.attach_alternative(html_content, 'text/html')
    message.send(fail_silently=False)

# generating transaction id no
def TransactID():
    code = str(random.randint(10, 99))
    transaction_id = str(code) + str(datetime.datetime.now())
    return transaction_id

# for generating account number
def AccountNo():
    uni = '1100'
    rand1 = str(random.randint(100000, 999999))
    acc_number = uni + rand1
    return acc_number


# logout function
def UserLogout(request):
    user = request.user
    if user.is_superuser:
        logout(request)
        return redirect("login")
    logout(request)
    return redirect("login")

# login user user out after 24 hours
def AutoLogout(request, timeout_day = 1):
    # timeout_minues = timeout_hour * 60 # for 12 hour
    timeout_minues = timeout_day * 24 * 60 # for 24 hour
    now = datetime.datetime.now()
    try:
        last_activity = request.session['last_activity']
        last_activity = datetime.datetime.fromisoformat(last_activity)
        if(now - last_activity).total_seconds() / 60 > timeout_minues:
            logout(request)
    except KeyError:
        pass
    # request.session['last_active']=datetime.datetime.now()
    request.session['last_activity'] = now.isoformat()

# login function
def UserLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # checking if user is super user or admin
            if user.is_superuser:
                # calling OPT functionn here
                # OTP(user)
                # loging in user after sending otp
                login(request, user)
                messages.success(request, f'{user.username}, Login successsfully')
                return redirect('adminPage')
            
            # for checking if user have verify his kyc
            profile = Profile.objects.get(user=user)
            if profile.kyc == False:
                # calling OPT functionn here
                # OTP(user)

                # loging in user after sending otp
                login(request, user)
                messages.info(request, f'{user.username}, verify you KYC')
                return redirect('kyc')
            # calling OPT functionn here
            # OTP(user)
            # loging in user after sending otp
            login(request, user)
            messages.success(request, f'{user.username}, Login successsfully')
            return redirect('dashboard')
        messages.error(request, 'Incorrect username or password, please try again')
        return redirect('login')
    context={}
    return render(request,"login.html",context)
    # return HttpResponse('welcome to django')

# user signup
def UserSignup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("mail")
        password2 = request.POST.get("password2")
        password1 = request.POST.get("password1")

        # calleing account number generator function
        acc_number = AccountNo()

        # verifing password
        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email have been used, try another email')
                return redirect("signup")
            profile = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password1,
            )
            Wallet.objects.create(
                user=profile,
                account_number=acc_number
            )
            Profile.objects.create(
                user=profile,
                # info=password1,
            )
            # calling sehding mail functionn here after creating account
            # SendMail(profile)
            messages.success(request, f'you successfully created new user account "{first_name}"')
            return redirect("login")
        messages.success(request, f'password and confirm password are not matching try again')
        return redirect("signup")
    return render(request,"signup.html")

# for getting coins info from coingecko api
def get_coins_info():
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 250,
        'page': 1,
        'sparkline': False
    }
    coins = []
    page = 1
    while True:
        params['page'] = page
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if not data:
                break
            coins.extend(data)
            page += 1
        else:
            break
    return coins

# for inex or landing page
def Index(request):
    coins = get_coins_info()
    context ={
        'coins': coins
    }
    return render(request, 'index.html', context)
    # return HttpResponse('welcome to django')

# for dashboard
@login_required(login_url='login')
def Dashboard(request):
    user = request.user
    # wallet = Wallet.objects.get(user=user)
    wallet, created = Wallet.objects.get_or_create(user=user)
    if wallet:
        balance = f"{wallet.balance:,}"
    profile = Profile.objects.get(user=user)
    # transactions = History.objects.filter( 
    #     Q(sender=user) & Q(receiver=user) 
    # )

    # Check if user has not set a pin
    investment = Investment.objects.filter( 
        Q(investor=user) & Q(due=False) 
    )
    if not wallet.pin:
        messages.warning(
            request, "You have not set your wallet pin yet. Please set it in your KYC before making any payments."
        )

    # call coins api function here
    coins = get_coins_info()[0:20]  # Get the first 20 coins
    context = {
        'balance': balance,
        'profile': profile,
        'coins': coins,
        # 'account_number': wallet.account_number,
        # 'total_investment': sum(int(amount.amount) for amount in investment),
        # 'investment_per': sum(int(invested.investment.interest) for invested in investment),
    }
    return render(request, 'dashboard/dashboard.html', context)

# fpr user profile
@login_required(login_url='login')
def UserProfile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    context = {
        'profile':profile,
    }
    return render(request, 'dashboard/profile.html', context)
    # return HttpResponse('welcome to django')

# for kyc
@login_required(login_url='login')
def KYC(request):
    wallet = Wallet.objects.get(user=request.user)
    balance = f"{wallet.balance:,}"
    user = request.user
    profile = Profile.objects.get(user=user)

    if request.method == 'POST':
        country = request.POST.get('country')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        date = request.POST.get('date')
        gender = request.POST.get('gender')

        pin = request.POST.get('pin')
        image = request.FILES.get('image')

        # verifing kyc data
        profile = Profile.objects.get(user=user)
        if profile:
            profile.country=country
            profile.phone_number=phone
            profile.address=address
            profile.kyc=True
            profile.gender=gender
            profile.date_birth=date
            # profile.profile_picture=image
            # profile.currency
            profile.save()
            messages.success(request, f'{user.username} your kyc have been varyfied')
            return redirect('kyc')
    context = {
        'balance':balance,
        'account_number':wallet.account_number,
        # 'user':user,
        'profile':profile,
    }
    return render(request, 'dashboard/kyc.html', context)
    # return HttpResponse('welcome to django')

@login_required(login_url='login')
def Settings(request):
    wallet = Wallet.objects.get(user=request.user)
    balance = f"{wallet.balance:,}"
    user = request.user
    profile = Profile.objects.get(user=request.user)
    context = {
        'balance':balance,
        'profile':profile,
    }
    return render(request, 'dashboard/setting.html', context)
    # return HttpResponse('welcome to django')

@login_required(login_url='login')
def Messages(request):
    user = request.user
    profile = Profile.objects.get(user=request.user)
    message = Message.objects.all().order_by('-id')
    context = {
        'profile':profile,
        'message': message,
    }
    return render(request, 'dashboard/message.html', context)
    # return HttpResponse('welcome to django')

@login_required(login_url='login')
def Coins(request):
    user = request.user
    profile = Profile.objects.get(user=request.user)

    # call coins api function here
    coins = get_coins_info()
    context = {
        'profile':profile,
        'coins': coins,
    }
    return render(request, 'dashboard/coins.html', context)
    # return HttpResponse('welcome to django')

@login_required(login_url='login')
def Investments(request):
    user = request.user
    profile = Profile.objects.get(user=request.user)
    plans = Plan.objects.all()
    context = {
        'profile':profile,
        'plans': plans,
    }
    return render(request, 'dashboard/investments.html', context)
    # return HttpResponse('welcome to django')

@login_required(login_url='login')
def Invest(request, pk):
    user = request.user
    profile = Profile.objects.get(user=user)
    plans = Plan.objects.all()

    wallet = Wallet.objects.get(user=user)
    plan = Plan.objects.get(id=pk)
    if plan:
        with transaction.atomic():
            if wallet.balance >= plan.amount:
                wallet.balance -= plan.amount
                wallet.save()
                Investment.objects.create(
                    investment=plan,
                    investor=user,
                    # amount=plan.amount,
                    due_time = plan.duration,
                )
                return render(request, 'extend/transaction_status.html', {
                    'status': 'success',
                    'amount': plan.amount,
                    'reciever': user,
                })
            return render(request, 'extend/transaction_status.html', {
                'status': 'warning',
                'message': 'Invalid amount.',
            })
    context = {
        'profile':profile,
        'plans': plans,
    }
    return render(request, 'dashboard/investments.html', context)
    # return HttpResponse('welcome to django')

@login_required(login_url='login')
def History(request):
    user = request.user
    profile, _ = Profile.objects.get_or_create(user=user)

    investment = Investment.objects.filter(investor=user)
    active_investment = investment.filter(due=False, investor=user)

    active_total = active_investment.aggregate(total=Sum('amount'))['total'] or 0
    total_total = investment.aggregate(total=Sum('amount'))['total'] or 0

    context = { 
        'profile': profile, 
        'investment': investment,
        'active_investment': active_total,
        'total_investment': total_total,
    } 

    return render(request, 'dashboard/history.html', context)

@login_required(login_url='login')
def Asset(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    wallet = Wallet.objects.get(user=user)
    balance = f"{wallet.balance:,}"

    history = Trasaction.objects.filter(
        Q(sender=user) | Q(receiver=user)
    ).order_by('-created_at')

    context = { 
        'profile': profile,
        'balance': balance,
        'history': history,
    } 
    return render(request, 'dashboard/asset.html', context)

@login_required(login_url='login')
def Fund(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    account = Account.objects.all()[:10]
    users = User.objects.filter(is_superuser=True)

    if request.method == "POST":
        amount = request.POST.get('amount')
        name = request.POST.get('name')
        address = request.POST.get('address')
        id = TransactID()

        # Validate amount
        try:
            amount = Decimal(amount)
        except:
            return render(request, 'extend/transaction_status.html', {
                'status': 'warning',
                'message': 'Invalid amount format.',
            })

        wallet = Wallet.objects.get(user=user)

        with transaction.atomic():
            if wallet.balance >= amount and amount > 0:
                wallet.balance -= amount
                wallet.save()

                Trasaction.objects.create(
                    account_number=address,
                    receiver_id=name,
                    sender=user,
                    amount=amount,
                    status='pending',
                    transaction_id=id,
                    user=user,
                )

                return render(request, 'extend/transaction_status.html', {
                    'status': 'pending',
                    'amount': amount,
                    'reciever': user,
                })
            else:
                return render(request, 'extend/transaction_status.html', {
                    'status': 'warning',
                    'message': 'Insufficient balance or invalid amount.',
                })

    context = {
        'profile': profile,
        'account': account,
        'users': users,
    }

    return render(request, 'dashboard/funds.html', context)

@login_required(login_url='login')
def Payment(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    payments = UserAccount.objects.filter(user=user)
    account = Account.objects.all()

    if request.method == 'POST':
        address = request.POST.get('address')
        address_name = request.POST.get('address_name')
        receiver_name = request.POST.get('receiver_name')
        UserAccount.objects.create(
            address = address,
            address_name = address_name,
            receiver_name = receiver_name,
            user = user,
        )
        messages.success(request, 'account was added successfully')
        return redirect('payment')
    
    context = { 
        'profile': profile, 
        'payments': payments,
        'account': account,
    }
    return render(request, 'dashboard/payments.html', context)

@login_required(login_url='login')
def DeleteUserAccount(request,pk):
    account = UserAccount.objects.get(id=pk)
    if account:
        account.delete()
        messages.success(request, 'account was deleted successfully')
        return redirect('newAccount')

# for admin
@login_required(login_url='login')
@CheckUser
def AdminPage(request):
    profile = request.user
    plan = Plan.objects.all()
    account = Account.objects.all()
    users = Wallet.objects.all()
    context = {
        'users':users,
        'profile': profile,
        'plan':plan,
        'account':account,
    }
    return render(request, 'admin/users.html', context)

@login_required(login_url='login')
@CheckUser
def Search(request):
    user = None

    if request.method == 'POST':
        query = request.POST.get('query','')
        user = Wallet.objects.filter(
            Q(account_number__icontains=query) |
            Q(user__username__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        )

    context = {
        'query': user,
    }
    return render(request, 'admin/search.html', context)

@login_required(login_url='login')
@CheckUser
def ViewUser(request,pk):
    user = get_object_or_404(User, id=pk)

    wallet = Wallet.objects.get(user=user)
    investments = Investment.objects.filter(
        Q(investor=user) # | Q(receiver=useraccount) 
    )

    profile = Profile.objects.get(user=user)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "balance":
            return redirect("addBalance", pk=wallet.user.id)

        # elif action == "investment":
        #     return redirect("investments")

        elif action == "reset":
            wallet.balance = 0
            wallet.save()

        elif action == "block":
            profile.block = True
            profile.save()

        elif action == "delete":
            profile.delete()
    context = {
        'wallet':wallet,
        'investments':investments,
    }
    return render(request, 'admin/userprofile.html', context)

@login_required(login_url='login')
@CheckUser
def AddBalance(request, pk):
    user = get_object_or_404(User, id=pk)
    wallet, _ = Wallet.objects.get_or_create(user=user)

    if request.method == 'POST':
        balance = request.POST.get('amount')

        try:
            amount = Decimal(balance)
            if amount <= 0:
                messages.error(request, "Amount must be greater than 0")
                return redirect('addBalance', pk=user.id)

        except (InvalidOperation, TypeError):
            messages.error(request, "Invalid amount entered")
            return redirect('addBalance', pk=user.id)

        wallet.balance += amount
        wallet.save()

        messages.success(request, "Balance updated successfully")
        return redirect('addBalance', pk=user.id)

    return render(request, 'admin/addbalance.html', {
        'wallet': wallet,
    })

# @login_required(login_url='login')
# @CheckUser
# def DeleteUser(request,pk):
#     useraccount = User.objects.get(id=pk)
#     if useraccount:
#         useraccount.delete()
#         messages.success(request, f'{useraccount.username}, was deleted')
#         return redirect('adminPage')

# @login_required(login_url='login')
# @CheckUser
# def BlockUser(request,pk):
#     useraccount = User.objects.get(id=pk)
#     profile = Profile.objects.get(user=useraccount)
#     if profile.block:
#         profile.block = False
#         profile.save()
#         messages.success(request, f'{useraccount.username}, accoun was unblock')
#         return redirect('viewUser', pk=useraccount.id)
#     profile.block = True
#     profile.save()
#     messages.success(request, f'{useraccount.username}, accoun was block')
#     return redirect('viewUser', pk=useraccount.id)
        
# @login_required(login_url='login')
# @CheckUser
# def ClearBalace(request,pk):
#     useraccount = User.objects.get(id=pk)
#     wallet = Wallet.objects.get(user=useraccount)
#     if wallet:
#         wallet.balance = 0
#         wallet.save()
#         return redirect('viewUser', pk=wallet.user.id)

@login_required(login_url='login')
@CheckUser
def ViewUserInvestment(request,pk):
    user = get_object_or_404(User, id=pk)
    wallet = Wallet.objects.get(user=user)
    balance = f"{wallet.balance:,}"
    investment = Investment.objects.filter(investor=user)

    dueinvestment = Investment.objects.filter( 
        Q(investor=user) & Q(due=False) 
    )

    total_investment = dueinvestment.aggregate(total=Sum('amount'))['total'] or 0
    investment_per = dueinvestment.aggregate(total=Sum('investment__interest'))['total'] or 0

    context = {
        'balance': balance,
        'account_number': wallet.account_number,
        'investment':investment,
        'total_investment': total_investment,
        'investment_per': investment_per,
    }
    return render(request, 'admin/userInvestment.html', context)

@login_required(login_url='login')
@CheckUser
# def AddPercent(request, pk):
#     investment = get_object_or_404(Investment, id=pk)

#     user = investment.investor
#     wallet = get_object_or_404(Wallet, user=user)

#     rate = investment.investment.interest

#     # profit based on PLAN %
#     profit = (investment.amount * rate) / 100

#     investment.amount += profit
#     investment.days_count += 1
#     investment.save()

#     wallet.balance += profit
#     wallet.save()

#     if investment.days_count >= investment.due_time:
#         investment.due = True
#         investment.save()

#     return redirect('viewUser', pk=user.id)
def AddPercent(request,pk): 
    investment = Investment.objects.get(id=pk) 
    user = User.objects.get(id=investment.investor.pk)
    wallet = get_object_or_404(Wallet, user=user)
    if investment: 
        # for adding percent to user inestment balance 
        investment.amount += Decimal(investment.investment.interest) 
        investment.days_count += 1 
        investment.save()
        # for adding percent to user wallet balance 
        wallet.balance += Decimal(investment.investment.interest) 
        wallet.save() 
        if investment.days_count == investment.due_time: 
            investment.due = True 
            investment.save() 
    return redirect('viewUser', pk=investment.investor.id)

@login_required(login_url='login')
@CheckUser
def NewInvestment(request):
    investments = Plan.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        interest = request.POST.get('pacent')
        amount = request.POST.get('price')
        duration = request.POST.get('duration')
        Plan.objects.create(
            amount = Decimal(amount),
            name = name,
            interest = Decimal(interest),
            duration = duration,
        )
        messages.success(request, 'investment plan was created successfully')
        return redirect('newInvestment')
    context = {
        'investments':investments,
    }
    return render(request,'admin/createinvestment.html',context)

@login_required(login_url='login')
@CheckUser
def DeleteInvestment(request,pk):
    investment = Plan.objects.get(id=pk)
    if investment:
        investment.delete()
        messages.success(request, 'investment plan was deleted successfully')
        return redirect('newInvestment')
    
@login_required(login_url='login')
@CheckUser
def NewAccount(request):
    account = Account.objects.all()
    if request.method == 'POST':
        address = request.POST.get('address')
        address_name = request.POST.get('address_name')
        receiver_name = request.POST.get('receiver_name')
        Account.objects.create(
            address = address,
            address_name = address_name,
            receiver_name = receiver_name,
        )
        messages.success(request, 'account was added successfully')
        return redirect('newAccount')
    context = {
        'account':account,
    }
    return render(request,'admin/newaccount.html',context)

@login_required(login_url='login')
@CheckUser
def DeleteAccount(request,pk):
    account = get_object_or_404(Account, id=pk)
    if account:
        account.delete()
        messages.success(request, 'account was deleted successfully')
        return redirect('newAccount')
@login_required(login_url='login')
@CheckUser
def UserHistory(request,pk):
    user = get_object_or_404(User, id=pk)

    wallet = Wallet.objects.get(user=user)
    history = Trasaction.objects.filter(
        Q(sender=user) | Q(receiver=user)
    ).order_by('-created_at')

    profile = Profile.objects.get(user=user)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "balance":
            return redirect("addBalance", pk=wallet.user.id)

        # elif action == "investment":
        #     return redirect("investments")

        elif action == "reset":
            wallet.balance = 0
            wallet.save()

        elif action == "block":
            profile.block = True
            profile.save()

        elif action == "delete":
            profile.delete()
    context = {
        'wallet':wallet,
        'history':history,
    }
    return render(request, 'admin/userhistory.html', context)

@login_required(login_url='login')
@CheckUser
def ApprovePayment(request, pk):
    history = get_object_or_404(Trasaction, id=pk)

    # user = get_object_or_404(User, id=pk)

    if history.paid == False:
        history.paid = True
        history.status = 'Success'
        history.save()

    return redirect('userhistory', pk=history.user.id)

