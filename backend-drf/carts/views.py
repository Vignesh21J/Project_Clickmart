from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import CartSerializer, CartItemSerializer

from .models import Cart, CartItem

from products.models import Product


# Create your views here.
class CartView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        
        # get or create the cart for logged in user
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    

class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # take the product input
        product_id = request.data.get('product_id')

        if not product_id:
            return Response({'error': 'product_id is required'})
        
        quantity = request.data.get('quantity')

        if not quantity:
            return Response({'error': 'quantity is required'})

        try:
            quantity = int(quantity)
        except ValueError:
            return Response({'error': 'quantity must be a number'})

        if quantity <= 0:
            return Response({'error': 'quantity must be at least 1'})
        
        # get the product
        product = get_object_or_404(Product, id=product_id, is_active=True)
        # print("product==>", product)
        

        # get or create the cart
        cart, _ = Cart.objects.get_or_create(user=request.user)  # user is the FK in the Cart model

        # get or create cartitem
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)


        # already existing cart
        if not created:
            item.quantity = item.quantity + quantity
        # new cart
        else:
            item.quantity = quantity
        
        item.save()


        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)



class ManageCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, item_id):
        # validation
        if 'change' not in request.data:
            return Response({"error":"Provide 'change' field"})
        
        change = int(request.data.get('change'))  # delta => -1 or +1

        item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)  # item is a  <CartItem object>. So item.product in models.py
        product = item.product
        
        # for adding, check the stock
        if change > 0:
            if item.quantity + change > product.stock:
                return Response({'error': 'Not enough stock'})
            
        new_qty = item.quantity + change   # delta => -1 or +1

        if new_qty <= 0:
            # remove the item from the cart
            item.delete()
            return Response({'detail': 'Item removed'})
        
        # save the new quantity
        item.quantity = new_qty
        item.save()

        # When giving back the full / updated response
        serializer = CartItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def delete(self, request, item_id):
        item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)