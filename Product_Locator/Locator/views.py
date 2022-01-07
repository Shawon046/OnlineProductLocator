

from django.http import HttpResponse
from django.shortcuts import render, redirect
from shopDB.models import Product, Shop, Log, User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib import messages
import math
import operator

#Functions and class for distance
def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d

#class embedded with Product and Distance
class pro_dist(object):
    def __init__(self, Product=None, Dist=None):
        self.Product = Product
        self.Dist = Dist

    def reg(self):
        return self.Dist



#Class and function for distance end here


# Create your views here.

def loc_input_view(request):
    #slug=5
    if request.method=='POST':
        print('reached')
        lati = request.POST.get('lat')
        longi = request.POST.get('lon')
        latitude = float(lati)
        longitude = float(longi)
        print(latitude, longitude)
        #getting distanced products
        prodList = [] #product list
        products = Product.objects.all().order_by('ProductID')
        for prod in products:
            dst = round(distance((latitude, longitude), (prod.shop.Latitude, prod.shop.Longitude)), 3) #Calculate the distance
            prodList.append(pro_dist(prod, dst)) #create and append the object
        prod_set = set(prodList)    #convert the list to set
        sorted_prod_set = sorted(prod_set, key=pro_dist.reg) #sort with regard to distance
        return render(request,'user_prod_view.html',{'products_list': sorted_prod_set,'Latitude':latitude, 'Longitude':longitude})

    return render(request, 'Map_input.html')


def search_view(request):
    lat_u = 23.77736487#23.72459528 #change later
    long_u = 90.41198730#90.39549494 #change later
    prodList = []
    if request.method=='POST':
        lati = request.POST.get('lat')
        longi = request.POST.get('lon')
        latitude = float(lati)
        longitude = float(longi)
        print(latitude, longitude)

        prod_name=request.POST.get('prod_name')
        if prod_name=="": #if searched without input, view all
            print("Product Name is Null")
            products = Product.objects.all().order_by('ProductID')
            for prod in products: #same distance calculation and object appending
                dst = round(distance((latitude, longitude), (prod.shop.Latitude, prod.shop.Longitude)), 3)
                prodList.append(pro_dist(prod, dst))
            prod_set = set(prodList)
            sorted_prod_set = sorted(prod_set, key=pro_dist.reg)
            return render(request, 'user_prod_view.html', {'products_list': sorted_prod_set, 'Latitude': latitude, 'Longitude': longitude,'S_val':''})

        print('search called with value ')
        print(prod_name)
        products = Product.objects.all().filter(ProductName=prod_name)
        for prod in products: #same distance calculation and object appending
            dst = round(distance((latitude, longitude), (prod.shop.Latitude, prod.shop.Longitude)), 3)
            prodList.append(pro_dist(prod, dst))
        prod_set = set(prodList)
        sorted_prod_set = sorted(prod_set, key=pro_dist.reg)
        return render(request, 'user_prod_view.html', {'products_list': sorted_prod_set,'Latitude':latitude, 'Longitude':longitude, 'S_val':prod_name})
    #initially load products
    products = Product.objects.all().order_by('ProductID')
    for prod in products:#same distance calculation and object appending
        dst = round(distance((lat_u, long_u), (prod.shop.Latitude, prod.shop.Longitude)), 3)
        prodList.append(pro_dist(prod, dst))
    prod_set = set(prodList)
    sorted_prod_set = sorted(prod_set, key=pro_dist.reg)
    return render(request, 'user_prod_view.html', {'products_list': sorted_prod_set,'Latitude':lat_u, 'Longitude':long_u, 'S_val':''})



def details(request, prod_id=1):
    prod = Product.objects.get(ProductID=prod_id) #show the product details
    print(prod.ProductName)
    return render(request, 'user_prod_details.html', {'Product': prod})



def search_2(request):
    lat_u = 23.72459528
    long_u = 90.39549494
    prodList = []
    if request.method == 'POST':
        prod_name = request.POST.get('prod_name')
        if prod_name == "":
            return redirect('Locator:testing')
        products = Product.objects.all().filter(ProductName=prod_name)
        for prod in products:
            dst = distance((lat_u, long_u), (prod.shop.Latitude, prod.shop.Longitude))
            prodList.append(pro_dist(prod, dst))
        prod_set = set(prodList)
        sorted_prod_set = sorted(prod_set, key=pro_dist.reg())
        return render(request, 'user_prod_view_test.html', {'products_list': sorted_prod_set})

    products = Product.objects.all().order_by('ProductID')
    for prod in products:
        dst = round(distance((lat_u, long_u),(prod.shop.Latitude, prod.shop.Longitude)),3)
        prodList.append(pro_dist(prod, dst))
    prod_set = set(prodList)
    sorted_prod_set = sorted(prod_set, key=pro_dist.reg)
    return render(request, 'user_prod_view_test.html', {'products_list': sorted_prod_set})




def shop_loc_view(request, shp_id=1):
    shp = Shop.objects.get(ShopID=shp_id)#show the shop location  details
    print (shp.ShopName)
    return render(request, 'shop_loc.html',{'Shop': shp})



def onl_view(request):
    shp = Shop.objects.all()
    for shop in shp:
        print(shop.ShopName)
    return render(request, 'online.html', {'shop_list': shp})
