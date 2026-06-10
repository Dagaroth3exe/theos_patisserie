"""Seed all restaurant menu items. Run once: python seed_menu.py"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
from app.extensions import db
from app.models import Product, CategoryEnum
from sqlalchemy import text

app = create_app()

# ── Menu data ────────────────────────────────────────────────────
C = CategoryEnum
MENU = [
    # ── Soups – Vegetarian ──────────────────────────────────────
    (C.SOUPS, True,  "Malaysian Bowl of Laksa",              495, "Spicy oriental vegetable broth with yellow noodles and rice noodles, coconut milk and lemon."),
    (C.SOUPS, True,  "Spinach & Porcini Mushroom Soup",      450, "Bright green spinach soup with Porcini mushrooms and herbs."),
    (C.SOUPS, True,  "Classic Minestrone Soup",              425, "Thick tomato & vegetable broth with Italian herbs, olive oil & parmesan."),
    (C.SOUPS, True,  "Mushroom Cappuccino",                  425, "Thick mushroom cream soup with oregano, cream foam and porcini dust."),
    (C.SOUPS, True,  "Broccoli & Almond Soup",               425, "Fresh broccoli & almond milk puree finished with cream and herbs."),
    (C.SOUPS, True,  "Tomato Basil Soup",                    380, "Rich and smooth fresh tomato soup with sweet basil and parmesan."),
    # ── Soups – Non-Vegetarian ──────────────────────────────────
    (C.SOUPS, False, "Malaysian Bowl of Laksa – Chicken",    475, "Spicy chicken broth with yellow egg noodles and rice noodles, coconut milk and lemon."),
    (C.SOUPS, False, "Malaysian Bowl of Laksa – Prawns & Chicken", 550, "Spicy chicken and prawn broth with yellow egg noodles and rice noodles."),
    (C.SOUPS, False, "Minestrone Soup – Chicken",            395, "Thick tomato, vegetable & chicken broth with Italian herbs, olive oil, parmesan & shredded chicken."),
    (C.SOUPS, False, "Minestrone Soup – Prawns",             450, "Thick tomato, vegetable & chicken broth with mild shredded prawn."),
    (C.SOUPS, False, "Cream of Chicken & Basil Soup",        425, "Flavorful chicken cream soup with Italian herbs, served hot with mild shredded chicken."),
    (C.SOUPS, False, "French Onion Soup",                    475, "Caramelized onion, chicken stock, wine & thyme topped with gratinated cheese."),
    # ── Salads – Vegetarian ─────────────────────────────────────
    (C.SALADS, True,  "Insalata Di Caprese",                 495, "Fresh Tomato, Bocconcini, Italian basil, Sundried Tomatoes, Black Olives, pesto oil & Balsamic."),
    (C.SALADS, True,  "Caesar Salad",                        495, "Mixed lettuce with garlic croutons in classic red wine Caesar dressing with parmesan."),
    (C.SALADS, True,  "Italian Tossed Salad",                495, "Cauliflower, Broccoli, French Beans, Bell Peppers, Yellow Corn, Baby corn, Cherry tomatoes in herb vinaigrette."),
    (C.SALADS, True,  "Fattoush",                            495, "Lebanese tossed salad with Lettuce, peppers, cucumber, tomato, olives in lemon dressing with Feta & crispy Pita."),
    (C.SALADS, True,  "Tabbouleh",                           495, "Lebanese Herb & Bulgur Salad in lemon dressing with Pita Bread, Hummus & Tahini."),
    (C.SALADS, True,  "Avocado Corn Salad",                  595, "Avocado, English cucumber, Pink Onions, Fresh Corn, Bell Peppers, Tomatoes in lemon cilantro dressing on lettuce."),
    # ── Salads – Non-Vegetarian ─────────────────────────────────
    (C.SALADS, False, "Warm Chicken Salad",                  575, "Grilled marinated chicken on Rocket leaves, tomatoes, broccoli, olives, beans and sliced onion."),
    (C.SALADS, False, "Chicken Caesar Salad",                575, "Mixed lettuce with grilled chicken, garlic croutons in Red wine & Caesar dressing."),
    (C.SALADS, False, "Chicken Caesar Salad with Crispy Bacon", 595, "Mixed lettuce with grilled chicken, garlic croutons, Red wine Caesar dressing and crispy bacon."),
    (C.SALADS, False, "Grilled Chicken And Leek Salad",      525, "Sliced grilled chicken with Cauliflower, Broccoli, French Beans, Leeks in a garlic Lemon dressing."),
    (C.SALADS, False, "Smoked Chicken Salad",                575, "Smoked Chicken on Lettuce, rocket leaves, fresh tomato, onion & olives in balsamic dressing."),
    # ── Starters – Vegetarian ───────────────────────────────────
    (C.STARTERS, True,  "Nachos Overload",                   480, "Cheesy Nachos with Avocado Guacamole, Fresh Tomato Salsa & Sour Cream."),
    (C.STARTERS, True,  "Hummus & Grilled Pita",             395, "Thick Pita Bread with inhouse Hummus, cucumber salad & pickle."),
    (C.STARTERS, True,  "Potato Wedges",                     350, "Herb & Tabasco Potato Wedges gratinated with cheese, Aioli, Mustard & spicy ketchup dip."),
    (C.STARTERS, True,  "French Fries",                      350, "Hot & Crispy fries with paprika, inhouse garlic mayo salad & condiments."),
    (C.STARTERS, True,  "Jalapeño & Sundried Tomato Arancini", 480, "Fried Italian risotto balls with Parmesan, Sundried Tomato, Mozzarella & Jalapeños."),
    (C.STARTERS, True,  "Mozzarella Caroza",                 480, "Deep fried Italian bread cutlets with hot molten mozzarella stuffing."),
    (C.STARTERS, True,  "Bruschetta – Tomato, Basil & Mozzarella", 395, "Toasted Garlic French baguette with Tomato, Basil & Mozzarella topping."),
    (C.STARTERS, True,  "Bruschetta – Mushroom",             395, "Toasted Garlic French baguette with Mushroom topping."),
    (C.STARTERS, True,  "Bruschetta – Exotic Vegetable & Olive Tapenade", 395, "Toasted Garlic French baguette with Exotic Vegetable & Olive Tapenade."),
    (C.STARTERS, True,  "Bruschetta – Avocado, Cilantro, Tomato & Onion", 475, "Cold bruschetta with Avocado, Cilantro, Tomato & Onion."),
    (C.STARTERS, True,  "Bruschetta – Assorted",             450, "Assorted toppings on Toasted Garlic French baguette."),
    (C.STARTERS, True,  "Wine & Mushroom Cheese Vol Au Vents", 450, "Crispy Puff shells stuffed with garlic mushrooms in creamy béchamel sauce."),
    (C.STARTERS, True,  "Cheesy Quesadillas",                595, "Toasted Mexican flat tortillas with yellow cheddar, Mozzarella, veggies, Mexican chilies, Salsa, Sour cream & Guacamole."),
    (C.STARTERS, True,  "Bean Tacos",                        595, "Soft white / Crispy Corn Tortilla (3 pieces) stuffed with Mexican rice and saucy bean filling."),
    (C.STARTERS, True,  "Falafel",                           595, "Lebanese Chickpea and herb cutlet with traditional hummus, tahini and freshly baked Pita Pockets."),
    # ── Starters – Non-Vegetarian ───────────────────────────────
    (C.STARTERS, False, "Fish N Chip – Basa Fish",           695, "Fish & Chips with Tartare sauce."),
    (C.STARTERS, False, "Fish N Chip – Sole Fish",           950, "Fish & Chips with Tartare sauce."),
    (C.STARTERS, False, "Chicken Strips",                    550, "Spicy Chicken strips with Hot wing sauce."),
    (C.STARTERS, False, "Chicken Wings",                     550, "Barbecue chicken wings with Jack Daniel sauce."),
    (C.STARTERS, False, "Prawn Aglio Olio Pepperonchino",    750, "Fresh prawns in chilli garlic & herby extra virgin olive oil, balsamic, white wine cherry tomatoes & shallots."),
    (C.STARTERS, False, "Zatar Chicken",                     675, "Boneless chicken thigh morsels in Zatar garlic marinade, served on Hummus with freshly baked Pita."),
    (C.STARTERS, False, "Bruschetta – Smoked Chicken",       450, "Toasted Garlic French baguette with Smoked Chicken topping."),
    (C.STARTERS, False, "Bruschetta – Grilled Chicken",      425, "Toasted Garlic French baguette with Grilled Chicken topping."),
    (C.STARTERS, False, "Wine & Chicken Cheese Vol Au Vents", 495, "Crispy Puff shells stuffed with shredded chicken in creamy bechamel sauce."),
    (C.STARTERS, False, "Chicken Satay",                     595, "Tender chicken supreme marinated in Thai spices, grilled and served with peanut sauce."),
    (C.STARTERS, False, "Hot Thai Crispy Chicken",           595, "Crispy fried boneless chicken thigh in spicy sweet Thai chilly sauce with greens and fish sauce."),
    (C.STARTERS, False, "Chicken Quesadillas",               595, "Toasted Mexican tortillas with yellow cheddar, Mozzarella, chicken, chilies, Salsa, Sour cream & Guacamole."),
    (C.STARTERS, False, "Chicken & Bean Tacos",              595, "Soft white / Crispy Corn Tortilla (3 pieces) stuffed with Mexican rice, saucy bean filling and Crispy chicken."),
    # ── Extras ──────────────────────────────────────────────────
    (C.EXTRAS, True,  "Lebanese Dips",                       150, "Hummus, Tzatski, Babaganoush, Tahini, Muhamara."),
    (C.EXTRAS, True,  "Mexican Dips",                        120, ""),
    # ── French Toast ────────────────────────────────────────────
    (C.FRENCH_TOAST, True, "Classic French Toast",           450, "With maple syrup & butter."),
    (C.FRENCH_TOAST, True, "Seasonal Fruit & Cream French Toast", 550, ""),
    (C.FRENCH_TOAST, True, "Blueberry & Cream French Toast", 550, ""),
    (C.FRENCH_TOAST, True, "Hazelnut Nutella & Cream French Toast", 550, ""),
    (C.FRENCH_TOAST, True, "Banana Caramel & Cream French Toast", 550, ""),
    # ── Pancakes ────────────────────────────────────────────────
    (C.PANCAKES, True, "Classic Buttermilk Pancake",         450, "Served with classic maple syrup & melted butter."),
    (C.PANCAKES, True, "Seasonal Fruit & Cream Pancake",     550, ""),
    (C.PANCAKES, True, "Sticky Toffee Pancake",              550, ""),
    (C.PANCAKES, True, "Blueberry Pancake",                  550, ""),
    (C.PANCAKES, True, "Dark Chocolate Pancake",             550, ""),
    (C.PANCAKES, True, "Banana Toffee Pancake",              550, ""),
    # ── Waffles ─────────────────────────────────────────────────
    (C.WAFFLES, True, "Classic Belgian Waffle",              450, "With maple syrup & butter."),
    (C.WAFFLES, True, "Seasonal Fruit & Cream Waffle",       550, ""),
    (C.WAFFLES, True, "Blueberry & Cream Waffle",            550, ""),
    (C.WAFFLES, True, "Hazelnut Nutella & Cream Waffle",     550, ""),
    (C.WAFFLES, True, "Banana Caramel & Cream Waffle",       550, ""),
    # ── Breakfast ───────────────────────────────────────────────
    (C.BREAKFAST, False, "Choice of 2 Eggs to Order",        380, "Sunny Side Up / Over Easy / Scrambled / Plain Omelette. Served with Toast, Grilled Tomato, Saute Vegetables, Potato Fries & Baked Beans."),
    (C.BREAKFAST, False, "Choice of 3 Eggs to Order",        425, "Sunny Side Up / Over Easy / Scrambled / Plain Omelette. Served with Toast, Grilled Tomato, Saute Vegetables, Potato Fries & Baked Beans."),
    (C.BREAKFAST, False, "Add-On: Grilled Bacon, Sausages or Smoked Ham", 250, ""),
    # ── Omelettes ───────────────────────────────────────────────
    (C.OMELETTES, False, "Eggs Kejriwal",                    480, "Toasted brioche with creamy mushroom duxelle, green chilli, fried egg & cheese gratinated. Served with potato fries."),
    (C.OMELETTES, False, "Masala Omelette",                  480, "4 Egg Omelette with Onion, Tomato, Green Chilli, Coriander and Indian Spices."),
    (C.OMELETTES, False, "Cheese Omelette",                  480, "4 Egg Cheese Omelette."),
    (C.OMELETTES, False, "Farm Fresh Veg Omelette",          480, "4 Egg Vegetable Omelette with Broccoli, Mushroom, Spinach & Tomato."),
    (C.OMELETTES, False, "Grilled Chicken Omelette",         480, "4 Egg Omelette with Grilled Chicken, Spinach & Tomatoes."),
    (C.OMELETTES, False, "Smoked Chicken Omelette",          480, "4 Egg Omelette with Smoked Chicken, Spinach & Tomatoes."),
    (C.OMELETTES, False, "French Omelette",                  480, "4 Egg Plain rolled Omelette with soft & creamy centre."),
    (C.OMELETTES, False, "Egg White Omelette",               480, "6 Egg White Plain Omelette."),
    (C.OMELETTES, False, "Egg White Cheese Omelette",        480, "6 Egg White Cheese Omelette."),
]

with app.app_context():
    # ── Add is_veg column if missing ────────────────────────────
    with db.engine.connect() as conn:
        cols = [r[1] for r in conn.execute(text("PRAGMA table_info(products)")).fetchall()]
        if 'is_veg' not in cols:
            conn.execute(text("ALTER TABLE products ADD COLUMN is_veg BOOLEAN DEFAULT 1"))
            conn.commit()
            print("Added is_veg column.")

    added = skipped = 0
    for cat, veg, name, price, desc in MENU:
        slug = Product.generate_slug(name)
        # skip if exact name already exists
        if Product.query.filter_by(name=name).first():
            skipped += 1
            continue
        p = Product(
            name=name,
            slug=slug,
            description=desc,
            price=float(price),
            category=cat,
            is_veg=veg,
            is_available=True,
            is_featured=False,
        )
        db.session.add(p)
        added += 1
    db.session.commit()
    print(f"Done — added {added}, skipped {skipped} existing.")
