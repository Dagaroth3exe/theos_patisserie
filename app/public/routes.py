from flask import render_template, request, redirect, url_for, flash, current_app
from flask_mail import Message
from app.public import public_bp
from app.extensions import db, mail
from app.models import Product, Order, Seasonal, CategoryEnum
from app.forms.order_form import OrderForm


@public_bp.route("/")
def index():
    featured = Product.query.filter_by(is_featured=True, is_available=True).limit(3).all()
    seasonals = Seasonal.query.filter_by(is_active=True).limit(2).all()
    categories = [e.value for e in CategoryEnum]
    return render_template("public/index.html", featured=featured, seasonals=seasonals, categories=categories)


@public_bp.route("/products")
def products():
    all_products = Product.query.filter_by(is_available=True).order_by(Product.created_at.desc()).all()
    categories = [e.value for e in CategoryEnum]
    return render_template("public/products.html", products=all_products, categories=categories)


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


def _send_order_emails(order):
    try:
        bakery_msg = Message(
            subject=f"New Enquiry #{order.id} — {order.customer_name}",
            recipients=[current_app.config["BAKERY_EMAIL"]],
            html=render_template("emails/order_notification.html", order=order),
        )
        mail.send(bakery_msg)

        customer_msg = Message(
            subject="We've received your enquiry — Theo's Patisserie",
            recipients=[order.email],
            html=render_template("emails/order_confirmation.html", order=order),
        )
        mail.send(customer_msg)
    except Exception as e:
        current_app.logger.error(f"Failed to send order emails: {e}")
