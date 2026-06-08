import os
import uuid
from flask import (
    render_template, request, redirect, url_for, flash,
    session, current_app
)
from app.admin import admin_bp
from app.admin.decorators import admin_required
from app.extensions import db
from app.models import Product, Order, Seasonal, CategoryEnum, OrderStatus
from app.forms.product_form import ProductForm
from app.forms.seasonal_form import SeasonalForm
from app.forms.auth_form import AdminLoginForm, DeleteForm


# ── Auth ──────────────────────────────────────────────────────────────────────

@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("admin_logged_in"):
        return redirect(url_for("admin.dashboard"))

    form = AdminLoginForm()
    if form.validate_on_submit():
        if (
            form.username.data == current_app.config["ADMIN_USERNAME"]
            and form.password.data == current_app.config["ADMIN_PASSWORD"]
        ):
            session["admin_logged_in"] = True
            session.permanent = True
            return redirect(url_for("admin.dashboard"))
        flash("Invalid credentials.", "error")

    return render_template("admin/login.html", form=form)


@admin_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("admin.login"))


# ── Dashboard ─────────────────────────────────────────────────────────────────

@admin_bp.route("/")
@admin_required
def dashboard():
    new_orders_count = Order.query.filter_by(status=OrderStatus.NEW).count()
    total_products = Product.query.count()
    active_specials = Seasonal.query.filter_by(is_active=True).count()
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    delete_form = DeleteForm()
    return render_template(
        "admin/dashboard.html",
        new_orders_count=new_orders_count,
        total_products=total_products,
        active_specials=active_specials,
        recent_orders=recent_orders,
        delete_form=delete_form,
    )


# ── Orders ────────────────────────────────────────────────────────────────────

@admin_bp.route("/orders")
@admin_required
def orders():
    status_filter = request.args.get("status")
    query = Order.query.order_by(Order.created_at.desc())
    if status_filter and status_filter in [s.value for s in OrderStatus]:
        query = query.filter_by(status=OrderStatus(status_filter))
    all_orders = query.all()
    delete_form = DeleteForm()
    return render_template("admin/orders.html", orders=all_orders, status_filter=status_filter, delete_form=delete_form)


@admin_bp.route("/orders/<int:order_id>/update-status", methods=["POST"])
@admin_required
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get("status")
    if new_status in [s.value for s in OrderStatus]:
        order.status = OrderStatus(new_status)
        db.session.commit()
        flash(f"Order #{order_id} status updated.", "success")
    return redirect(url_for("admin.orders"))


# ── Products ──────────────────────────────────────────────────────────────────

@admin_bp.route("/products")
@admin_required
def products():
    all_products = Product.query.order_by(Product.created_at.desc()).all()
    delete_form = DeleteForm()
    return render_template("admin/products.html", products=all_products, delete_form=delete_form)


@admin_bp.route("/products/new", methods=["GET", "POST"])
@admin_required
def new_product():
    form = ProductForm()
    if form.validate_on_submit():
        image_filename = None
        if form.image.data:
            image_filename = _save_image(form.image.data)

        slug = Product.generate_slug(form.name.data)
        product = Product(
            name=form.name.data,
            slug=slug,
            description=form.description.data or "",
            price=form.price.data,
            category=CategoryEnum[form.category.data],
            allergens=form.allergens.data,
            is_available=form.is_available.data,
            is_featured=form.is_featured.data,
            image_filename=image_filename,
        )
        db.session.add(product)
        db.session.commit()
        flash(f"Product '{product.name}' created.", "success")
        return redirect(url_for("admin.products"))

    return render_template("admin/product_form.html", form=form, title="New Product", product=None)


@admin_bp.route("/products/<int:product_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)

    if request.method == "GET":
        form.category.data = product.category.name

    if form.validate_on_submit():
        if form.image.data and form.image.data.filename:
            if product.image_filename:
                _delete_image(product.image_filename)
            product.image_filename = _save_image(form.image.data)

        if product.name != form.name.data:
            product.slug = Product.generate_slug(form.name.data)

        product.name = form.name.data
        product.description = form.description.data or ""
        product.price = form.price.data
        product.category = CategoryEnum[form.category.data]
        product.allergens = form.allergens.data
        product.is_available = form.is_available.data
        product.is_featured = form.is_featured.data
        db.session.commit()
        flash(f"Product '{product.name}' updated.", "success")
        return redirect(url_for("admin.products"))

    return render_template("admin/product_form.html", form=form, title="Edit Product", product=product)


@admin_bp.route("/products/<int:product_id>/delete", methods=["POST"])
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    if product.image_filename:
        _delete_image(product.image_filename)
    db.session.delete(product)
    db.session.commit()
    flash(f"Product '{product.name}' deleted.", "success")
    return redirect(url_for("admin.products"))


# ── Seasonals ─────────────────────────────────────────────────────────────────

@admin_bp.route("/specials")
@admin_required
def specials():
    all_specials = Seasonal.query.order_by(Seasonal.id.desc()).all()
    delete_form = DeleteForm()
    return render_template("admin/specials.html", specials=all_specials, delete_form=delete_form)


@admin_bp.route("/specials/new", methods=["GET", "POST"])
@admin_required
def new_special():
    form = SeasonalForm()
    if form.validate_on_submit():
        image_filename = _save_image(form.image.data) if form.image.data and form.image.data.filename else None
        special = Seasonal(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            available_from=form.available_from.data,
            available_until=form.available_until.data,
            is_active=form.is_active.data,
            image_filename=image_filename,
        )
        db.session.add(special)
        db.session.commit()
        flash(f"Special '{special.name}' created.", "success")
        return redirect(url_for("admin.specials"))

    return render_template("admin/special_form.html", form=form, title="New Special", special=None)


@admin_bp.route("/specials/<int:special_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_special(special_id):
    special = Seasonal.query.get_or_404(special_id)
    form = SeasonalForm(obj=special)

    if form.validate_on_submit():
        if form.image.data and form.image.data.filename:
            if special.image_filename:
                _delete_image(special.image_filename)
            special.image_filename = _save_image(form.image.data)

        special.name = form.name.data
        special.description = form.description.data
        special.price = form.price.data
        special.available_from = form.available_from.data
        special.available_until = form.available_until.data
        special.is_active = form.is_active.data
        db.session.commit()
        flash(f"Special '{special.name}' updated.", "success")
        return redirect(url_for("admin.specials"))

    return render_template("admin/special_form.html", form=form, title="Edit Special", special=special)


@admin_bp.route("/specials/<int:special_id>/delete", methods=["POST"])
@admin_required
def delete_special(special_id):
    special = Seasonal.query.get_or_404(special_id)
    if special.image_filename:
        _delete_image(special.image_filename)
    db.session.delete(special)
    db.session.commit()
    flash(f"Special '{special.name}' deleted.", "success")
    return redirect(url_for("admin.specials"))


# ── Helpers ───────────────────────────────────────────────────────────────────

def _save_image(file_storage):
    ext = file_storage.filename.rsplit(".", 1)[-1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    file_storage.save(path)
    return filename


def _delete_image(filename):
    path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    try:
        os.remove(path)
    except OSError:
        pass
