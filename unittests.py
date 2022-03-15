import unittest
from wsgiref import validate
from flask import Flask, render_template, request, url_for, redirect
from sqlalchemy import false
from app import app
from forms import manageForm
from model import Customer, Account,Transaction

class TransactionTestCase(unittest.TestCase):
    def setUp(self):
        self.ctx =app.app_context()
        self.ctx.push()
        app.config["SERVER_NAME"]="hejhopp.se"
        app.config["WTF_CSRF_ENSBLED"]=false
        app.config["WTF_CSRF_METHODS"]=[]
        app.config["TESTING"]=True



    def test_draw_should_valid(self):
        test_client = app.test_client()
        with test_client:
            url = "/manage"
            response = test_client.post(url, data={"Type":"Credit","Operation":"Bank withdrawal","Amount":100,"AccountId":1,"Date": "2022-02-03 22:38:26"})
            print(response.status_code)
            assert response.status_code == 302 
    

    def test_transfer_more_than_account_balance_should_invalid(self):
        test_client = app.test_client()
        with test_client:
            url = "/manage"
            response = test_client.post(url, data={"Type":"Credit","Operation":"Payment","Amount":10000000000,"AccountId":1,"Date":"2022-01-03 22:38:26"})
            assert response.status_code == 200 

    def test_save_should_valid(self):
        test_client = app.test_client()
        with test_client:
            url = "/manage"
            response = test_client.post(url, data={"Type":"Credit","Operation":"Deposit cash","Amount":100,"AccountId":1,"Date":"2022-01-04 22:09:26"})
            assert response.status_code == 302 

    def test_draw_negative_should_invalid(self):
        test_client = app.test_client()
        with test_client:
            url = "/manage"
            response = test_client.post(url, data={"Type":"Credit","Operation":"Bank withdrawal","Amount":-100,"AccountId":1,"Date":"2022-01-04 22:09:26"})
            assert response.status_code == 200 


if __name__ == "__main__":
    unittest.main()

