import os
from flask import render_template, request, redirect, url_for, flash, current_app, jsonify
from flask_mail import Message
from app.public import public_bp
from app.extensions import db, mail, csrf
from app.models import Product, Order, Seasonal, CategoryEnum
from app.forms.order_form import OrderForm


@public_bp.route("/")
def index():
    featured = Product.query.filter_by(is_featured=True, is_available=True).limit(3).all()
    seasonals = Seasonal.query.filter_by(is_active=True).limit(2).all()
    categories = [e.value for e in CategoryEnum]

    videos_dir = os.path.join(current_app.static_folder, 'videos')
    reel_videos = sorted([
        f for f in os.listdir(videos_dir)
        if f.lower().endswith(('.mp4', '.mov', '.webm'))
    ]) if os.path.isdir(videos_dir) else []

    return render_template("public/index.html",
                           featured=featured, seasonals=seasonals,
                           categories=categories, reel_videos=reel_videos)


@public_bp.route("/products")
def products():
    _patisserie = [
        CategoryEnum.CAKES, CategoryEnum.TARTS, CategoryEnum.ECLAIRS,
        CategoryEnum.MACARONS, CategoryEnum.CROISSANTS, CategoryEnum.BOXES,
    ]
    _restaurant = [
        CategoryEnum.SOUPS, CategoryEnum.SALADS, CategoryEnum.STARTERS,
        CategoryEnum.FRENCH_TOAST, CategoryEnum.PANCAKES,
        CategoryEnum.WAFFLES, CategoryEnum.BREAKFAST, CategoryEnum.OMELETTES,
        CategoryEnum.EXTRAS,
    ]
    _restaurant_order = {cat: i for i, cat in enumerate(_restaurant)}

    patisserie_products = (
        Product.query
        .filter(Product.is_available == True, Product.category.in_(_patisserie))
        .order_by(Product.category, Product.created_at.asc())
        .all()
    )
    restaurant_products = sorted(
        Product.query
        .filter(Product.is_available == True, Product.category.in_(_restaurant))
        .all(),
        key=lambda p: (_restaurant_order.get(p.category, 99), p.created_at or 0)
    )
    patisserie_cats = [e.value for e in _patisserie]
    restaurant_cats = [e.value for e in _restaurant]
    return render_template(
        "public/products.html",
        patisserie_products=patisserie_products,
        restaurant_products=restaurant_products,
        patisserie_cats=patisserie_cats,
        restaurant_cats=restaurant_cats,
    )


@public_bp.route("/products/<slug>")
def product_detail(slug):
    product = Product.query.filter_by(slug=slug).first_or_404()
    related = (
        Product.query
        .filter_by(category=product.category, is_available=True)
        .filter(Product.id != product.id)
        .limit(3).all()
    )
    return render_template("public/product_detail.html", product=product, related=related)


@public_bp.route("/specials")
def specials():
    active_specials = Seasonal.query.filter_by(is_active=True).all()
    return render_template("public/specials.html", specials=active_specials)


@public_bp.route("/our-story")
def our_story():
    return render_template("public/our_story.html")


@public_bp.route("/order", methods=["GET", "POST"])
def order():
    form = OrderForm()
    prefill_product = None

    if request.method == "GET":
        product_slug = request.args.get("product")
        if product_slug:
            prefill_product = Product.query.filter_by(slug=product_slug).first()
            if prefill_product:
                form.product_preferences.data = prefill_product.name

    if form.validate_on_submit():
        new_order = Order(
            customer_name=form.customer_name.data,
            email=form.email.data,
            phone=form.phone.data,
            occasion=form.occasion.data,
            product_preferences=form.product_preferences.data,
            delivery_date=form.delivery_date.data,
            special_requirements=form.special_requirements.data,
        )
        db.session.add(new_order)
        db.session.commit()

        _send_order_emails(new_order)

        flash("Your enquiry has been sent! We'll be in touch within 24 hours.", "success")
        return redirect(url_for("public.order_thank_you"))

    return render_template("public/order.html", form=form, prefill_product=prefill_product)


@public_bp.route("/order/thank-you")
def order_thank_you():
    return render_template("public/order_thank_you.html")


@public_bp.route("/contact")
def contact():
    return render_template("public/contact.html")


@public_bp.route("/api/chat", methods=["POST"])
@csrf.exempt
def chat_api():
    data = request.get_json(silent=True) or {}
    user_message = str(data.get("message", "")).strip()[:500]
    history = data.get("history", [])[-8:]  # last 4 turns max

    if not user_message:
        return jsonify({"error": "empty message"}), 400

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key or api_key.startswith("sk-ant-..."):
        return jsonify({"reply": "The AI assistant is not configured yet. Please contact the restaurant directly."}), 200

    # Build live menu context from DB
    products = Product.query.filter_by(is_available=True).order_by(Product.category).all()
    menu_lines = []
    current_cat = None
    for p in products:
        cat = p.category.value
        if cat != current_cat:
            menu_lines.append(f"\n{cat.upper()}:")
            current_cat = cat
        veg = "veg" if p.is_veg else "non-veg"
        menu_lines.append(f"  • {p.name} — ₹{p.price:.0f}" + (f" ({veg})" if p.is_veg is not None else ""))

    system_prompt = f"""You are the AI assistant for Theo's Patisserie & Chocolatier, a luxury French-style café and restaurant in Noida, India (also in Delhi NCR). You're knowledgeable, warm, and concise.

About Theo's:
- Upscale French patisserie and full-service restaurant
- Signature items: macarons, éclairs, entremets, croissants, custom cakes
- Restaurant serves: soups, salads, starters, breakfast, brunch, and more
- Instagram: @theosfoodindia (26K followers)
- For reservations or large orders, customers can use the "Place an Enquiry" form on the website

Current Menu:
{"".join(menu_lines)}

Answer questions about the menu, ingredients, dietary options (veg/non-veg/gluten-free), pricing, occasions, pairings, and general restaurant info. Keep replies under 3 sentences unless listing items. If you don't know something specific (like today's hours), say so politely and suggest contacting the restaurant."""

    try:
        import anthropic as _anthropic
        client = _anthropic.Anthropic(api_key=api_key)
        messages = []
        for turn in history:
            role = turn.get("role")
            content = str(turn.get("content", ""))[:300]
            if role in ("user", "assistant") and content:
                messages.append({"role": role, "content": content})
        messages.append({"role": "user", "content": user_message})

        resp = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=350,
            system=system_prompt,
            messages=messages,
        )
        reply = resp.content[0].text
    except Exception as e:
        current_app.logger.error(f"Chat API error: {e}")
        reply = "I'm having a moment — please try again or contact us directly."

    return jsonify({"reply": reply})


def _send_order_emails(order):
    try:
        bakery_msg = Message(
            subject=f"New Enquiry #{order.id} — {order.customer_name}",
            recipients=[current_app.config["BAKERY_EMAIL"]],
            html=render_template("emails/order_notification.html", order=order),
        )
        mail.send(bakery_msg)

        customer_msg = Message(
            subject="We've received your enquiry — Theos Patisserie",
            recipients=[order.email],
            html=render_template("emails/order_confirmation.html", order=order),
        )
        mail.send(customer_msg)
    except Exception as e:
        current_app.logger.error(f"Failed to send order emails: {e}")
