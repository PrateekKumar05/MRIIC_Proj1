from django.shortcuts import render
from django.http import HttpResponse
from .models import blog_category, contact_info, Subscription
from .forms import Blog_Form, CommentForm, blog_post_form
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from .models import blog_post, Comment
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone 

# Create your views here.
def home(request):
    # return HttpResponse('<h1>this is the home page</h1>')
    #fetch the data from db
    x=blog_category.objects.all()
    # print (x)
    return render(request, 'myblogs/home.html',{"category":x})

def findproduct(request):
    if request.method =="POST":
        x= request.POST.get('prod_search')
        # print(x)
        mydata = blog_category.objects.filter(Q(blog_cat__icontains = x))
        #print(mydata)
        if mydata:
            return render(request,'myblogs/home.html', {'category':mydata})
        else:
            return render(request,'myblogs/home.html', {'warning':"No Match Found"})
        
def contact(request):
    # return HttpResponse('<h1>this is the contact page</h1>')
    if request.method == 'GET':
        return render(request, 'myblogs/contact.html')
    elif request.method == 'POST':
        email = request.POST.get('user_email')
        message = request.POST.get('message')
        x = contact_info(u_email=email, u_message=message)
        x.save()
        print(email)
        print(message)
        return render(request,'myblogs/contact.html',{'feedback':'Your message has been recorded'})
    
def subscription(request):
    if request.method == 'GET':
        return render(request, 'myblogs/subscription.html')
    elif request.method == 'POST':
        email = request.POST.get('u_email')
        membership = request.POST.get('u_membership')
        x = Subscription(u_email=email, u_membership=membership)
        if(Subscription.objects.filter(u_email = email).exists()):
          return render(request, 'myblogs/subscription.html', {'feedback' : "You are already a subscribed user!!"})  
        else:    
            x.save()
            print(x)
            print(email)
            print(membership)
            return render(request, 'myblogs/subscription.html', {'feedback' : "Thanks for Subscribing!!"})
    
@login_required(login_url='loginuser')
def blog(request):
    x = blog_post_form()
    if request.method == "GET":
        return render(request,'myblogs/blog.html',{"x":x})
    else:
        print("hi")
        form = blog_post_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print("hi")
            return redirect('home')
        else:
            return render(request,'myblogs/blog.html',{"x":x})  
        
@login_required(login_url='loginuser')        
def allblogs(request):
    y = blog_post.objects.all()
    paginator = Paginator(y, 3)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return render(request,"myblogs/allblogs.html",{"y": page_obj})

def blog_details(request,blog_id):
    obj = get_object_or_404(blog_post, pk=blog_id)
    z = obj.views_count
    z=z+1
    obj.views_count = z
    obj.save()
    print(blog_id)
    print(obj)
    form = CommentForm()
    return  render(request, 'myblogs/blog_details.html',{"obj":obj, "form":form})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'myblogs/loginuser.html', {'form':AuthenticationForm()})
    else:
        a = request.POST.get('username')
        b = request.POST.get('password')
        user = authenticate(request, username=a, password=b)
        if user is None:
            return render(request,'myblogs/loginuser.html', {'form':AuthenticationForm(), 'error':'Invalid Credentials'})
        else:
            login(request, user)
            return redirect('home')


def signupuser(request):
        if request.method == 'GET':
            return render(request, 'myblogs/signupuser.html', {'form':UserCreationForm()})
        else:
            a = request.POST.get('username')
            b = request.POST.get('password1')
            c = request.POST.get('password2')
            if b==c:
                #Check whether user name is unique
                if (User.objects.filter(username = a)):
                    return render(request, 'myblogs/signupuser.html', {'error':'Username Already Exists Try again with different username'})
                else:
                    user = User.objects.create_user(username = a, password=b)
                    user.save()
                    login(request,user)
                    return redirect('home')
            else:
                return render(request, 'myblogs/signupuser.html', {'form':UserCreationForm(), 'error':'Password Mismatch Try Again'})
       
def logoutuser(request):
    if request.method == 'GET':
        logout(request)
        return redirect('home')
    
def blog_cat(request, blog_cat):
    # print(blog_cat)
    x = blog_category.objects.get(blog_cat= blog_cat)
    a = blog_post.objects.filter(blog_cat=x)
    paginator = Paginator(a, 3)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request,'myblogs/allblogs.html',{"y": page_obj})
    # return HttpResponse('blog_details')

def add_likes(request, blog_id):
    obj = get_object_or_404(blog_post, pk=blog_id)
    print(obj.like_count)
    y = obj.like_count
    y=y+1
    obj.like_count = y
    obj.save()   
    return redirect('blog_details', obj.id)

def add_comment(request, blog_id):
    post = get_object_or_404(blog_post, pk=blog_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.created_at = timezone.now()  # Add this line to save the current timestamp
            comment.save()
            return redirect('blog_details', blog_id=post.id)

def delete_comment(request, blog_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    return redirect( 'blog_details', blog_id=blog_id)

def edit_comment(request, blog_id, comment_id):
    # Retrieve the comment object
    comment = Comment.objects.get(id=comment_id)
    
    if request.method == 'POST':
        # Process the form submission
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog_details', blog_id=blog_id)
    else:
        # Populate the form with existing comment data
        form = CommentForm(instance=comment)
    
    return render(request, 'myblogs/edit_comment.html', {'form': form})