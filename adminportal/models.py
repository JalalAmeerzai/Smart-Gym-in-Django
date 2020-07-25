from django.db import models

# Create your models here.
class AdminData(models.Model):
    admin_id = models.CharField(max_length=500, primary_key=True, default="")
    admin_name = models.CharField(max_length=500, default="")
    admin_email = models.CharField(max_length=500, unique=True, default="")
    admin_password = models.CharField(max_length=500, default="admin5003")
    admin_contact = models.CharField(max_length=500, default="")
    admin_address = models.CharField(max_length=500, default="")
    admin_dob = models.CharField(max_length=500, default="")
    admin_status = models.CharField(max_length=500, default="Active")
    admin_role = models.CharField(max_length=500, default="Admin")
    admin_img_name = models.CharField(max_length=500, default="adm.jpg")
    admin_added_by = models.CharField(max_length=500, default="")
    admin_added_on = models.CharField(max_length=500, default="")


class TrainerData(models.Model):
    trainer_id = models.CharField(max_length=500, primary_key=True, default="")
    trainer_name = models.CharField(max_length=500, default="")
    trainer_email = models.CharField(max_length=500, unique=True, default="")
    trainer_about = models.CharField(max_length=500, default="")
    trainer_img_name = models.CharField(max_length=500, default="tr.jpg")
    trainer_contact = models.CharField(max_length=500, default="")
    trainer_address = models.CharField(max_length=500, default="")
    trainer_dob = models.CharField(max_length=500, default="")
    trainer_height = models.CharField(max_length=500, default="")
    trainer_weight = models.CharField(max_length=500, default="")
    trainer_fb = models.CharField(max_length=500, default="")
    trainer_ig = models.CharField(max_length=500, default="")
    trainer_status = models.CharField(max_length=500, default="Active")
    trainer_added_by = models.CharField(max_length=500, default="")
    trainer_added_on = models.CharField(max_length=500, default="")



class PackageData(models.Model):
    package_id = models.CharField(max_length=500, primary_key=True, default="")
    package_name = models.CharField(max_length=500, default="", unique=True)
    package_desc = models.CharField(max_length=500, default="")
    package_features = models.TextField(default="")
    package_price = models.IntegerField(max_length=500, default=0)
    package_admission = models.IntegerField(max_length=500, default=0)
    package_added_by = models.CharField(max_length=500, default="")
    package_added_on = models.CharField(max_length=500, default="")



class EquipmentData(models.Model):
    equipment_id = models.CharField(max_length=500, primary_key=True, default="")
    equipment_name = models.CharField(max_length=500, default="")
    equipment_brand = models.CharField(max_length=500, default="")
    equipment_quantity = models.IntegerField(max_length=500, default=0)
    equipment_price = models.IntegerField(max_length=500, default=0)
    equipment_total = models.IntegerField(max_length=500, default=0)
    equipment_added_by = models.CharField(max_length=500, default="")
    equipment_added_on = models.CharField(max_length=500, default="")


class ClassData(models.Model):
    class_id = models.CharField(max_length=500, primary_key=True, default="")
    class_name = models.CharField(max_length=500, default="")
    class_desc = models.CharField(max_length=500, default="")
    class_img_name = models.CharField(max_length=500, default="cls.jpg")
    class_days = models.CharField(max_length=500, default="")
    class_stime = models.CharField(max_length=500, default="")
    class_etime = models.CharField(max_length=500, default="")
    class_trainer = models.CharField(max_length=500, default="")
    class_added_by = models.CharField(max_length=500, default="")
    class_added_on = models.CharField(max_length=500, default="")


class ExpenseData(models.Model):
    class Meta:
        unique_together = (('expense_name', 'expense_month', 'expense_year'),)

    expense_id = models.CharField(max_length=500, primary_key=True, default="")
    expense_name = models.CharField(max_length=500, default="")
    expense_price = models.IntegerField(max_length=500, default=0)
    expense_month = models.CharField(max_length=500, default="")
    expense_year = models.IntegerField(max_length=500, default=0)
    expense_added_by = models.CharField(max_length=500, default="")
    expense_added_on = models.CharField(max_length=500, default="")


