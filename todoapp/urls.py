from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    
    path('',login,name="login"),
    path('index/',index,name="index"),
    path('register/',register,name="register"),
    path('reset_pass/',reset_pass,name="reset_pass"),
    path('profile/',profile,name="profile"),
    path('reg_data/',reg_data,name="reg_data"),
    path('login_data/',login_data,name="login_data"),
    path('sign_out/',sign_out,name="sign_out"),
    path('profile_update/',profile_update,name="profile_update"),
    path('change_password/',change_password,name="change_password"),
    path('search_ref/',search_ref,name="search_ref"),
    path('create_todo/',create_todo,name="create_todo"), 
    
    
    # upload profile pic

    path('upload_image/',upload_image,name="upload_image"), 


    # path('form_data/',form_data,name="form_data"),

]
# if settings.DEBUG:
#         urlpatterns += static(settings.MEDIA_URL,
#                               document_root=settings.MEDIA_ROOT)

