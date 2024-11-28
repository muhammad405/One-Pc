from rest_framework import generics, views, status
from rest_framework.response import Response

from common import models, serializers


class ContactUsApiView(generics.CreateAPIView):
    serializer_class = serializers.ContactUsSerializer
    queryset = models.ContactUs.objects.all()


class AboutUsListApiView(views.APIView):
    def get(self, request):
        queryset = models.AboutUs.objects.all()
        serializer = serializers.AboutUsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdvertisementApiView(views.APIView):
    def get(self, request):
        queryset = models.Advertisement.objects.all()
        serializer = serializers.AdvertisingSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
