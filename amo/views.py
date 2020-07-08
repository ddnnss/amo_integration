import logging
from datetime import datetime
import pytz
from .models import TicketHolder
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string

logger = logging.getLogger('django',)


def print_log(text):
    logger.info('--------------------------------------------')
    logger.info(f'{datetime.now()} | {text}')
    logger.info('---------------------------------------------')


@csrf_exempt
def hook(request):
    print_log('New request from AMO')
    # req = request.POST
    req =  {'leads[add][0][id]': ['939197'],
            'leads[add][0][name]': [''],
            'leads[add][0][status_id]': ['33710260'],
            'leads[add][0][price]': ['0'],
            'leads[add][0][responsible_user_id]': ['6130027'],
            'leads[add][0][last_modified]': ['1594206823'],
            'leads[add][0][modified_user_id]': ['6130027'],
            'leads[add][0][created_user_id]': ['6130027'],
            'leads[add][0][date_create]': ['1594206823'],
            'leads[add][0][pipeline_id]': ['3369178'],
            'leads[add][0][account_id]': ['28942735'],
            'leads[add][0][custom_fields][0][id]': ['44991'],
             'leads[add][0][custom_fields][0][name]': ['First Name'],
            'leads[add][0][custom_fields][0][values][0][value]': ['1'],
             'leads[add][0][custom_fields][1][id]': ['45335'],
            'leads[add][0][custom_fields][1][name]': ['Last Name'],
            'leads[add][0][custom_fields][1][values][0][value]': ['2'],
            'leads[add][0][custom_fields][2][id]': ['44995'],
            'leads[add][0][custom_fields][2][name]': ['E-mail'],
            'leads[add][0][custom_fields][2][values][0][value]': ['3'],
            'leads[add][0][custom_fields][3][id]': ['69375'],
            'leads[add][0][custom_fields][3][name]': ['Event'],
            'leads[add][0][custom_fields][3][values][0][value]': ['4'],
            'leads[add][0][custom_fields][4][id]': ['126837'],
            'leads[add][0][custom_fields][4][name]': ['Type of event'],
            'leads[add][0][custom_fields][4][values][0][value]': ['5'],
            'leads[add][0][custom_fields][5][id]': ['69397'],
            'leads[add][0][custom_fields][5][name]': ['Date of the event'],
             'leads[add][0][custom_fields][5][values][0][value]': ['1594206823'],
            'leads[add][0][custom_fields][6][id]': ['127001'],
             'leads[add][0][custom_fields][6][name]': ['Time of the workshop'],
            'leads[add][0][custom_fields][6][values][0][value]': ['1594206823'],
             'leads[add][0][custom_fields][7][id]': ['45285'],
            'leads[add][0][custom_fields][7][name]': ['Ticket number'],
             'leads[add][0][custom_fields][7][values][0][value]': ['8'],
            'leads[add][0][created_at]': ['1594206823'],
             'leads[add][0][updated_at]': ['1594206823'], 'account[subdomain]': ['akamocfcbigideascom'], 'account[id]': ['28942735'],
             'account[_links][self]': ['https://akamocfcbigideascom.amocrm.ru']}

    if req['leads[add][0][status_id]'][0] == '33710260':  #33710263
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
        try:
            first_name = req['leads[add][0][custom_fields][0][values][0][value]'][0]
        except:
            print_log('first_name not set')

        try:
            last_name = req['leads[add][0][custom_fields][1][values][0][value]'][0]
        except:
            print_log('last_name not set')

        try:
            email = req['leads[add][0][custom_fields][2][values][0][value]'][0]
        except:
            print_log('email not set')

        try:
            event = req['leads[add][0][custom_fields][3][values][0][value]'][0]
        except:
            print_log('event not set')

        try:
            type_of_event = req['leads[add][0][custom_fields][4][values][0][value]'][0]
        except:
            print_log('type_of_event not set')

        try:
            date_of_event = utc_dt = datetime.utcfromtimestamp(int(req['leads[add][0][custom_fields][5][values][0][value]'][0])).replace(tzinfo=pytz.utc)
            print_log(f'date_of_event {date_of_event}')
        except:
            print_log('date_of_event not set')

        try:
            time_of_the_workshop =  datetime.utcfromtimestamp(int(req['leads[add][0][custom_fields][6][values][0][value]'][0])).replace(tzinfo=pytz.utc)
            print_log(f'time_of_the_workshop {time_of_the_workshop}')
        except:
            print_log('time_of_the_workshop not set')

        try:
            ticket_number = req['leads[add][0][custom_fields][7][values][0][value]'][0]
        except:
            print_log('ticket_number not set')

        new_ticket = TicketHolder.objects.create(first_name=first_name,
                                    last_name=last_name,
                                    amo_number=req['leads[add][0][id]'][0],
                                    email=email,
                                    ticket_number=ticket_number,
                                    type_of_event=type_of_event,
                                    event=event,
                                    date_of_event=date_of_event,
                                    time_of_the_workshop=time_of_the_workshop)
        print_log(f'New tickes is : {new_ticket.id}')
        print_log(f'Sending E-mail to : {email}')
        msg_html = render_to_string('reg.html', {
            'p': request.GET.get("phone"),
            'n': request.GET.get("name"),
        })

        send_mail(f'Registration', None, 'no-reply@specsintez-pro.ru',
                  [email],
                  fail_silently=False, html_message=msg_html)

    else:
        print_log('This is NOT item in ticket holders')

    return HttpResponse(status=200)
