
# import here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Shop, Log, User, Discount
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib import messages
from django.conf import settings
from django.core.files.storage import FileSystemStorage

#added by shawon for session
from django.contrib.auth.decorators import login_required

# Create your views here.

def All_products_view(request, shp_id=6):
    try:
        shop = Shop.objects.get(ShopID=shp_id)#if get function doesn't get a single object, it raises exception
    except:
        return render(request, 'noShop_error.html')
    user = User.objects.get(user=shop)
    if user.status != 'active': #user is idle, not logged in
        print(user)
        return render(request, 'error.html')
    #clear to go
    products = Product.objects.all().filter(shop=shop).order_by('ProductID') #gets all the products of the certain shop
    return render(request, 'products_list.html', {'products_list': products, 'Shop': shop})


def sellsLog_view(request, shp_id=6):
    try:
        shop = Shop.objects.get(ShopID=shp_id)#if get function doesn't get a single object, it raises exception
    except:
        return render(request, 'noShop_error.html')
    user = User.objects.get(user=shop)
    if user.status != 'active':#user is idle, not logged in
        print('user is not logged in')
        return render(request, 'error.html')

    log = Log.objects.all().filter(shop=shop) #gets all the logs of the certain shop
    return render(request, 'sells_log.html', {'logs': log, 'Shop': shop})


def editInfo_view(request, shp_id=6):

    if request.method=='POST':
        use_id = request.POST.get('id_use')
        try:
            shop = Shop.objects.get(ShopID=use_id)#if get function doesn't get a single object, it raises exception
        except:
            return render(request, 'noShop_error.html')
        user = User.objects.get(user=shop)
        if user.status != 'active':#user is idle, not logged in
            print('user is not logged in')
            return render(request, 'error.html')
        shpname = request.POST.get('shop_name')
        loc = request.POST.get('shop_location')
        prop = request.POST.get('user_name')
        mob = request.POST.get('shop_mobile')
        email = request.POST.get('shop_mail')
        latitude = request.POST.get('lati')
        longitude = request.POST.get('longi')

        #gets the shop and updates it
        up_shop = Shop.objects.get(ShopID=use_id)
        up_shop.ShopName = shpname
        up_shop.Location = loc
        up_shop.ContactNumber = mob
        up_shop.Email = email
        up_shop.UserName = prop
        up_shop.Longitude = longitude
        up_shop.Latitude = latitude
        up_shop.save() #saves the shop after updating
        #slug = use_id
        #up_user.update(name=uname, address=add, birthyear=b_yr, mobile_number=mob, email_id=email, profession=proff, bkash_account_no=bkash_acc)
        messages.success(request, "Changes saved", )
        return redirect('shopDB:edit_Info', shp_id=use_id )

    try:
        shop = Shop.objects.get(ShopID=shp_id)#if get function doesn't get a single object, it raises exception
    except:
        return render(request, 'noShop_error.html')
    user = User.objects.get(user=shop)
    if user.status != 'active':#user is idle, not logged in
        print('user is not logged in')
        return render(request, 'error.html')
    #shp = Shop.objects.get(ShopID=shp_id)
    print (shop.ShopName)
    return render(request, 'Edit_Profile.html', {'Shop': shop})




def add_Disc(request):
    if request.method == 'POST':
        perc = request.POST.get('percentage')
        max_amnt = request.POST.get('mx_amnt')
        diamnt = request.POST.get('disc_amnt')
        print(perc, diamnt)
        #all data are received
        if perc is None or perc=="":
            print('perc is null')
            if diamnt is None or diamnt=="":
                print(max_amnt)
                print('Null Entered')
                messages.success(request, "Discount not Added, No value entered", )
                #if no value is entered, discount isn't saved and redirected to actual page
                return render(request, 'Discount_add_pop.html')
        new_disc = Discount(Percentage=perc, DiscountAmount=diamnt, MaxAmount=max_amnt)
        new_disc.save()
        messages.success(request, "Discount Added", ) #Discount added and will be redirected to pop up page
        return render(request, 'Discount_add_pop.html')

    return render(request, 'Discount_add_pop.html')




