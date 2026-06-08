from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional
from wtforms.widgets import DateInput


class OrderForm(FlaskForm):
    customer_name = StringField(
        "Your Name",
        validators=[DataRequired(), Length(max=200)],
        render_kw={"placeholder": "Full name"},
    )
    email = StringField(
        "Email Address",
        validators=[DataRequired(), Email(), Length(max=200)],
        render_kw={"placeholder": "you@example.com"},
    )
    phone = StringField(
        "Phone Number",
        validators=[DataRequired(), Length(max=30)],
        render_kw={"placeholder": "+91 98765 43210"},
    )
    occasion = StringField(
        "Occasion",
        validators=[Optional(), Length(max=200)],
        render_kw={"placeholder": "Birthday, Wedding, Corporate, Diwali…"},
    )
    product_preferences = TextAreaField(
        "What would you like?",
        validators=[Optional(), Length(max=2000)],
        render_kw={"rows": 4, "placeholder": "Tell us which items you're interested in, quantities, flavours…"},
    )
    delivery_date = DateField(
        "Preferred Date",
        validators=[Optional()],
        render_kw={"type": "date"},
    )
    special_requirements = TextAreaField(
        "Special Requirements",
        validators=[Optional(), Length(max=2000)],
        render_kw={"rows": 3, "placeholder": "Allergies, dietary restrictions, inscriptions, packaging preferences…"},
    )
    submit = SubmitField("Send Enquiry")
