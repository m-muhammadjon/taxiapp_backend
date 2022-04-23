from rest_framework.permissions import IsAuthenticated

from .support_serializer import SupportSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def support_create(request):
    serializer = SupportSerializer(data=request.data)
    if serializer.is_valid():
        if request.data.get('photo'):
            serializer.save(user=request.user, photo=request.data.get('photo'))
        else:
            serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