class ExerciseData(models.Model):
    exercise_id = models.CharField(max_length=500, primary_key=True, default="")
    exercise_name = models.CharField(max_length=500, default="")
    exercise_desc = models.CharField(max_length=500, default="")
    exercise_img_name = models.CharField(max_length=500, default="exr.jpg")
    exercise_equipment = models.CharField(max_length=500, default="")
    exercise_muscle = models.CharField(max_length=500, default="")
    exercise_sets = models.CharField(max_length=500, default="")
    exercise_tutorial = models.CharField(max_length=500, default="")
    exercise_added_by = models.CharField(max_length=500, default="")
    exercise_added_on = models.CharField(max_length=500, default="")


class DietData(models.Model):
    diet_id = models.CharField(max_length=500, primary_key=True, default="")
    diet_name = models.CharField(max_length=500, default="")
    diet_desc = models.CharField(max_length=500, default="")
    diet_json = models.TextField(default="")
    diet_added_by = models.CharField(max_length=500, default="")
    diet_added_on = models.CharField(max_length=500, default="")


class RoutineData(models.Model):
    routine_id = models.CharField(max_length=500, primary_key=True, default="")
    routine_name = models.CharField(max_length=500, default="")
    routine_img_name = models.CharField(max_length=500, default="rt.jpg")
    routine_desc = models.CharField(max_length=500, default="")
    routine_json = models.TextField(default="")
    routine_added_by = models.CharField(max_length=500, default="")
    routine_added_on = models.CharField(max_length=500, default="")


class MemberData(models.Model):
    member_id = models.CharField(max_length=500, primary_key=True, default="")
    member_package = models.CharField(max_length=500, default="pkg")
    member_img_name = models.CharField(max_length=500, default="mem.jpg")
    member_name = models.CharField(max_length=500, default="")
    member_email = models.CharField(max_length=500, unique=True, default="")
    member_password = models.CharField(max_length=500, default="admin5003")
    member_contact = models.CharField(max_length=500, default="")
    member_address = models.CharField(max_length=500, default="")
    member_dob = models.CharField(max_length=500, default="")
    member_height = models.CharField(max_length=500, default="")
    member_weight = models.CharField(max_length=500, default="")
    member_routine = models.CharField(max_length=500, default="rtn")
    member_diet = models.CharField(max_length=500, default="dt")
    member_status = models.CharField(max_length=500, default="Active")
    member_added_by = models.CharField(max_length=500, default="")
    member_added_on = models.CharField(max_length=500, default="")




class MessageData(models.Model):
    msg_id = models.AutoField(primary_key=True)
    msg_sender_name = models.CharField(max_length=500, default="")
    msg_sender_email = models.CharField(max_length=500, default="")
    msg_sender_time = models.CharField(max_length=500, default="")
    msg_sender_date = models.CharField(max_length=500, default="")
    msg_sender_subject = models.CharField(max_length=500, default="")
    msg_sender_mail = models.TextField(default="")


class ArchivedMessageData(models.Model):
    msg_id = models.AutoField(primary_key=True)
    msg_sender_name = models.CharField(max_length=500, default="")
    msg_sender_email = models.CharField(max_length=500, default="")
    msg_sender_time = models.CharField(max_length=500, default="")
    msg_sender_date = models.CharField(max_length=500, default="")
    msg_sender_subject = models.CharField(max_length=500, default="")
    msg_sender_mail = models.TextField(default="")


class ReplyMessageData(models.Model):
    msg_id = models.AutoField(primary_key=True)
    msg_sender_name = models.CharField(max_length=500, default="")
    msg_sender_email = models.CharField(max_length=500, default="")
    msg_sender_time = models.CharField(max_length=500, default="")
    msg_sender_date = models.CharField(max_length=500, default="")
    msg_sender_subject = models.CharField(max_length=500, default="")
    msg_sender_mail = models.TextField(default="")
    msg_reciever_name = models.CharField(max_length=500, default="")
    msg_reciever_email = models.CharField(max_length=500, default="")
    msg_reciever_time = models.CharField(max_length=500, default="")
    msg_reciever_date = models.CharField(max_length=500, default="")
    msg_reciever_mail = models.TextField(default="")