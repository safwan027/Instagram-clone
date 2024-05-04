from django.urls import path
from . import views

urlpatterns = [
    path('feedbase/<str:username>/',views.feedbase,name='feedbase'),
    path('header/',views.header,name='header'),
    path('userhome/',views.user_home,name='userhome'),
    path('create/',views.create,name='create'),
    path('more/',views.more,name='more'),
    path("adminhome/",views.admin_home,name='adminhome'),
    path('search/',views.search,name='search'),
    path('profile/',views.add_profile,name='addprofile'),
    path('postview/<int:id>/',views.post_view,name='postview'),
    path('editpost/<int:id>/',views.edit_post,name='editpost'),
    path('deletepost/<int:id>/',views.delete_post,name='deletepost'),
    path('editcomment/<int:id>/',views.edit_comment,name='editcomment'),
    path('deletecomment/<int:id>/',views.delete_comment,name='deletecomment'),
    path('',views.sign_in,name='signin'),
    path('signup/',views.sign_up,name='signup'),
    path('signout/',views.sign_out,name='signout'),
    path('forgot/',views.forgot_password,name='forgotpassword'),
    path('verify/<str:username>/',views.verify_password,name='verifypassword'),
    path('set/<int:id>/',views.set_password,name='setpassword'),
    path('userprofile/<username>/',views.User_profile,name='userprofile'),
    path('<str:username>/follow/<int:option>/',views.follow_user,name='followuser'),
    path('favorite/<int:post_id>/',views.favourite,name='favorite'),
    path('fav/',views.list_fav,name='fav'), 
    path('addstory/',views.add_story,name='addstory'),
    path('deletestory/<int:id>',views.delete_story,name='deletestory'),
    path('storyview/<str:username>',views.story_view,name='storyview'),

] 

