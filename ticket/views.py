from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from amo.models import TicketHolder

from amo.views import print_log

def ticket(request,id):
    ticket = get_object_or_404(TicketHolder,ticket_url=id)
    print_log(f'Ticket ID : {ticket.id} is viewed')
    first_name = ticket.first_name
    last_name = ticket.last_name
    date = ticket.date_of_event.split(' ')[0]
    name = ticket.event
    ticket_number = ticket.ticket_number
    email = ticket.email
    if ticket.type_of_event == 'workshop':
        event_name = 'Name of the workshop'
        time = f"{ticket.time_of_the_workshop.split(' ')[1].split('+')[0]} CET"
        return render(request, 'Ticket.html', locals())
    elif ticket.type_of_event == 'panel day':
        event_name = 'Panel day ticket'
        return render(request, 'Ticket.html', locals())
    elif ticket.type_of_event == 'panel day startup':
        event_name = 'Panel day ticket'
        return render(request, 'Ticket.html', locals())
    else:
        print_log(f'ERROR while open ticket ID : {ticket.id}')
        return HttpResponse("<h1>Some error is happening</h1><p>Please contact us : <a href='mailto:support@inclusionforum.global'>support@inclusionforum.global</a></p>")


