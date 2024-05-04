from django.shortcuts import render,redirect,HttpResponse,get_object_or_404,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.core.mail import send_mail
from . models import otp,profile,Post,comment,Like,follow,story
import random,string
from django.conf import settings
from django.db import transaction
from . forms import StoryForm
from django.core.paginator import Paginator






def header(request):
    return render(request,'header.html')





def sign_up(request):
    if request.method == 'POST':
        temp_full_name = request.POST.get("name")
        temp_user_name = request.POST.get("username")
        temp_email = request.POST.get("email")
        temp_pasword = request.POST.get("password")
        temp_confirm = request.POST.get("confirm")
        if temp_pasword == temp_confirm:
            User.objects.create_user(
                first_name = temp_full_name,
                username = temp_user_name,
                email = temp_email,
                password = temp_pasword,
            )
            return redirect('signin')
        return HttpResponse("Password doesnt match")
    return render(request,'signup.html')

def sign_in(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        pword = request.POST.get("password")
        user = authenticate(username = uname,password = pword)
        if user is not None:
            login(request,user)
            if user.is_staff:
                return redirect('adminhome')
            try:
                page = user.profile
                return redirect('userhome')
            except profile.DoesNotExist:
                return redirect('addprofile')
        else:
            messages.error(request,"Sorry, your password was incorrect,\nPlease double-check your password.")
    return render(request,"signin.html")

def sign_out(request):
    logout(request)
    return redirect('signin')

def generate_otp():
    digits = string.digits
    temp = random.sample(digits,6)
    otp = ''.join(temp)
    return otp

def send_mail_to_user(email,otp,username):
    subject = "Reset Password !"
    message = f"here is your otp:{otp},Please click the link to reset the password http://127.0.0.1:8000/verify/{username}/"
    recipient_list = [ email ]
    return send_mail (subject, settings.EMAIL_HOST_USER, message, [recipient_list] ,fail_silently=False)

def forgot_password(request):
    if request.method == "POST":
        temp_email = request.POST.get("email")
        user = User.objects.filter(email=temp_email).first()
        if user is not None :
            data = otp.objects.filter(fk_user=user).first()
            if data:
                data.delete()
            new_otp = generate_otp()
            otp.objects.create(
                otp = new_otp,
                fk_user = user,
            )
            send_mail_to_user(temp_email,new_otp,user.username)
            messages.success(request,"OTP has been sent succesfully")
        else:
            messages.error(request,"User doesnt exist")        
    return render(request,'forgotpassword.html')

def verify_password(request,username):
    data = otp.objects.filter(fk_user__username = username).first()
    if request.method == 'POST':
        temp_otp = request.POST.get("otp")
        if data.otp == temp_otp:
            messages.success(request,"OTP is verfied succesfully")
            return redirect('setpassword',id=data.id)
        return messages.error(request,"Invalid OTP")
    return render(request,'verifypassword.html')
    
def set_password(request,id):
    data = otp.objects.filter(id=id).first()
    user = data.fk_user
    if request.method == 'POST':
        temp_pass1 = request.POST.get("pass1")
        temp_pass2 = request.POST.get("pass2")
        if temp_pass1 == temp_pass2:
            user.set_password(temp_pass1)
            user.save()
            data.delete()
            return redirect('signin')
        else:
            return messages.error(request,"Passwords do not match")
    return render (request,'setpassword.html')

        




def add_profile(request):
    current_user = request.user
    if request.method == 'POST':
        temp_image = request.FILES.get("profile_image")
        temp_bio = request.POST.get("bio")
        profile.objects.create(
            image = temp_image,
            bio = temp_bio,
            fk_user = current_user,
        )
        return redirect('userhome')
    return render(request,'addprofile.html')





def feedbase(request): 
    user = profile.objects.get(fk_user=request.user)
    return render(request, "feedbase.html",{'user':user})












def create(request):
    current_user = request.user
    data = Post.objects.all()
    if request.method == 'POST':
        temp_image = request.FILES.get('image')
        temp_caption = request.POST.get('caption')
        Post.objects.create(
            image = temp_image,
            caption = temp_caption,
            fk_user = current_user,
        )
        return redirect('userhome')
    return render(request,"create.html")




def search(request):
    Profile = profile.objects.all()
    post = Post.objects.all() 
    if request.method == 'POST':
        temp_username = request.POST.get('search')
        try:
            user = User.objects.get(username=temp_username)
            profile1 = get_object_or_404(profile, fk_user__username = user) 
        except User.DoesNotExist: 
            return HttpResponse('User doesnt exist !') 
        except profile.DoesNotExist:
           return HttpResponse('User doesnt exist !')
        return redirect('userprofile', username=profile1.fk_user.username)
    context = {
        'post':post,
        'Profile' : Profile,
    }
    return render(request, 'search.html',context)                                                       





def edit_post(request,id):
    postview = Post.objects.get(id=id)
    if request.method == 'POST' :
        temp_image = request.FILES.get('image')
        temp_caption = request.POST.get('caption')
        postview.caption = temp_caption
        postview.image = temp_image
        postview.save()
        return redirect('postview',id=postview.id)
    return render(request,'editpost.html',{ 'post' : postview})

def delete_post(request,id):
    postview = Post.objects.get(id=id)
    postview.delete()
    return redirect('userhome')

def edit_comment(request,id):
    c_data = comment.objects.get(id=id)
    if request.method == 'POST':
        temp_comment = request.POST.get('comment')
        c_data.comment = temp_comment
        c_data.save()
        return redirect('postview',id=c_data.fk_post.id)
    return render(request,'editcomment.html',{ "c_data" : c_data })

def delete_comment(request, id):
    current_user = request.user
    comment_to_delete = comment.objects.get(id=id, fk_user=current_user)
    post = get_object_or_404(Post, id=comment_to_delete.fk_post.id)
    comment_to_delete.delete()
    post.comment_count -= 1
    post.save()
    return redirect('postview', id=post.id)












def post_view(request,id):
    current_user = request.user
    postview = Post.objects.get(id=id)
    c_data = comment.objects.filter(fk_post__id=id) 
    if request.method == 'POST' :
        if 'action1'  in request.POST:
            temp_comment = request.POST.get('comment')
            comment.objects.create(
                fk_user = current_user,
                comment = temp_comment,
                fk_post = postview,
                )
            postview.comment_count +=1
            postview.save()
            return redirect('postview',id=postview.id)

        if 'action2' in  request.POST:
            check = Like.objects.filter(fk_user=current_user, fk_post=postview)
            if not check.exists():
                Like.objects.create(
                    fk_user = current_user,
                    fk_post = postview,
                )
                postview.like_count += 1
                postview.save()
            else:
                check.delete()
                postview.like_count -=1
                postview.save()   
            return redirect('postview',id=postview.id) 
    return render(request,'postview.html',{ 'post' : postview,"c_data":c_data})





def follow_user(request,username,option):
    current_user = request.user         
    following = get_object_or_404(User, username=username)

    try:
        f,created = follow.objects.get_or_create(follower = current_user, following = following)
        if int(option) == 0:
            f.delete()
        else:
            posts = Post.objects.filter(fk_user=following)[:10]  
        return redirect('userprofile',username=username) 
    except User.DoesNotExist:
        return redirect('userprofile',username=username)


def user_home(request):         
    current_user = request.user 
    image = profile.objects.get(fk_user=current_user)
    posts = Post.objects.all()   
    all_users = User.objects.all()
    follow_status = follow.objects.filter(following=current_user, follower=request.user).exists()
    stories = story.objects.all()[:6]

    context = {
        'post':posts, 
        'profile':image,
        'follow_status':follow_status,
        'all_users':all_users,
        'stories':stories,
    }
    return render(request,'userhome.html',context)



def admin_home(request):
    current_user = request.user 
    image = profile.objects.get(fk_user=current_user)
    posts = Post.objects.all()   
    all_users = User.objects.all()
    follow_status = follow.objects.filter(following=current_user, follower=request.user).exists()
    stories = story.objects.all()[:6]

    context = { 
        'post':posts,   
        'profile':image,
        'follow_status':follow_status,
        'all_users':all_users,     
        'stories':stories,
    }  
    
    return render(request,'adminhome.html',context)






def User_profile(request, username): 
    pro = profile.objects.filter(fk_user=request.user).first()
    user = get_object_or_404(User,username=username)
    Profile = profile.objects.filter(fk_user=user).first()
    posts = Post.objects.filter(fk_user=user)

    #url_name = resolve(request.path).url_name
    #if url_name == 'Profile':
    #    posts = Post.objects.filter(fk_user=user).order_by('-created_at')[:5]
    #else:
    #    posts = profile.favourite.all()  

    posts_count = Post.objects.filter(fk_user=user).count()
    following_count = follow.objects.filter(follower=user).count()
    followers_count = follow.objects.filter(following=user).count()
    follow_status = follow.objects.filter(following=user, follower=request.user).exists()


    context = {
        'pro':pro,
        'profile':Profile,
        'post':posts,
        'posts_count':posts_count,
        'following_count':following_count,
        'followers_count':followers_count, 
        'follow_status':follow_status,
        }            
          
    return render(request, 'userprofile.html',context)   


def favourite(request,post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    Profile = profile.objects.filter(fk_user=user).first()

    if Profile.favorite.filter(id=post_id).exists():
        Profile.favorite.remove(post)         
    else:       
        Profile.favorite.add(post)      
    return redirect ('userprofile',post_id=post.post_id) 

def list_fav(request):
    pro = profile.objects.get(fk_user=request.user)  
    fav_post = pro.favorite.all()                
    return render(request,'favorites.html',{"fav_post":fav_post})     


def more(request):
    return render(request, 'more.html')



def add_story(request): 
    user = request.user
    if request.method == 'POST':
        form = StoryForm(request.POST,request.FILES)
        if form.is_valid():
            fk_user = user,
            form.save()
            return redirect('userhome')
        else:
            HttpResponse(form.errors)  
    else:
        form = StoryForm()
    return render(request,'addstory.html',{'form':form})    
    


def delete_story(request,id):
    story_obj = get_object_or_404(story,id=id)
    story_obj.delete()
    return redirect('userhome')

def story_view(request,username):
    queryset = story.objects.filter(fk_user__username=username)  
    items = 1
    paginator = Paginator(queryset,items)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj':page_obj,
        'queryset':queryset,
    } 

    return render(request,'storyview.html',context)






