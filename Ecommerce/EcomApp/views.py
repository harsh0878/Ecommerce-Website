
import random
from django.shortcuts import redirect, render,HttpResponse
from . models import Product,CartItem,Order
from django.db.models import Q
from . forms import CreateUserForm,AddProduct
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
import razorpay

# Create your views here.
def index (request):
    products = Product.objects.all()
    context = {}
    context['products'] = products
    return render(request, "index.html",context)


def details(req,pid):
    products = Product.objects.get(product_id = pid)
    context = {'products':products}
    return render(req,"details.html",context)

def cart(req):
    if req.user.is_authenticated:
        allproducts = CartItem.objects.filter(user=req.user)
    else:
        return redirect("/login")
    context = {}
    context['cart_items'] = allproducts
    total_price=0
    for x in allproducts:
        total_price += (x.product.price * x.quantity)
        print(total_price)
    context['total'] = total_price
    length = len(allproducts)
    context['items'] = length
    return render(req, "cart.html", context)

def add_cart(req,pid):
    products = Product.objects.get(product_id = pid)
    user = req.user if req.user.is_authenticated else None
    print(products)
    if user:
        cart_item,created = CartItem.objects.get_or_create(product=products,user=user)
        print(cart_item,created)
    else:
        return redirect("/login")
       # cart_item,created = CartItem.objects.get_or_create(product=products)

    if not created:
        cart_item.quantity += 1

    else:
        cart_item.quantity = 1
    cart_item.save()
    return redirect("/cart")

def delete(req,pid):
    d = CartItem.objects.filter(product_id=pid,user=req.user)
    d.delete()
    return redirect('/cart')

def search(req):
    query = req.POST['q']
    print(f"Received query is {query}")
    if not query: 
        result = Product.objects.all()
    else:
        result =  Product.objects.filter(
            Q(product_name__icontains = query)|
            Q(price__icontains = query)|
            Q(category__icontains = query)
            
        )
    return render(req, 'search.html',{'result':result,'query':query})

def range(req):
    r1 = req.POST.get("min")
    r2 = req.POST.get("max")
    print(r1,r2)
    if r1 is not None and r2 is not None and r1!="" and r2 !="":
        queryset= Product.prod.get_price_range(r1,r2)
        print(queryset)
        context={'products':queryset}
        return render(req,"index.html",context)
    

def watchList(req):
    queryset = Product.prod.watch_list()
    print(queryset)
    context={'products':queryset}
    return render(req,"index.html", context)


def laptopList(req):
    queryset = Product.prod.laptop_list()
    print(queryset)
    context={'products':queryset}
    return render(req,"index.html", context)


def mobileList(req):
    queryset = Product.prod.mobile_list()
    print(queryset)
    context={'products':queryset}
    return render(req,"index.html", context)

def sort(req):
    queryset = Product.objects.all().order_by("price")
    context = {'products':queryset}
    return render(req,"index.html",context)


def hightolow(req):
    queryset = Product.objects.all().order_by("price")
    queryset=Product.prod.price_order()
    context = {'products':queryset}
    return render(req,"index.html",context)

def updateqty(req,uval,pid):
    #products = CartItem.objects.get(product_id = pid)
    user = req.user
    c = CartItem.objects.filter(product_id = pid,user=user)
    if uval == 1:
        a = c[0].quantity + 1
        c.update(quantity = a)
        print(c[0].quantity)
    else:
        a = c[0].quantity -1
        c.update(quantity=a)
        print(c[0].quantity)
    return redirect ("/cart")

def register_user(req):
    form = CreateUserForm()
    if req.method == "POST":
        form = CreateUserForm(req.POST)
        if form.is_valid():
            form.save()
            messages.success(req,("User Created Successfully"))
            return redirect ("/login")
        else:
            messages.error(req,"Incorrect Password Format")
    context = {'form':form}
    return render(req,"register.html",context)


def login_user(req):
    if req.method == "POST":
        username = req.POST["username"]
        password = req.POST["password"]
        user = authenticate(req,username=username,password=password)
        if user is not None:
            login(req,user)
            messages.success(req,("User Logged Successfully"))
            return redirect("/")
        else: 
            messages.error(req,"Incorrect username or password ")
            return redirect("/login")
    else:
        return render(req,"login.html")


def logout_user(req):


    logout(req)
    messages.success(req,("You have logged out"))
    return redirect("/")


def vieworder(req):
    c=CartItem.objects.filter(user=req.user)
    """ oid=random.randrange(1000,9999)
    for x in c:
        Order.objects.create(order_id=oid,product_id=x.product.product_id, user=req.user , quantity=x.quantity)
        orders= Order.objects.filter(user=req.user,is_completed= False) """
    context={}
    context['cart_items']=c
    total_price=0
    for x in c:
        total_price += (x.product.price*x.quantity)
        print(total_price)
    context['total']= total_price
    length= len(c)
    context['item']= length
    return render(req,'vieworder.html',context)
        
def payment(req):
    c = CartItem.objects.filter(user=req.user)
    oid=random.randrange(1000,9999)
    for x in c:
        Order.objects.create(order_id=oid,product_id=x.product.product_id, user=req.user , quantity=x.quantity)

    orders = Order.objects.filter(user=req.user,is_completed = False)
    total_price = 0
    for x in orders:
       total_price += (x.product.price * x.quantity)
       oid = x.order_id
       print(oid)
    client = razorpay.Client(auth=("rzp_test_nWxKqH6dkJnveX", "PlbasuQTznlAIlT9GPscUWip",))
    data ={ 
      "amount": total_price * 100,
      "currency": "INR",
      "receipt": "oid"
    }
    payment = client.order.create(data = data)
    print(payment)
    context = {}
    context['data'] = payment
    context['amount'] = payment["amount"]
    c = CartItem.objects.filter(user=req.user)
    c.delete()
    orders.update(is_completed= True)
    return render(req,"payment.html",context)


def insertProduct(req):
    if req.user.is_authenticated:
        if req.method=="GET":
            form = AddProduct()
            return render(req,"insertProd.html",{'form':form})
        else:
            form = AddProduct(req.POST,req.FILES or None)
            if form.is_valid():
                form.save()
                messages.success(req,("Product Entered Successfully"))
                return redirect("/")
            else:
                messages.error(req,"Incorrect data")
                return render(req,"insertProd.html",{'form':form})
    else:
        return redirect("/login")
  
        

