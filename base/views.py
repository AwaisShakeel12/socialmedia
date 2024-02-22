from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth import login, logout,  authenticate
from django.contrib import messages
from .models import *
from django.db.models import Q


# Create your views here.

def startpage(request):
    return render(request, 'base/startpage.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password1 = request.POST['password1']

        if password == password1:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'username already exsist')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password)
                user.save()

                user_login= auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user= user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('home')
        else:        
            messages.info(request, 'invalid data')
            return redirect('register')
        
    # context = {'messages':messages}


    return render(request, 'base/register.html')


def login(request):

    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'invalid data')
            return redirect('login')
    else:
        return render(request, 'base/login.html')


def logout(request):
    auth.logout(request)
    return redirect('login')


def home(request):

    posts = Post.objects.all()
    profiles = Profile.objects.all()
    
    context = {'posts':posts, 'profiles':profiles}
    return render(request, 'base/home.html', context)


def addinfo(request):

    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        if request.FILES.get('image') == None:
            
            image = user_profile.profileimage
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimage = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
            
        
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimage = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        return redirect('home') 

    context = {'user_profile':user_profile}  


    return render(request, 'base/add_info.html', context)

def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()
        return redirect('home')
    else:
        HttpResponse('invalid data enterd')

    return render(request, 'base/upload_post.html')    


def likepost(request):

    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)



    like_filter = LikePost.objects.filter(username=username, post_id=post_id).first()

    if like_filter == None:
        new_like = LikePost.objects.create(username=username, post_id=post_id)
        new_like.save()
        post.no_of_likes = post.no_of_likes +1
        post.save()
        return redirect('home')
    
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('home')
    
def profile(request, pk):
    user_object = User.objects.get(username = pk)
    user_profile = Profile.objects.get(user=user_object)

    user_post = Post.objects.filter(user=pk)
    user_post_len = len(user_post)

    follower = request.user.username 
    user = pk

    if FollowCount.objects.filter(user=user, follower=follower).first():
        button_text = 'unfollow'
    else:    
        button_text = 'follow'


    context = {'user_object':user_object, 
               'user_profile': user_profile,
               'user_post':user_post,
               'user_post_len':user_post_len,
               'button_text':button_text
               }


    return render(request, 'base/profile.html', context)    



def follow(request):

    if request.method =='POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
            
        
        else:
            new_follower = FollowCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
            

    else:
        return redirect('home')    
    

def openpost(request, pk):
    post = Post.objects.get(id=pk)
    post_comment = post.comment_set.all().order_by('-created')
    
    if request.method == 'POST':
        comment = Comment.objects.create(
            user= request.user,
            post= post,
            body = request.POST.get('body')
        )
        post.no_of_comments = post.no_of_comments +1

    commnet_count = len(post_comment)   
    context = {'post':post, 'post_comment':post_comment,  'commnet_count':commnet_count}
    return render(request, 'base/open_post.html',context )

# def comment(request, pk):
#     post = Post.objects.get(id=pk)
#     comments = Comment.objects.get(id=pk)
#     context = {'comments':comments}
#     return render(request, 'base/comment.html', context)


def message(request, pk):
    user = User.objects.get(username=pk)
    profile = Profile.objects.get(user=user)
    user_message = profile.message_set.filter(

        Q(sender = request.user)
        # Q(reciver= request.reciver)
        )
    
    if request.method == "POST":
        message = Message.objects.create(
            sender = request.user,
            reciver = profile.user,
            profile = profile,
            body = request.POST.get('body'),

        )
       
    context = {"profile":profile, 'user_message':user_message }
    return render(request, 'base/message.html', context)