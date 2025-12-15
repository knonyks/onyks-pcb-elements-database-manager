from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, PasswordField, FileField, BooleanField
from wtforms.validators import DataRequired, Length, Email, Optional
from flask_wtf.file import FileField, FileRequired, FileAllowed

def get_creating_element_form(categories):
    zippedCategories = zip(categories, categories)
    zippedCategories = list(zippedCategories)

    class CreatingElementForm(FlaskForm):
        
        part_name = StringField('Part Name', validators=[DataRequired(), Length(max=256)])
        manufacturer = StringField('Manufacturer', validators=[Length(max=256)])
        manufacturer_part_name = StringField('Manufacturer Part Name', validators=[Length(max=256)])
        category = SelectField('Category', choices=zippedCategories)
        datasheet = FileField('Datasheet', validators=[FileAllowed(['pdf'], "Tylko pliki PDF są dozwolone!")])
        description = TextAreaField('Description', validators=[Length(max=256)])
        generate_description = SubmitField('Generate')
        value = StringField('Value', validators=[Length(max=256)])
        availability = StringField('Availability', validators=[Length(max=256)])

        library_ref = StringField('Library Reference')
        library_path = StringField('Library Path')

        datasheet_must_be_deleted = BooleanField('Do not change and delete the current datasheet', default=False)
        datasheet_the_same = BooleanField('The same datasheet like the original?', default=False)

        footprint_ref_1 = StringField('Footprint Reference No. 1')
        footprint_path_1 = StringField('Footprint Path No. 1')
        
        footprint_ref_2 = StringField('Footprint Reference No. 2')
        footprint_path_2 = StringField('Footprint Path No. 2')

        footprint_ref_3 = StringField('Footprint Reference No. 3')
        footprint_path_3 = StringField('Footprint Path No. 3')

        accept = SubmitField('Accept')
    
    return CreatingElementForm

def get_login_form():

    class LoginForm(FlaskForm):
        username = StringField("Login lub e-mail", validators=[DataRequired()])
        password = PasswordField("Hasło", validators=[DataRequired()])
        accept = SubmitField("Zaloguj")
    return LoginForm

def get_change_user_data_form():

    class ChangeUserData(FlaskForm):
        new_password = PasswordField("Hasło")
        new_email = StringField("e-mail", validators=[Email(), Optional()])
        new_username = StringField("Login")
        old_password = PasswordField("Hasło", validators=[DataRequired()])
        accept = SubmitField("Zmień")
    return ChangeUserData

def get_add_user_form():

    class AddUserForm(FlaskForm):
        name = StringField("Name", validators=[DataRequired()])
        family_name = StringField("Family name", validators=[DataRequired()])
        email = StringField("Email", validators=[DataRequired()])
        expired_access_time = SelectField('Wybierz opcję', choices=[('1', '30 dni'), ('2', '90 dni'), ('3', '6 miesięcy'), ('4', '12 miesięcy'), ('5', 'Na zawsze')], validators=[DataRequired()])
        is_admin = SelectField('Wybierz opcję', choices=[('1', 'Nie'), ('2', 'Tak')], validators=[DataRequired()])
        accept = SubmitField("Dodaj")
        users_file = FileField('Plik uzytkowników', validators=[FileAllowed(['pdf'], "Tylko pliki CSV są dozwolone!")])
        users_file_submit = SubmitField("Dodaj przez plik CSV")

    return AddUserForm
