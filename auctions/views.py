from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from .models import *
from .forms import CreateListingForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime



def index(request):
    product = Product.objects.all()
    if request.user.is_authenticated:  
        try: 
            watchlist = Watchlist.objects.get(user=request.user)        
            return render(request, "auctions/index.html", {
                "watchlist": watchlist,
                "product": product
            })
        except ObjectDoesNotExist:
            return render(request, "auctions/index.html", { 
            "product": product
            }) 
    return render(request, "auctions/index.html", { 
        "product": product
    })
    



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create_listing(request):
    try:
        if request.method == "POST":
            form = CreateListingForm(request.POST, request.FILES) #create an instance of the form from "forms.py" file, CreateListing - class name in forms.py
            if form.is_valid():
                instance = form.save(commit=False) # Return an object without saving to the DB
                instance.user = request.user # Add an User field which will contain current user's id
                instance.save() # Save the final "real form" to the DB      
            else:
                messages.error(request, "Error! Try again.")
            return HttpResponseRedirect("/")

        form = CreateListingForm()
        products = Product.objects.all() 
        watchlist = Watchlist.objects.get(user=request.user) 

        return render(request, "auctions/createListing.html", {
            "form": form,
            "products": products,
            "watchlist": watchlist        
        })
    except ObjectDoesNotExist:
        return render(request, "auctions/createListing.html", { 
        "form": form,
        "products": products,
        })

def categories(request):
        
    categories = Category.objects.all()
    try:
        watchlist = Watchlist.objects.get(user=request.user)     

        return render(request, "auctions/categories.html", {
            "watchlist": watchlist,
            "categories": categories
        })
    except ObjectDoesNotExist:
        return render(request, "auctions/categories.html", {
            "categories": categories
        })
    

def category_view(request, category):
    category = Category.objects.get(name=category)
    product = Product.objects.filter(category=category).all()
    try:
        watchlist = Watchlist.objects.get(user=request.user)     

        return render(request, "auctions/categoryView.html", {
            "watchlist": watchlist,
            "category": category,
            "product": product
        })
    except ObjectDoesNotExist:
        return render(request, "auctions/categoryView.html", {
            "category": category,
            "product": product
        })


@login_required(login_url="/login")
def listing_page(request, product):
    if request.method == "GET":
        try:
            product = Product.objects.get(title=product)
            watchlist = Watchlist.objects.get(user=request.user)          
            
            return render(request, "auctions/listingPage.html", {            
                "product": product,
                "watchlist": watchlist
            })
        except ObjectDoesNotExist:            
             return render(request, "auctions/listingPage.html", {            
                "product": product
            })



def add_to_watchlist(request, product):
    if request.method == "POST":
        product_to_watchlist = Product.objects.get(title=product)
        watchlist, created = Watchlist.objects.get_or_create(user=request.user)

        if product_to_watchlist in watchlist.product.all():
            watchlist.product.remove(product_to_watchlist)
            watchlist.save()
        else:
           watchlist.product.add(product_to_watchlist)
           watchlist.save()
        return render(request, "auctions/watchlist.html", {

            "watchlist": watchlist
        })


def show_watchlist(request):
    try:
        watchlist = Watchlist.objects.get(user=request.user)
        num_of_prod = watchlist.product.count()
        return render(request, "auctions/watchlist.html", {
            "watchlist": watchlist,
            "num_of_prod": num_of_prod
        })
    except ObjectDoesNotExist:
        return render(request, "auctions/watchlist.html")

def set_new_bid(request, product):
    if request.method == "POST":
        product = Product.objects.get(title=product)
        new_bid = request.POST.get("new-bid")
        default_bid = Bid.objects.create(user=request.user, product=product, bid=product.start_bid)              
        bid = Bid.objects.create(user=request.user, product=product, bid=new_bid) #create an instance of a bid       
            
        try: 
           error_check = product.last_bid.bid # without this check AttributeError, when try to set first new bid
        except AttributeError:
            product.last_bid = default_bid
            product.save()   
        
        if float(new_bid) > product.last_bid.bid:            
            #set last bid for product
            product.last_bid = bid
            product.bids.add(bid) #add bid to liat of bids
            product.save()
        else:
            messages.error(request, "Your bid should be greater then current bid!")        

        return redirect(request.META.get('HTTP_REFERER')) # refresh page after form submitting
        
def comment(request, product):
    product = Product.objects.get(title=product)
    prod_comments = product.comment.all()

    if request.method == "POST":        
        comment = request.POST.get("comment")
        new_comment = Comment.objects.create(user=request.user, product=product, text=comment)
        product.comment.add(new_comment)
        new_comment.save()
    return redirect(request.META.get('HTTP_REFERER'))

def close_auction(request, product):
    if request.method == "GET":
        product = Product.objects.get(title=product)
        product.closed = True 
        product.save()

    return redirect(request.META.get('HTTP_REFERER'))

def delete_product(request, product):
    if request.method == "GET":
        product = Product.objects.get(title=product)
        product.delete()
        
    return HttpResponseRedirect("/")

def my_listings(request):
    product = Product.objects.filter(user=request.user).all()
    try:
        watchlist = Watchlist.objects.get(user=request.user)        
        return render(request, "auctions/myListings.html", {
            "product": product,
            "watchlist": watchlist
        })
    except ObjectDoesNotExist:
        return render(request, "auctions/myListings.html", {
            "product": product
        })



