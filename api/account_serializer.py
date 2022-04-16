from rest_framework import serializers

from account.models import User

from phonenumber_field.modelfields import PhoneNumberField


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user


class UserItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']


class UserUpdateSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(required=False, max_length=30)
    email = serializers.EmailField(required=False, max_length=30)
    phone_number = PhoneNumberField()
    image = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = ['fullname', 'email', 'phone_number', 'image']
        extra_kwargs = {'phone_number': {'required': False}}

    def update(self, instance, validated_data):
        print(validated_data)
        password = validated_data.pop('password', None)
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UserPasswordUpdateSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(max_length=50)
    new_password1 = serializers.CharField(max_length=50)
    new_password2 = serializers.CharField(max_length=50)

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
