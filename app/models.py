import enum
from datetime import datetime
from slugify import slugify
from app.extensions import db


class CategoryEnum(enum.Enum):
    CAKES = "Cakes"
    TARTS = "Tarts"
    ECLAIRS = "Éclairs"
    MACARONS = "Macarons"
    CROISSANTS = "Croissants"
    BOXES = "Boxes"


class OrderStatus(enum.Enum):
    NEW = "new"
    CONTACTED = "contacted"
    FULFILLED = "fulfilled"


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(220), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False, default="")
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.Enum(CategoryEnum), nullable=False)
    image_filename = db.Column(db.String(300))
    is_available = db.Column(db.Boolean, default=True, nullable=False)
    is_featured = db.Column(db.Boolean, default=False, nullable=False)
    allergens = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def generate_slug(name):
        base = slugify(name)
        slug = base
        counter = 2
        while Product.query.filter_by(slug=slug).first():
            slug = f"{base}-{counter}"
            counter += 1
        return slug

    def __repr__(self):
        return f"<Product {self.name}>"


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    occasion = db.Column(db.String(200))
    product_preferences = db.Column(db.Text)
    delivery_date = db.Column(db.Date)
    special_requirements = db.Column(db.Text)
    status = db.Column(db.Enum(OrderStatus), default=OrderStatus.NEW, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Order #{self.id} {self.customer_name}>"


class Seasonal(db.Model):
    __tablename__ = "seasonals"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    image_filename = db.Column(db.String(300))
    available_from = db.Column(db.Date)
    available_until = db.Column(db.Date)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<Seasonal {self.name}>"
