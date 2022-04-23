from rest_framework import serializers

from taxi.models import Order, Driver

from .account_serializer import UserItemSerializer


class DriverSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Driver
        fields = '__all__'

    def get_user(self, obj):
        return UserItemSerializer(obj.user, many=False).data


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['rider', 'price', 'pick_up_lat', 'pick_up_lng', 'drop_off_lat', 'drop_off_lng']


