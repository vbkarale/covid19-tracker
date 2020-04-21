from django.shortcuts import render
from django.http import HttpResponse
import datetime
from datetime import date
import json
import requests
import pycountry


def loadcountries(request):
    error = 'No internet connection'
    country = []
    dt = {}
    i = 0
    url = "https://coronavirus-monitor.p.rapidapi.com/coronavirus/cases_by_country.php"

    headers = {
         'x-rapidapi-host': "coronavirus-monitor.p.rapidapi.com",
          'x-rapidapi-key': "600accc2d1msh6a879fcb9fc8c48p155e80jsn3c283317ffe5"
         }
    try:
        response = requests.request("GET", url, headers=headers)
        data = json.loads(response.text)
    except requests.ConnectionError:
        return render(request, 'error.html', {'error': error})

    for d2 in data["countries_stat"]:
        cname = d2.get('country_name')
        if cname == "USA":
            cname = "United States"
        elif cname == "UK":
            cname = "United Kingdom"
        elif cname == "UAE":
            cname = "Unites Arab Emirates"
        d = pycountry.countries.get(name=cname)
        if d != None:
            dt = d.alpha_2
            d2["code"] = dt
            d2["image"] = "https://www.countryflags.io/"+ dt +"/shiny/16.png"
        elif d == None:
            d2["code"] = ''
            d2["image"] = ''
        i = +1
        country.append(d2.copy())
    return country

