import psycopg2
from django.shortcuts import render, redirect
from django.views import View
from django.urls.exceptions import NoReverseMatch 
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from psycopg2.extras import DictCursor, RealDictCursor

from .forms import LoginForm, OptionsForm, SearchForm, SaveSearchForm
logged_user = None
all_phones = """select phonecpu.*, gpu.name as gpu_name into temp tempphone
                from	
	                (select phonechipset.*, cpu.name as cpu_name 
	                 from
		                 (select phonebrand.*, chipset.name as chipset_name 
	 	                  from 
			                  (select phone.*, brand.name as brand_name 
			                   from phone
			                   join brand
			                   on phone.brand_id = brand.brand_id) as phonebrand
		                  join chipset
	 	                  on chipset.chipset_id=phonebrand.chipset_id) as phonechipset
	                 join cpu 
	                 on phonechipset.cpu_id = cpu.cpu_id) as phonecpu
                join gpu
                on gpu.gpu_id=phonecpu.gpu_id"""
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
            register = form.cleaned_data['register']
            conn = psycopg2.connect(dbname='phones', user='postgres', password='pass1234', host='localhost')
            cursor = conn.cursor()
            if register == True:
                pass
            cursor.execute("SELECT password, is_admin FROM \"user\" WHERE email = %s;", (username,))
            results = cursor.fetchone()
            conn.close()
            global logged_user
            if results is None:
                form = LoginForm()
            elif results[0]==password and results[1]==False:
                logged_user = username
                return redirect('options')
            elif results[0]==password and results[1]==True:
                logged_user = username
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
            manage = form.cleaned_data['manage']
            if compare == True:
                return redirect('compare')
            elif findphone == True:
                return redirect('search')
            elif savesearch == True:
                return redirect('savesearch')
            elif manage == True:
                return redirect('manage')
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
        form = SearchForm(request.POST)
        if form.is_valid():
            conn = psycopg2.connect(dbname='phones', user='postgres', password='pass1234', host='localhost')
            with  conn.cursor() as cursor:
                searchform = form.cleaned_data
                searchform = {k: v for k, v in searchform.items() if v is not None and v != '' and v!=False}

                if 'model' in searchform:
                    cursor.execute("SELECT phone_id FROM phone WHERE model = %s;", (searchform['model'],))
                    results = cursor.fetchone()
                    conn.commit()
                    conn.close()

                    try:
                        return redirect('phone', phone_id=results[0])
                    except NoReverseMatch:
                        return redirect('noresults')

                elif len(searchform) != 0:

                    findPhone = all_phones+";"
                    cursor.execute(findPhone)

                    removable_columns = ["brand_id", "cpu_id", "gpu_id", "chipset_id", "image_url"]
                    remove_query = """ALTER TABLE tempphone DROP %s;"""
                    for remove in removable_columns:
                        cursor.execute(remove_query % remove)  

                    search_query = "SELECT phone_id FROM tempphone WHERE "
                    for k in searchform.keys():
                        if k == "ram" or k == "internal_memory":
                            search_query += "%s = ANY("+k+") AND "
                        elif k=="bluetooth_version" or k=="width" or k=="height" or k=="thickness":
                            search_query+= k +" = real \'%s\' AND "
                        else:
                            search_query += k + " = \'%s\' AND "
                    search_query = search_query[:-5] + ";"
                    cursor.execute(search_query % tuple(searchform.values()))
                    results = cursor.fetchall()
                    resultsphoneids = "/".join([str(x[0]) for x in results])
                    conn.commit()
                    conn.close()

                    try:
                        return redirect('searchresult', phone_ids=resultsphoneids)
                    except NoReverseMatch:
                       return redirect('noresults')
                else:
                    form = SearchForm()
        else:
            form = SearchForm()
                
        return render(request, self.template, {"form":form})

