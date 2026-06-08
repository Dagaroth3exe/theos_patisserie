from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, FloatField, BooleanField, DateField, SubmitField
from wtforms.validators import DataRequired, Optional, Length, NumberRange


class SeasonalForm(FlaskForm):
    name = StringField("Item Name", validators=[DataRequired(), Length(max=200)])
    description = TextAreaField("Description", validators=[Optional(), Length(max=2000)], render_kw={"rows": 4})
    price = FloatField("Price (₹)", validators=[Optional(), NumberRange(min=0)])
    available_from = DateField("Available From", validators=[Optional()], render_kw={"type": "date"})
    available_until = DateField("Available Until", validators=[Optional()], render_kw={"type": "date"})
    is_active = BooleanField("Currently Active", default=True)
    image = FileField("Image", validators=[Optional(), FileAllowed(["jpg", "jpeg", "png", "webp"], "Images only.")])
    submit = SubmitField("Save Special")
