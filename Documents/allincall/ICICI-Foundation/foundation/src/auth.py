

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from django.http.response import JsonResponse

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponseForbidden

from django.shortcuts import redirect


#from allauth.account.signals import user_signed_up, user_logged_in,pre_social_login

# @receiver(pre_social_login)
# def social_login_fname_lname_profilepic(sociallogin, user):
#     pass



class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin ):
        data = vars(sociallogin.account)
        user = super().pre_social_login(request, sociallogin)

        user = (sociallogin.account.extra_data['email'])
        
        print('&&&&&&&&&&&&')
        print(user)
        print(user.split('@')[1])
        print('&&&&&&&&&&&&')



        

               

        return HttpResponseForbidden()

        return JsonResponse({'errors' : 'You are not allowed'})            
        
        # Optionally, set as staff now as well.
        # This is useful if you are using this for the Django Admin login.
        # Be careful with the staff setting, as some providers don't verify
        # email address, so that could be considered a security flaw.
        #u.is_staff = u.email.split('@')[1] == "customdomain.com"
        #return u.email.split('@')[1] == "allincall.in"
    
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        try:
            picture = sociallogin.account.extra_data['picture']
            user_field(user, "profile_photo", picture)
        except Exception as e:
            pass
        return user