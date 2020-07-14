from django.db import models


class TicketHolder(models.Model):
    first_name = models.CharField(max_length=255,blank=True,null=True)
    last_name = models.CharField(max_length=255,blank=True,null=True)
    amo_number = models.CharField(max_length=255,blank=True,null=True)
    email = models.CharField(max_length=255,blank=True,null=True)
    ticket_number = models.CharField(max_length=255,blank=True,null=True)
    ticket_url = models.CharField(max_length=255,blank=True,null=True)
    type_of_event = models.CharField(max_length=255,blank=True,null=True)
    event = models.CharField(max_length=255,blank=True,null=True)
    date_of_event = models.CharField(max_length=255,blank=True,null=True)
    time_of_the_workshop = models.CharField(max_length=255,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)


class Event(models.Model):
    event_id=models.CharField(max_length=255,blank=True,null=True)


class Keys(models.Model):
    access_token = models.TextField(blank=True, null=True)
    refresh_token = models.TextField(blank=True, null=True)
    expires_in = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)



