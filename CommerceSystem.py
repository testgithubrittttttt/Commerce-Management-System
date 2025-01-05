class Product:#this class helps in representing the product in the system. 
    def __init__(self, product_id, name, price, quantity):#this is our constructor which is automiatically called whenever this class is called.
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity

    def __str__(self):#this is the function which converts the product object into a readable string representation.
        return f"ID: {self.product_id}, Name: {self.name}, Price: {self.price}, Quantity: {self.quantity}"


class Customer:#this class represents a customer in the system
    def __init__(self, customer_id, name, contact):
        self.customer_id = customer_id
        self.name = name
        self.contact = contact

    def __str__(self):
        return f"ID: {self.customer_id}, Name: {self.name}, Contact: {self.contact}"


class Order:
    def __init__(self, order_id, customer, products):
        self.order_id = order_id
        self.customer = customer
        self.products = products
        self.total = sum(p.price * p.quantity for p in products)#Here our total cost of the order is calculated as price × quantity for each product.

    def __str__(self):
        products_details = "\n".join(str(p) for p in self.products)
        return f"Order ID: {self.order_id}, Customer: {self.customer.name}, Total: {self.total}\nProducts:\n{products_details}"


class CommerceSystem:#this class handles the overall functionality of the system, including managing products, customers, and orders.
    def __init__(self):
        self.products = {}#A dictionary to store Product objects along with there product_id as the key.
        self.customers = {}#A dictionary to store Customer objects along with there customer_id as the key.
        self.orders = {}#A dictionary to store Order objects along with there order_id as the key.
        self.sales = {}#A dictionary to track the number of units sold for each product.
        
        #This counter keeps track of the next unique (product,customer,order) ID to be assigned when a new (product,customer,order) is added to the system.
        #with the help of .next whenever new thing comes automatically counter increases.
        #I pu this so that guarantee of every product, customer, or order has a unique identifier.
        #this thing also helps in distingushing between the orders.

        self.next_product_id = 1
        self.next_customer_id = 1
        self.next_order_id = 1

    # Product Management
    def add_product(self, name, price, quantity):
        product = Product(self.next_product_id, name, price, quantity)#through this we are calling a construtor of product class which is automatically to be called whenever object of product class is made.
        self.products[self.next_product_id] = product#Tracking of product = dictionary that stores Product objects eg(keys = product_id,value = product itself(which has name,price and quantity))
        self.sales[self.next_product_id] = 0  # Initialize sales tracking = it is also a dictionary for storing key=product_id and value = total number of units to be sold
        self.next_product_id += 1#jab new unique product_id ka product add hogaa this thing will be incrmented
        print(f"Product added: {product}")#at the end we get everything related ti product.

    def update_product(self, product_id, price=None, quantity=None):#This function helps in updating the price and quantity of the existing product
        if product_id in self.products:#here we are identifying whether this prduct_id product exists or not
            if price is not None:
                self.products[product_id].price = price#If price provided, updates the price of the product with the given product_id
            if quantity is not None:
                self.products[product_id].quantity = quantity#If provided, updates the quantity of the product with the given product_id.
            print(f"Product updated: {self.products[product_id]}")
        else:
            print(f"Product ID {product_id} not found.")#if the orduct_id product could not exist than not found

    def delete_product(self, product_id):#This function ensures the product exists if yes than delete it and provides feedback to the user.
        if product_id in self.products:#Ensuring that the product with the given product_id exists in the self.products dictionary
            del self.products[product_id]#delete the product from the self.products dictionary.
            del self.sales[product_id]  # Remove its associated sales data also for ensureing that the system doesn't retain unnecessary sales tracking data for a deleted product.
            print(f"Product ID {product_id} deleted.")
        else:
            print(f"Product ID {product_id} not found.")

    def view_products(self):#this function is responsible for displaying all the products currently stored in the our system. If no products are available, it notifies the user
        if not self.products:#Checking whether the self.products dictionary is empty.
            print("No products available.")
        for product in self.products.values():#here we are iterating over the values of dictionary name self.products. from here we get out put like this 
            print(product)#[Product(1, "Laptop", 1000.0, 50), Product(2, "Phone", 500.0, 100)]

    # Customer Management
    def add_customer(self, name, contact):
        customer = Customer(self.next_customer_id, name, contact)
        self.customers[self.next_customer_id] = customer
        self.next_customer_id += 1
        print(f"Customer added: {customer}")

    def delete_customer(self, customer_id):
        if customer_id in self.customers:
            del self.customers[customer_id]
            print(f"Customer ID {customer_id} deleted.")
        else:
            print(f"Customer ID {customer_id} not found.")

    def view_customers(self):
        if not self.customers:
            print("No customers available.")
        for customer in self.customers.values():
            print(customer)

    # Order Management
    def create_order(self, customer_id, product_ids_quantities):
        if customer_id not in self.customers:
            print("Invalid customer ID.")
            return

        customer = self.customers[customer_id]
        products = []
        for product_id, quantity in product_ids_quantities.items():
            if product_id in self.products and self.products[product_id].quantity >= quantity:
                product = self.products[product_id]
                products.append(Product(product.product_id, product.name, product.price, quantity))
                self.products[product_id].quantity -= quantity
                self.sales[product_id] += quantity  # Update sales data
            else:
                print(f"Product ID {product_id} is unavailable or has insufficient stock.")
                return

        order = Order(self.next_order_id, customer, products)
        self.orders[self.next_order_id] = order
        self.next_order_id += 1
        print(f"Order created: {order}")

    def view_orders(self):
        if not self.orders:
            print("No orders available.")
        for order in self.orders.values():
            print(order)

    def view_orders_by_customer(self, customer_id):
        if customer_id not in self.customers:
            print("Invalid customer ID.")
            return

        print(f"Orders for customer ID {customer_id}:")
        for order in self.orders.values():
            if order.customer.customer_id == customer_id:
                print(order)

    # Reports
    def generate_sales_report(self):
        print("\n--- Sales Report ---")
        total_sales = 0
        for product_id, quantity_sold in self.sales.items():
            product = self.products.get(product_id)
            if product:
                revenue = product.price * quantity_sold
                total_sales += revenue
                print(f"{product.name}: Sold {quantity_sold}, Revenue {revenue}")
        print(f"Total Sales Revenue: {total_sales}")

    def view_inventory(self):
        print("\n--- Inventory Report ---")
        for product in self.products.values():
            print(f"{product.name}: Quantity in stock: {product.quantity}")


