import psycopg2
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from psycopg2.extras import DictCursor

from .forms import LoginForm, OptionsForm, SearchForm

class Index(View):
    template = 'index.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template, {"form":form})
    
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            conn = psycopg2.connect(dbname='phones', user='postgres', password='pass1234', host='localhost')
            cursor = conn.cursor()
            cursor.execute("SELECT password, is_admin FROM \"user\" WHERE email = %s;", (username,))
            results = cursor.fetchone()
            cursor.close()
            if results is None:
                form = LoginForm()
            elif results[0]==password and results[1]==False:
                return redirect('options')
            elif results[0]==password and results[1]==True:
                return redirect('admin')
        else:
            form = LoginForm()
        return render(request, self.template, {"form":form})

class Options(View):
    template = 'options.html'
    def get(self, request):
        form =OptionsForm()
        return render(request, self.template, {"form":form})

    def post(self, request):
        form = OptionsForm(request.POST)
        if form.is_valid():
            compare = form.cleaned_data['compare']
            findphone = form.cleaned_data['findphone']
            savesearch = form.cleaned_data['savesearch']
            if compare == True:
                return redirect('compare')
            elif findphone == True:
                return redirect('search')
            elif savesearch == True:
                return redirect('savesearch')
            else:
                form = OptionsForm()
        else:
            form = OptionsForm()
        return render(request, self.template, {"form":form})

class Search(View):
    template = 'search.html'
    def get(self, request):
        form = SearchForm()
        return render(request, self.template, {"form":form})
        
    def post(self, request):
        pass

class Compare(View):
    template = 'porownywarka.html'
    # def get(self, request):
    #     return render(request, self.template)

    def get(self, request):
        connection = psycopg2.connect(dbname='postgres', user='postgres', password='mysecretpassword', host='localhost')
        cursor = connection.cursor()
        cursor.execute("SELECT brand_id, name FROM brand;")
        brands = cursor.fetchall()
        cursor.execute("SELECT phone_id, model, brand_id FROM phone")
        models = cursor.fetchall()
        return render(request, self.template, {'brands': brands, 'models': models})

    def post(self, request):
        phone1_brand = request.POST.get('phone1_brand')
        phone1_model = request.POST.get('phone1_model')
        phone2_brand = request.POST.get('phone2_brand')
        phone2_model = request.POST.get('phone2_model')
        brand_id = request.POST.get('brand_id')

        connection = psycopg2.connect(dbname='postgres', user='postgres', password='mysecretpassword', host='localhost')
        cursor = connection.cursor(cursor_factory=DictCursor)
        cursor.execute("SELECT phone_id, model FROM phone WHERE brand_id = %s", [brand_id])
        models = cursor.fetchall()
        cursor.execute("SELECT * FROM phone WHERE brand_id = %s AND phone_id = %s", [phone1_brand, phone1_model])
        phone1_specs = cursor.fetchall()
        cursor.execute("SELECT * FROM phone WHERE brand_id = %s AND phone_id = %s", [phone2_brand, phone2_model])
        phone2_specs = cursor.fetchall()

        print(phone1_specs)
        print(phone2_specs)
        return JsonResponse({'models': models,'phone1_specs': phone1_specs, 'phone2_specs': phone2_specs}, safe=False)


class SaveSearch(View):
    template = "savesearch.html"
    def get(self, request):
        form = SearchForm()
        return render(request, self.template, {"form":form})



class Admin(View):
    template = 'admin.html'
    def get(self, request):
        return render(request, self.template)
    def post(self, request):
        pass


#class Database(View):
#    template = 'database.html'
#    def get(self, request):
#        return render(request, self.template)
#    #def get(request):
#    #    conn = psycopg2.connect(dbname='phones', user='postgres', password='pass1234', host='localhost')
#
    #    cursor = conn.cursor()
#
    #    cursor.execute("SELECT * FROM phone LIMIT 15")
    #    results = cursor.fetchall()
    #    print(results)
#
    #    conn.close()
#
    #    return render(request, 'database.html', {'results': results})