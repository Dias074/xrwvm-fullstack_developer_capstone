import json
from datetime import date
from functools import wraps
from urllib.parse import quote
import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import CarMake, CarModel
from .restapis import get_request, post_review, analyze_review_sentiments

def failure(message, status=400):
    return JsonResponse({'status':status,'error':message},status=status)

def api_errors(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except (ValueError, KeyError, TypeError):
            return failure('Invalid or missing request fields')
        except requests.RequestException:
            return failure('A backend service is temporarily unavailable',502)
    return wrapped

@require_GET
@ensure_csrf_cookie
def session(request):
    return JsonResponse({'userName':request.user.username if request.user.is_authenticated else None})

@require_POST
@api_errors
def login_user(request):
    data=json.loads(request.body)
    user=authenticate(request,username=data['userName'],password=data['password'])
    if user is None:
        return failure('Invalid username or password',401)
    login(request,user)
    return JsonResponse({'status':'Authenticated','userName':user.username})

@require_POST
def logout_user(request):
    logout(request)
    return JsonResponse({'status':200,'message':'Logged out'})

@require_POST
@api_errors
def registration(request):
    data=json.loads(request.body)
    username=data['userName'].strip()
    if not username or len(username)>150 or not data['firstName'].strip() or not data['lastName'].strip():
        return failure('Username, first name and last name are required')
    try:
        validate_email(data['email'])
        validate_password(data['password'])
        user=User.objects.create_user(username=username,password=data['password'],email=data['email'],first_name=data['firstName'].strip(),last_name=data['lastName'].strip())
    except ValidationError as exc:
        return failure('; '.join(exc.messages))
    except IntegrityError:
        return failure('Username already exists',409)
    login(request,user)
    return JsonResponse({'status':200,'userName':user.username})

@require_GET
@api_errors
def get_dealers(request,state='All'):
    endpoint='fetchDealers' if state in ('All','') else 'fetchDealers/'+quote(state,safe='')
    return JsonResponse({'status':200,'dealers':get_request(endpoint)})

@require_GET
@api_errors
def get_dealer(request,dealer_id):
    dealer=get_request(f'fetchDealer/{dealer_id}')
    if not dealer:
        return failure('Dealer not found',404)
    return JsonResponse({'status':200,'dealer':dealer})

@require_GET
@api_errors
def get_reviews(request,dealer_id):
    reviews=get_request(f'fetchReviews/dealer/{dealer_id}')
    for review in reviews:
        review['sentiment']=analyze_review_sentiments(review['review'])
    return JsonResponse({'status':200,'reviews':reviews})

@require_GET
def get_cars(request):
    models=[{'id':m.id,'CarMake':m.car_make.name,'CarModel':m.name,'year':m.year} for m in CarModel.objects.select_related('car_make').all()]
    return JsonResponse({'status':200,'CarMakes':list(CarMake.objects.values('id','name','description')),'CarModels':models})

@require_POST
@api_errors
def add_review(request):
    if not request.user.is_authenticated:
        return failure('Login required',401)
    data=json.loads(request.body)
    if not str(data['review']).strip() or len(data['review'])>5000:
        return failure('Review must contain 1 to 5000 characters')
    if not 2015<=int(data['car_year'])<=2026:
        return failure('Invalid car year')
    purchased=date.fromisoformat(data['purchase_date'])
    if purchased>date.today():
        return failure('Purchase date cannot be in the future')
    if not get_request(f"fetchDealer/{int(data['dealership'])}"):
        return failure('Dealer not found',404)
    if not CarModel.objects.filter(name=data['car_model'],car_make__name=data['car_make']).exists():
        return failure('Unknown car make or model')
    payload={k:data[k] for k in ('dealership','review','purchase_date','car_make','car_model','car_year')}
    payload['name']=request.user.get_full_name() or request.user.username
    payload['purchase']=True
    return JsonResponse({'status':200,'review':post_review(payload)})
