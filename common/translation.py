from modeltranslation.translator import TranslationOptions, register

from common import models


@register(models.AboutUs)
class AboutUsTranslation(TranslationOptions):
    fields = ['title', 'description']

