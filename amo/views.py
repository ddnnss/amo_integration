import logging
from datetime import datetime
import pytz
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
import uuid
from random import choices
import string
logger = logging.getLogger('django',)


def print_log(text):
    logger.info('--------------------------------------------')
    logger.info(f'{datetime.now()} | {text}')
    logger.info('---------------------------------------------')


@csrf_exempt
def hook(request):
    print_log('New request from AMO')
    req = request.POST
    print_log(req)
    if req['leads[add][0][status_id]'] == '33766144':  #33710263
        print_log('New item in ticket holders')
        local_tz = pytz.timezone("Europe/Paris")
        first_name = None
        last_name = None
        amo_number = None
        email = None
        ticket_number = None
        event = None
        type_of_event = None
        date_of_event = None
        time_of_the_workshop = None

        for i in range(0,10):
            id=None
            try:
                id = req[f'leads[add][0][custom_fields][{i}][id]']
            except:
                pass

            if id:
                if id == '44991':
                    first_name = req[f'leads[add][0][custom_fields][{i}][values][0][value]']
                    print_log('first_name set')

                if id == '45335':
                    last_name = req[f'leads[add][0][custom_fields][{i}][values][0][value]']
                    print_log('last_name set')

                if id == '44995':
                    email = req[f'leads[add][0][custom_fields][{i}][values][0][value]']
                    print_log('email set')

                if id == '69375':
                    event = req[f'leads[add][0][custom_fields][{i}][values][0][value]']
                    print_log('event set')

                if id == '126837':
                    type_of_event = req[f'leads[add][0][custom_fields][{i}][values][0][value]']
                    print_log('type_of_event set')

                if id == '133731':
                    date_of_event = datetime.utcfromtimestamp(int(req[f'leads[add][0][custom_fields][{i}][values][0][value]'])).replace(tzinfo=pytz.utc)
                    print_log('date_of_event set')

                if id == '127001':
                    time_of_the_workshop = datetime.utcfromtimestamp(int(req[f'leads[add][0][custom_fields][{i}][values][0][value]'])).replace(tzinfo=pytz.utc)
                    print_log('time_of_the_workshop set')

                if id == '45285':
                    ticket_number = req[f'leads[add][0][custom_fields][{i}][values][0][value]']
                    print_log('ticket_number set')

                if id == '46517':
                    tiket_url = req[f'leads[add][0][custom_fields][{i}][values][0][value]']
                    print_log('tiket_url set')

        random_string = ''.join(choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=8))
        url = f'{random_string}--{ticket_number}'
        new_ticket = TicketHolder.objects.create(first_name=first_name,
                                    last_name=last_name,
                                    amo_number=req['leads[add][0][id]'],
                                    email=email,
                                    ticket_number=ticket_number,
                                    ticket_url=url,
                                    type_of_event=type_of_event,
                                    event=event,
                                    date_of_event=date_of_event,
                                    time_of_the_workshop=time_of_the_workshop)
        print_log(f'New tickes is : {new_ticket.id}')
        print_log(f'Sending E-mail to : {email}')
        
        event = Event.objects.first()

        ticket_url = f'https://mailsender.inclusionforum.global/ticket/{url}/'
        msg_html = render_to_string('reg.html', {
            'event_id':event.event_id,
            'first_name':first_name,
            'ticket_number': ticket_number,
            'ticket_url':  ticket_url,
        })

        send_mail(f'Registration', None, 'tickets@inclusionforum.global',
                  [email],
                  fail_silently=False, html_message=msg_html)
        send_mail(f'Registration', None, 'tickets@inclusionforum.global',
                  ['tickets-sent@inclusionforum.global'],
                  fail_silently=False, html_message=msg_html)
        print_log(f'Sending E-mail to : tickets-sent@inclusionforum.global')

    else:
        print_log('This is NOT item in ticket holders')

    return HttpResponse(status=200)
