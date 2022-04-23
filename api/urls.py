from django.urls import path

from . import account_views, taxi_views, support_views

urlpatterns = [
    path('user-create/', account_views.user_create),
    path('user-login/', account_views.user_login),
    path('user-update/', account_views.user_update),
    path('user-update-password/', account_views.update_password),
    path('get-user/', account_views.get_user),
    path('send-code/', account_views.send_code),

    path('get-taxi/', taxi_views.get_taxi),
    path('set-taxi-loc/', taxi_views.taxi_set_location),
    path('order-taxi/', taxi_views.order_taxi),
    path('accept-order/', taxi_views.accept_order),
    path('cancel-order/', taxi_views.cancel_order),
    path('get-price/', taxi_views.get_price),

    path('support-create/', support_views.support_create),
]
