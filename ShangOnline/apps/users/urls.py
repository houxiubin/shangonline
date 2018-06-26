"""ShangOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from .views import UserRegisterView,user_login,user_logout,active,forget,reset,user_info,user_updateinfo,user_updateimage\
    ,user_sendcode,user_changeemail,user_course,user_org,user_teacher,user_mycourse,user_msg

urlpatterns = [
    url(r'^register/$',UserRegisterView.as_view(),name='register'),
    url(r'^login/$',user_login,name='login'),
    url(r'^logout/$',user_logout,name='logout'),

    url(r'^active/(\w+)/$',active,name='active'),
    url(r'^forget/$',forget,name='forget'),
    url(r'^reset/(\w+)/(.*\..*)/$',reset,name='reset'),

    url(r'^user_info/$',user_info,name='user_info'),
    url(r'^user_updateimage/$',user_updateimage,name='user_updateimage'),
    url(r'^user_updateinfo/$',user_updateinfo,name='user_updateinfo'),
    url(r'^user_sendcode/$',user_sendcode,name='user_sendcode'),
    url(r'^user_changeemail/$',user_changeemail,name='user_changeemail'),
    url(r'^user_collect_org/$',user_org,name='user_collect_org'),
    url(r'^user_collect_course/$',user_course,name='user_collect_course'),
    url(r'^user_collect_teacher/$',user_teacher,name='user_collect_teacher'),
    url(r'^user_mycourse/$',user_mycourse,name='user_mycourse'),
    url(r'^user_msg/$',user_msg,name='user_msg'),
]
