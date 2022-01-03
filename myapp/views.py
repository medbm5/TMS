from django.shortcuts import render
import pandas as pd
# Create your views here.
from django.http import HttpResponse
import csv, io
from django.shortcuts import render
from django.contrib import messages
from .models import Profile
from .algo import get_bnb,get_NN,get_CW,get_RL

def index(request):
    return render(request,'myapp/index.html')

def results(request):
    return HttpResponse("Hello, world. You're at the results index.")


# Create your views here.
# one parameter named request
def profile_upload(request):
    algorithmID = str(request.POST["flexRadioDefault"])

    print('req',request.POST["flexRadioDefault"])
    # declaring template
    template = "index.html"
    data = Profile.objects.all()
# prompt is a context variable that can have different values      depending on their context
    prompt = {
        'order': 'Order of the CSV should be name, latitude, longitude',
        'profiles': data    
              }
    # GET request returns the value of the data with the specified key.
    if request.method == "GET":
        return render(request, 'myapp/results.html', prompt)
    
    csv_file = request.FILES['file']
    # let's check if it is a csv file
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')
    data_set = csv_file.read().decode('UTF-8')
    # setup a stream which is when we loop through each line we are able to handle a data in a stream
    io_string = io.StringIO(data_set)
    next(io_string)
    print('hello')
    location=[]
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        print(column)
        line={'latitude':column[0],'longitude':column[1]}
        location.append(line)
    df = pd.DataFrame(location) 
    print(df) 
    if(algorithmID)=="1":
        routes=get_CW(df)
        print('clarck and wright')
    elif(algorithmID=="2"):
        print('branch and bound')
        routes=get_bnb(df)
    elif(algorithmID=="3"):
        print('neres tneighbor')
        routes=get_NN(df)
    elif(algorithmID=="4"):
        print('rl')
        routes=get_RL(df)
    print(df) 
       
    return render(request, 'myapp/results.html', {'routes':routes})