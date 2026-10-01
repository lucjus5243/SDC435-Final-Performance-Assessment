# Name: Lucas Justiniano
# Date: October 1, 2026
# Selected Option: Option 1 - Document Database (MongoDB)
# Summary: This Python application connects to the Amazon_EN_Reviews
# MongoDB database and provides a menu-driven system for performing
# CRUD operations on the ReviewData and ProductData collections.

from pymongo import MongoClient

# ------------------------------------------------------------
# DATABASE CONNECTION
# ------------------------------------------------------------

client = MongoClient("mongodb://localhost:27017/")

db = client["Amazon_EN_Reviews"]
review_collection = db["ReviewData"]
product_collection = db["ProductData"]


# ------------------------------------------------------------
# CREATE PRODUCT DATA FROM IMPORTED REVIEW DATA
# ------------------------------------------------------------

def create_product_data():
    """
    Populates ProductData using the product information contained
    in the imported ReviewData collection.
    """

    if product_collection.count_documents({}) == 0:

        products = {}

        for review in review_collection.find(
            {},
            {"product_id": 1, "product_category": 1}
        ):
            product_id = review.get("product_id")
            category = review.get("product_category")

            if product_id:
                products[product_id] = {
                    "product_id": product_id,
                    "product_category": category
                }

        if products:
            product_collection.insert_many(list(products.values()))

        print("ProductData collection created from imported review data.")


# ------------------------------------------------------------
# INSERT NEW DATA
# ------------------------------------------------------------

def insert_new_data():

    print("\n--- Insert New Data ---")

    review_id = input("Enter review ID: ")
    product_id = input("Enter product ID: ")
    reviewer_id = input("Enter reviewer ID: ")
    stars = input("Enter star rating (1-5): ")
    review_title = input("Enter review title: ")
    review_body = input("Enter review body: ")
    product_category = input("Enter product category: ")

    review = {
        "review_id": review_id,
        "product_id": product_id,
        "reviewer_id": reviewer_id,
        "stars": stars,
        "review_title": review_title,
        "review_body": review_body,
        "language": "en",
        "product_category": product_category
    }

    review_collection.insert_one(review)

    product_collection.update_one(
        {"product_id": product_id},
        {
            "$set": {
                "product_id": product_id,
                "product_category": product_category
            }
        },
        upsert=True
    )

    print("\nNew data successfully inserted into ReviewData and ProductData.")


# ------------------------------------------------------------
# DISPLAY REVIEW BY REVIEW ID
# ------------------------------------------------------------

def display_review():

    print("\n--- Find Review by Review ID ---")

    review_id = input("Enter review ID: ")

    review = review_collection.find_one(
        {"review_id": review_id}
    )

    if review:

        print("\nReview Information")
        print("------------------")

        for key, value in review.items():
            if key != "_id":
                print(f"{key}: {value}")

    else:
        print("Review not found.")


# ------------------------------------------------------------
# DISPLAY DISTINCT PRODUCT CATEGORIES
# ------------------------------------------------------------

def display_categories():

    print("\n--- Distinct Product Categories ---")

    categories = product_collection.distinct(
        "product_category"
    )

    categories = sorted(
        category for category in categories if category
    )

    for category in categories:
        print(category)

    print(f"\nTotal distinct categories: {len(categories)}")


# ------------------------------------------------------------
# COUNT 4 AND 5 STAR REVIEWS
# ------------------------------------------------------------

def positive_review_count():

    print("\n--- 4- and 5-Star Review Count ---")

    category = input("Enter product category: ")

    count = review_collection.count_documents(
        {
            "product_category": {
                "$regex": f"^{category}$",
                "$options": "i"
            },
            "stars": {"$in": ["4", "5", 4, 5]}
        }
    )

    print(
        f"\nNumber of 4- and 5-star reviews "
        f"for '{category}': {count}"
    )


# ------------------------------------------------------------
# COUNT 1 AND 2 STAR REVIEWS
# ------------------------------------------------------------

