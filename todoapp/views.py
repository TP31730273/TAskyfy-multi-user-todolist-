from django.db import connections
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from .models import *
from random import randint
import datetime
default_data = {
    'form_membership': ['login', 'register', 'reset_pass'],

}

# serialize function 

def seri(model_object):
    d={}
    for k,v in model_object.__dict__.items():
        if k.startswith('_') or k.endswith('_'):
            continue
        d.setdefault(k,v)
    return d

def login(request):
    if 'email' in request.session:
        return redirect(profile)
    
    default_data['current_page'] = 'login'
    return render(request, 'todoapp/login.html', default_data)


def index(request):
    return redirect(login)


def register(request):
    default_data['current_page'] = 'register'
    return render(request, 'todoapp/register.html', default_data)


def reset_pass(request):
    default_data['current_page'] = 'reset_pass'
    return render(request, 'todoapp/recovery-password.html', default_data)

# profile data
def profile_data(request):
    master= Master.objects.get(Email=request.session['email'])
    profile=Profile.objects.get(Master= master)
    
    
    load_connection(request)    
    load_todo(request)
    
    try:
        pr=profile_pic.objects.get(Master=master)
        show_pic(request)
        all_pics(request)
    except:
        print("You don't have profile picture")
    
    default_data['profile_data']=seri(profile)
    default_data['gender_choice']=[{'short_val': i, 'text' : j} for i,j in choice_gender]

# profile page

def profile(request):
    profile_data(request)
    default_data['current_page'] = 'profile'
    return render(request, 'todoapp/profile.html', default_data)
# update profile data 

def profile_update(request):
    master= Master.objects.get(Email=request.session['email'])
    profil=Profile.objects.get(Master= master)
    profil.FullName=request.POST['fname']
    profil.Mobile=request.POST['phone']
    profil.Gender=request.POST['gender']
    x=request.POST['dob']
    
    # j=x.split('/')
    # t=str(j[2])+'-'+str(j[0])+'-'+str(j[1])
    
    # profil.Birthdate=x
    profil.City=request.POST['city']
    profil.State=request.POST['state']
    profil.Country=request.POST['country']
    profil.Address=request.POST['address']
    profil.save()

    profile_data(request)
    default_data['t']=x
    return JsonResponse(default_data)

# change password
def change_password(request):
    master= Master.objects.get(Email=request.session['email'])
    old_pwd=request.POST['old_password']    
    new_pwd=request.POST['new_password']    
    if master.Password == old_pwd:
        master.Password = new_pwd
        master.save()
        print("password change successfully ")
        return redirect(profile)
    else:
        msg="password incorrect please enter again"
        print(msg)
        del request.session['email']
        return redirect(login)


# register data

# create reference id

def reg_data(request):
    master = Master.objects.create(Email=request.POST['email'],Password=request.POST['password'])

    ref_id=f"{request.POST['email'].split('@')[0]}{randint(1000,9999)}"
    print("reference id: ",ref_id)
    Profile.objects.create(Master=master,RefID=ref_id)
    print("user registrated sussessfully")
    return redirect(register)
    
    

# login functionality

def login_data(request):
    eml=request.POST['email']
    password=request.POST['password']
    
    try:
        master= Master.objects.get(Email=eml)
        if master.Password == password:
            request.session['email']=eml
            print("login sucess",master)
            return redirect(profile)
        else:
            msg="Username of password incorrect please enter again"
            print(msg)
           
    except Master.DoesNotExist:
        print(f"{eml} does not exist please register it.")
    return redirect(login)




# ---------------------connections view------------------------------------------------------#

# search reference

def search_ref(request):
    profile= Profile.objects.get(RefID=request.POST['refid'])
    default_data['ref_data']= seri(profile)
    default_data['msg']='reference succcessfully found'
    return JsonResponse(default_data)
    
 
# request new connection

def request_connection(request):
    master= Master.objects.get(Email=request.session['email'])
    profile= Profile.objects.get(RefID=request.POST['refid'])
    
    connection.objects.create(Master=master, Profile=profile)


# load connection

