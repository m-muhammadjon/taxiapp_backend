from django.db import models
from django.contrib.gis.db.models import PointField
from account.models import User


class Car(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class CarType(models.Model):
    name = models.CharField(max_length=20)
    price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Driver(models.Model):
    type = models.ForeignKey(CarType,
                             related_name='drivers',
                             on_delete=models.SET_NULL,
                             null=True)
    user = models.OneToOneField(User,
                                related_name='driver',
                                on_delete=models.CASCADE)
    car = models.ForeignKey(Car,
                            related_name='drivers',
                            on_delete=models.SET_NULL,
                            null=True)
    created = models.DateTimeField(auto_now_add=True)

    likes = models.ManyToManyField(User,
                                   related_name='drivers_liked',
                                   blank=True)
    plate_number = models.CharField(max_length=8, unique=True)
    last_location = PointField(srid=4326, null=True, blank=True, )
    last_lat = models.FloatField(null=True)
    last_lng = models.FloatField(null=True)

    def __str__(self):
        return f'Driver for user: {self.user.fullname}, Last loc: {self.last_location}'


class Location(models.Model):
    driver = models.ForeignKey(Driver,
                               related_name='locations_history',
                               on_delete=models.CASCADE)
    location = PointField(srid=4326, null=True)

    def __str__(self):
        return f'{self.location} for driver {self.driver.user.fullname}'


class Order(models.Model):
    STATUS_CHOICES = (
        ('requested', 'Requested'),
        ('in_progress', 'In_progress'),
        ('started', 'Started'),
        ('ended', 'Ended'),
        ('cancelled', 'Cancelled')
    )
    rider = models.ForeignKey(User,
                              related_name='orders',
                              on_delete=models.SET_NULL,
                              null=True)
    driver = models.ForeignKey(Driver,
                               related_name='orders',
                               on_delete=models.SET_NULL,
                               null=True, blank=True)
    pick_up_address = PointField(srid=4326)
    pick_up_lat = models.FloatField(null=True)
    pick_up_lng = models.FloatField(null=True)
    drop_off_address = PointField(srid=4326)
    drop_off_lat = models.FloatField(null=True)
    drop_off_lng = models.FloatField(null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')
    price = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)  # Buyurtma yaratilgan vaqt
    arrived = models.DateTimeField(null=True, blank=True)  # Taxi kelgan vaqt
    started = models.DateTimeField(null=True, blank=True)  # Taxi yo'lovchini olgan vaqt
    ended = models.DateTimeField(null=True, blank=True)  # Manzilga kelgan vaqt
    penalty_price = models.PositiveIntegerField(null=True, blank=True)
    cancellation_reason = models.ForeignKey('CancellationReason',
                                            on_delete=models.SET_NULL,
                                            related_name='orders',
                                            null=True, blank=True)
    # cancellation_reason = models.CharField(max_length=200, null=True)


class OrderNotificationDriver(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, null=True, blank=True)


class CancellationReason(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class SMSToken(models.Model):
    token = models.TextField()

    def __str__(self):
        return self.token
