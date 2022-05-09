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
    BucketProductUpdateProduct


def get_sales(product_list):
    sales = Sale.objects.filter(start_date__lte=timezone.now(),
                                end_date__gte=timezone.now())

    was_single = False
    if not isinstance(product_list, Iterable):
        product_list = [product_list]
        was_single = True

    for product in product_list:
        best_sale = None
        for sale in sales:
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


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        queryset = get_sales(queryset)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance = get_sales(instance)
        serializer = self.get_serializer(instance)
        # if discount:
        #     serializer.data['price'] = instance.price * (1 - discount / 100)

        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def bucket_total(request):
    """
    List all product in bucket of authorized user
    """

    bp_qs = BucketProduct.objects.filter(
        bucket__user=request.user).select_related('product')
    for elem in bp_qs:
        elem.product = get_sales(elem.product)

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
        elem.product = get_sales(elem.product)
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
        elem.product = get_sales(elem.product)
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
        elem.product = get_sales(elem.product)
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
