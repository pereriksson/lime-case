from flask import Flask, render_template, jsonify
import locale
from templates.filters import format_amount
from util.api import Api

locale.setlocale(locale.LC_ALL, 'sv_se')

app = Flask(__name__, static_url_path='/static')

# Filters
app.jinja_env.filters["format_amount"] = format_amount

api = Api()

# JSON routes
@app.route('/valuePerCompany')
def value_per_company():
    return jsonify(api.get_value_per_company())

@app.route('/dealsPerMonth')
def deals_per_month():
    return jsonify(api.get_deals_per_month())

# Server-side rendered
@app.route('/')
def home():
    avg_deal_value = api.get_avg_deal_value_for_last_year()
    deals_per_month = api.get_deals_per_month()
    value_per_company = api.get_value_per_company()
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
