from flask import Flask, render_template, jsonify
from datetime import *
import functools
import locale
from templates.filters import format_amount
#from util.api import get_deals, get_deals_per_month, deal_is_won_last_year, get_value_per_company, updated_company_statuses, get_avg_deal_value_for_last_year
from util.api import Api

locale.setlocale(locale.LC_ALL, 'sv_se')


app = Flask(__name__, static_url_path='/static')

# Filters
app.jinja_env.filters["format_amount"] = format_amount

# JSON routes
@app.route('/valuePerCompany')
def value_per_company():
    api = Api()
    return jsonify(api.get_value_per_company())

@app.route('/dealsPerMonth')
def deals_per_month():
    api = Api()
    return jsonify(api.get_deals_per_month())

# Server-side rendered
@app.route('/')
def home():
    api = Api()

    # Avg all deals won last year
    avg_deal_value = api.get_avg_deal_value_for_last_year()

    # Number of won all deals per month last year
    deals_per_month = api.get_deals_per_month()

    # Total value of won all deals per customer last year
    value_per_company = api.get_value_per_company()

    # Updated company statuses
    updated_companies = api.updated_company_statuses()

    return render_template(
        "home.html",
        avg_deal_value=avg_deal_value,
        deals_per_month=deals_per_month,
        value_per_company=value_per_company,
        updated_companies=updated_companies
    )


if __name__ == '__main__':
    app.secret_key = 'somethingsecret'
    app.run(debug=True, port=5001)
