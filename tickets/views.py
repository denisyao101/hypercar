from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

line_of_clients = {'oil': [],
                   'tires': [],
                   'diagnostics': []
                   }
clients_list = []
processed_client = []


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')


class MenuPage(View):
    menu = ({'text': "Change oil", 'link': "/get_ticket/change_oil"},
            {'text': "Inflate tires", 'link': "/get_ticket/inflate_tires"},
            {'text': "Get diagnostic test", 'link': "/get_ticket/diagnostic"},
            )

    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/menu.html', context={'menu': self.menu})


class ClientPage(View):
    req_url = ''

    minutes = 0

    def get(self, request, *args, **kwargs):
        self.req_url = request.path_info
        clients_list.append(len(clients_list) + 1)

        if self.req_url == '/get_ticket/change_oil/':
            self.minutes = len(line_of_clients['oil']) * 2
            line_of_clients.get('oil').append(clients_list[-1])

        elif self.req_url == '/get_ticket/inflate_tires/':
            self.minutes = len(line_of_clients['oil']) * 2 + len(line_of_clients['tires']) * 5
            line_of_clients.get('tires').append(clients_list[-1])

        elif self.req_url == '/get_ticket/diagnostic/':
            self.minutes = len(line_of_clients['oil']) * 2 + len(line_of_clients['tires']) * 5 + \
                           len(line_of_clients['diagnostics']) * 30
            line_of_clients.get('diagnostics').append(clients_list[-1])

        context = {'number': len(clients_list), 'minutes': self.minutes}

        return render(request, 'tickets/clientPage.html', context)


class OperatorPage(View):

    def post(self, request, *args, **kwargs):
        if len(line_of_clients['oil']) > 0:
            self.last_c = line_of_clients['oil'].pop(0)
            # clients_list.remove(self.last_c)
        elif len(line_of_clients['tires']) > 0:
            self.last_c = line_of_clients['tires'].pop(0)
        elif len(line_of_clients['diagnostics']) > 0:
            self.last_c = line_of_clients['diagnostics'].pop(0)
        if len(clients_list) > 0:
            clients_list.remove(self.last_c)
        processed_client.append(self.last_c)

        return redirect('/processing')

    def get(self, request, *args, **kwargs):
        context = {'clients_line': line_of_clients}
        return render(request, 'tickets/operatorPage.html', context)


class NextClient(View):
    current_client = None

    def get(self, request, *arg, **kwargs):
        next_client = None
        print(processed_client)
        if len(processed_client) > 0:
            # if len(line_of_clients['oil']) > 0:
            #     next_client = line_of_clients['oil'][0]
            # elif len(line_of_clients['tires']) > 0:
            #     next_client = line_of_clients['tires'][0]
            # elif len(line_of_clients['diagnostics']) > 0:
            #     next_client = line_of_clients['diagnostics'][0]
            next_client = processed_client[-1]
        context = {'next_client': next_client}
        return render(request, 'tickets/nextClient.html', context)
