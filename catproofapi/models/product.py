from django.db import models



class Product(models.Model):
    
    cat_user = models.ForeignKey("CatUser", on_delete=models.CASCADE, related_name="products")
    title = models.CharField(max_length=25)
    approved = models.BooleanField(default=False)
    publication_date = models.DateField(auto_now_add=True)
    description = models.TextField(max_length=200)
    company = models.CharField(max_length=25)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(max_length=400)
    areas = models.ManyToManyField("Area", through="ProductArea", related_name="products")