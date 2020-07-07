from django.shortcuts import render
import logging

logger = logging.getLogger('django',)

def hook(request):
    print(request.GET)
    logger.info('--------------------------------------------')
    logger.info('Something went wrong!')
    logger.info('----------------------------------------------')
