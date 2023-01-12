import psycopg2
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponseRedirect

from .forms import LoginForm, OptionsForm, SearchForm
logged_user = None
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
            cursor.close()
            if results is None:
                form = LoginForm()
            elif results[0]==password and results[1]==False:
                logged_user = username
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
        pass

class Compare(View):
    template = 'compare.html'
    def get(self, request):
        return render(request, self.template)

class SaveSearch(View):
    template = "savesearch.html"
    def get(self, request):
        form = SearchForm()
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