from django.shortcuts import render, redirect
from AdminApp.models import Category, Product, UserInfo, PaymentMaster
from UserApp.models import MyCart, OrderMaster
from django.core.paginator import Paginator
from django.contrib import messages
from datetime import datetime
# from django.db.models import 

product_per_page = 16
# Create your views here.
def homepage(request):
    # Fetch all records from category table
    cats = Category.objects.all()

    ordering = request.GET.get('ordering', "")     # http://www.wondershop.in:8000/listproducts/?page=1&ordering=price
    search = request.GET.get('query', "")
    price = request.GET.get('price', "")

    # Pagination logic
    items = Product.objects.all().order_by("id")
    paginator = Paginator(items, product_per_page)
    page_number = request.GET.get('page')
    ServiceDataFinal = paginator.get_page(page_number)
    totalPage = ServiceDataFinal.paginator.num_pages

    return render(request, "index.html",{"cats":cats,
            "books":[n+1 for n in range(totalPage)],
            "ServiceData":ServiceDataFinal,
            'lastpage':totalPage})

def signin(request):
    cats = Category.objects.all()
    books = Product.objects.all()
    if(request.method == "GET"):
        return render(request,"signin.html",{"cats":cats, "books":books})
    else:
        uname = request.POST["uname"]
        password = request.POST["password"]
        try:
            user = UserInfo.objects.get(username=uname, password=password)
        except:
            return redirect(signin)
        else:
            # Create session
            request.session["uname"]=uname
            return redirect(homepage)

def signup(request):
    cats = Category.objects.all()
    books = Product.objects.all()
    if(request.method == "GET"):
        return render(request,"signup.html",{"cats":cats, "books":books})
    else:
        uname = request.POST["uname"]
        email = request.POST["email"]
        password = request.POST["password"]
        user = UserInfo(uname, email, password)
        user.save()
        return redirect(homepage)

def search(request):
    cats = Category.objects.all()
    books = Product.objects.all()

    query = request.GET["query"]
    allPosts = Product.objects.filter(pname__icontains=query).values()
    # print("Output:",allPosts)
    return render(request,'search.html',{"cats":cats, "books":books,"allProd":allPosts,"query":query})

def userProfile(request):
    cats = Category.objects.all()  
    books = Product.objects.all()
    return render(request,"Profile.html",{"cats":cats,"books":books})

def signout(request):
    request.session.clear()
    return redirect(homepage)        

def addToCart(request):
    if(request.method == "POST"):
        if("uname" in request.session):
            # Add to cart
            # User & Product
            bookid = request.POST["bookid"]
            user = request.session["uname"]
            qty = request.POST["qty"]
            book = Product.objects.get(id=bookid)
            user = UserInfo.objects.get(username=user)
            # Check for duplicate entry
            try:
                cart = MyCart.objects.get(book=book, user=user)
            except:
                cart = MyCart()
                cart.user = user
                cart.book = book
                cart.qty = qty
                cart.save()
                return redirect(ShowAllCartItems)
            else:
                return redirect(signin)

def ShowAllCartItems(request):
    # Cart items- cats,books
    cats = Category.objects.all()
    books = Product.objects.all()

    unam = request.session["uname"]
    user = UserInfo.objects.get(username=unam)
    if(request.method == "GET"):
        cartitems = MyCart.objects.filter(user=user)
        total_p = 0
        for item in cartitems:
            total_p += round(item.qty*item.book.price,2)
        
        if total_p > 249:
            request.session["total"] = total_p
        elif total_p == 0:
            request.session["total"] = 0
        else:
            request.session["total"] = total_p + 40

        return render(request,"ShowAllCartItems.html",{"items":cartitems, "cats":cats, "books":books})
    else:
        b_id = request.POST["bookid"]
        book = Product.objects.get(id=b_id)
        item = MyCart.objects.get(user=user, book=book)            
        bookid = request.POST['bookid']
        qty = request.POST['qty']
        book = Product.objects.get(id=bookid)
        cart = MyCart.objects.get(book=book, user=user)
        cart.qty = qty
        cart.save()
        return redirect(ShowAllCartItems)

def removeItem(request):
    # Remove product code
    u_name = request.session["uname"]
    user = UserInfo.objects.get(username = u_name)
    b_id = request.POST["bookid"]
    book = Product.objects.get(id = b_id)
    item = MyCart.objects.get(user = user, book = book)
    item.delete()
    item.save()
    return redirect(ShowAllCartItems)

def MakePayment(request):
    if(request.method == "GET"):
        return render(request,"MakePayment.html",{})
    else:
        cardno = request.POST["cardno"]
        cvv = request.POST["cvv"]
        expiry = request.POST["expiry"]
        try:
            buyer = PaymentMaster.objects.get(cardno=cardno, cvv=cvv, expiry=expiry)
        except:
            return redirect(MakePayment)
        else:
            # it is a Match
            owner = PaymentMaster.objects.get(cardno='1111 2222 3333 4444', cvv='549', expiry='10/2028')
            owner.balance += request.session["total"]
            buyer.balance -= request.session["total"]
            owner.save()
            buyer.save()
            # Delete data from cart
            unam = request.session["uname"]
            user = UserInfo.objects.get(username=unam)
            order = OrderMaster()
            order.user = user
            order.amount = request.session["total"]
            details = ""
            items = MyCart.objects.filter(user=user)
            for item in items:
                details += (item.book.p_short_name)+","
                item.delete()     
            order.details = details
            order.save()
            messages.success(request,"Ordered Successfully 💐")
            return redirect(homepage)


def ShowBooks(request,id):
    # Get returns single object
    id = Category.objects.get(id=id)
    # Filter returns multiple objects
    books = Product.objects.filter(cat = id)
    cats = Category.objects.all()
    return render(request,"index.html",{"cats":cats, "books":books})

def ViewDetails(request,id):
    # cart items
    cats = Category.objects.all()
    books = Product.objects.all()

    book = Product.objects.get(id=id)
    return render(request,"ViewDetais.html",{"book":book,"cats":cats, "books":books})

def payments(request):
    cats = Category.objects.all()
    books = Product.objects.all()
    return render(request,"payments.html",{"cats":cats, "books":books})

def returns(request):
    cats = Category.objects.all()
    books = Product.objects.all()
    return render(request,"returns.html",{"cats":cats, "books":books})

def aboutTheProg(request):
    cats = Category.objects.all()
    books = Product.objects.all()
    return render(request,"aboutTheProg.html",{"cats":cats, "books":books})

def tandc(request):
    cats = Category.objects.all()
    books = Product.objects.all()
    return render(request,"t&c.html",{"cats":cats, "books":books})

def contactUs(request):
    cats = Category.objects.all()
    books = Product.objects.all()
    return render(request,"contactUs.html",{"cats":cats, "books":books})

def shipping(request):
    cats = Category.objects.all()
    books = Product.objects.all()
    return render(request,"shipping.html",{"cats":cats, "books":books})

def aboutus(request):
    cats = Category.objects.all()
    books = Product.objects.all()
    return render(request,"aboutus.html",{"cats":cats, "books":books})

def careers(request):
    cats = Category.objects.all()
    books = Product.objects.all()
    return render(request,"careers.html",{"cats":cats, "books":books})

def faq(request):
    cats = Category.objects.all()
    books = Product.objects.all()
    return render(request,"FAQs.html",{"cats":cats, "books":books})

def privacypolicy(request):
    cats = Category.objects.all()
    books = Product.objects.all()
    return render(request,"Pri-Pol.html",{"cats":cats, "books":books})