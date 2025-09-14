from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length, Email

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
