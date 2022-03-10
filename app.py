from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
from flask_user import  UserMixin, UserManager,current_user
from flask_login import current_user,LoginManager
from model import * #db, seedData, Customer, Account, User, Role, UserRoles, UserRegistration, Transaction,user_manager
from flask import Flask, render_template, request, url_for, redirect
from random import randint
from flask_user import login_required, roles_required
from sqlalchemy import func
from forms import PersonEditForm, PersonNewForm, UserRegistrationForm, PersonSearchForm, manageForm


 
app = Flask(__name__)
app.config.from_object('config.ConfigDebug')
db.app = app
db.init_app(app)
migrate = Migrate(app,db)

user_manager.app = app
user_manager.init_app(app,db, User)



@app.route("/")
def indexPage():
    activePage = "startPage"
    antalPersoner = Customer.query.count()
    antalKonto = Account.query.count()
    antalBalance = Account.query.with_entities(func.sum(Account.Balance)).scalar()

    return render_template('startPage.html', antalPersoner = antalPersoner, antalKonto = antalKonto,antalBalance=antalBalance, activePage=activePage)

@app.route("/personer")
#@login_required
#@roles_accepted('Customer', 'Admin') # AND # OR
def personerPage():
    
    sortColumn = request.args.get('sortColumn', 'Surname')
    sortOrder = request.args.get('sortOrder', 'asc')
    page = int(request.args.get('page', 1))

    searchWord = request.args.get('q','')

    activePage = "personerPage"
    allaPersoner = Customer.query.filter(
        Customer.Surname.like('%' + searchWord + '%') | 
        Customer.City.like('%' + searchWord + '%')  | 
        Customer.Id.like(searchWord)          )

    if sortColumn == "Surname":
        if sortOrder == "desc":
            allaPersoner = allaPersoner.order_by(Customer.Surname.desc())
        else:
            allaPersoner = allaPersoner.order_by(Customer.Surname.asc())

    if sortColumn == "City":
        if sortOrder == "desc":
            allaPersoner = allaPersoner.order_by(Customer.City.desc())
        else:
            allaPersoner = allaPersoner.order_by(Customer.City.asc())


    paginationObject = allaPersoner.paginate(page,20,False)


    return render_template('personerPage.html', 
            allaPersoner=paginationObject.items, 
            page=page,
            sortColumn=sortColumn,
            sortOrder=sortOrder,
            q=searchWord,
            has_next=paginationObject.has_next,
            has_prev=paginationObject.has_prev, 
            pages=paginationObject.pages, 
            activePage=activePage)




@app.route("/person/<id>")  # EDIT   3
#@roles_required("Admin")
def personPage(id):
    inforpersonFromDb = Customer.query.filter(Customer.Id == id).first_or_404()
    personFromDb = Account.query.join(Customer, Customer.Id == Account.CustomerId).add_columns(Customer.Id.label("CustomerId"),Customer.City,Account.Id, Account.AccountType, Account.Balance).filter(Customer.Id == id).all()
    personantalBalance = Account.query.join(Customer, Customer.Id == Account.CustomerId).with_entities(func.sum(Account.Balance)).filter(Customer.Id == id).scalar()

    return render_template('personPage.html',account=personFromDb,personantalBalance=personantalBalance,inforpersonFromDb=inforpersonFromDb)


@app.route("/person/<id>/<accountid>")  # EDIT   3
#@roles_required("Admin")
def accountPage(id,accountid):
    inforpersonFromDb = Customer.query.filter(Customer.Id == id).first_or_404()
    personFromDb = Account.query.join(Customer, Customer.Id == Account.CustomerId).add_columns(Customer.Id.label("CustomerId"), Account.Id, Account.AccountType, Account.Balance).filter(Customer.Id == id).all()
    accountpersonFromDb = Transaction.query.join(Account,Transaction.AccountId==Account.Id).join(Customer, Customer.Id == Account.CustomerId).add_columns(Customer.Id.label("CustomerId"),Account.Id, Account.AccountType, Account.Balance, Transaction.Date, Transaction.Operation, Transaction.Type,Transaction.Amount).filter(Customer.Id == id).filter(Account.Id == accountid).all()
    inforaccountFromDb = Account.query.filter(Account.CustomerId == id, Account.Id == accountid).first_or_404()

    return render_template('personAccountPage.html',account=personFromDb,inforpersonFromDb=inforpersonFromDb,accountpersonFromDb=accountpersonFromDb,inforaccountFromDb=inforaccountFromDb)




@app.route("/manage",methods=["GET", "POST"]) 
def managePage():
    form = manageForm(request.form) 

    if request.method == "GET":
        return render_template('manageTemplate.html',form=form)

    if form.validate_on_submit():
        tranctionFromDb = Transaction()
        tranctionFromDb.Type = form.Type.data
        tranctionFromDb.Operation = form.Operation.data 
        tranctionFromDb.Date = form.Date.data 
        tranctionFromDb.Amount = form.Amount.data 
        tranctionFromDb.NewBalance = form.NewBalance.data 
        tranctionFromDb.AccountId = form.AccountId.data 


        db.session.add(tranctionFromDb)
        db.session.commit()

        

        admin = Account.query.filter_by(Id=form.AccountId.data).first()
        admin.Balance = form.NewBalance.data
        db.session.commit()



        return "ok!"

    return render_template('manageTemplate.html',form=form)





if __name__  == "__main__":
    with app.app_context():
        upgrade()
        seedData(db)
    app.run()

