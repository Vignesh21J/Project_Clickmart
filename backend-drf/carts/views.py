from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import CartSerializer

from .models import Cart, CartItem


# Create your views here.
class CartView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        
        # get or create the cart for logged in user
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(Cart)
        return Response(serializer.data)