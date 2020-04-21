from django.shortcuts import render
from django.http import HttpResponse
from adminlte import countries
import json
import requests
import http.client
import pycountry
from adminlte.models import Country, Countrydata, Dailydata
from django.db.models import Count, Q
from datetime import datetime
from datetime import date
from django.utils.timezone import get_current_timezone
from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_aware, make_aware


def index(request):
    error = "No internet connection"
    path = ""
    url = "https://coronavirus-monitor.p.rapidapi.com/coronavirus/worldstat.php"

    headers = {
        'x-rapidapi-host': "coronavirus-monitor.p.rapidapi.com",
        'x-rapidapi-key': "600accc2d1msh6a879fcb9fc8c48p155e80jsn3c283317ffe5"
    }

    try:
        response = requests.request("GET", url, headers=headers)
        data = json.loads(response.text)
    except requests.ConnectionError:
        return render(request, 'error.html', {'error': error})

    date = parse_datetime(data['statistic_taken_at'])
    if not is_aware(date):
        date = make_aware(date)

    data2 = countries.loadcountries(request)
    affected = [{'cname': 'India', 'code': 'IN', 'image': 'https://www.countryflags.io/IN/shiny/32.png'},
                {'cname': 'United States', 'code': 'US',
                    'image': 'https://www.countryflags.io/US/shiny/32.png'},
                {'cname': 'Spain', 'code': 'ES',
                    'image': 'https://www.countryflags.io/ES/shiny/32.png'},
                {'cname': 'Italy', 'code': 'IT',
                    'image': 'https://www.countryflags.io/IT/shiny/32.png'},
                {'cname': 'France', 'code': 'FR',
                    'image': 'https://www.countryflags.io/FR/shiny/32.png'},
                {'cname': 'Germany', 'code': 'DE',
                    'image': 'https://www.countryflags.io/DE/shiny/32.png'},
                {'cname': 'United Kingdom', 'code': 'UK',
                    'image': 'https://www.countryflags.io/GB/shiny/32.png'},
                {'cname': 'Iran', 'code': 'IR',
                    'image': 'https://www.countryflags.io/IR/shiny/32.png'},
                {'cname': 'Turkey', 'code': 'TR',
                    'image': 'https://www.countryflags.io/TR/shiny/32.png'},
                {'cname': 'Belgium', 'code': 'BE',
                    'image': 'https://www.countryflags.io/BE/shiny/32.png'},
                {'cname': 'Switzerland', 'code': 'CH',
                    'image': 'https://www.countryflags.io/CH/shiny/32.png'},
                {'cname': 'Netherlands', 'code': 'NL',
                    'image': 'https://www.countryflags.io/NL/shiny/32.png'},
                {'cname': 'China', 'code': 'CN',
                    'image': 'https://www.countryflags.io/CN/shiny/32.png'},
                {'cname': 'Russia', 'code': 'RU',
                    'image': 'https://www.countryflags.io/RU/shiny/32.png'}]

#################################################################################################
    gnews = []
    n = {}
    j = 0
    url2 = ('http://newsapi.org/v2/top-headlines?'
            'sources=the-times-of-india&'
            'apiKey=34cf10d01da242f2ba2f5c59121bb8db')

    try:
        response2 = requests.get(url2)
        data3 = json.loads(response2.text)
    except requests.ConnectionError:
        return render(request, 'error.html', {'error': error})

    for g in data3['articles']:
        if j < 4:
            n['source'] = g.get('source')
            n['url'] = g.get('url')
            n['image'] = g.get('urlToImage')
            n['title'] = g.get('title')
            gnews.append(n.copy())
        j = j+1

    return render(request, 'index.html', {'date': date, 'result': data, 'result2': data2, 'result3': affected,'result4':gnews})


