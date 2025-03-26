from django.urls import path
from urlshortner import views

urlpatterns = [
    path('url/<str:hash>/', views.redirect_origin),
    path('url/', views.create_shorturl),
    path('url/data/<str:hash>', views.get_urldata),
]