def addProduct_view(request, shp_id=6):
    if request.method == 'POST':
        shops_id = request.POST.get('shops_idd')
        try:
            shop = Shop.objects.get(ShopID=shops_id)#if get function doesn't get a single object, it raises exception
        except:
            return render(request, 'noShop_error.html')
        user = User.objects.get(user=shop)
        if user.status != 'active':
            print('user is not logged in')
            return render(request, 'error.html')
        name = request.POST.get('product_name')
        pri = request.POST.get('product_sell_price')
        cst = request.POST.get('product_cost')
        qtt = request.POST.get('available_quantity')
        disc = request.POST.get('percentage_discount')
        mfg = request.POST.get('prod_mfg')
        exp = request.POST.get('prod_exp')
        #if date are not entered, it'll be set to none
        if exp == "":
            exp = None
        if mfg =="":
            mfg = None

        if len(request.FILES) != 0: #check if photo was uploaded
            print('photo chosen')
            photo = request.FILES['filebutton']
        else:#if not uploaded, set photo to none
            print('No photo chosen')
            photo = None

        shp=Shop.objects.get(ShopID=shops_id)
        discount = Discount.objects.get(DiscountID=disc) #while saving we need whole discount model, not just id
        print (name,pri,cst, shp_id)
        try:
            all_shop_prods = Product.objects.all().filter(shop=shp)#if get function doesn't get a single object, it raises exception
            prod = all_shop_prods.get(ProductName=name)
            print(prod)
        #print(type(prod))
        #if type(prod) is set or type(prod) is list :
        except: #exception means the set is empty and there is not same named product as this one... So, good to save
            new_prod = Product(ProductName=name, BuyingPrice=cst, SellingPrice=pri, image=photo, shop=shp, Quantity=qtt,
                               discount=discount, Mfg=mfg, Exp=exp)
            new_prod.save()
            messages.success(request, "Product Added", )
            print(shops_id)
            return redirect('shopDB:add_products', shp_id=shops_id)

        #No exception means set isn't empty and there is already a product
        print('Already Exists')
        messages.success(request, "Product not Added, Already Exists", )
        return redirect('shopDB:add_products', shp_id=shops_id)

    try:
        shop = Shop.objects.get(ShopID=shp_id)#if get function doesn't get a single object, it raises exception
    except:
        return render(request, 'noShop_error.html')
    user = User.objects.get(user=shop)
    if user.status != 'active':
        print('user is not logged in')
        return render(request, 'error.html')
    #shp = Shop.objects.get(ShopID=shp_id)
    discs = Discount.objects.all().order_by('Percentage') #For dropdown list of Discount
    return render(request, 'product_Add.html', {'Shop': shop, 'discounts':discs})




def editProduct_view(request, slug='abcd', shp_id=6):

    if request.method=='POST':
        shops_id = request.POST.get('shops_idd')
        try:
            shop = Shop.objects.get(ShopID=shops_id)#if get function doesn't get a single object, it raises exception
        except:
            return render(request, 'noShop_error.html')
        user = User.objects.get(user=shop)
        if user.status != 'active':
            print('user is not logged in')
            return render(request, 'error.html')
        prod_id = request.POST.get('product_id')
        prod_name = request.POST.get('product_name')
        cst = request.POST.get('product_cost')
        quan = request.POST.get('available_quantity')
        pro_pri = request.POST.get('product_sell_price')
        disc = request.POST.get('percentage_discount')
        mfg = request.POST.get('prod_mfg')
        exp = request.POST.get('prod_exp')
        #Got all the data
        discunt = Discount.objects.get(DiscountID=disc)

        #now get the product from database
        up_prod = Product.objects.get(ProductID=prod_id)
        up_prod.ProductName = prod_name
        up_prod.SellingPrice = pro_pri
        up_prod.BuyingPrice = cst
        up_prod.Quantity = quan
        up_prod.discount = discunt
        #dates will be updated only if it was changed
        if mfg != "":
            up_prod.Mfg = mfg
        if exp != "":
            up_prod.Exp = exp
        #check if the photo was uploaded
        if len(request.FILES) != 0:
            print('photo chosen')
            photo = request.FILES['filebutton']
            up_prod.image = photo
        up_prod.save() #saved after updating
        #slug = use_id
        #up_user.update(name=uname, address=add, birthyear=b_yr, mobile_number=mob, email_id=email, profession=proff, bkash_account_no=bkash_acc)
        messages.success(request, "Changes saved", )
        return redirect('shopDB:edit_products', slug=prod_name, shp_id=shops_id )

    try:
        shop = Shop.objects.get(ShopID=shp_id)#if get function doesn't get a single object, it raises exception
    except:
        return render(request, 'noShop_error.html')
    user = User.objects.get(user=shop)
    if user.status != 'active':
        print('user is not logged in')
        return render(request, 'error.html')
    #shp = Shop.objects.get(ShopID=shp_id)
    all_shop_prods = Product.objects.all().filter(ProductName=slug)
    prod = all_shop_prods.get(shop=shop)
    discs = Discount.objects.all().order_by('Percentage')
    return render(request, 'product_Edit.html',{'Product':prod,'Shop': shop, 'discounts':discs})




