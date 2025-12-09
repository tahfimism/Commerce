# Commerce - Auction Site

A Django-based e-commerce auction site where users can post auction listings, place bids on listings, comment on those listings, and add listings to a "watchlist".

## Features

*   **Create Listings:** Users can create new auction listings with a title, description, starting bid, and category.
*   **Active Listings Page:** The default route displays all currently active auction listings.
*   **Listing Page:** Clicking on a listing allows users to view details, current price, and place bids.
    *   If the user is signed in, they can add the item to their watchlist.
    *   If the user is the owner, they can close the auction.
*   **Watchlist:** Users can view a list of all listings they have added to their watchlist.
*   **Categories:** Listings can be filtered by category.
*   **Comments:** Users can leave comments on listing pages.
*   **Admin Interface:** Site administrators can view, add, edit, and delete listings, comments, and bids.

## Project Structure

The project consists of the following main components:

*   `auctions/`: The main application containing models, views, and templates for the auction functionality.
    *   `models.py`: Defines the database schema (User, Category, Item, Bid, Comment).
    *   `views.py`: Contains the business logic for handling requests and rendering templates.
    *   `urls.py`: Defines the URL patterns for the application.
    *   `templates/auctions/`: Contains the HTML templates.
*   `commerce/`: The project configuration directory.
    *   `settings.py`: Project settings and configuration.
    *   `urls.py`: Root URL configuration.
*   `manage.py`: Django's command-line utility.

## Getting Started

### Prerequisites

*   Python 3.x
*   Django

### Installation

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    cd commerce
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  Apply database migrations:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

4.  Create a superuser (optional, for admin access):
    ```bash
    python manage.py createsuperuser
    ```

### Usage

1.  Run the development server:
    ```bash
    python manage.py runserver
    ```

2.  Open your web browser and navigate to `http://127.0.0.1:8000/`.

## Contributing

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature-branch`).
3.  Make your changes.
4.  Commit your changes (`git commit -am 'Add new feature'`).
5.  Push to the branch (`git push origin feature-branch`).
6.  Create a Pull Request.
