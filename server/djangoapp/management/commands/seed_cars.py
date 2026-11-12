from django.core.management.base import BaseCommand
from djangoapp.models import CarMake, CarModel
class Command(BaseCommand):
    help='Idempotently seed demonstration car makes and models'
    def handle(self,*args,**options):
        for make,model,kind in [('Toyota','Camry','Sedan'),('Honda','Civic','Sedan'),('Ford','Explorer','SUV'),('Tesla','Model 3','Sedan'),('Subaru','Outback','Wagon')]:
            m,_=CarMake.objects.get_or_create(name=make,defaults={'description':f'{make} vehicles'})
            CarModel.objects.get_or_create(car_make=m,name=model,defaults={'type':kind,'year':2023})
        self.stdout.write('Seeded 5 car makes and 5 car models')
