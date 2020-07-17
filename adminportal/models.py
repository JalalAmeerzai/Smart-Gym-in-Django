from django.db import models

# Create your models here.
class AdminData(models.Model):
    admin_id = models.CharField(max_length=10, primary_key=True, default="")
    admin_name = models.CharField(max_length=40, default="")
    admin_email = models.CharField(max_length=40, unique=True, default="")
    admin_contact = models.CharField(max_length=20, default="")
    admin_address = models.CharField(max_length=100, default="")
    admin_dob = models.CharField(max_length=12, default="")
    admin_status = models.CharField(max_length=10, default="Active")
    admin_role = models.CharField(max_length=10, default="Admin")
    admin_img_name = models.CharField(max_length=10, default="adm.jpg")
    admin_added_by = models.CharField(max_length=10, default="")
    admin_added_on = models.CharField(max_length=12, default="")