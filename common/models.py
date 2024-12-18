import uuid

from django.db import models
from django.db.models import CharField
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    # uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Advertisement(models.Model):
    image_en = models.ImageField(upload_to='media/common/advertisement', null=True)
    image_uz = models.ImageField(upload_to='media/common/advertisement', null=True)
    image_ru = models.ImageField(upload_to='media/common/advertisement', null=True)
    link = models.URLField()

    class Meta:
        verbose_name = 'Advertisement'
        verbose_name_plural = 'Advertisements'


class ContactUs(BaseModel):
    name = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=120)
    is_contacted = models.BooleanField(default=False)

    def __str__(self) -> CharField:
        return self.name or self.phone_number

    class Meta:
        verbose_name = _('Contact Us')
        verbose_name_plural = _('Contact Us')
        ordering = ['is_contacted']


class AboutUs(BaseModel):
    title = models.CharField(max_length=120)
    description = models.TextField()
    video = models.FileField(upload_to='common/about-us/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('About Us')
        verbose_name_plural = _('About Us')