def load_connection(request):
    master= Master.objects.get(Email=request.session['email'])
    Connections=connection.objects.filter(Master=master)
    
    for i in Connections:
        name=i.profile.FullName.split()
        if len(name)>1:
            i.profile.short_name= f"{name[0][0]}{name[1][0]}"
        else:
            i.profile.short_name= f"{name[0][0]}"

    print(Connections)
    default_data['myconnections']=Connections
    
# add new connection
def add_connection(request):
    master= Master.objects.get(Email=request.session['email'])
    profile= Profile.objects.get(Master=master)

    Connection=connection.objects.get(Profile=profile)
    Connection.status = 'active'


# ---------------------Todo  view------------------------------------------------------#


# create todo
def create_todo(request):
    master= Master.objects.get(Email=request.session['email'])  
    profile_obj= Profile.objects.get(Master=master)
    print(request.POST['todo_deadline'])
    print(request.POST['todo_time'])
    dat=request.POST['todo_deadline'].split('-')
    print(dat)
    tim=request.POST['todo_time'].split(':')
    print(tim)

    day=int(dat[2])
    month=int(dat[1])
    year=int(dat[0])
    hrs=int(tim[0])
    minit=int(tim[1])
    date_time=datetime.datetime(year,month,day,hrs,minit)
    todo=ToDo.objects.create(master=master,Title=request.POST['title'],Tags=request.POST['tags'],Deadline=date_time,Description=request.POST['todo_description'])
    todo.save()

    if 'participate' in request.POST:
        participate=request.POST.getlist('participate')
        for p in participate:
            con=connection.objects.get(id=int(p))
            ToDoMember.objects.create(
                todo=todo,
                profile=Profile.objects.get(id=con.profile.id)
            )

    # if request.POST['members']:
    #     todo.Profile
    load_todo(request)
    return redirect(profile)


# remove todo

def remove_todo(request,pk):
    ToDo.objects.get(id=pk).delete()
    return redirect(profile)
    
# load Todo and members

def load_members(request):
    master= Master.objects.get(Email=request.session['email'])
    todo= ToDo.objects.get(Master=master)
    todo_members=ToDoMember.objects.filter(ToDo=todo)
    default_data['todo_members']=todo_members
    

# name shortner
def shortner(obj):
    obj = obj.split()
    if len(obj) > 1:
        print("data: ", obj)
        return f"{obj[0][0]}{obj[1][0]}"
    else:
        return f"{obj[0][0]}"

# load todo

def load_todo(request):
    master= Master.objects.get(Email=request.session['email'])
    my_todo= ToDo.objects.filter(master=master)

    default_data['my_todo']=[]

    for i in my_todo:
        i.Date= i.Deadline.strftime("%m/%d/%Y")
        i.Time= i.Deadline.strftime("%X")[:-3]
        members = ToDoMember.objects.filter(todo = i)

        for m in members:
            m.Profile.SortName = shortner(m.Profile.FullName)

        default_data['my_todo'].append({
            'todo':i,
            'members':members,
        })
       
    default_data['my_todo'] = default_data['my_todo'][::-1]
    print(default_data['my_todo'])  
    
    # default_data['todo_members']=todo_members


# ------------upload image-----------------------------------#
def upload_image(request):
    img=request.FILES['imag']
    master= Master.objects.get(Email=request.session['email'])
    try:
        proff=profile_pic.objects.get(Master=master)
        if proff:
            proff.delete()
      
        pro=profile_pic.objects.create(Master=master,Img=img)
        pro.save()
    except:
        pro=profile_pic.objects.create(Master=master,Img=img)
        pro.save()
    return redirect(profile)

#--------------- show profile picture-------------#
def show_pic(request):
    master= Master.objects.get(Email=request.session['email'])
    prof=profile_pic.objects.get(Master=master)
    
    default_data['profile_pic']=prof


#--------------- show all pictures-------------#

def all_pics(request):
    prof=profile_pic.objects.all()
    default_data['all_pics']=prof

# ---------------------sign out view------------------------------------------------------#

# sign-out
def sign_out(request):
    if 'email' in request.session:
        print("deleted : ",request.session['email'])
        del request.session['email']
    
    return redirect(login)
    
