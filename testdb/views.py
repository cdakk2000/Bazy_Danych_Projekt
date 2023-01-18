import psycopg2
from django.shortcuts import render, redirect
from django.views import View
from django.urls.exceptions import NoReverseMatch 
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from psycopg2.extras import DictCursor, RealDictCursor

from .forms import LoginForm, OptionsForm, SearchForm, SaveSearchForm, AdminOptionsForm, AdminPhoneForm, AdminDeletePhoneForm, CommentForm
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


class Phone(View):
    template = 'phone.html'
    def get(self, request, phone_id):
        form = CommentForm()
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

            findcamerasquery = """SELECT mp, f FROM "camera"
                                WHERE camera_id IN 
                                (SELECT camera_id FROM "phone-camera" 
                                WHERE phone_id = %s)
                                ORDER BY mp DESC;"""
            cursor.execute(findcamerasquery, [phone_id,])
            cameras = cursor.fetchall()
            conn.commit()
            conn.close()
        return render(request, self.template, {"phone":results, "comments": comments, "cameras":cameras, "form":form})

    def post(self, request, phone_id):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data
            """TODO: wstawienie komentarza od bazy
            tutaj jest na razie tylko słownik {"comment": "tresc komentarza"}
            jak będzie jednak robić to uwierzytalnianie za każdym razem to trzeba będzie dorabić pola email i hasło
            i szukać czy user jest autoryzowany
            po dadaniu trzeba wyrenderować jeszcze raz stronę  z telefonem"""
            return redirect('phone', phone_id=phone_id)
        else:
            form = CommentForm()

        return redirect('phone', phone_id=phone_id)


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

class Admin(View):
    template = 'admin.html'
    def get(self, request):
        form = AdminOptionsForm()
        return render(request, self.template, {"form":form})

    def post(self, request):
        form = AdminOptionsForm(request.POST)
        if form.is_valid():
            results = form.cleaned_data
            if results["addphone"] == True:
                return redirect('addphone')
            elif results["deletephone"] == True:
                return redirect('deletephone')
            elif results["editphone"] == True:
                return redirect('editphone')
            elif results["comments"] == True:
                pass
            elif results["deleteuser"] == True:
                pass
            else:
                form = AdminOptionsForm()
        else:
            form = AdminOptionsForm()
        return render(request, self.template, {"form":form})

class AddPhone(View):
    template = 'addphone.html'
    def get(self, request):
        form = AdminPhoneForm()
        return render(request, self.template, {"form":form})

    def post(self, request):
        form = AdminPhoneForm(request.POST)
        if form.is_valid():
            results = form.cleaned_data
            cameras = results["cameras"]
            if len(cameras) != 0:
                cameraslist = []
                for camera in cameras.split(', '):
                    i = camera.split('/')
                    cameraslist.append({"mp":int(i[0]), "f":float(i[1])})
            boolfields = ["memory_card_dedicated", "audio_jack", "gps", "nfc", "radio", "battery_removable"]
            for field in boolfields:
                if results[field] == True:
                    results[field] = True
                else:
                    results[field] = False
            """TODO: dodawanie telefonu do bazy
            zakładam że admin musi podać model i markę telefonu
            generalnie z formularzu dodstajemy dane w formie
            {'model': 'asdf', 'brand_name': 'asdf', 'release': None, 'height': None, 'width': None, 'thickness': None, 'resolution': '', 
            'ppi': None, 'cpu_name': '', 
            'chipset_name': '', 'gpu_name': '', 'memory_card_dedicated': False, 'internal_memory': None, 'ram': None, 'wifi': '',
             'sim': '', 'connector': '', 'audio_jack': False, 'bluetooth_version': None, 'gps': False, 'nfc': False, 
            'radio': False, 'battery_capacity': None, 'battery_removable': False, 'cameras': '14/3, 108/1.8', 'photourl': ''}
            
            kamery dodstosowałem tak żeby można je było łatwiej instertować do bazy
            [{'mp': '14', 'f': '3'}, {'mp': '108', 'f': '1.8'}]
            trzeba wyciągnąć ze słownika dane chipset_name, cpu_name, gpu_name, brand_name bo mają swoje tabele
            typu results["chipset_name"] itp;
            dane typu bool w formularzu mam jako char bo w polach bool nie mogę dać None
            """ 
            #na końcu przekirownie do jakiejś stonki która wyświetla że dodano telefon
            #jak robisz jakieś ify to które sprawdzają czy dane zostaną dodane to na końcu daj
            #if cośtam: return render(request, 'results.html', {'operation': 'edited'}) to jest przekierowanie jeśli się udało
            #napisłem na dole jak to może wyglądać 
            #else : form = AdminPhoneForm() to jest jak się nie uda
            #wtedy jak coś pujdzie nie tak to zresetuje się formularz 
            #możesz zobaczyc jak to wyglądało w tym co robiłem wcześniej
            context = {'operation': 'added'}
            return render(request, 'results.html', context)
        else:
            form = AdminPhoneForm()
    
        return render(request, self.template, {"form":form})

