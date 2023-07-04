import requests
import json
from dateutil.parser import *
from datetime import *
from dateutil.relativedelta import *

def updated_company_statuses():
    updated_companies = get_companies()
    all_deals = get_deals()
    for company in updated_companies:
        company_deals = list(filter(lambda x: get_deals_won_by_company(x, company["_id"]), all_deals))
        company_deals_last_year = list(
            filter(lambda x: deal_is_won_in_the_last_year_by_company(x, company["_id"]), all_deals))

        if company["buyingstatus"]["key"] == "notinterested":
            status = "notinterested"
        elif len(company_deals_last_year) > 0:
            status = "customer"
        elif len(company_deals) > 0:
            status = "inactive"
        elif len(company_deals) == 0:
            status = "prospect"
        company["new_status"] = status
    return updated_companies

def get_value_per_company():
    all_deals = get_deals()
    won_deals_last_year = list(filter(deal_is_won_last_year, all_deals))
    all_companies = get_companies()
    value_per_customer = []
    for deal in won_deals_last_year:
        entry = next((item for item in value_per_customer if item["company"] == deal["company"]), None)

        if entry is not None:
            entry["value"] += deal["value"]
        else:
            company = next((item for item in all_companies if item["_id"] == deal["company"]), None)
            value_per_customer.append({
                "company": deal["company"],
                "company_name": company["name"],
                "value": deal["value"]
            })
    value_per_customer = sorted(value_per_customer, key=lambda c: c["value"], reverse=True)
    return value_per_customer

def deal_is_won_last_year(deal):
    if not deal["closeddate"]:
        return False
    one_year_ago = datetime.now().replace(tzinfo=timezone(offset=timedelta())) - relativedelta(years=1)
    return deal["dealstatus"]["key"] == "agreement" and parse(deal["closeddate"]) > one_year_ago


def get_deals_won_by_company(deal, company):
    if not deal["closeddate"]:
        return False
    return deal["dealstatus"]["key"] == "agreement" and deal["company"] == company


def deal_is_won_in_the_last_year_by_company(deal, company_id):
    if not deal["closeddate"]:
        return False
    one_year_ago = datetime.now().replace(tzinfo=timezone(offset=timedelta())) - relativedelta(years=1)
    return deal["dealstatus"]["key"] == "agreement" and parse(deal["closeddate"]) > one_year_ago and \
           deal["company"] == company_id

def get_deals_per_month(won_deals_last_year):
    deals_per_month = []
    for deal in won_deals_last_year:
        if not deal["closeddate"]:
            continue
        closed_month = parse(deal["closeddate"]).strftime("%B")
        closed_month_number = parse(deal["closeddate"]).month
        entry = next((item for item in deals_per_month if item["month_number"] == closed_month_number), None)
        if entry is not None:
            entry["deals"] += 1
        else:
            deals_per_month.append({
                "month": closed_month,
                "month_number": closed_month_number,
                "deals": 1
            })
    deals_per_month = sorted(deals_per_month, key=lambda d: d["deals"], reverse=True)
    return deals_per_month

def get_companies():
    return get_api_data(
        url="https://api-test.lime-crm.com/api-test/api/v1/limeobject/company/?_limit=50"
    )

def get_deals():
    return get_api_data(
        url="https://api-test.lime-crm.com/api-test/api/v1/limeobject/deal/?_limit=50"
    )

def get_api_data(url):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/hal+json",
        "x-api-key": "860393E332148661C34F8579297ACB000E15F770AC4BD945D5FD745867F590061CAE9599A99075210572"
    }

    # First call to get first data page from the API
    response = requests.get(url=url,
                            headers=headers,
                            data=None,
                            verify=False)

    # Convert response string into json data and get embedded limeobjects
    json_data = json.loads(response.text)
    limeobjects = json_data.get("_embedded").get("limeobjects")

    # Check for more data pages and get thoose too
    nextpage = json_data.get("_links").get("next")
    while nextpage is not None:
        url = nextpage["href"]
        response = requests.get(url=url,
                                headers=headers,
                                data=None,
                                verify=False)

        json_data = json.loads(response.text)
        limeobjects += json_data.get("_embedded").get("limeobjects")
        nextpage = json_data.get("_links").get("next")

    return limeobjects