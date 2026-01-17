from rest_framework import serializers
from .models import Cart, CartItem

# class CartSerializer(serializers.ModelSerializer):
#     items = CartItemSerializer(many=True)
#     class Meta:
#         model=Cart
#         fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    tax_percent = serializers.DecimalField(source='product.tax_percent', max_digits=10, decimal_places=2, read_only=True)
    class Meta:
        model=CartItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    subtotal = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    class Meta:
        model=Cart
        fields = '__all__'

    def get_subtotal(self, obj):    # obj means Cart model instance. Because model=Cart in Meta class
        # subtotal = 0

        # # Cart model=> [FK ->] =>CartItem model. Its instance related_name='items' [Reverse LookUp]. So obj.items
        # for item in obj.items.all():
        #     subtotal = subtotal + item.product.price * item.quantity

        # return subtotal

        return sum(
            item.product.price * item.quantity
            for item in obj.items.all()
        )
    
    def get_total(self, obj):
        final_amount = 0

        for item in obj.items.all():
            subtotal = item.product.price * item.quantity
            tax = subtotal * (item.product.tax_percent / 100)

            final_amount += subtotal + tax

        return final_amount
