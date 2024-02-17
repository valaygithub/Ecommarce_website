import random

import razorpay
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import HttpResponse, redirect, render
from estore.models import Cart, Order, Products

# Create your views here.



def register(request):
    context = {}
    if request.method == "POST":
        fname = request.POST["sname"]
        lname = request.POST["lname"]
        uname = request.POST["uname"]
        pwd = request.POST["pwd"]
        cpwd = request.POST["cpwd"]
        if fname == "" or lname == "" or uname == "" or pwd == "" or cpwd == "":
            context["errmsg"] = "Field not empty"
            return render(request, "register.html", context)
        elif pwd != cpwd:
            context["errmsg"] = "Password Does Not Match"
            return render(request, "register.html", context)
        else:
            try:
                u = User.objects.create(
                    password=pwd, username=uname, first_name=fname, last_name=lname
                )
                u.set_password(pwd)
                u.save()
                context["success"] = "user created succesfully"
                return redirect("/login")
            except Exception:
                context["errmsg"] = "user with same username already exist"
                return render(request, "register.html", context)
    else:
        return render(request, "register.html")


def user_login(request):
    context = {}
    if request.method == "POST":
        uname = request.POST["uname"]
        pwd = request.POST["pwd"]
        # print(uname)
        # print(pwd)
        # return HttpResponse("data fetch succesfully")
        if uname == "" or pwd == "":
            context["errmsg"] = "field cannot be empty"
            return render(request, "login.html", context)
        else:
            u = authenticate(username=uname, password=pwd)
            # print(u)
            # print(u.is_superuser)
            # return HttpResponse("data is fetched")
            if u is not None:
                login(request, u)
                return redirect("/main")

            else:
                context["errmsg"] = "Invalid credentials"
                return render(request, "login.html", context)
    else:
        return render(request, "login.html")


def user_logout(request):
    logout(request)
    return redirect("/main")


def homeapp(request):
    context = {}
    p = Products.objects.filter(is_active=True)
    context["products"] = p
    return render(request, "index.html", context)


def catfilter(request, cv):
    q1 = Q(is_active=True)
    q2 = Q(category=cv)
    p = Products.objects.filter(q1 & q2)
    context = {}
    context["products"] = p
    return render(request, "index.html", context)


def sort(request, sv):
    if sv == "0":
        col = "price"
    else:
        col = "-price"
    p = Products.objects.filter(is_active=True).order_by(col)
    context = {}
    context["products"] = p
    return render(request, "index.html", context)


def Product_Detail(request, pid):
    context = {}
    context["products"] = Products.objects.filter(id=pid)
    return render(request, "productdetail.html", context)


def addtocart(request, pid):
    if request.user.is_authenticated:
        u = User.objects.filter(id=request.user.id)
        # print(u)
        # print(u[0])
        # print(u[0].username)
        # print(u[0].is_superuser)
        p = Products.objects.filter(id=pid)
        # check product exists or not
        q1 = Q(uid=u[0])
        q2 = Q(pid=p[0])
        c = Cart.objects.filter(q1 & q2)
        n = len(c)
        context = {}
        context["products"] = p
        if n == 1:
            context["msg"] = "products already exist in cart"
        else:
            c = Cart.objects.create(uid=u[0], pid=p[0])
            c.save()

            context["success"] = "product added succesfully to cart"

        return render(request, "productdetail.html", context)
    else:
        return redirect("/login")


def cart(request):
    userid = request.user.id
    c = Cart.objects.filter(uid=userid)
    # print(c)
    # print(c[0])
    # print(c[0].uid)
    # print(c[0].pid.name)
    s = 0
    np = len(c)
    for x in c:
        # print(x)
        # print(x.pid.price)
        s = s + x.pid.price * x.qty
    context = {}
    context["products"] = c
    context["total"] = s
    context["n"] = np
    return render(request, "cart.html", context)


def remove(request, cid):
    c = Cart.objects.filter(id=cid)
    c.delete()
    return redirect("/cart")


def updateqty(request, qv, cid):
    # print(type(qv))
    # return HttpResponse("in update quantity")
    c = Cart.objects.filter(id=cid)
    print(c)
    print(c[0])
    print(c[0].qty)
    if qv == "1":
        t = c[0].qty + 1
        c.update(qty=t)
    else:
        if c[0].qty > 1:
            t = c[0].qty - 1
            c.update(qty=t)
    return redirect("/cart")


def place_order(request):
    userid = request.user.id
    c = Cart.objects.filter(uid=userid)
    # print(c)
    oid = random.randrange(1000, 9999)
    print("order id:", oid)
    for x in c:
        # print(x)
        # print(x.pid)
        # print(x.uid)
        # print(x.qty)
        o = Order.objects.create(order_id=oid, pid=x.pid, uid=x.uid, qty=x.qty)
        o.save()
        # x.delete()
    orders = Order.objects.filter(uid=request.user.id)
    s = 0
    np = len(orders)
    for x in orders:
        s = s + x.pid.price * x.qty
    context = {}
    context["products"] = orders
    context["total"] = s
    context["n"] = np
    context["u"] = orders
    return render(request, "place_order.html", context)


def makepayment(request):
    orders = Order.objects.filter(uid=request.user.id)
    s = 0
    # np=len(c)
    for x in orders:
        # print(x)
        # print(x.pid.price)
        s = s + x.pid.price * x.qty
        oid = x.order_id
    client = razorpay.Client(
        auth=("rzp_test_TuohmRdB5px4RT", "h8g132xQNvAAJ6356qXILTrn")
    )

    data = {"amount": s * 100, "currency": "INR", "receipt": "oid"}
    payment = client.order.create(data=data)
    print(payment)
    context = {}
    context["data"] = payment
    x=request.user.username
    context['mail']=x
    return render(request, "pay.html", context)


def sendusermail(request,mail):
    uemail = request.user.username
    print(request.user.is_authenticated)
    uemail=mail
    # #print(uemail)

    send_mail(
        "Ekart-order place successfully",
        "order details are:",
        "valaykhade04@gmail.com",
        [uemail],
        fail_silently=False,
    )
    return HttpResponse("Receipt Share succesfully send")


def myaccount(request):
    return render(request, "my_account.html")


def ordercomplete(request):
    return render(request, "order_completed")