def country(request, cname):
    error = "No internet connection"
    path = "country"

    if(cname == 'IN'):

        url = "https://covid-193.p.rapidapi.com/statistics"

        querystring = {"country": "India"}

        headers = {
            'x-rapidapi-host': "covid-193.p.rapidapi.com",
            'x-rapidapi-key': "600accc2d1msh6a879fcb9fc8c48p155e80jsn3c283317ffe5"
        }

        try:
            response = requests.request(
                "GET", url, headers=headers, params=querystring)
            final = json.loads(response.text)
            final2 = final['response'][0]
            new = final2['cases']['new']

            # data update date and time
            date = parse_datetime(final2['time'])
            if not is_aware(date):
                date = make_aware(date)

        except requests.ConnectionError:
            return render(request, 'error.html', {'error': error})

        url = "https://corona-virus-world-and-india-data.p.rapidapi.com/api_india"

        headers = {
            'x-rapidapi-host': "corona-virus-world-and-india-data.p.rapidapi.com",
            'x-rapidapi-key': "600accc2d1msh6a879fcb9fc8c48p155e80jsn3c283317ffe5"
        }

        try:

            response = requests.request("GET", url, headers=headers)
            data = json.loads(response.text)
        except requests.ConnectionError:
            return render(request, 'error.html', {'error': error})

        # get data from json array to store in database
        arr = []
        arr2 = {}
        arr3 = []

        total = (data['total_values'])
        cc = total['confirmed']
        rr = total['recovered']
        dd = total['deaths']
        now_date = datetime.now()
        today = now_date.strftime("%Y-%m-%d")

      # store data from array in database in countrydata table

        daily_date = Dailydata.objects.values(
            'date').filter(country_id=1, date=today)

        if new != None:
            if daily_date:
                Dailydata.objects.filter(country_id=1, date=today).update(
                    cases=new)
            else:
                ddt = Dailydata(country_id=1, cases=new, date=today)
                ddt.save()

        data_date = Countrydata.objects.values(
            'date').filter(country_id=1, date=today)

        if data_date:
            Countrydata.objects.filter(country_id=1, date=today).update(
                confirmed=total['confirmed'])
        else:
            cd = Countrydata(country_id=1, confirmed=cc,
                             deaths=dd, recovered=rr, date=today)
            cd.save()

        # state wise data array
        arr = (data['state_wise'])
        state = [{'name': 'Maharashtra'}, {'name': 'Delhi'}, {'name': 'Tamil Nadu'}, {'name': 'Rajasthan'}, {'name': 'Madhya Pradesh'}, {'name': 'Telangana'}, {'name': 'Gujarat'}, {'name': 'Uttar Pradesh'},
                 {'name': 'Andhra Pradesh'}, {'name': 'Kerala'}, {'name': 'Jammu and Kashmir'}, {
            'name': 'Karnataka'}, {'name': 'Haryana'}, {'name': 'Punjab'}, {'name': 'West Bengal'},
            {'name': 'Bihar'}, {'name': 'Odisha'}, {'name': 'Uttarakhand'}, {'name': 'Himachal Pradesh'}, {
            'name': 'Chhattisgarh'}, {'name': 'Assam'}, {'name': 'Jharkhand'}, {'name': 'Chandigarh'},
            {'name': 'Ladakh'}, {'name': 'Andaman and Nicobar Islands'}, {'name': 'Goa'}, {'name': 'Puducherry'}, {
            'name': 'Tripura'}, {'name': 'Manipur'}, {'name': 'Mizoram'}, {'name': 'Arunachal Pradesh'},
            {'name': 'Dadra and Nagar Haveli'}, {'name': 'Nagaland'}, {'name': 'Meghalaya'}, {'name': 'Daman and Diu'}, {'name': 'Lakshadweep'}, {'name': 'Sikkim'}]

        for s in state:
            st = arr.get(s['name'])
            arr2['confirm'] = st.get('confirmed')
            arr2['deaths'] = st.get('deaths')
            arr2['recovered'] = st.get('recovered')
            arr2['state'] = st.get('state')
            arr2['code'] = st.get('statecode')
            arr2['active'] = st.get('active')
            arr2['deltaconfirm'] = st.get('deltaconfirmed')
            arr2['deltadeaths'] = st.get('deltadeaths')
            arr2['deltarecovered'] = st.get('deltarecovered')
            arr2['lastupdatedtime'] = st.get('lastupdatedtime')
            arr3.append(arr2.copy())

         # daily new cases , deaths, recovered data
        data1 = Countrydata.objects.values(
            'confirmed').filter(country_id=1).order_by('id')
        data2 = Countrydata.objects.values(
            'deaths').filter(country_id=1).order_by('id')
        data3 = Countrydata.objects.values(
            'recovered').filter(country_id=1).order_by('id')
        data4 = Countrydata.objects.values(
            'date').filter(country_id=1).order_by('id')

        # daily new cases data
        data5 = Dailydata.objects.values(
            'date').filter(country_id=1).order_by('id')
        data6 = Dailydata.objects.values(
            'cases').filter(country_id=1).order_by('id')

        # store and filter data in array to display on chart
        arry1 = list()
        arry2 = list()
        arry3 = list()
        arry4 = list()
        arry5 = list()
        arry6 = list()

        for d1 in data1:
            arry1.append(d1['confirmed'])

        for d2 in data2:
            arry2.append(d2['deaths'])

        for d3 in data3:
            arry3.append(d3['recovered'])

        for d4 in data4:
            d = d4['date']
            arry4.append(d.strftime("%Y-%m-%d"))

        for d5 in data5:
            d = d5['date']
            arry5.append(d.strftime("%Y-%m-%d"))

        for d6 in data6:
            arry6.append(d6['cases'])

        # news data
        gnews = []
        n = {}

        url3 = ('http://newsapi.org/v2/top-headlines?'
                'sources=google-news-in&'
                'apiKey=34cf10d01da242f2ba2f5c59121bb8db')
        try:
            response3 = requests.get(url3)
            gnews2 = json.loads(response3.text)
        except requests.ConnectionError:
            return render(request, 'error.html', {'error': error})

        j = 0
        for g in gnews2['articles']:
            if j < 8:
                n['source'] = g.get('source')
                n['url'] = g.get('url')
                n['image'] = g.get('urlToImage')
                n['title'] = g.get('title')
                gnews.append(n.copy())
            j = j+1

        prevention = [{'title': 'There is enough of everything, everyday for everyone', 'image': 'images/covid1.png', 'url': 'https://www.mohfw.gov.in/pdf/socialdistancingEnglish.pdf'},
                      {'title': 'Whom to Test', 'image': 'images/covid2.png',
                       'url': 'https://www.mohfw.gov.in/pdf/FINAL_14_03_2020_ENg.pdf'},
                      {'title': 'Protective measures', 'image': 'images/covid3.png',
                       'url': 'https://www.mohfw.gov.in/pdf/ProtectivemeasuresEng.pdf'},
                      {'title': 'When to wear a mask?', 'image': 'images/covid5.png',
                       'url': 'https://www.mohfw.gov.in/pdf/Mask-Eng.pdf'},
                      {'title': 'Travellers returning to India', 'image': 'images/covid4.png',
                       'url': 'https://www.mohfw.gov.in/pdf/PostrerEnglishtraveller.pdf'},
                      {'title': 'Protect yourself and others', 'image': 'images/covid6.png', 'url': 'https://www.mohfw.gov.in/pdf/Poster_Corona_ad_Eng.pdf'}]

        return render(request, 'country.html', {'path': path, 'date': date, 'result': arr3, 'result2': total, 'result3': final2, 'result4': gnews,  'result5': prevention, 'arr1': json.dumps(arry1), 'arr2': json.dumps(arry2), 'arr3': json.dumps(arry3), 'arr4': json.dumps(arry4), 'arr5': json.dumps(arry5), 'arr6': json.dumps(arry6)})

    elif cname == 'US':

        url = "https://covid-193.p.rapidapi.com/statistics"

        querystring = {"country": "USA"}

        headers = {
            'x-rapidapi-host': "covid-193.p.rapidapi.com",
            'x-rapidapi-key': "600accc2d1msh6a879fcb9fc8c48p155e80jsn3c283317ffe5"
        }

        try:
            response = requests.request(
                "GET", url, headers=headers, params=querystring)
            us_final = json.loads(response.text)
            us_final2 = us_final['response'][0]
            date = parse_datetime(us_final2['time'])
            if not is_aware(date):
                date = make_aware(date)

            cc = us_final2['cases']['total']
            dd = us_final2['deaths']['total']
            rr = us_final2['cases']['recovered']
            new = us_final2['cases']['new']
            new2 = new.replace('+', '')

            now_date = datetime.now()
            today = now_date.strftime("%Y-%m-%d")
            data_date = Countrydata.objects.values(
                'date').filter(country_id=2, date=today)
            daily_date = Dailydata.objects.values(
                'date').filter(country_id=2, date=today)

            if new != None:
                if daily_date:
                    Dailydata.objects.filter(country_id=2, date=today).update(
                        cases=new2)
                else:
                    ddt = Dailydata(country_id=2, cases=new2, date=today)
                    ddt.save()

            if data_date:
                Countrydata.objects.filter(country_id=2, date=today).update(
                    confirmed=cc)
            else:
                cd2 = Countrydata(country_id=2, confirmed=cc,
                                  deaths=dd, recovered=rr, date=today)
                cd2.save()

        except requests.ConnectionError:
            return render(request, 'error.html', {'error': error})


