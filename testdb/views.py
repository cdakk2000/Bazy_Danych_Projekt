import psycopg2

import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from pip._vendor.rich import json


class Index(View):
    template = 'porownywarka.html'

    def get(self, request):
        return render(request, self.template)

    def database_view(request):
        conn = psycopg2.connect(dbname='postgres', user='postgres', password='mysecretpassword', host='localhost')

        cursor = conn.cursor()

        cursor.execute("SELECT * FROM phone")
        results = cursor.fetchall()

        conn.close()

        return render(request, 'database.html', {'results': results})

    # def model_brand_view(request):
    #     conn = psycopg2.connect(dbname='postgres', user='postgres', password='mysecretpassword', host='localhost')
    #
    #     cursor = conn.cursor()
    #
    #     with cursor as cursor:
    #         cursor.execute("SELECT brand.name, p.model FROM brand left join phone p on p.phone_id = brand.brand_id;")
    #         choices = cursor.fetchall()
    #     print('Dziala')
    #
    #     conn.close()
    #     return render(request, 'porownywarka.html', {'choices': choices})
    #
    #
    # def get_models(request):
    #     conn = psycopg2.connect(dbname='postgres', user='postgres', password='mysecretpassword', host='localhost')
    #     mark_id = request.GET.get('mark_id')
    #     with conn.cursor() as cursor:
    #         cursor.execute("SELECT brand.name, p.model FROM brand left join phone p on p.phone_id = brand.brand_id WHERE brand.name = %s", [mark_id])
    #         models = cursor.fetchall()
    #     json_models = json.dumps(models)
    #     return HttpResponse(json_models, content_type='application/json')

    def phone_brands_models(request):
        connection = psycopg2.connect(dbname='postgres', user='postgres', password='mysecretpassword', host='localhost')
        if request.method == 'GET':
            cursor = connection.cursor()
            cursor.execute("SELECT brand_id, name FROM brand;")
            brands = cursor.fetchall()
            cursor.execute("SELECT phone_id, model, brand_id FROM phone")
            models = cursor.fetchall()
            return render(request, 'porownywarka.html', {'brands': brands, 'models': models})
        elif request.method == 'POST':
            brand_id = request.POST.get('brand_id')
            cursor = connection.cursor()
            cursor.execute("SELECT phone_id, model FROM phone WHERE brand_id = %s", [brand_id])
            models = cursor.fetchall()
            return JsonResponse({'models': models}, safe=False)