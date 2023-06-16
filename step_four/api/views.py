from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BuyStockAPISerializer
from utils import check_user_credentials
from .tasks import verify_user_async


class BuyStockAPIView(APIView):

    def post(self, request, format=None):
        
        serializer = BuyStockAPISerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        purchase_data = serializer.data
        if check_user_credentials(purchase_data['user'], purchase_data['stockname'], purchase_data['quantity']):
            
            return Response(status=status.HTTP_200_OK, data={'msg': 'Accepted'})
        
        return Response(status=status.HTTP_403_FORBIDDEN, data={'msg': 'Your credit for the purchase is low!'})
    

class AsyncBuyStockAPIView(APIView):
    def post(self, request, format=None):
        serializer = BuyStockAPISerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        purchase_data = serializer.data

        response_data = {'msg': 'Request received. Verifying user...'}
        response = Response(status=status.HTTP_200_OK, data=response_data)

        # Extract relevant data from the response
        response_data = response.data
        status_code = response.status_code

        # Perform the user verification asynchronously
        verify_user_async.delay(purchase_data, response_data, status_code)

        return response