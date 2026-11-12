from django.urls import path
from . import views
urlpatterns=[
    path('session',views.session),
    path('login',views.login_user),
    path('logout',views.logout_user),
    path('register',views.registration),
    path('get_dealers',views.get_dealers),
    path('get_dealers/<str:state>',views.get_dealers),
    path('dealer/<int:dealer_id>',views.get_dealer),
    path('reviews/dealer/<int:dealer_id>',views.get_reviews),
    path('get_cars',views.get_cars),
    path('add_review',views.add_review),
]
