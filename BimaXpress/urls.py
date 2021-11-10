from django.conf.urls import url
from BimaXpress import views

from django.conf.urls.static import static
from django.conf import settings


urlpatterns=[
    url(r'^user$',views.UsersAPI.as_view()),
    url(r'^user/([0-9]+)$',views.UsersAPI.delete),
    url(r'^role$',views.ClaimAPI.as_view()),
    url(r'^doctor$',views.DoctorAPI.as_view()),


    # url(r'^employee/savefile',views.SaveFile)
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)