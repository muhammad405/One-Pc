from rest_framework import serializers

from common import models
from core.settings import BASE_URL


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ContactUs
        fields = ['name', 'phone_number']


class AboutUsSerializer(serializers.ModelSerializer):
    video = serializers.SerializerMethodField(method_name='get_video')

    class Meta:
        model = models.AboutUs
        fields = [
            'id', 'title_uz', 'title_ru', 'title_en', 'description_uz', 'description_ru', 'description_en', 'video'
        ]

    def get_video(self, obj):
        return f'{BASE_URL}{obj.video.url}'


class AdvertisingSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(method_name='get_image')

    class Meta:
        model = models.Advertisement
        fields = ['id', 'image', 'link']

    def get_image(self, obj):
        return f'{BASE_URL}{obj.image.url}'