import products

# from products.factories import CategoryFactory, ProductFactory , OrderItemFactory
# from orders.factories import OrderFactory
# from pharmacy.factories import PharmacyFactory
# import factory
# # Create 100 categories
# categories = CategoryFactory.create_batch(size=100)

# # Create 100 products with random categories
# products = ProductFactory.create_batch(
#     size=100, category=factory.Iterator(categories)
# )

# # Create 50 pharmacies
# pharmacies = PharmacyFactory.create_batch(size=50)

# # Create 100 orders with random pharmacies
# orders = OrderFactory.create_batch(
#     size=100, pharmacy=factory.Iterator(pharmacies)
# )

# # Create 100 order items with random orders and products
# order_items = OrderItemFactory.create_batch(
#     size=100,
#     order=factory.Iterator(orders),
#     product=factory.Iterator(products),
# )

# print(f"Created 100 categories, 100 products, 50 pharmacies, 100 orders, and 100 order items.")
