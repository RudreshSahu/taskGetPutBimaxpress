"""bimaxpessproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls import url,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index', views.index, name='index'),
    path('', views.login, name="login"),
    path('postsignIn',views.postsignIn, name="postsignIn"),
    # path('usercreation',views.usercreation, name="usercreation"),
    path('mainpage',views.mainpage, name="mainpage"),
    path('sendmail',views.sendmail,name="sendmail"),
    path('logout',views.logout, name="logout"),
    path('resendemail', views.resendemail ,name="resendemail"),
    #<-----EMAILER------>
    path('bunny',views.bunny , name="bunny"),
    path('sent',views.sentmail , name="sentmail"),
    # path('trash',views.trashmail , name="trashmail"),
    path('starred',views.starredemail , name="starredmail"),
    path('drafts',views.draftmail , name="draftmail"),
    path('replymail',views.replymail , name="replymail"),
    # path('savefinal',vie
    # ws.savefinal , name="savefinal"),
    # <-----gouravCode---->
    
    
    # <---------------Palash---------------------->
    url(r'^',include('BimaXpress.urls'))
    
]

handler404 = 'bimaxpessproject.views.error_404'

handler500 = 'bimaxpessproject.views.error_500'

handler403 = 'bimaxpessproject.views.error_403'

handler400 = 'bimaxpessproject.views.error_400'
