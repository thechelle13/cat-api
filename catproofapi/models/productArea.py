from django.db import models

class ProductArea(models.Model):
    """Database model for tracking events"""

    area = models.ForeignKey("Area", on_delete=models.CASCADE, related_name="product_areas")
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="product_areas" )