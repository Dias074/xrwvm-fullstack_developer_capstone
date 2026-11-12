import json
from unittest.mock import patch
import requests
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import CarMake, CarModel


class PortalTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('driver', password='Testing-only-283!', first_name='Test', last_name='Driver')
        make = CarMake.objects.create(name='Toyota')
        CarModel.objects.create(car_make=make, name='Camry', type='Sedan', year=2023)
        self.review = dict(dealership=1, review='Fantastic services', purchase_date='2025-01-10', car_make='Toyota', car_model='Camry', car_year=2023)

    def post(self, path, data):
        return self.client.post('/djangoapp/'+path, json.dumps(data), content_type='application/json')

    def test_anonymous_session(self):
        self.assertIsNone(self.client.get('/djangoapp/session').json()['userName'])

    def test_login_success(self):
        response = self.post('login', {'userName':'driver','password':'Testing-only-283!'})
        self.assertEqual(response.json()['status'], 'Authenticated')
        self.assertEqual(self.client.get('/djangoapp/session').json()['userName'], 'driver')

    def test_login_invalid(self):
        self.assertEqual(self.post('login', {'userName':'driver','password':'wrong'}).status_code, 401)

    def test_logout(self):
        self.client.force_login(self.user)
        self.assertEqual(self.post('logout', {}).status_code, 200)
        self.assertIsNone(self.client.get('/djangoapp/session').json()['userName'])

    def test_logout_requires_post(self):
        self.assertEqual(self.client.get('/djangoapp/logout').status_code, 405)

    def test_registration(self):
        data=dict(userName='newdriver',firstName='New',lastName='Driver',email='new@example.com',password='Test-only-418!')
        self.assertEqual(self.post('register',data).status_code,200)
        self.assertTrue(User.objects.get(username='newdriver').check_password(data['password']))
        self.assertEqual(self.post('register',data).status_code,409)

    def test_invalid_registration(self):
        data=dict(userName='newdriver',firstName='New',lastName='Driver',email='bad',password='123')
        self.assertEqual(self.post('register',data).status_code,400)
        self.assertFalse(User.objects.filter(username='newdriver').exists())

    def test_invalid_json(self):
        self.assertEqual(self.client.post('/djangoapp/login','{',content_type='application/json').status_code,400)

    def test_csrf_enforced(self):
        client=Client(enforce_csrf_checks=True)
        self.assertEqual(client.post('/djangoapp/login','{}',content_type='application/json').status_code,403)
        client.get('/djangoapp/session')
        response=client.post('/djangoapp/login',json.dumps({'userName':'driver','password':'Testing-only-283!'}),content_type='application/json',HTTP_X_CSRFTOKEN=client.cookies['csrftoken'].value)
        self.assertEqual(response.status_code,200)

    @patch('djangoapp.views.get_request',return_value=[{'id':1,'state':'Kansas'}])
    def test_state_filter(self, get):
        response=self.client.get('/djangoapp/get_dealers/Kansas')
        get.assert_called_once_with('fetchDealers/Kansas')
        self.assertEqual(response.json()['dealers'][0]['state'],'Kansas')

    @patch('djangoapp.views.get_request',return_value=[])
    def test_unknown_dealer(self, get):
        self.assertEqual(self.client.get('/djangoapp/dealer/999999').status_code,404)

    @patch('djangoapp.views.get_request',side_effect=requests.ConnectionError())
    def test_service_failure(self, get):
        self.assertEqual(self.client.get('/djangoapp/get_dealers').status_code,502)

    def test_car_catalog(self):
        data=self.client.get('/djangoapp/get_cars').json()
        self.assertEqual(data['CarModels'][0]['CarModel'],'Camry')
        self.assertEqual(data['CarMakes'][0]['name'],'Toyota')

    def test_review_requires_login(self):
        self.assertEqual(self.post('add_review',self.review).status_code,401)

    @patch('djangoapp.views.post_review',return_value={'id':101})
    @patch('djangoapp.views.get_request',return_value=[{'id':1}])
    def test_review_uses_authenticated_author(self, get, post):
        self.client.force_login(self.user)
        self.review['name']='Spoofed Author'
        self.assertEqual(self.post('add_review',self.review).status_code,200)
        self.assertEqual(post.call_args.args[0]['name'],'Test Driver')

    def test_invalid_review_year(self):
        self.client.force_login(self.user)
        self.review['car_year']=1900
        self.assertEqual(self.post('add_review',self.review).status_code,400)

    def test_future_purchase(self):
        self.client.force_login(self.user)
        self.review['purchase_date']='2099-01-01'
        self.assertEqual(self.post('add_review',self.review).status_code,400)

    @patch('djangoapp.views.analyze_review_sentiments',return_value='positive')
    @patch('djangoapp.views.get_request',return_value=[{'id':1,'review':'Fantastic services'}])
    def test_review_sentiment(self, get, sentiment):
        self.assertEqual(self.client.get('/djangoapp/reviews/dealer/1').json()['reviews'][0]['sentiment'],'positive')

    def test_static_pages(self):
        self.assertContains(self.client.get('/about'),'About Us')
        self.assertContains(self.client.get('/contact'),'support@bestcars.example')