def sellProduct_view(request, slug='abcd', shp_id=6):
    #Selling a product is basically create a new log entry and reduce the quantity
    if request.method == 'POST':
        shops_id = request.POST.get('shops_idd')
        try:
            shop = Shop.objects.get(ShopID=shops_id)#if get function doesn't get a single object, it raises exception
        except:
            return render(request, 'noShop_error.html')
        user = User.objects.get(user=shop)
        if user.status != 'active':
            print('user is not logged in')
            return render(request, 'error.html')

        prod_id = request.POST.get('product_id')
        buyer_name = request.POST.get('buy_name')
        buy_mob = request.POST.get('buy_contact')
        buy_mail = request.POST.get('buy_email')
        net_pri = request.POST.get('net_price')
        numb = request.POST.get('quantity')

        #get all inputs
        sh = Shop.objects.get(ShopID=shops_id)
        pro = Product.objects.get(ProductID=prod_id)
        tot_cost = pro.BuyingPrice*float(numb) #calculate cost
        prof = float(net_pri) - tot_cost #calculate profit
        #save the log
        new_log = Log(shop=sh, product=pro, Buyer_Name=buyer_name, Buyer_Mobile_No=buy_mob, Buyer_Email=buy_mail, No_of_prods=numb, Net_Price=net_pri, Profit=prof)
        new_log.save()
        #reduce quantity
        pro.Quantity = pro.Quantity - int(numb)
        pro.save()
        prod_name = pro.ProductName
        messages.success(request, "Product sold", )
        return redirect('shopDB:sell_products', slug=prod_name, shp_id=shops_id)

    try:
        shop = Shop.objects.get(ShopID=shp_id)#if get function doesn't get a single object, it raises exception
    except:
        return render(request, 'noShop_error.html')
    user = User.objects.get(user=shop)
    if user.status != 'active':
        print('user is not logged in')
        return render(request, 'error.html')

    all_shop_prods = Product.objects.all().filter(ProductName=slug)
    prod = all_shop_prods.get(shop=shop)
#calculate the discounted value
    if prod.discount.DiscountAmount is None or prod.discount.DiscountAmount == 0:
        print('yes none')
        disc_val = prod.SellingPrice * prod.discount.Percentage/100
        print(disc_val)
        if disc_val > prod.discount.MaxAmount:
            print('exceeds max')
            disc_val = prod.discount.MaxAmount
    else:
        print('not none')
        disc_val = prod.discount.DiscountAmount

    discounted_price = prod.SellingPrice - disc_val
    if discounted_price < 0:
        discounted_price = 0
    return render(request, 'product_Sell.html', {'Product': prod, 'Shop': shop, 'disco_price':discounted_price})




def login_view_s(request):
    if request.method == 'POST':
        print(request.POST.get('username'))
        user = request.POST.get('username')
        passwd = request.POST.get('psw')
        #get the user
        try:
            db_user = User.objects.get(username=user)#if get function doesn't get a single object, it raises exception
        except :
            print('No user found')
            return render(request, 'wrong_pass.html')
        #match password
        if db_user.password == passwd :
            print('Password Matched')
            shop=db_user.user
            db_user.status='active'
            db_user.save()
            return render(request, 'shop_user_profile.html', {'Shop': shop})
        else:#password didn't match
            return render(request, 'wrong_pass.html')
    else:#not a post request
        return render(request, 'login_new.html')



def login_success_view(request, shp_id=6):
    try:
        shop = Shop.objects.get(ShopID=shp_id)#if get function doesn't get a single object, it raises exception
    except:
        return render(request, 'noShop_error.html')
    user = User.objects.get(user=shop)
    if user.status!='active':#user not active, idle
        print('user is not logged in')
        return render(request, 'error.html')

    return render(request, 'shop_user_profile.html', {'Shop': shop})





def logout_view(request, shp_id=6):
    shop = Shop.objects.get(ShopID=shp_id)
    logged_user = User.objects.get(user=shop)
    logged_user.status = 'idle' #switch stat to idle
    logged_user.save()#and save
    return render(request, 'login_new.html')



def signup_view(request):
    if request.method == 'POST':
        #shops_id = request.POST.get('shops_idd')
        print('New Post Request')
        name = request.POST.get('shop_name')
        propriet = request.POST.get('proprietor_name')
        location = request.POST.get('loct')
        latitude = request.POST.get('lat')
        longitude = request.POST.get('lon')
        shp_mob = request.POST.get('mob')
        shp_mail = request.POST.get('email')
        log_user = request.POST.get('username')
        pass_1 = request.POST.get('password_1')
        pass_2 = request.POST.get('password_2')
        if(pass_1 != pass_2):#password has to be confirmed
            print('Password didnot matched')
            messages.success(request, "Passwords didn't match",)
            return redirect('shopDB:user_regs')
        #print (name,pri,cst, shp_id)
        #create new shop and save
        new_shp = Shop(ShopName=name, UserName=propriet, Location=location, Latitude=latitude, Longitude=longitude, ContactNumber=shp_mob, Email=shp_mail)
        new_shp.save()
        print(new_shp.ShopID)
        #create new user and save for login authentication
        new_usr = User(username=log_user, password=pass_1, Mobile=shp_mob, status='idle', user=new_shp)
        new_usr.save()
        messages.success(request, "Shop Added", )
        return redirect('shopDB:user_regs')
    return render(request, 'register_shop.html')



def product_detail(request, slug='abcd', shp_id=6):
    try:
        shop = Shop.objects.get(ShopID=shp_id) #if get function doesn't get a single object, it raises exception
    except:
        return render(request, 'noShop_error.html')
    user = User.objects.get(user=shop)
    if user.status != 'active': #user not active
        print('user is not logged in')
        return render(request, 'error.html')

    try:
        all_shop_prods = Product.objects.all().filter(ProductName=slug)
        prod = all_shop_prods.get(shop=shop)
    except:
        print('Product not found') #now redirect to previous page
        return redirect('shopDB:shop_products', shp_id=shp_id)
    return render(request,'Product_Details_new.html',{'Product':prod, 'Shop': shop})