from rest_framework import serializers



class BuyStockAPISerializer(serializers.Serializer):

    user = serializers.CharField(max_length=5)
    stockname = serializers.CharField(max_length=6)
    quantity = serializers.IntegerField()


    def validate_stockname(self, value):

        if value not in ['stock1', 'stock2', 'stock3']:
            raise serializers.ValidationError('Invalid stock name!')
        
        return value
    
    def validate_user(self, value):
        if value not in ['user1', 'user2']:
            raise serializers.ValidationError('Invalid user account!')
        
        return value