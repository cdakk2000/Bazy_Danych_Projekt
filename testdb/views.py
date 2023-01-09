import psycopg2
from django.shortcuts import render
from django.views import View


class Index(View):
    template = 'index.html'

    def get(self, request):
        return render(request, self.template)

    def database_view(request):
        conn = psycopg2.connect(dbname='postgres', user='postgres', password='mysecretpassword', host='localhost')

        cursor = conn.cursor()

        cursor.execute("SELECT * FROM phone LIMIT 15")
        results = cursor.fetchall()

        conn.close()

        return render(request, 'database.html', {'results': results})