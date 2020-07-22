from django.db import models

# Create your models here.
class AdminData(models.Model):
    admin_id = models.CharField(max_length=10, primary_key=True, default="")
    admin_name = models.CharField(max_length=40, default="")
    admin_email = models.CharField(max_length=40, unique=True, default="")
    admin_password = models.CharField(max_length=200, default="admin123")
    admin_contact = models.CharField(max_length=20, default="")
    admin_address = models.CharField(max_length=100, default="")
    admin_dob = models.CharField(max_length=12, default="")
    admin_status = models.CharField(max_length=10, default="Active")
    admin_role = models.CharField(max_length=10, default="Admin")
    admin_img_name = models.CharField(max_length=10, default="adm.jpg")
    admin_added_by = models.CharField(max_length=10, default="")
    admin_added_on = models.CharField(max_length=12, default="")


class TrainerData(models.Model):
    trainer_id = models.CharField(max_length=10, primary_key=True, default="")
    trainer_name = models.CharField(max_length=40, default="")
    trainer_email = models.CharField(max_length=40, unique=True, default="")
    trainer_about = models.CharField(max_length=200, default="")
    trainer_img_name = models.CharField(max_length=10, default="tr.jpg")
    trainer_contact = models.CharField(max_length=20, default="")
    trainer_address = models.CharField(max_length=100, default="")
    trainer_dob = models.CharField(max_length=12, default="")
    trainer_height = models.CharField(max_length=15, default="")
    trainer_weight = models.CharField(max_length=10, default="")
    trainer_fb = models.CharField(max_length=50, default="")
    trainer_ig = models.CharField(max_length=50, default="")
    trainer_status = models.CharField(max_length=10, default="Active")
    trainer_added_by = models.CharField(max_length=10, default="")
    trainer_added_on = models.CharField(max_length=12, default="")



class PackageData(models.Model):
    package_id = models.CharField(max_length=10, primary_key=True, default="")
    package_name = models.CharField(max_length=40, default="", unique=True)
    package_desc = models.CharField(max_length=200, default="")
    package_features = models.TextField(default="")
    package_price = models.IntegerField(max_length=20, default=0)
    package_added_by = models.CharField(max_length=10, default="")
    package_added_on = models.CharField(max_length=12, default="")



class EquipmentData(models.Model):
    equipment_id = models.CharField(max_length=10, primary_key=True, default="")
    equipment_name = models.CharField(max_length=40, default="")
    equipment_brand = models.CharField(max_length=40, default="")
    equipment_quantity = models.IntegerField(max_length=20, default=0)
    equipment_price = models.IntegerField(max_length=20, default=0)
    equipment_total = models.IntegerField(max_length=20, default=0)
    equipment_added_by = models.CharField(max_length=10, default="")
    equipment_added_on = models.CharField(max_length=12, default="")


class ClassData(models.Model):
    class_id = models.CharField(max_length=10, primary_key=True, default="")
    class_name = models.CharField(max_length=40, default="")
    class_desc = models.CharField(max_length=200, default="")
    class_img_name = models.CharField(max_length=10, default="cls.jpg")
    class_days = models.CharField(max_length=70, default="")
    class_stime = models.CharField(max_length=20, default="")
    class_etime = models.CharField(max_length=20, default="")
    class_trainer = models.CharField(max_length=10, default="")
    class_added_by = models.CharField(max_length=10, default="")
    class_added_on = models.CharField(max_length=12, default="")