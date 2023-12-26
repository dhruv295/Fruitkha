from http.client import HTTPResponse
from django.shortcuts import render,redirect
from matplotlib.pyplot import get
import razorpay

from myfruit.models import CustomeraddressModel, MaincategoryModel, Order, ProductModel, cartmodel, contactmodel, wishlistmodel
from .form import ContactForm, CustomeraddressForm, PassChangeForm, SigninForm, SignupForm, UserProfileChangeForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def HomeView(request):
    main = MaincategoryModel.objects.all()
    product=ProductModel.objects.all()
    cart_count = cartmodel.objects.filter(user=request.user).count()
    return render(request,'home.html',{'product':product,'main':main,'cart_count':cart_count})

def SignupView(request):
    main = MaincategoryModel.objects.all()
    product=ProductModel.objects.all()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            usrname= form.cleaned_data['username']
            print(usrname)
            form.save() 
            messages.success(request,'{usrname} Successfully Registred')
            
        return redirect("/signin/")
    else:
        form = SignupForm()
        context = {'form': form,'product':product,'main':main }
    return render(request, 'signup.html', context)
def SigninView(request):
    main = MaincategoryModel.objects.all()
    product=ProductModel.objects.all()
    form = SigninForm()
    if request.method == 'POST':
        uname = request.POST['uname']
        upass = request.POST['upass']
        user = authenticate(username=uname,password=upass)
        if user is None:
            messages.error(request,'Please Enter Correct Credinatial')
            return redirect('/signin/')
        else:
            login(request,user)
            messages.success(request,'Login Successful')
        return redirect('/')
    else:
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return render(request,'signin.html',{'form':form,'product':product,'main':main})


def logoutView(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, 'You are Successfully Logged Out !')
        return redirect('/signin')
    else:
        messages.info(request, 'Please Login First')
    return redirect('/signin')


def ChangePassView(request):
    cart_count = cartmodel.objects.filter(user=request.user).count()
    main = MaincategoryModel.objects.all()
    product=ProductModel.objects.all()
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PassChangeForm(user = request.user, data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,'Password Successfully Changed')
        else:
            form = PassChangeForm(user =request.user)
            
        context= {'form':form,'product':product,'main':main,'cart_count':cart_count}
        return render(request,'chpass.html',context)
    else:
        messages.info(request, '☹︎ Please Login First')
    return redirect('/signin/')


def ProfileView(request):
    cart_count = cartmodel.objects.filter(user=request.user).count()
    main = MaincategoryModel.objects.all()
    product=ProductModel.objects.all()
    if request.user.is_authenticated:
        form =UserProfileChangeForm(instance=request.user)
        context = {'form':form,'product':product,'main':main,'cart_count':cart_count}
        if request.method == 'POST':
            form =UserProfileChangeForm(request.POST,instance=request.user)
            if form.is_valid():
                form.save()
                messages.info(request,'Profile Successfully Updated')
                return redirect('/profile/')
            else:
                form =UserProfileChangeForm(instance=request.user)
                user_data = request.user
                context = {'form':form,'user_data':user_data,'product':product,'main':main,'cart_count':cart_count}
                return render(request,'profile.html',context)
        
        return render(request,'profile.html',context)
    else:
        messages.info(request, '☹︎ Please Login First')
        return redirect('/signin')


def cartview(request):
    main = MaincategoryModel.objects.all()
    product=ProductModel.objects.all()
    if request.user.is_authenticated:
     
        user = request.user
        carts=cartmodel.objects.all()
        cart_count = cartmodel.objects.filter(user=request.user).count()
        cart_items = cartmodel.objects.filter(user=request.user)

        context={'carts':carts,'user':user,'main':main,'product':product}
        sub_total = 0
        ship_charge =0
    
        grand_total = 0
        for i in cart_items:
            sub_total += i.prod_total()
            ship_charged=(sub_total*10)/100
            ship_charge=int(ship_charged)
        grand_total = sub_total + ship_charge 

        context = {'cart_count': cart_count, 'cart_items': cart_items, 'sub_total': sub_total,
               'ship_charge': ship_charge, 'grand_total': grand_total,'user':user,'main':main,'product':product}
        return render(request,'cart.html',context)
    
    
