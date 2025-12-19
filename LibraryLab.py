class LibraryItem:
    def __init__(self, item_id, title, item_type, daily_rate):
        self.item_id = item_id
        self.title = title
        self.item_type = item_type
        self.daily_rate = daily_rate

class CheckoutItem:
    def __init__(self, library_item, days):
        self.library_item = library_item 
        self.days = days

    def get_total(self):
        return self.library_item.daily_rate * self.days


# ==================================================
# LOAD LIBRARY CATALOG FROM FILE
# Reads items from catalog.txt
# ==================================================
def load_catalog(filename):
  
    with open(filename, "r") as file:
        for line in file:
            parts = line.strip().split(",")

            # Create a LibraryItem from the file data
            item = LibraryItem(
                int(parts[0]),     # item ID
                parts[1],          # title
                parts[2],          # type
                float(parts[3])    # daily rate
            )

            catalog.append(item)

    return catalog


# ==================================================
# SAVE CHECKOUT ITEMS TO FILE
# ==================================================
def save_checkout(filename, checkout_list):
    with open(filename, "w") as file:
        for item in checkout_list:
            file.write(
                f"{item.library_item.item_id},"
                f"{item.library_item.title},"
                f"{item.days}\n"
            )


# ==================================================
# LOAD CHECKOUT ITEMS FROM FILE
# ==================================================
def load_checkout(filename, catalog):
    checkout = []
    with open(filename, "r") as file:
        for line in file:
            item_id, _, days = line.strip().split(",")

            # Find matching item in catalog
            for lib_item in catalog:
                if lib_item.item_id == int(item_id):
                    checkout.append(
                        CheckoutItem(lib_item, int(days))
                    )

    return checkout


# ==================================================
# MAIN PROGRAM
# ==================================================
def main():
    catalog_file = "catalog.txt"
    checkout_file = "checkout.txt"

    catalog = load_catalog(catalog_file)
    checkout_items = load_checkout(checkout_file, catalog)

    print("=" * 50)
    print("        Welcome to the City Library")
    print("=" * 50)

    while True:
        print("\nMenu:")
        print("1 - View catalog")
        print("2 - Checkout item")
        print("3 - View checkout list")
        print("4 - Finalize checkout")
        print("5 - Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            print("\nAvailable Items:")
            for item in catalog:
                print(
                    f"{item.item_id}) {item.title} "
                    f"({item.item_type}) "
                    f"- ${item.daily_rate:.2f}/day"
                )

        elif choice == "2":
            try:
                item_id = int(input("Enter item ID: "))
                days = int(input("Number of days: "))
            except ValueError:
                print("Enter numbers only.")
                continue

            found = False

            for item in catalog:
                if item.item_id == item_id:
                    checkout_items.append(
                        CheckoutItem(item, days)
                    )
                    print(f"{item.title} checked out for {days} days.")
                    found = True
                    break

            if not found:
                print("Item ID not found.")

        elif choice == "3":
            if not checkout_items:
                print("No items checked out.")
                continue

            print("\nYour Checkout List:")
            total = 0

            for i, item in enumerate(checkout_items, start=1):
                cost = item.get_total()
                total += cost
                print(
                    f"{i}) {item.library_item.title} "
                    f"- {item.days} days = ${cost:.2f}"
                )

            print(f"Current Total: ${total:.2f}")

        elif choice == "4":
            if not checkout_items:
                print("Nothing to checkout.")
                continue

            subtotal = sum(item.get_total() for item in checkout_items)
            discount = 0

            if subtotal >= 10:
                discount = subtotal * 0.10
                print("10% discount applied.")

            total = subtotal - discount

            print("\n---- RECEIPT ----")
            for item in checkout_items:
                print(
                    f"{item.library_item.title} "
                    f"({item.days} days) "
                    f"${item.get_total():.2f}"
                )

            print(f"Subtotal: ${subtotal:.2f}")
            print(f"Discount: -${discount:.2f}")
            print(f"Total Due: ${total:.2f}")
            print("-------------------------")
            print("Thank you for using the library!")

            save_checkout(checkout_file, checkout_items)
            checkout_items.clear()

        elif choice == "5":
            save_checkout(checkout_file, checkout_items)
            print("Goodbye!")
            break

        else:
            print("Please choose a valid option.")


if __name__ == "__main__":
    main()