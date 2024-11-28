from django.urls import path

from common import views


urlpatterns = [
    path('contact-us/', views.ContactUsApiView.as_view(), name='contact-us'),
    path('about-us/', views.AboutUsListApiView.as_view(), name='about-us-videos'),
    path('advertisement/', views.AdvertisementApiView.as_view(), name='advertisement'),
]