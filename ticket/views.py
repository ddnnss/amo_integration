from django.shortcuts import render,get_object_or_404
from amo.models import TicketHolder


def ticket(request,id):
    t_number = id.split('--')[1]
    ticket = get_object_or_404(TicketHolder,ticket_number=t_number)
    return render(request, 'Ticket.html', locals())