class DeletePhone(View):
    template = 'deletephone.html'
    def get(self, request):
        form = AdminDeletePhoneForm()
        return render(request, self.template, {"form":form})
    
    def post(self, request):
        form = AdminDeletePhoneForm(request.POST)
        if form.is_valid():
            results = form.cleaned_data
            """TODO: usuwanie telefonu z bazy
            tutaj raczej nie mam co edytować masz po prosty słownik z modelem i marką telefonu
            {'model': 'asdf', 'brand_name': 'asdf'} itp.
            """
            #tutaj też trzeba zrobić render  tak jak pisałem w addphone i editphone
            #formularz tutaj to nie AdminPhoneForm tylko AdminDeletePhoneForm
            context = {'operation': 'deleted'}
            return render(request, 'results.html', context)
        else:
            form = AdminDeletePhoneForm()
        return render(request, self.template, {"form":form})


class EditPhone(View):
    template = 'editphone.html'
    def get(self, request):
        form = AdminPhoneForm()
        return render(request, self.template, {"form":form})

    def post(self, request):
        form  = AdminPhoneForm(request.POST)
        if form.is_valid():
            results = form.cleaned_data
            results = {k:v for k,v in results.items() if v != None or v != ''}
            if "cameras" in results.results():
                cameras = results["cameras"]
                cameraslist = []
                for camera in cameras.split(', '):
                    i = camera.split('/')
                    cameraslist.append({"mp":int(i[0]), "f":float(i[1])})
            
            boolfields = ["memory_card_dedicated", "audio_jack", "gps", "nfc", "radio", "battery_removable"]
            for field in boolfields:
                if field in results.keys():
                    if results[field][0] == "y" or results[field][0] == "Y":
                        results[field] = True
                    else:
                        results[field] = False

            #na końcu przekirownie do jakiejś stonki która wyświetla że zedytowano telefon
            #jak robisz jakieś ify to które sprawdzają czy dane zostaną zedytowane to na końcu daj
            #if cośtam: return render(request, 'results.html', {'operation': 'edited'}) to jest przekierowanie jeśli się udało
            #else : form = AdminPhoneForm() to jest jak się nie uda
            #wtedy jak coś pujdzie nie tak to zresetuje się formularz 
            #tak samo jak w dodawaniu telefonu
        else:
            form = AdminPhoneForm()
        """TODO: edycja telefonu
        zakładam że user musi podać model i markę telefonu
        tutaj dostajesz tylko dane które zostły wskazane przez admina do edycji więc słownik nie będzie zawierał wszystkich pól tak jak
        w przypadku dodawania telefonu tylko te które zostały podane w formularzu
        generalnie tak zrobiłem z polami bool bo domyślnie nie można dać None w tych polach
        jeśli kamera ma być edydtowna to ma swoją tablicę która wygląda tak samo jak w przypadku dodawania telefonu
        """
        return render(request, self.template, {"form":form})


