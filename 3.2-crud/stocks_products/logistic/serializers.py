from rest_framework import serializers

from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["title", "description"]


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ["quantity", "price", "product"]


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ["address", "positions"]

    def create(self, validated_data):
        positions = validated_data.pop("positions")
        stock = super().create(validated_data)
        for position in positions:
            StockProduct.objects.create(stock_id=stock.pk, **position)
        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop("positions")
        stock = super().update(instance, validated_data)
        for position in positions:
            StockProduct.objects.select_for_update().filter(
                product=position["product"].id
            ).update(stock_id=stock.id, **position)
        return stock