# Main Function
def main():
    system = CommerceSystem()
    while True:
        print("\n--- Commerce Management System ---")
        print("1. Add Product")
        print("2. Update Product")
        print("3. Delete Product")
        print("4. View Products")
        print("5. Add Customer")
        print("6. Delete Customer")
        print("7. View Customers")
        print("8. Create Order")
        print("9. View Orders")
        print("10. View Orders by Customer")
        print("11. Generate Sales Report")
        print("12. View Inventory Report")
        print("13. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter product name: ")
            price = float(input("Enter product price: "))
            quantity = int(input("Enter product quantity: "))
            system.add_product(name, price, quantity)
        elif choice == '2':
            product_id = int(input("Enter product ID: "))
            price = float(input("Enter new price (or leave blank): ") or "0") or None
            quantity = int(input("Enter new quantity (or leave blank): ") or "0") or None
            system.update_product(product_id, price, quantity)
        elif choice == '3':
            product_id = int(input("Enter product ID: "))
            system.delete_product(product_id)
        elif choice == '4':
            system.view_products()
        elif choice == '5':
            name = input("Enter customer name: ")
            contact = input("Enter customer contact: ")
            system.add_customer(name, contact)
        elif choice == '6':
            customer_id = int(input("Enter customer ID: "))
            system.delete_customer(customer_id)
        elif choice == '7':
            system.view_customers()
        elif choice == '8':
            customer_id = int(input("Enter customer ID: "))
            n = int(input("Enter number of products: "))
            product_ids_quantities = {}
            for _ in range(n):
                product_id = int(input("Enter product ID: "))
                quantity = int(input("Enter quantity: "))
                product_ids_quantities[product_id] = quantity
            system.create_order(customer_id, product_ids_quantities)
        elif choice == '9':
            system.view_orders()
        elif choice == '10':
            customer_id = int(input("Enter customer ID: "))
            system.view_orders_by_customer(customer_id)
        elif choice == '11':
            system.generate_sales_report()
        elif choice == '12':
            system.view_inventory()
        elif choice == '13':
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
