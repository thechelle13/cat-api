from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from catproofapi.models import Product, CatUser, Area
from django.contrib.auth.models import User
from .users import CatUserSerializer
from .areas import AreaSerializer

class SimpleProductSerializer(serializers.ModelSerializer):


    class Meta:
        model = Product
        fields = [
           
            "title",
            "image_url",
            "company",
            "cat_user",
            "description",
            "approved",
            "areas",
            # "is_owner",
        ]


class ProductSerializer(serializers.ModelSerializer):
    cat_user = CatUserSerializer(many=False)
    is_owner = serializers.SerializerMethodField()
    areas = AreaSerializer(many=True)
    # area = AreaSerializer(many=False)


    def get_is_owner(self, obj):
        # Check if the authenticated user is the owner
        return self.context["request"].user == obj.cat_user.user

    class Meta:
        model = Product
        fields = [
            "id",
            "cat_user",
            "title",
            "image_url",
            "company",
            "publication_date",
            "description",
            "approved",
            "areas",
            "is_owner",
        ]


class ProductViewSet(viewsets.ViewSet):
    def list(self, request):
        product = Product.objects.all()
        serializer = ProductSerializer(product, many=True, context={"request": request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product, context={"request": request})
            return Response(serializer.data)

        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        # Get the data from the client's JSON payload
        cat_user = CatUser.objects.get(user=request.auth.user)
       
        title = request.data.get("title")
        publication_date = request.data.get("publication_date")
        image_url = request.data.get("image_url")
        company = request.data.get("company")
        description = request.data.get("description")
        approved = request.data.get("approved")
        area_id = request.data.get("area")
        area = Area.objects.get(pk=area_id)
       

        # Create a post database row first, so you have a
        # primary key to work with
        product = Product.objects.create(
            cat_user=cat_user,
          
            title=title,
            publication_date=publication_date,
            image_url=image_url,
            company=company,
            description=description,
            approved=approved,
            area=area,
        )
        
        # Establish the many-to-many relationships
        area_ids = request.data.get("areas", [])
        product.areas.set(area_ids)

        serializer = ProductSerializer(product, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)

            # Is the authenticated user allowed to edit this post?
            self.check_object_permissions(request, product)

            serializer = SimpleProductSerializer(data=request.data)
            if serializer.is_valid():
                
                product.title = serializer.validated_data["title"]
                # post.publication_date = serializer.validated_data["publication_date"]
                product.company = serializer.validated_data["company"]
                product.image_url = serializer.validated_data["image_url"]
                product.description = serializer.validated_data["description"]
                product.approved = serializer.validated_data["approved"]
                
                # product.area = serializer.validated_data["area"]
                
                product.save()

                area_ids = request.data.get("areas", [])
                product.areas.set(area_ids)

                serializer = ProductSerializer(product, context={"request": request})
                return Response(None, status.HTTP_204_NO_CONTENT)

            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
            self.check_object_permissions(request, product)
            product.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
