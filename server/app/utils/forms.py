from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length

def getCreatingElementForm(categories):
    zippedCategories = [str(i) for i in range(1, len(categories) + 1)]
    zippedCategories = zip(zippedCategories, categories)
    zippedCategories = list(zippedCategories)

    class CreatingElementForm(FlaskForm):
        
        category = SelectField('Wybierz opcję', choices=zippedCategories, validators=[DataRequired()])
        # ('1', 'Opcja 1'), ('2', 'Opcja 2'), ('3', 'Opcja 3')

        part_name = StringField('Part Name', validators=[DataRequired(), Length(min=1, max=100)])
        
        manufacturer = StringField('Manufacturer', validators=[Length(min=1, max=100)])
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
    
    return CreatingElementForm