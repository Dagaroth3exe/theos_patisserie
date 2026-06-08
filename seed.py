"""
Run once to populate the database with Theo's Patisserie menu items.
Usage: python seed.py
"""
import os
from app import create_app
from app.extensions import db
from app.models import Product, Seasonal, CategoryEnum


PRODUCTS = [
    {
        "name": "Rose & Raspberry Macaron",
        "description": "Delicate almond shells filled with a fragrant rose and tangy raspberry ganache. A crowd favourite made fresh daily.",
        "price": 125.0,
        "category": CategoryEnum.MACARONS,
        "is_featured": False,
        "allergens": "Almonds, Eggs, Dairy",
    },
    {
        "name": "Passion Fruit Milk Chocolate Macaron",
        "description": "Tropical passion fruit curd nestled in a silky milk chocolate ganache, sandwiched between two perfect almond shells.",
        "price": 125.0,
        "category": CategoryEnum.MACARONS,
        "is_featured": False,
        "allergens": "Almonds, Eggs, Dairy",
    },
    {
        "name": "Pistachio Macaron",
        "description": "House-made pistachio praline ganache in a vibrant green shell. One of our most requested items.",
        "price": 125.0,
        "category": CategoryEnum.MACARONS,
        "is_featured": True,
        "allergens": "Almonds, Pistachios, Eggs, Dairy",
    },
    {
        "name": "Double Chocolate Éclair",
        "description": "Classic choux pastry filled with rich dark chocolate crème pâtissière, glazed with a mirror-finish chocolate ganache.",
        "price": 380.0,
        "category": CategoryEnum.ECLAIRS,
        "is_featured": True,
        "allergens": "Gluten, Eggs, Dairy",
    },
    {
        "name": "Blueberry Cheesecake Slice",
        "description": "New York-style baked cheesecake on a buttery biscuit base, topped with a fresh blueberry compote.",
        "price": 450.0,
        "category": CategoryEnum.CAKES,
        "is_featured": False,
        "allergens": "Gluten, Eggs, Dairy",
    },
    {
        "name": "New York Baked Cheesecake",
        "description": "The classic. Dense, velvety, perfectly golden-topped baked cheesecake. No fruit, no fuss — pure indulgence.",
        "price": 480.0,
        "category": CategoryEnum.CAKES,
        "is_featured": True,
        "allergens": "Gluten, Eggs, Dairy",
    },
    {
        "name": "Red Velvet Cheesecake",
        "description": "A dramatic swirl of crimson red velvet and cream cheese cheesecake batter, baked to silky perfection.",
        "price": 460.0,
        "category": CategoryEnum.CAKES,
        "is_featured": False,
        "allergens": "Gluten, Eggs, Dairy",
    },
    {
        "name": "Smoked Chicken Croissant",
        "description": "Buttery, laminated all-butter croissant filled with house-smoked chicken, a touch of Dijon mustard, and gruyère.",
        "price": 320.0,
        "category": CategoryEnum.CROISSANTS,
        "is_featured": False,
        "allergens": "Gluten, Dairy, Eggs",
    },
    {
        "name": "Tiramisu",
        "description": "Espresso-soaked ladyfingers layered with Mascarpone cream and dusted with premium Valrhona cocoa powder.",
        "price": 420.0,
        "category": CategoryEnum.CAKES,
        "is_featured": False,
        "allergens": "Gluten, Eggs, Dairy",
    },
    {
        "name": "Oreo Brownie",
        "description": "Fudgy dark chocolate brownie studded with Oreo cookie crumble, baked until crackle-topped and gooey inside.",
        "price": 280.0,
        "category": CategoryEnum.CAKES,
        "is_featured": False,
        "allergens": "Gluten, Eggs, Dairy",
    },
    {
        "name": "Mushroom Vol-au-Vent",
        "description": "Puff pastry shell filled with a creamy sauté of wild mushrooms, thyme, and a touch of cream.",
        "price": 350.0,
        "category": CategoryEnum.TARTS,
        "is_featured": False,
        "allergens": "Gluten, Dairy",
    },
    {
        "name": "Festive Chocolate Box",
        "description": "A curated selection of hand-crafted chocolates, bonbons, and pralines. Includes 24 pieces. Perfect for gifting.",
        "price": 1800.0,
        "category": CategoryEnum.BOXES,
        "is_featured": False,
        "allergens": "Dairy, Nuts (varies by selection)",
    },
]

SEASONAL = [
    {
        "name": "Diwali Mithai Box",
        "description": "A festive assortment of hand-painted milk chocolate bonbons, rose macarons, and Indian-spiced truffles. Limited edition for Diwali.",
        "price": 2200.0,
        "is_active": True,
    },
]


def seed():
    app = create_app("development")
    with app.app_context():
        db.create_all()

        seeded = 0
        for data in PRODUCTS:
            slug = Product.generate_slug(data["name"])
            if Product.query.filter_by(slug=slug).first():
                print(f"  skip  {data['name']} (already exists)")
                continue
            product = Product(
                name=data["name"],
                slug=slug,
                description=data["description"],
                price=data["price"],
                category=data["category"],
                is_featured=data["is_featured"],
                is_available=True,
                allergens=data.get("allergens"),
            )
            db.session.add(product)
            seeded += 1
            print(f"  add   {data['name']}")

        for data in SEASONAL:
            if Seasonal.query.filter_by(name=data["name"]).first():
                print(f"  skip  {data['name']} (already exists)")
                continue
            special = Seasonal(
                name=data["name"],
                description=data["description"],
                price=data["price"],
                is_active=data["is_active"],
            )
            db.session.add(special)
            seeded += 1
            print(f"  add   {data['name']}")

        db.session.commit()
        print(f"\nSeeded {seeded} items successfully.")


if __name__ == "__main__":
    seed()