###############################################################################################

        url2 = "https://covid19-data.p.rapidapi.com/us"

        headers = {
            'x-rapidapi-host': "covid19-data.p.rapidapi.com",
            'x-rapidapi-key': "600accc2d1msh6a879fcb9fc8c48p155e80jsn3c283317ffe5"
        }

        try:
            response = requests.request("GET", url2, headers=headers)
            us_state = json.loads(response.text)
            us_state_list = us_state['list']
        except requests.ConnectionError:
            return render(request, 'error.html', {'error': error})

#################################################################################

        data1 = Countrydata.objects.values(
            'confirmed').filter(country_id=2).order_by('id')
        data2 = Countrydata.objects.values(
            'deaths').filter(country_id=2).order_by('id')
        data3 = Countrydata.objects.values(
            'recovered').filter(country_id=2).order_by('id')
        data4 = Countrydata.objects.values(
            'date').filter(country_id=2).order_by('id')

        # daily new cases data
        data5 = Dailydata.objects.values(
            'date').filter(country_id=2).order_by('id')
        data6 = Dailydata.objects.values(
            'cases').filter(country_id=2).order_by('id')

        arry1 = list()
        arry2 = list()
        arry3 = list()
        arry4 = list()
        arry5 = list()
        arry6 = list()

        for d1 in data1:
            arry1.append(d1['confirmed'])

        for d2 in data2:
            arry2.append(d2['deaths'])

        for d3 in data3:
            arry3.append(d3['recovered'])

        for d4 in data4:
            d = d4['date']
            arry4.append(d.strftime("%Y-%m-%d"))

        for d5 in data5:
            d = d5['date']
            arry5.append(d.strftime("%Y-%m-%d"))

        for d6 in data6:
            arry6.append(d6['cases'])

