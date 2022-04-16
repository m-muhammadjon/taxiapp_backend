from django.urls import path

from . import account_views, taxi_views

urlpatterns = [
    path('user-create/', account_views.user_create),
    path('user-login/', account_views.user_login),
    path('user-update/', account_views.user_update),
    path('user-update-password/', account_views.update_password),
    path('get-user/', account_views.get_user),
    path('get-taxi/', taxi_views.get_taxi),
    path('set-taxi-loc/', taxi_views.taxi_set_location),
    path('order-taxi/', taxi_views.order_taxi),

]
