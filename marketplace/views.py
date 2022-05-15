from typing import Iterable

from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from marketplace.models import Category, Bucket, BucketProduct
from marketplace.serializers import CategorySerializer
from marketplace.models import Category, Product, Sale
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import CategorySerializer, ProductSerializer, \
    BucketProductSerializer, BucketProductAddSerializer, \
    BucketProductUpdateProduct, ProductWriteSerializer
from django.db.models import Q


def sale_is_open(sale):
    no_users = sale.users.values_list('id', flat=True) is []
    no_groups = sale.groups.values_list('id', flat=True) is []
    if no_users and no_groups:
        return True
    return False


def user_in_sale(sale, user):
    has_user = set(sale.users.values_list('id', flat=True)).intersection(set([user.id]))
    has_groups = set(sale.groups.values_list('id', flat=True)).intersection(set([user.groups]))
    if has_user or has_groups:
        return False
    return True


def get_sales(product_list, user):
    sales = Sale.objects.filter(start_date__lte=timezone.now(), end_date__gte=timezone.now())

    was_single = False
    if not isinstance(product_list, Iterable):
        product_list = [product_list]
        was_single = True

    for product in product_list:
        best_sale = None
        for sale in sales:
            if sale_is_open(sale) or user_in_sale(sale, user):
                has_categories = set(product.categories.values_list('id', flat=True)).intersection(
                    set(sale.categories.values_list('id', flat=True)))
                if sale.products.filter(
                        id=product.id).exists() or has_categories:
                    if not best_sale:
                        best_sale = sale
                        continue
                    if sale.discount > best_sale.discount:
                        best_sale = sale
        product.best_sale = best_sale
        if best_sale:
            product.price_with_discount = product.price * (1 - best_sale.discount)
        else:
            product.price_with_discount = product.price
    if was_single:
        return product_list[0]
    return product_list


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if request.user.is_staff:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        if request.user.is_staff:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        return Response(status=status.HTTP_403_FORBIDDEN)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        queryset = get_sales(queryset, request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance = get_sales(instance, request.user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if request.user.is_staff:
            serializer = ProductWriteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        return Response(status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def bucket_total(request):
    """
    List all product in bucket of authorized user
    """

    bp_qs = BucketProduct.objects.filter(
        bucket__user=request.user).select_related('product')
    for elem in bp_qs:
        elem.product = get_sales(elem.product, request.user)

    serializer = BucketProductSerializer(bp_qs, many=True)

    total = 0
    total_with_discount = 0
    for bp in bp_qs:
        total += bp.number * bp.product.price
        total_with_discount += bp.number * bp.product.price_with_discount

    response_data = {
        'total': total,
        'total_with_discount': total_with_discount,
        'products': serializer.data,
    }
    return Response(response_data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bucketproduct_add(request):
    data = request.data
    data['product_id'] = data['id']
    data['bucket_id'] = Bucket.objects.get(user=request.user).id

    serializer = BucketProductAddSerializer(data=data)
    serializer.is_valid(True)
    serializer.save()

    bp_qs = BucketProduct.objects.filter(
        bucket__user=request.user).select_related('product')
    for elem in bp_qs:
        elem.product = get_sales(elem.product, request.user)
    total = 0
    total_with_discount = 0
    for bp in bp_qs:
        total += bp.number * bp.product.price
        total_with_discount += bp.number * bp.product.price_with_discount
    response_data = {
        'total': total,
        'total_with_discount': total_with_discount,

    }

    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def product_update(request, pk):
    data = request.data
    instance = BucketProduct.objects.get(product_id=pk, bucket_id=Bucket.objects.get(user=request.user).id)
    serializer = BucketProductUpdateProduct(instance, data=data)
    serializer.is_valid(True)
    serializer.save()

    bp_qs = BucketProduct.objects.filter(
        bucket__user=request.user).select_related('product')
    for elem in bp_qs:
        elem.product = get_sales(elem.product, request.user)
    total = 0
    total_with_discount = 0
    for bp in bp_qs:
        total += bp.number * bp.product.price
        total_with_discount += bp.number * bp.product.price_with_discount
    response_data = {
        'total': total,
        'total_with_discount': total_with_discount,

    }

    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def product_delete(request, pk):
    product = BucketProduct.objects.get(product_id=pk,
                                        bucket_id=Bucket.objects.get(
                                            user=request.user).id)
    product.delete()
    bp_qs = BucketProduct.objects.filter(
        bucket__user=request.user).select_related('product')

    for elem in bp_qs:
        elem.product = get_sales(elem.product, request.user)
    total = 0
    total_with_discount = 0
    for bp in bp_qs:
        total += bp.number * bp.product.price
        total_with_discount += bp.number * bp.product.price_with_discount
    response_data = {
        'total': total,
        'total_with_discount': total_with_discount,

    }

    return Response(response_data, status=status.HTTP_200_OK)
