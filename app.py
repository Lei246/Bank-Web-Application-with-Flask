from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
from flask_user import  UserMixin, UserManager,current_user
from flask_login import current_user,LoginManager
from model import * #db, seedData, Customer, Account, User, Role, UserRoles, UserRegistration, Transaction,user_manager
from flask import Flask, render_template, request, url_for, redirect
from random import randint
from flask_user import login_required, roles_required


 
app = Flask(__name__)
app.config.from_object('config.ConfigDebug')
db.app = app
db.init_app(app)
migrate = Migrate(app,db)

#user_manager.app = app
#user_manager.init_app(app,db, User)



@app.route("/")
def indexPage():
    activePage = "startPage"
    antalPersoner = Customer.query.count()
    antalKonto = Account.query.count()
    return render_template('startPage.html', antalPersoner = antalPersoner, antalKonto = antalKonto, activePage=activePage)

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






if __name__  == "__main__":
    with app.app_context():
        upgrade()
        seedData(db)
    app.run()