######################################################################################
        gnews = []
        n = {}

        url3 = ('http://newsapi.org/v2/top-headlines?'
                'sources=usa-today&'
                'apiKey=34cf10d01da242f2ba2f5c59121bb8db')
        try:
            response3 = requests.get(url3)
            gnews2 = json.loads(response3.text)
        except requests.ConnectionError:
            return render(request, 'error.html', {'error': error})

        j = 0
        for g in gnews2['articles']:
            if j < 4:
                n['source'] = g.get('source')
                n['url'] = g.get('url')
                n['image'] = g.get('urlToImage')
                n['title'] = g.get('title')
                gnews.append(n.copy())
            j = j+1

        return render(request, 'us.html', {'path': path, 'result': us_final2, 'date': date, 'result2': us_state_list, 'result3': gnews, 'arr1': json.dumps(arry1), 'arr2': json.dumps(arry2), 'arr3': json.dumps(arry3), 'arr4': json.dumps(arry4), 'arr5': json.dumps(arry5), 'arr6': json.dumps(arry6)})

    else:
        if cname == 'ES':
            country = 'Spain'
            code = 3
        elif cname == 'IT':
            country = 'Italy'
            code = 4
        elif cname == 'FR':
            country = 'France'
            code = 5
        elif cname == 'DE':
            country = 'Germany'
            code = 6
        elif cname == 'UK':
            country = 'UK'
            code = 7
        elif cname == 'IR':
            country = 'Iran'
            code = 8
        elif cname == 'TR':
            country = 'Turkey'
            code = 9
        elif cname == 'BE':
            country = 'Belgium'
            code = 10
        elif cname == 'CH':
            country = 'Switzerland'
            code = 11
        elif cname == 'NL':
            country = 'Netherlands'
            code = 12
        elif cname == 'CN':
            country = 'China'
            code = 13
        elif cname == 'RU':
            country = 'Russia'
            code = 14

        url = "https://covid-193.p.rapidapi.com/statistics"

        querystring = {"country": country}

        headers = {
            'x-rapidapi-host': "covid-193.p.rapidapi.com",
            'x-rapidapi-key': "600accc2d1msh6a879fcb9fc8c48p155e80jsn3c283317ffe5"
        }

        try:
            response = requests.request(
                "GET", url, headers=headers, params=querystring)
            c_final = json.loads(response.text)
            c_final2 = c_final['response'][0]
            date = parse_datetime(c_final2['time'])
            if not is_aware(date):
                date = make_aware(date)

            cc = c_final2['cases']['total']
            dd = c_final2['deaths']['total']
            rr = c_final2['cases']['recovered']
            new = c_final2['cases']['new']
            new2 = new.replace('+', '')

            now_date = datetime.now()
            today = now_date.strftime("%Y-%m-%d")
            data_date = Countrydata.objects.values(
                'date').filter(country_id=code, date=today)

            daily_date = Dailydata.objects.values(
                'date').filter(country_id=code, date=today)

            if new != None:
                if daily_date:
                    Dailydata.objects.filter(country_id=code, date=today).update(
                        cases=new2)
                else:
                    ddt = Dailydata(country_id=code, cases=new2, date=today)
                    ddt.save()

            if data_date:
                Countrydata.objects.filter(country_id=code, date=today).update(
                    confirmed=cc)
            else:
                cd2 = Countrydata(country_id=code, confirmed=cc,
                                  deaths=dd, recovered=rr, date=today)
                cd2.save()

            data1 = Countrydata.objects.values(
                'confirmed').filter(country_id=code).order_by('id')
            data2 = Countrydata.objects.values(
                'deaths').filter(country_id=code).order_by('id')
            data3 = Countrydata.objects.values(
                'recovered').filter(country_id=code).order_by('id')
            data4 = Countrydata.objects.values(
                'date').filter(country_id=code).order_by('id')

            # daily new cases data
            data5 = Dailydata.objects.values(
                'date').filter(country_id=code).order_by('id')
            data6 = Dailydata.objects.values(
                'cases').filter(country_id=code).order_by('id')

            arry1 = list()
            arry2 = list()
            arry3 = list()
            arry4 = list()
            arry5 = list()
            arry6 = list()

            for d1 in data1:
                arry1.append(d1['confirmed'])

            for d2 in data2:
                arry2.append(d2['deaths'])

            for d3 in data3:
                arry3.append(d3['recovered'])

            for d4 in data4:
                d = d4['date']
                arry4.append(d.strftime("%Y-%m-%d"))

            for d5 in data5:
                d = d5['date']
                arry5.append(d.strftime("%Y-%m-%d"))

            for d6 in data6:
                arry6.append(d6['cases'])

        except requests.ConnectionError:
            return render(request, 'error.html', {'error': error})

        return render(request, 'common.html', {'path': path, 'country': country, 'result': c_final2, 'date': date, 'arr1': json.dumps(arry1), 'arr2': json.dumps(arry2), 'arr3': json.dumps(arry3), 'arr4': json.dumps(arry4), 'arr5': json.dumps(arry5), 'arr6': json.dumps(arry6)})


def demo(request):
    error = 'No internet connection'
    country = []
    dt = {}
    i = 0
    url = "https://covid-193.p.rapidapi.com/statistics"

    headers = {
    'x-rapidapi-host': "covid-193.p.rapidapi.com",
    'x-rapidapi-key': "600accc2d1msh6a879fcb9fc8c48p155e80jsn3c283317ffe5"
    }

    response = requests.request("GET", url, headers=headers)
    data = json.loads(response.text)
    

    for d2 in data["response"]:
        cname = d2.get('country')
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

    return render(request, 'demo.html', {'result': data})
