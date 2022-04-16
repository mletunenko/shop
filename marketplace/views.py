from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from marketplace.models import Category, Bucket, BucketProduct
from marketplace.serializers import CategorySerializer
from marketplace.models import Category, Product
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import CategorySerializer, ProductSerializer, \
    BucketProductSerializer, BucketProductAddSerializer, \
    BucketProductUpdateProduct


# class CategoryViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     permission_classes = [permissions.IsAuthenticated]
#
# class ProductViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = [permissions.IsAuthenticated]

@api_view(['GET', 'POST'])
def category_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def product_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        product = Product.objects.all()
        category = request.query_params.get('category')
        sort = request.query_params.get('sort')

        if category:
            category = int(category)
            if category > 0:
                product = product.filter(category=category)
            else:
                category = abs(category)
                product = product.exclude(category=category)
            if sort:
                product = product.order_by(sort)
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        product = Product.objects.get(pk=pk)
    except product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def bucket_total(request):
    """
    List all product in bucket of authorized user
    """

    bp_qs = BucketProduct.objects.filter(
        bucket__user=request.user).select_related('product')
    serializer = BucketProductSerializer(bp_qs, many=True)

    total = 0
    for bp in bp_qs:
        total += bp.number * bp.product.price

    response_data = {
        'total': total,
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

    total = 0
    for bp in bp_qs:
        total += bp.number * bp.product.price

    response_data = {
        'total': total
    }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def product_update(request, pk):
    data = request.data
    instance = BucketProduct.objects.get(product_id=pk,
                                         bucket_id=Bucket.objects.get(
                                             user=request.user).id)
    serializer = BucketProductUpdateProduct(instance, data=data)
    serializer.is_valid(True)
    serializer.save()

    bp_qs = BucketProduct.objects.filter(
        bucket__user=request.user).select_related('product')

    total = 0
    for bp in bp_qs:
        total += bp.number * bp.product.price

    response_data = {
        'total': total
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

    total = 0
    for bp in bp_qs:
        total += bp.number * bp.product.price

    response_data = {
        'total': total
    }
    return Response(response_data, status=status.HTTP_200_OK)
