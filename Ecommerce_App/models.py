from django.db import models

# Create your models here.
class Products(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50)
    original_price = models.IntegerField()
    discount_price = models.IntegerField()
    discount_percentage = models.CharField(max_length=10)
    image_url = models.TextField()

    class Meta:
        db_table = 'products'  # Name of the manually created table

    def __str__(self):
        return self.name


# Cart Model
class Cart(models.Model):
    # A Foreign Key is a field in one table that creates a relationship (link) with another table.
    # This ensures that each cart item is tied to a specific user and a specific product.
    # The Foreign Key in the database stores the unique id of the related row in the other table (auth.User and Products).


    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # Links the cart to a specific user, CASCADE means If a user is deleted, all their cart items are also deleted
    product = models.ForeignKey(Products, on_delete=models.CASCADE)  # Links the cart item to the products table (or) This creates a Foreign Key relationship between the Cart model and your custom Products model.
    # on_delete=models.CASCADE means If a product is deleted from the Products table, any associated cart items are also deleted.

    quantity = models.PositiveIntegerField(default=1)  # Quantity of the product in the cart
    added_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the item was added

    def __str__(self):
        return f"{self.product.name} - Quantity: {self.quantity}"

    # Optional helper to calculate the total price of this cart item
    def total_price(self):
        return self.quantity * self.product.discount_price


    # Why does the database create user_id and product_id columns?
    # In the database, Foreign Key relationships are represented using numeric IDs that reference the primary key (id) of the related table.
    # Django appends _id to the field name when creating the actual column in the database.
    # product_id will only store primary key (i.e id) of the corresponding product in the Products table.


class ContactForm(models.Model):
    Full_Name = models.CharField(max_length=255, null=False, blank=False)
    Email_Address = models.EmailField(null=False, blank=False)
    Subject = models.CharField(max_length=100, null=False, blank=False)
    Message = models.TextField(null=False, blank=False)

    def __str__(self):
        return self.Full_Name

