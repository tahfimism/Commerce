from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Item, Comment, Category, Bid


def index(request):
    """
    Renders the index page displaying active and closed auction items.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered index page.
    """
    return render(request, "auctions/index.html", {
        "items": Item.objects.filter(isopen=True).all(),
        "closed_items": Item.objects.filter(isopen=False).all(),

    })


def item(request, item_id):
    """
    Renders the details page for a specific auction item and handles interactions.

    This view handles displaying item details, placing bids, adding/removing
    from watchlist, adding comments, and closing the auction.

    Args:
        request (HttpRequest): The HTTP request object.
        item_id (int): The ID of the item to display.

    Returns:
        HttpResponse: The rendered item page.
    """
    item = Item.objects.get(pk=item_id)
    bids = item.bids.all().order_by('-amount')
    price = bids.order_by('-amount').first().amount if bids.exists() else item.starting_bid
    message = None
    winning_bidder = None

    if request.method == "POST":
        # Watchlist actions
        if "watchlist_action" in request.POST:
            if request.POST["watchlist_action"] == "add":
                request.user.watchlist.add(item)
                message = "Added to watchlist"
            else:
                request.user.watchlist.remove(item)
                message = "Removed from watchlist"

        # Bidding actions
        elif "bid_place" in request.POST:
            bid_input = request.POST.get("bid_place")
            try:
                bid_placed = float(bid_input)
                if (bids.exists() and bid_placed > bids.first().amount) or ((not bids.exists()) and bid_placed > item.starting_bid):
                    Bid.objects.create(amount=bid_placed, item=item, bidder=request.user)
                    message = "Bid successful"
                else:
                    message = "Bid too low"
            except (TypeError, ValueError):
                message = "Invalid bid amount."

        # Comment actions
        elif "comment_text" in request.POST:
            comment_text = request.POST.get("comment_text")
            if comment_text and request.user.is_authenticated:
                Comment.objects.create(text=comment_text, item=item, by=request.user)
                message = "Comment added."

        # Close auction
        elif "close_auction" in request.POST and request.user == item.owner:
            item.isopen = False
            item.owner = item.bids.order_by('-amount').first().bidder
            item.save()
            message = f"Auction closed. Item is now owned by {item.owner}"

    # Always render once at the end
    return render(request, "auctions/item.html", {
        "item": item,
        "price": price,
        "bids": bids,
        "message": message,
        "comments": item.comments.all(),
        "winning_bidder": winning_bidder,
    })


def watchlist(request):
    """
    Renders the user's watchlist.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered watchlist page.
    """
    items = request.user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "items": items,
    })


def categories(request):
    """
    Renders a list of all categories.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered categories page.
    """
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })


def category(request, category_name):
    """
    Renders the items within a specific category.

    Args:
        request (HttpRequest): The HTTP request object.
        category_name (str): The name of the category to display.

    Returns:
        HttpResponse: The rendered category page.
    """
    category = Category.objects.get(name=category_name)
    return render(request, "auctions/category.html", {
        "category": category,
    })


def create(request):
    """
    Handles the creation of a new auction item.

    If the request method is POST, it processes the form data to create a new item.
    Otherwise, it renders the item creation form.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered creation page or a redirect to index.
    """
    if request.method == "POST":
        form = request.POST
        Item.objects.create(
            title=form["title"],
            starting_bid=form["starting_bid"],
            category=Category.objects.get(pk=form["category"]),
            image=form["image_url"],
            description=form["description"],
            isopen=True,
            owner=request.user
        )
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/create.html", {
        "categories": Category.objects.all()
    })


def login_view(request):
    """
    Handles user login.

    If the request method is POST, it attempts to authenticate the user.
    Otherwise, it renders the login form.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered login page or a redirect to index.
    """
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
    """
    Handles user logout.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A redirect to the index page.
    """
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    """
    Handles user registration.

    If the request method is POST, it attempts to create a new user.
    Otherwise, it renders the registration form.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered registration page or a redirect to index.
    """
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
