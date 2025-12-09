from django.contrib.auth.models import AbstractUser
from django.db import models


class Category(models.Model):
    """
    Represents a category for auction items.

    Attributes:
        name (str): The name of the category.
    """
    name = models.CharField(max_length=64)

    def __str__(self):
        """
        Returns the string representation of the category.

        Returns:
            str: The name of the category.
        """
        return str(self.name)


class Item(models.Model):
    """
    Represents an item available for auction.

    Attributes:
        title (str): The title of the item.
        description (str): A description of the item.
        starting_bid (Decimal): The starting bid amount for the item.
        isopen (bool): Whether the auction for this item is currently open.
        category (Category): The category the item belongs to.
        owner (User): The user who owns the item.
        image (str): URL of the item's image.
    """
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=200, null=True)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    isopen = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name="items", null=True)
    owner = models.ForeignKey('User', on_delete=models.CASCADE, related_name="owned_items")
    image = models.URLField(default="https://images.vexels.com/media/users/3/145641/isolated/preview/30bc99162bca69bdbd27451ceeef8848-earth-stone-illustration.png")

    def __str__(self):
        """
        Returns the string representation of the item.

        Returns:
            str: The title and owner of the item.
        """
        return f"{self.title}: owned by {self.owner}"


class User(AbstractUser):
    """
    Represents a user in the auction system.

    Attributes:
        watchlist (ManyToManyField): Items that the user has added to their watchlist.
    """
    watchlist = models.ManyToManyField(Item, blank=True, related_name="watched_by")

    def __str__(self):
        """
        Returns the string representation of the user.

        Returns:
            str: The username.
        """
        return self.username


class Comment(models.Model):
    """
    Represents a comment made on an auction item.

    Attributes:
        text (str): The content of the comment.
        item (Item): The item the comment is associated with.
        like (int): Number of likes the comment has received.
        by (User): The user who made the comment.
    """
    text = models.TextField(max_length=200)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="comments")
    like = models.PositiveIntegerField(default=0)
    by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", null=True)

    def __str__(self):
        """
        Returns the string representation of the comment.

        Returns:
            str: The content of the comment.
        """
        return self.text


class Bid(models.Model):
    """
    Represents a bid placed on an auction item.

    Attributes:
        amount (Decimal): The amount of the bid.
        item (Item): The item the bid is placed on.
        timestamp (datetime): The time the bid was placed.
        bidder (User): The user who placed the bid.
    """
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="bids")
    timestamp = models.DateTimeField(auto_now_add=True)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        """
        Returns the string representation of the bid.

        Returns:
            str: A string describing the bidder and the amount.
        """
        return f"{self.bidder} bids {self.amount}"
