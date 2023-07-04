from flask import Flask, render_template, jsonify
from datetime import *
import functools
import locale
from templates.filters import format_amount
from util.api import get_companies, get_deals, get_deals_per_month, deal_is_won_last_year, get_value_per_company, updated_company_statuses

locale.setlocale(locale.LC_ALL, 'sv_se')


app = Flask(__name__, static_url_path='/static')

# Filters
app.jinja_env.filters["format_amount"] = format_amount


@app.route('/valuePerCompany')
def value_per_company():
    return jsonify(get_value_per_company())

@app.route('/dealsPerMonth')
def deals_per_month():
    all_deals = get_deals()
    won_deals_last_year = list(filter(deal_is_won_last_year, all_deals))
    return jsonify(get_deals_per_month(won_deals_last_year))

@app.route('/')
def home():
    # Fetch data
    all_deals = get_deals()
    all_companies = get_companies()

    # Avg all deals won last year
    won_deals_last_year = list(filter(deal_is_won_last_year, all_deals))
    avg_deal_value = round(functools.reduce(lambda a, b: a + b["value"], won_deals_last_year, 0) / len(won_deals_last_year))

    # Number of won all deals per month last year
    deals_per_month = get_deals_per_month(won_deals_last_year)

    # Total value of won all deals per customer last year
    value_per_company = get_value_per_company()

    updated_companies = updated_company_statuses()

    return render_template(
        "home.html",
        avg_deal_value=avg_deal_value,
        deals_per_month=deals_per_month,
        value_per_company=value_per_company,
        updated_companies=updated_companies
    )



# DEBUGGING
"""
If you want to debug your app, one of the ways you can do that is to use:
import pdb; pdb.set_trace()
Add that line of code anywhere, and it will act as a breakpoint and halt
your application
"""

if __name__ == '__main__':
    app.secret_key = 'somethingsecret'
    app.run(debug=True, port=5001)