def Add_to_cartView(request, id):
    user = request.user
    prod = ProductModel.objects.get(id=id)
    
    
    item_exist = cartmodel.objects.filter(product=prod).exists()

    if item_exist:
        get_item = cartmodel.objects.get(product__id=id)
        
        get_item.quantity += 1
        get_item.save()
        return redirect('/cart/')
    else:
        product = ProductModel.objects.get(id=id)
        
    cartmodel(user=user,product=product).save()
    return redirect('/cart/')


def deleteview(request,id):
    data=cartmodel.objects.get(id=id)
    data.delete()
    return redirect("/cart/")


def changequantity(request,id):
    get_item =cartmodel.objects.get(id=id)
    if get_item.quantity:
        get_item.quantity+=1
        get_item.save()
        return redirect('/cart/')

def Minusquantity(request,id):
    get_item = cartmodel.objects.get(id=id)
    if get_item:
        get_item.quantity -= 1
        get_item.save()
        if get_item.quantity==0:
            get_item.delete()
            return redirect('/')
        return redirect('/cart/')

def ClearcartView(request):
    get_item = cartmodel.objects.all()
    get_item.delete()
    return redirect('/')
    
def Add_to_wishlistView(request, id):
    user = request.user
    prod = ProductModel.objects.get(id=id)
    
    
    item_exist = wishlistmodel.objects.filter(product=prod).exists()

    if item_exist:
        get_item = wishlistmodel.objects.get(product__id=id)
        
        get_item.quantity += 1
        get_item.save()
        return redirect('/wishlist/')
    else:
        product = ProductModel.objects.get(id=id)
        
    wishlistmodel(user=user,product=product).save()
    return redirect('/wishlist/')


def wishlistview(request):
    main = MaincategoryModel.objects.all()
    product=ProductModel.objects.all()
    cart_count = cartmodel.objects.filter(user=request.user).count()
    wish = wishlistmodel.objects.filter(user=request.user)
    return render(request,'wishlist.html',{"wish":wish,'main':main,'product':product,'cart_count':cart_count})

def deletewishlishview(request,id):
    data=wishlistmodel.objects.get(id=id)
    data.delete()
    return redirect("/wishlist/")

def ClearwishlistView(request):
    get_item = wishlistmodel.objects.all()
    get_item.delete()
    return redirect('/')

# def CustomerAddressView(request):
#     all_address = CustomeraddressModel.objects.filter(user=request.user)
#     if request.user.is_authenticated:
#         if request.method == 'POST':
#             user=request.POST["user"]
#             fname=request.POST["fname"]
#             lname=request.POST["lname"]
#             email=request.POST["email"]
#             mobile=request.POST["mobile"]
#             counrty=request.POST["counrty"]
#             state = request.POST["state"]
#             city=request.POST["city"]
#             pincode = request.POST["pincode"]
#             add1=request.POST["add1"]
#             add2 = request.POST["add2"]
#             usr=CustomeraddressModel(user=user,fname=fname,lname=lname,email=email,mobile=mobile,counrty=counrty,state=state,city=city,pincode=pincode,add1=add1,
#             add2=add2)
#             usr.save()
#         return render(request,'address.html',{'all_address':all_address})
#     else:
#         messages.info(request, '☹ Please Login First')
#         return redirect('/signin/')

def CustomerAddressView(request):
    main = MaincategoryModel.objects.all()
    product=ProductModel.objects.all()
    cart_count = cartmodel.objects.filter(user=request.user).count()
    all_address = CustomeraddressModel.objects.filter(user=request.user)
    if request.user.is_authenticated:
        form = CustomeraddressForm(instance=request.user)
        context = {'form': form}
        if request.method == 'POST':
            form = CustomeraddressForm(request.POST)
            if form.is_valid():
                fm = form.save(commit=False)
                fm.user = request.user
                fm.save()

                messages.info(request, 'Address Successfully Added')
                return redirect('/address/')
        else:
            form = CustomeraddressForm(instance=request.user)

        context = {'form': form, 'all_address': all_address,'main':main,'product':product,'cart_count':cart_count}
        return render(request, 'address.html', context)
    else:
        messages.info(request, '☹ Please Login First')
        return redirect('/signin/')


