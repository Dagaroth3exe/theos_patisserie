from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, FloatField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Optional, Length, NumberRange
from app.models import CategoryEnum


class ProductForm(FlaskForm):
    name = StringField("Product Name", validators=[DataRequired(), Length(max=200)])
    description = TextAreaField("Description", validators=[Optional(), Length(max=2000)], render_kw={"rows": 4})
    price = FloatField("Price (₹)", validators=[DataRequired(), NumberRange(min=0)])
    category = SelectField(
        "Category",
        choices=[(e.name, e.value) for e in CategoryEnum],
        validators=[DataRequired()],
    )
    allergens = StringField("Allergens", validators=[Optional(), Length(max=500)], render_kw={"placeholder": "e.g. Gluten, Dairy, Nuts"})
    is_available = BooleanField("Available for order", default=True)
    is_featured = BooleanField("Featured (Signature item)")
    image = FileField("Product Image", validators=[Optional(), FileAllowed(["jpg", "jpeg", "png", "webp"], "Images only.")])
    submit = SubmitField("Save Product")
