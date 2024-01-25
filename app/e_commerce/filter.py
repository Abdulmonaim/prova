from e_commerce import models

from django_filters import FilterSet, RangeFilter


class ProductFilter(FilterSet):
    product_price = RangeFilter()

    class Meta:
        model = models.Product
        fields = ['product_price', 'product_brand', 'product_category']#, 'product_color', 'product_size']