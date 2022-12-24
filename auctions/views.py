from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Category, Listings, Comment, Bid


def closeAuction(request, id):
    listingObject = Listings.objects.get(pk=id)
    listingObject.active = False
    listingObject.save()
    categories = Category.objects.all()
    listingExistInWatchList = request.user in listingObject.watchlist.all()
    comments = Comment.objects.filter(product = listingObject)
    return render(request, "auctions/listing.html",{
        "listing": listingObject,
        "categories" : categories,
        "listingExistInWatchList": listingExistInWatchList,
        "comments":comments,
        "message": "The auction is closed."
        })

def removeFromWatchList(request, id):
    listingObject = Listings.objects.get(pk=id)
    listingObject.watchlist.remove(request.user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def addComment(request, id):
    listingObject = Listings.objects.get(pk=id)
    user = request.user
    comment = request.POST["comment"]

    newComment = Comment(
        customer=user,
        product=listingObject,
        message=comment
    )
    newComment.save()

    return HttpResponseRedirect(reverse("listing", args=(id, )))

def addBid(request, id):
    listingObject = Listings.objects.get(pk=id)
    categories = Category.objects.all()
    listingExistInWatchList = request.user in listingObject.watchlist.all()
    comments = Comment.objects.filter(product = listingObject)
    user = request.user
    newbid = request.POST["newbid"]
    if int(newbid) > listingObject.price.bid:
        currentPrice = Bid(
            bidder=user,
            bid=int(newbid)
        )
        currentPrice.save()
        listingObject.price = currentPrice
        listingObject.save()

        return render(request, "auctions/listing.html",{
        "listing": listingObject,
        "categories" : categories,
        "listingExistInWatchList": listingExistInWatchList,
        "comments":comments,
        "message": "Bid successfull",
        "success": True
        })

    else:
        return render(request, "auctions/listing.html",{
        "listing": listingObject,
        "categories" : categories,
        "listingExistInWatchList": listingExistInWatchList,
        "comments":comments,
        "message": "Bid error. The bid must be greater than the starting bid.",
        "success": False
        })
    

def displayWatchList(request):
    currentUser = request.user
    watchlists = currentUser.wishlist.all()
    return render(request, "auctions/watchlist.html",{
        "listings": watchlists
    })

def addToWatchList(request, id):
    listingObject = Listings.objects.get(pk=id)
    listingObject.watchlist.add(request.user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))
    

def listing(request, id):
    listingObject = Listings.objects.get(pk=id)
    categories = Category.objects.all()
    listingExistInWatchList = request.user in listingObject.watchlist.all()
    comments = Comment.objects.filter(product = listingObject)

    return render(request, "auctions/listing.html",{
        "listing": listingObject,
        "categories" : categories,
        "listingExistInWatchList": listingExistInWatchList,
        "comments":comments
    })

def index(request):
    listings = Listings.objects.filter(active=True)
    nonactiveListing = Listings.objects.filter(active=False)
    categories = Category.objects.all()
    return render(request, "auctions/index.html",{
        "listings": listings,
        "categories" : categories,
        "nonactiveListing":nonactiveListing
    })

def selected_category(request):
    if request.method == "POST":
        selectedCategory = request.POST['category']
        category = Category.objects.get(category_name=selectedCategory)
        listings = Listings.objects.filter(active=True, category=category)
        categories = Category.objects.all()
        return render(request, "auctions/index.html",{
            "category_name":selectedCategory,
            "listings": listings,
            "categories" : categories,
            "show_category":True
        })


def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html",{
        "categories" : categories 
    })

@login_required
def create(request):
    if request.method == "GET":
        categories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories" : categories 
        }) 
        
    elif request.method == "POST":
        user = request.user
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"]
        image = request.POST["image"]
        category = request.POST["category"]

        # add the listing to the listings 

        category_objects = Category.objects.get(category_name=category)
        bidPrice = Bid(
            bid = int(price),
            bidder = user
        )
        bidPrice.save()

        newListing = Listings(
            owner = user,
            title=title,
            description=description,
            price= bidPrice,
            image=image,
            category=category_objects
        )
        newListing.save()
        return HttpResponseRedirect(reverse("index"))

def login_view(request):
    categories = Category.objects.all()
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
                "message": "Invalid username and/or password.",
                "categories" : categories 
            })
    else:
        return render(request, "auctions/login.html",{
            "categories" : categories 
        })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    categories = Category.objects.all()
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match.",
                "categories" : categories 
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken.",
                "categories" : categories 
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html",{
            "categories" : categories 
        })