def deleteaddressview(request,id):
    data=CustomeraddressModel.objects.get(id=id)
    data.delete()
    return redirect("/address/")

def UpdateaddressView(request, id):
    address = CustomeraddressModel.objects.all()  # Show data of Student Table
    set_address = CustomeraddressModel.objects.get(id=id)
    if request.method == 'POST':
        form = CustomeraddressForm(
            request.POST, request.FILES, instance=set_address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student Successfully Updated')
            return redirect('/address/')
    else:
        form = CustomeraddressForm(instance=set_address)
    context = {'form': form, 'address': address}
    return render(request, 'address.html', context)



def AllproductView(request):
    main = MaincategoryModel.objects.all()
    product=ProductModel.objects.all()
    all_categories = MaincategoryModel.objects.all()
    all_products = ProductModel.objects.all()
    cart_count = cartmodel.objects.filter(user=request.user).count()

    get_cat_id = request.GET.get('catesid')
    if get_cat_id:
        all_products = ProductModel.objects.filter(mcate__id=get_cat_id)

    get_product_name = request.GET.get('byname')
    if get_product_name:
        all_products = ProductModel.objects.filter(
            name__icontains=get_product_name)

    
    context = {'all_categories': all_categories, 'all_products': all_products,
               'cart_count': cart_count,'main':main,'product':product}
    return render(request, 'allproducts.html', context)

def CheckoutView(request):
    main = MaincategoryModel.objects.all()
    product=ProductModel.objects.all()
    cart_count = cartmodel.objects.filter(user=request.user).count()
    cart_items = cartmodel.objects.filter(user=request.user)
    all_address = CustomeraddressModel.objects.filter(user=request.user)
    # totals count -----
    sub_total = 0
    ship_charge = 0
    GST = 0
    grand_total = 0
    # get data for order
    usr = request.user
    get_address_id = request.GET.get('add')

    for i in cart_items:
        sub_total += i.prod_total()
        shiped= (sub_total*10)/100
        ship_charge=int(shiped)
        gst= (sub_total*5)/100
        GST= int(gst)
        grand_total = sub_total + ship_charge + GST
    # payment Start
    amount = (grand_total)*100 
    client = razorpay.Client(
        auth=("rzp_test_ZLqfk4WQ6xORgy", "T7NECwZVNhvOpW1jFp2qu6QB"))
    payment = client.order.create(
        {'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
    # payment End
    if get_address_id:
        address = CustomeraddressModel.objects.get(id=get_address_id)
        for i in cart_items:
            order_data = Order(
                user=usr,
                customer=address,
                product=i.product,
                quantity=i.quantity

            )
            order_data.save()
        cart_items.delete()
        
    context = {'cart_count': cart_count, 'cart_items': cart_items, 'sub_total': sub_total,
               'ship_charge': ship_charge, 'GST': GST, 'grand_total': grand_total, 'all_address': all_address,
               'payment': payment,'main':main,'product':product}
    return render(request, 'checkout.html', context)

def orderview(request):
    main = MaincategoryModel.objects.all()
    product=ProductModel.objects.all()
    cust_order= Order.objects.filter(user=request.user) 
    return render(request, 'orders.html', {'cust_order':cust_order,'main':main,'product':product})


def contactview(request):
    contacts=contactmodel.objects.filter(user=request.user)
    if request.user.is_authenticated:
        form=ContactForm(instance=request.user)
        context={'form':form}
        if request.POST:
            form=ContactForm(request.POST)
            if form.is_valid():
                fm=form.save(commit=False)
                fm.user=request.user
                fm.save()

                messages.info(request,'your message has been successfully send')
                return redirect('/contact/')

        else:
            form=ContactForm(instance=request.user)
        context={'form':form,'contacts':contacts}
        return render(request,'contact.html',context)
    
    else:
        messages.info(request, '☹ Please Login First')
        return redirect('/signin/')

def serchview(request):
    if request.method=='GET':
        searched=request.GET.get('searched')
        if searched:
            datas=ProductModel.objects.filter(name__icontains=searched)
    
            context={'searched':searched,'datas':datas}
            return render(request,'search.html',context)
        else:
            return HTTPResponse(request,"your search is not found")