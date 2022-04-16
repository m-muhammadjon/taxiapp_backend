from rest_framework.decorators import api_view, permission_classes
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import GeometryDistance
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from taxi.models import Driver, Location, Order

from .taxi_serializer import DriverSerializer, OrderCreateSerializer, OrderSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def taxi_set_location(request):
    driver = Driver.objects.get(user_id=request.user.id)
    pnt = Point(float(request.data.get('lng')), float(request.data.get('lat')))
    Location.objects.create(driver_id=driver.id, location=pnt)
    return Response('success')


def order_send(order_id, driver_ids):
    order = Order.objects.get(id=order_id)
    order_serializer = OrderSerializer(order, many=False)
    layer = get_channel_layer()
    for id in driver_ids:
        async_to_sync(layer.group_send)(
            f'user_{id}', {
                'type': 'order_message',
                'status': 'order_created',
                'order': order_serializer.data
            }
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_taxi(request):
    pnt = Point(float(request.data.get('lng')), float(request.data.get('lat')))
    drivers = Driver.objects.filter(last_location__distance_lte=(pnt, D(km=float(request.data.get('dist'))))) \
        .annotate(distance=GeometryDistance(pnt, 'last_location')) \
        .order_by('distance')
    driver_ids = [x.user.id for x in drivers]
    order = Order.objects.get(id=request.data.get('order_id'))
    order_send(order.id, driver_ids)
    return Response(DriverSerializer(drivers, many=True).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def order_taxi(request):
    pnt = Point(float(request.data.get('pick_up_lng')), float(request.data.get('pick_up_lat')))
    drivers = Driver.objects.filter(user__is_online=True,
                                    last_location__distance_lte=(pnt, D(km=1.5))) \
        .annotate(distance=GeometryDistance(pnt, 'last_location')) \
        .order_by('distance')
    order_serializer = OrderCreateSerializer(data=request.data, many=False)
    if order_serializer.is_valid():
        drop_off_loc = Point(float(request.data.get('drop_off_lng')), float(request.data.get('drop_off_lat')))
        order = order_serializer.save(pick_up_address=pnt, drop_off_address=drop_off_loc)
        driver_ids = [x.user.id for x in drivers]
        order_send(order.id, driver_ids)
        print('saved')
    else:
        print(order_serializer.errors)

    return Response('salom')


@api_view(['GET'])
def get_price(request):
    print(request.data)

    return Response('salom')
