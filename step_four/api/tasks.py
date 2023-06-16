from rest_framework import status
from django.http import HttpResponse
from rest_framework.response import Response
from celery import shared_task
import json
from celery.exceptions import SoftTimeLimitExceeded

from utils import check_user_credentials


@shared_task(bind=True, time_limit=5)
def verify_user_async(self, purchase_data, response_data, status_code):
    # Perform the user verification
    verification_result = check_user_credentials(purchase_data['user'], purchase_data['stockname'], purchase_data['quantity'], 2)

    if verification_result:
        # User verification successful
        response_data['msg'] = 'Accepted'
    else:
        # User verification failed
        response_data['msg'] = 'Your credit for the purchase is low!'
        status_code = status.HTTP_403_FORBIDDEN

    # Create an HttpResponse object with the updated response data
    response = HttpResponse(content_type='application/json')
    response.status_code = status_code
    response.content = json.dumps(response_data)

    
    return response