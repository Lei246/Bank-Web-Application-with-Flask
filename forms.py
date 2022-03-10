from flask_wtf import FlaskForm
from wtforms import Form, StringField, validators
from wtforms.fields import IntegerField, SelectField, BooleanField

class PersonEditForm(FlaskForm):
    name = StringField("name",[validators.Length(min=3, max=80, message="Skriv in mellan 2 och 80 tecken")])
    city = StringField("city",[validators.Length(min=5, max=30)])
    postalcode = IntegerField("postalcode",[validators.NumberRange(10000,99999)])
    pwd = StringField("pwd",[validators.Length(min=5, max=30), validators.EqualTo('pwdagain') ])
    #["kalle", "lisa" ]
    pwdagain = StringField("pwdagain",[validators.Length(min=5, max=30)])
    position = SelectField("Spelar position", choices=[('g', 'Goalie'), ('d', 'Defence'), ('f', 'Forward')])    


class PersonNewForm(FlaskForm):
    name = StringField("name",[validators.Length(min=3, max=80, message="Skriv in mellan 2 och 80 tecken")])
    city = StringField("city",[validators.Length(min=5, max=30)])
    postalcode = IntegerField("postalcode",[validators.NumberRange(10000,99999)])
    position = SelectField("Spelar position", choices=[('g', 'Goalie'), ('d', 'Defence'), ('f', 'Forward')])    


class UserRegistrationForm(FlaskForm):
    email = StringField("Epost",[validators.Email()])
    firstname = StringField("Förnamn",[validators.Length(min=5, max=40)])
    lastname = StringField("Efternamn",[validators.Length(min=5, max=40)])
    
    val = []
    val.append(validators.Length(min=5, max=30))
    val.append(validators.EqualTo('pwdagain'))
    pwd = StringField("pwd",val)

    pwdagain = StringField("pwdagain",[validators.Length(min=5, max=30)])
    updates = BooleanField("Send me important updates")

class PersonSearchForm(FlaskForm):
    id = IntegerField("Id",[validators.NumberRange(1,9999)])



from flask_wtf import FlaskForm
from wtforms import Form, StringField, validators
from wtforms.fields import IntegerField, SelectField, BooleanField, SubmitField,DateTimeField


    
class manageForm(FlaskForm):
    Type = SelectField("Choose transaction type:", choices=[('Debit'), ('Credit')])    
    Operation = SelectField("Choose operation", choices=[('Salary'), ('Payment'), ('Transfer'),('Deposit cash'),('Bank withdrawal')])    
    Amount = IntegerField("Please enter amount:") ## change later
    #NewBalance = IntegerField("please enter new balance:") ## change later
    AccountId = IntegerField("Please enter the account ID",[validators.NumberRange(1,99999)])
    Date = DateTimeField("Which date and time the transaction happened?")
