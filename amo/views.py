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
import requests
import datetime as dt
from datetime import datetime
from django.utils import timezone
import settings
logger = logging.getLogger('django',)

#https://akamocfcbigideascom.amocrm.ru/api/v4/contacts/2266189
#https://akamocfcbigideascom.amocrm.ru/api/v4/leads/1031991/links

def print_log(text):
    logger.info('--------------------------------------------')
    logger.info(f'{datetime.now()} | {text}')
    logger.info('---------------------------------------------')

def check_token():
    print_log('Checking access_token.........')
    token_info = Keys.objects.first()
    if (timezone.now() - token_info.updated_at).total_seconds() < token_info.expires_in:
        print_log('Access_token is ok')
        return token_info.access_token

    else:
        print_log('Changing access_token')
        headers = {
            'Content-Type': 'application/json',
        }
        data ={"client_id" : settings.AMO_ID,"client_secret":settings.AMO_SECRET,"grant_type":"refresh_token","refresh_token":token_info.refresh_token,"redirect_uri":"https://mailsender.inclusionforum.global/amo/token"}
        response = requests.post('https://akamocfcbigideascom.amocrm.ru/oauth2/access_token', headers=headers, json=data)
        print_log('AMO response')
        print_log(response.json())
        token_info.access_token = response.json()['access_token']
        token_info.refresh_token = response.json()['refresh_token']
        token_info.expires_in = response.json()['expires_in']
        token_info.save()
        print_log('Changing access_token successful')
        return response.json()['access_token']





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
        name = None
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
        access_token = check_token()

        r = requests.get(f"https://akamocfcbigideascom.amocrm.ru/api/v4/leads/{req['leads[add][0][id]']}/links",
                         headers={"Authorization": f'Bearer {access_token}'})
        contact_id = r.json()['_embedded']['links'][0]['to_entity_id']
        r = requests.get(f"https://akamocfcbigideascom.amocrm.ru/api/v4/contacts/{contact_id}",
                         headers={"Authorization": f'Bearer {access_token}'})

        try:
            name = r.json()['name']
        except:
            pass

        try:
            first_name = r.json()['first_name']
        except:
            pass
        try:
            last_name = r.json()['last_name']
        except:
            pass

        if not first_name:
            first_name = name

        ticket = None
        try:
            tiket = TicketHolder.objects.get(amo_number=req['leads[add][0][id]'])
        except:
            pass

        if not ticket:
            print_log('Creating ticket record')
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
            print_log('Ticket record exists')

    else:
        print_log('This is NOT item in ticket holders')

    return HttpResponse(status=200)
