from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, PasswordField, FileField
from wtforms.validators import DataRequired, Length, Email

def getCreatingElementForm(categories):
    zippedCategories = [str(i) for i in range(1, len(categories) + 1)]
    zippedCategories = zip(zippedCategories, categories)
    zippedCategories = list(zippedCategories)

    class CreatingElementForm(FlaskForm):
        
        part_name = StringField('Part Name')
        manufacturer = StringField('Manufacturer')
        manufacturer_part_name = StringField('Manufacturer Part Name')
        category = SelectField('Category', choices=zippedCategories)
        datasheet = FileField('Datasheet')
        description = TextAreaField('Description')
        generate_description = SubmitField('Generate')
        value = StringField('Value')
        availability = StringField('Availability')

        library_ref = StringField('Library Reference')
        library_path = StringField('Library Path')

        footprint_ref_1 = StringField('Footprint Ref 1')
        footprint_path_1 = StringField('Footprint Path 1')
        
        footprint_ref_2 = StringField('Footprint Ref 2')
        footprint_path_2 = StringField('Footprint Path 2')

        footprint_ref_3 = StringField('Footprint Ref 3')
        footprint_path_3 = StringField('Footprint Path 3')


        accept = SubmitField('Accept')
    
    return CreatingElementForm

def getLoginForm():

    class LoginForm(FlaskForm):
        username = StringField("Login lub e-mail", validators=[DataRequired()])
        password = PasswordField("Hasło", validators=[DataRequired()])
        accept = SubmitField("Zaloguj")
    return LoginForm

def getChangeUserDataForm():

    class ChangeUserData(FlaskForm):
        old_username = StringField("Login lub e-mail", validators=[DataRequired()])
        old_password = PasswordField("Hasło", validators=[DataRequired()])
        new_password = PasswordField("Hasło")
        new_email = StringField("e-mail", validators=[Email()])
        new_username = StringField("Login")
        accept = SubmitField("Zmień")
    return ChangeUserData

def getAddUserForm():

    class ChangeUserData(FlaskForm):
        name = StringField("Name", validators=[DataRequired()])
        family_name = StringField("Family name", validators=[DataRequired()])
        email = StringField("Email", validators=[DataRequired()])
        expired_access_time = SelectField('Wybierz opcję', choices=[('1', '30 dni'), ('2', '90 dni'), ('3', '6 miesięcy'), ('4', '12 miesięcy'), ('5', 'Na zawsze')], validators=[DataRequired()])
        is_admin = SelectField('Wybierz opcję', choices=[('1', 'Nie'), ('2', 'Tak')], validators=[DataRequired()])
        accept = SubmitField("Dodaj")

    return ChangeUserData
