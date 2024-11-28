from rest_framework.test import APITestCase

from common import models


class ContactUsTestCase(APITestCase):
    def test_user_can_contact(self):
        data = {
            'name': 'Behruz',
            'phone_number': '+998947099971',
        }
        response = self.client.post('/api/v1/common/contact-us/', data=data)

        self.assertEqual(response.status_code, 201)
        self.assertIn('name', response.data)
        self.assertIn('phone_number', response.data)


class AboutUsTestCase(APITestCase):
    def test_user_can_see_about_us(self):
        models.AboutUs.objects.create(
            title_uz='title_uz', title_ru='title_ru', title_en='title_en',
            description_uz='description_uz', description_ru='description_ru', description_en='description_en',
            video='test.mp4'
        )
        response = self.client.get('/api/v1/common/about-us/')

        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response.data[0])
        self.assertIn('title_uz', response.data[0])
        self.assertIn('title_ru', response.data[0])
        self.assertIn('title_en', response.data[0])
        self.assertIn('description_uz', response.data[0])
        self.assertIn('description_ru', response.data[0])
        self.assertIn('description_en', response.data[0])
        self.assertIn('video', response.data[0])


class AdvertisementTestCase(APITestCase):
    def test_advertisement_list(self):
        models.Advertisement.objects.create(
            image='test.png',
            link='test.com',
        )
        response = self.client.get('/api/v1/common/advertisement/')

        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response.data[0])
        self.assertIn('image', response.data[0])
        self.assertIn('link', response.data[0])
