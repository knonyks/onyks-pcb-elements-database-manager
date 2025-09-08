from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class ElementForm(FlaskForm):
    part_name = StringField('Part Name', validators=[DataRequired(), Length(min=1, max=100)])
    manufacturer = StringField('Manufacturer', validators=[DataRequired(), Length(min=1, max=100)])
    description = TextAreaField('Description', validators=[Length(max=256)])
    library_ref = StringField('Library Reference', validators=[Length(max=256)])
    library_path = StringField('Library Path', validators=[Length(max=256)])

    footprint_ref_1 = StringField('Footprint Ref 1', validators=[Length(max=256)])
    footprint_path_1 = StringField('Footprint Path 1', validators=[Length(max=256)])
    
    footprint_ref_2 = StringField('Footprint Ref 2', validators=[Length(max=256)])
    footprint_path_2 = StringField('Footprint Path 2', validators=[Length(max=256)])

    footprint_ref_3 = StringField('Footprint Ref 3', validators=[Length(max=256)])
    footprint_path_3 = StringField('Footprint Path 3', validators=[Length(max=256)])


    accept = SubmitField('Accept')