def negative_review_count():

    print("\n--- 1- and 2-Star Review Count ---")

    category = input("Enter product category: ")

    count = review_collection.count_documents(
        {
            "product_category": {
                "$regex": f"^{category}$",
                "$options": "i"
            },
            "stars": {"$in": ["1", "2", 1, 2]}
        }
    )

    print(
        f"\nNumber of 1- and 2-star reviews "
        f"for '{category}': {count}"
    )


# ------------------------------------------------------------
# SEARCH WORD IN REVIEW TITLE USING $REGEX
# ------------------------------------------------------------

def search_title():

    print("\n--- Search Review Titles ---")

    word = input("Enter a word to search for in review titles: ")

    reviews = review_collection.find(
        {
            "review_title": {
                "$regex": word,
                "$options": "i"
            }
        }
    )

    found = False

    for review in reviews:
        found = True

        print("\n------------------------------")
        print("Review ID:", review.get("review_id"))
        print("Product ID:", review.get("product_id"))
        print("Stars:", review.get("stars"))
        print("Title:", review.get("review_title"))

    if not found:
        print("No reviews found containing that word in the title.")


# ------------------------------------------------------------
# SEARCH WORD IN REVIEW BODY USING $REGEX
# ------------------------------------------------------------

def search_body():

    print("\n--- Search Review Bodies ---")

    word = input("Enter a word to search for in review bodies: ")

    reviews = review_collection.find(
        {
            "review_body": {
                "$regex": word,
                "$options": "i"
            }
        }
    )

    found = False

    for review in reviews:
        found = True

        print("\n------------------------------")
        print("Review ID:", review.get("review_id"))
        print("Product ID:", review.get("product_id"))
        print("Stars:", review.get("stars"))
        print("Title:", review.get("review_title"))
        print("Body:", review.get("review_body"))

    if not found:
        print("No reviews found containing that word in the body.")


# ------------------------------------------------------------
# DELETE A REVIEW
# ------------------------------------------------------------

def delete_review():

    print("\n--- Delete Review ---")

    review_id = input("Enter review ID to delete: ")

    result = review_collection.delete_one(
        {"review_id": review_id}
    )

    if result.deleted_count > 0:
        print("Review successfully deleted.")
    else:
        print("Review not found.")


# ------------------------------------------------------------
# DELETE REVIEWDATA AND PRODUCTDATA
# ------------------------------------------------------------

def delete_collections():

    print("\n--- Delete ReviewData and ProductData ---")

    confirm = input(
        "Are you sure you want to delete both collections? (yes/no): "
    )

    if confirm.lower() == "yes":

        review_collection.drop()
        product_collection.drop()

        print("ReviewData and ProductData successfully deleted.")

    else:
        print("Delete cancelled.")


# ------------------------------------------------------------
# MENU
# ------------------------------------------------------------

def menu():

    while True:

        print("\n==========================================")
        print("     AMAZON ENGLISH REVIEWS DATABASE")
        print("==========================================")
        print("1. Insert new data")
        print("2. Display review by review ID")
        print("3. Display all distinct product categories")
        print("4. Display count of 4- and 5-star reviews")
        print("5. Display count of 1- and 2-star reviews")
        print("6. Search for a word in review titles")
        print("7. Search for a word in review bodies")
        print("8. Delete a review")
        print("9. Delete ReviewData and ProductData")
        print("10. Exit")
        print("==========================================")

        choice = input("Enter your choice: ")

        if choice == "1":
            insert_new_data()

        elif choice == "2":
            display_review()

        elif choice == "3":
            display_categories()

        elif choice == "4":
            positive_review_count()

        elif choice == "5":
            negative_review_count()

        elif choice == "6":
            search_title()

        elif choice == "7":
            search_body()

        elif choice == "8":
            delete_review()

        elif choice == "9":
            delete_collections()

        elif choice == "10":
            print("\nProgram closed.")
            break

        else:
            print("\nInvalid choice. Please enter a number from 1-10.")


# ------------------------------------------------------------
# START PROGRAM
# ------------------------------------------------------------

try:

    client.admin.command("ping")

    print("Successfully connected to MongoDB.")

    create_product_data()

    menu()

except Exception as error:

    print("An error occurred:")
    print(error)

finally:

    client.close()