class Compare(View):
    template = 'porownywarka.html'
    # def get(self, request):
    #     return render(request, self.template)

    def get(self, request):
        connection = psycopg2.connect(dbname='postgres', user='postgres', password='pass1234', host='localhost')
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

        connection = psycopg2.connect(dbname='postgres', user='postgres', password='pass1234', host='localhost')
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
        form = SaveSearchForm()
        return render(request, self.template, {"form":form})

    def post(self, request):
        form = SaveSearchForm(request.POST)
        if form.is_valid():
            conn = psycopg2.connect(dbname='phones', user = 'postgres', password = 'pass1234', host = 'localhost')
            brand_id = None
            phone_id = None
            with conn.cursor() as cursor:
                searchform = form.cleaned_data
                searchform = {k: v for k, v in searchform.items() if v is not None and v != ''}
                print(searchform)
                if 'brand' in searchform.keys():
                    cursor.execute("SELECT brand_id FROM brand WHERE name = %s;", (searchform['brand'],))
                    brand_id = cursor.fetchone()[0]
                
                if 'model' in searchform.keys():
                    cursor.execute("SELECT phone_id FROM phone WHERE model = %s;", (searchform['model'],))
                    phone_id = cursor.fetchone()[0]
                
                conn.commit()
                if len(searchform) == 0:
                    return redirect('noresults')

            with conn.cursor() as cursor:
                global logged_user
                if brand_id is not None and logged_user is not None:
                        cursor.execute("""INSERT INTO brand_subscription (brand_id, user_id)
                                         VALUES (%s, (SELECT user_id FROM \"user\" WHERE email = %s));""", (brand_id, logged_user))
                        conn.commit()

                if phone_id is not None and logged_user is not None:
                        cursor.execute("""INSERT INTO phone_subscription (phone_id, user_id)
                                         VALUES (%s, (SELECT user_id FROM \"user\" WHERE email = %s));""", (phone_id, logged_user))
                        conn.commit()

            conn.close()

        form = SaveSearchForm()
        return render(request, self.template, {"form":form})
            
class Manage(View):
    template = 'manage.html'
    def get(self, request):
        return render(request, self.template)



class Admin(View):
    template = 'admin.html'
    def get(self, request):
        return render(request, self.template)
    def post(self, request):
        pass

class Phone(View):
    template = 'phone.html'
    def get(self, request, phone_id):
        conn = psycopg2.connect(dbname='phones', user= 'postgres',  password='pass1234', host='localhost')
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            findPhone = all_phones+""" where phone_id = %s;"""
            cursor.execute(findPhone, [phone_id,])
            
            removable_columns = ["brand_id", "cpu_id", "gpu_id", "chipset_id", "phone_id"]
            remove_query = """ALTER TABLE tempphone DROP %s;"""
            for remove in removable_columns:
                cursor.execute(remove_query % remove)
            
            cursor.execute("select * from tempphone;")
            results = cursor.fetchone()
            
            cursor.execute("drop table tempphone;")
            conn.commit()
            findcommentsquery = """select "user".email, "comment".content from comment 
                                    join "user"
                                    on "user".user_id = "comment".user_id
                                    where "comment".phone_id = %s;"""
            cursor.execute(findcommentsquery, [phone_id,])
            comments = cursor.fetchall()
            conn.commit()
            conn.close()
        return render(request, self.template, {"phone":results, "comments": comments})

class SearchResult(View):
    template = 'searchresult.html'
    def get(self, request, phone_ids):
        phone_ids = [int(x) for x in phone_ids.split('/')]
        conn = psycopg2.connect(dbname='phones', user= 'postgres', password='pass1234', host='localhost')
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            findPhones = all_phones+""" where phone_id in %s;"""
            cursor.execute(findPhones, [tuple(phone_ids),])

            removable_columns = ["brand_id", "cpu_id", "gpu_id", "chipset_id", "phone_id", "image_url"]
            remove_query = """ALTER TABLE tempphone DROP %s;"""
            for remove in removable_columns:
                cursor.execute(remove_query % remove)

            cursor.execute("select * from tempphone;")
            results = cursor.fetchall()
            cursor.execute("drop table tempphone;")
        
        return render(request, self.template, {"phones":results})

class NoResults(View):
    template = 'noresult.html'
    def get(self, request):
        return render(request, self.template)
