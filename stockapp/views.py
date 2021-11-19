from threading import Thread

from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from yahoo_fin.stock_info import *  #using yahoo_fin library for stock data
import time
import queue

# Create your views here.
def home(request):
    return render(request,'stockapp/index.html')


def signup(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # backend validation
        if not uname.isalnum():
            messages.error(request,'Please enter alphanumeric username')
            return redirect('home')

        if User.objects.filter(username = uname):
            messages.error(request, 'Username is already exist, please select another usrename')
            return redirect('home')

        if len(uname)>10:
            messages.error(request, 'Please maintain username length less than 10')
            return redirect('home')

        if User.objects.filter(email = email):
            messages.error(request, 'Email already exist, please select another email')
            return redirect('home')

        if pass1 != pass2:
            messages.error(request, 'Password doesn\'t match' )
            return redirect('home')

        myuser = User.objects.create_user(uname,email,pass1) #creating user
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save() #user details have been saved inside DB
        messages.success(request, 'User has been successfully created')
        return redirect('signin') # after successfully user creation, redirect user to Signin page

    return render(request,'stockapp/signup.html')

def signin(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        pass1 = request.POST['pass1']

        #validating user
        myuser =authenticate(username = uname, password = pass1)

        if myuser is not None:
            login(request,myuser)
            fname = myuser.first_name
            messages.success(request, 'you have successfully logged in')
            return redirect('stockpicker')
            #return render(request,'stockapp/stockpicker.html',{'fname':fname,'user':myuser })
            #return render(request,'stockapp/index.html',{'fname':fname,'user':myuser })
        else:
            messages.error(request, 'Failed to login')
            return redirect('signin')
    return render(request, 'stockapp/signin.html')

def signout(request):
    logout(request)
    messages.success(request, 'Successfully singout')
    return redirect('stockpicker')

def stockPicker(request):
    stock_picker = tickers_nifty50()
    print(stock_picker)
    return render(request, 'stockapp/stockpicker.html',{'stockpicker': stock_picker})

def stockTracker(request):
    details = get_quote_table('RELIANCE.NS')
    print(details)
    stockpicker = request.GET.getlist('stockpicker')
    data = {}
    availabke_stocks = tickers_nifty50() #gives list of nifty50 stocks name
    #check if user selected stock is available in Nifty50 list
    for i in stockpicker:
        if i in availabke_stocks:
            pass
        else:
            return HttpResponse('Error')
    start = time.time()

    #fetching stock specific details base on our selected stocks
    #achieve this task using thread
    '''
    n_threads = len(stockpicker)
    thread_list = []
    que = queue.Queue()
    for i in range(n_threads):
        thread = Thread(target = lambda q, args1: q.put({stockpicker[i] : get_quote_table(args1)}, args = (que, stockpicker[i])))
        thread_list.append(thread)
        thread_list[i].start()

    for thread in thread_list:
        thread.join()

    while not que.empty():
        result = que.get()
        data.update(result)
        '''
    for i in stockpicker:
        result = get_quote_table(i)
        data.update({i: result})
    end = time.time()
    time_taken = end - start
    print('Time taken: ',time_taken)
    print(data)

    return render(request,'stockapp/stocktracker.html', {'data': data})
#KNC5088ES4H64X13