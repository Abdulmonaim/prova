from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status, filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from e_commerce import serializers
from e_commerce import models
from e_commerce import permissions
from e_commerce import filter





class RegisterViewSet(viewsets.ModelViewSet):
    """Handle creating, creating and updating profiles"""
    serializer_class = serializers.RegisterSerializer
    queryset = models.User.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    authentication_classes = (TokenAuthentication,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)

    def get_permissions(self):

        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'list':
            permission_classes = [IsAdminUser]
        else:
                permission_classes = [permissions.UpdateOwnProfile]
        return [permission() for permission in permission_classes]


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 6


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        response = super(UserLoginApiView, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = models.User.objects.get(id=token.user_id)
        cart = models.Cart.objects.get(cart_user=user)
        return Response({'id': token.user_id,'cart': cart.id, 'token': token.key})



class ProductViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    authentication_classes = (TokenAuthentication,)
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['product_title']
    filter_class = filter.ProductFilter
    ordering_fields = ['product_price']
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):

        if self.action == 'retrieve' or self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


    def retrieve(self, request, pk= None, *args, **kwargs):
        reviews = models.Review.objects.filter(review_product=pk)            
        queryset, total = models.Product.objects.get(pk=pk), 0
        sizes_colors = models.Quantity.objects.filter(product_id=pk)
        images = models.Image.objects.filter(images_product=pk)
        size, color, image = [], [], []


        for i in sizes_colors:
            size.append(i.quantity_size.size_name)
            color.append(i.quantity_color.color_name) 

        for i in images:
            image.append(str(i.img))  

        def CustomSerializer(serializer):

            product = dict()
            product = serializer.data
            product['sizes'] = size
            product['colors'] = color
            product['images'] = image

            return product

        if len(reviews) == 0:
            product_serializer = serializers.ProductSerializer(queryset)
            return Response(CustomSerializer(product_serializer))

        for review in reviews:
            total += review.review_rating 

        avg = total / len(reviews)
        queryset.product_rating = avg
        queryset.save()

        product_serializer = serializers.ProductSerializer(queryset)

        return Response(CustomSerializer(product_serializer))

    # def list(self, request, pk= None, *args, **kwargs):          
    #     queryset = models.Product.objects.all()
    #     images = models.Image.objects.filter(images_product=pk)

    #     for i in images:
    #         image.append(str(i.img))  

    #     def CustomSerializer(serializer):

    #         product = dict()
    #         product = serializer.data
    #         product['image'] = image

    #         return product

    #     product_serializer = serializers.ProductSerializer(queryset)

    #     return Response(CustomSerializer(product_serializer))



class ReviewViewSet(viewsets.ModelViewSet):

    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    authentication_classes = (TokenAuthentication,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_product', 'review_user']

    def get_permissions(self):

        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
                permission_classes = [permissions.UpdateOwnProfile]
        return [permission() for permission in permission_classes]
        



class CategoryViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()



class CartViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.CartSerializer
    queryset = models.Cart.objects.all()

    def retrieve(self, request, pk= None, *args, **kwargs):
        items = models.CartItem.objects.filter(cart_item_cart=pk)            
        queryset, total = models.Cart.objects.get(pk=pk), 0
        items_num  = len(items)

        if queryset.promo_code == "Wessam" and queryset.promo_counter == 1:
            cart_serializer = serializers.CartSerializer(queryset)
            item_serializer = serializers.CartItemSerializer(items, many=True)
            return Response({'cart':cart_serializer.data, 'items': item_serializer.data})

        for item in items:
            total += item.cart_item_price * item.cart_item_quantity

        queryset.items_num = items_num
        queryset.cart_total = total

        if queryset.cart_total >= 300:
            queryset.grand_total = queryset.cart_total
            queryset.shipping_charge = 0

        else:
            queryset.grand_total = queryset.cart_total + queryset.shipping_charge
            queryset.shipping_charge = 25

        if queryset.promo_code == "Wessam" and queryset.promo_counter == 0:
            queryset.grand_total = queryset.grand_total / 2
            queryset.promo_counter = 1
    
        queryset.save()
        cart_serializer = serializers.CartSerializer(queryset)
        item_serializer = serializers.CartItemSerializer(items, many=True)

        return Response({'cart':cart_serializer.data, 'items': item_serializer.data})



class CartItemViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.CartItemSerializer
    queryset = models.CartItem.objects.all()



class ImageViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.ImageSerializer
    queryset = models.Image.objects.all()
    parser_classes = (MultiPartParser, FormParser)



class ColorViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.ColorSerializer
    queryset = models.Color.objects.all()



class SizeViewSet(viewsets.ModelViewSet):
    
    serializer_class = serializers.SizeSerializer
    queryset = models.Size.objects.all()



class QuantityViewSet(viewsets.ModelViewSet):
    
    serializer_class = serializers.QuantitySerializer
    queryset = models.Quantity.objects.all()
    

class CheckedCartViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.CheckedCartSerializer
    queryset = models.CheckedCart.objects.all()

    def list(self, request, pk= None, *args, **kwargs):
        cart_checkout = models.CheckedCart.objects.filter(user_id=request.query_params['user_id'])
        carts = []

        for cart in cart_checkout:
            items = models.CheckedCartItem.objects.filter(checked_cart=cart)
            cart_serializer = serializers.CheckedCartSerializer(cart)
            item_serializer = serializers.CheckedCartItemSerializer(items, many=True)
            cart_res = {'cart':cart_serializer.data, 'items': item_serializer.data}
            carts.append(cart_res)         

        return Response(carts)


class CheckedCartItemViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.CheckedCartItemSerializer
    queryset = models.CheckedCartItem.objects.all()