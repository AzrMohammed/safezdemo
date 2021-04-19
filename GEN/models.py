import inspect
import os
import sys

from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify

from GEN import GEN_Constants

# from django.contrib.postgres.fields import ArrayField
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from GEN import dbconstants,value_constant
from .value_constant import get_string_value_by_user

import element_types

class AppUserType(models.Model):
    name = models.CharField(max_length=200, unique=False)
    code = models.CharField(max_length=200, unique=True)
    pic = models.ImageField(upload_to='profile_pics', blank=True)
    is_available = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(null=True)

    def __str__(self):
        return str(self.name)


class UserProfileInfo(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    app_user_name = models.CharField(max_length=40, unique=False, default=dbconstants.VAL_STR_DEFAULT)
    password = models.CharField(max_length=16, unique=False, default=dbconstants.VAL_STR_DEFAULT)
    gender = models.CharField(max_length=10, unique=False, choices=dbconstants.GENDER_SET, default=dbconstants.GENDER_MALE)
    guardian = models.ForeignKey('self', on_delete=models.CASCADE, null = True, unique= False, related_name="user_guardian",  blank=True)
    age = models.CharField(max_length=2, unique=False, null = True)
    user_m_status = models.CharField(max_length=3, choices=dbconstants.M_STATUS_TYPES, default = dbconstants.M_STATUS_NOT_TESTED)
    app_user_type = models.ForeignKey(AppUserType, on_delete=models.CASCADE, null=True)
    phone_primary = models.CharField(max_length=10, unique=False, default=dbconstants.VAL_STR_DEFAULT)
    phone_secondary = models.CharField(max_length=10, unique=False, default=dbconstants.VAL_STR_DEFAULT)
    location_area = models.CharField(max_length=280, unique=False, default=dbconstants.VAL_STR_DEFAULT)
    location_sublocality = models.CharField(max_length=280, unique=False, default=dbconstants.VAL_STR_DEFAULT)
    location_locality = models.CharField(max_length=280, unique=False, default=dbconstants.VAL_STR_DEFAULT)
    device_token = models.CharField(max_length=250, default=dbconstants.VAL_STR_DEFAULT, null=True)
    symptom_total = models.IntegerField(default=0)
    location_city = models.CharField(max_length=280, unique=False, default=dbconstants.VAL_STR_DEFAULT)
    location_state = models.CharField(max_length=80, unique=False, choices=dbconstants.STATE_LIST, default=dbconstants.STATE_TAMIL_NADU)
    location_pincode = models.CharField(max_length=6, unique=False, default="601201")
    location_latitude = models.CharField(max_length=50, unique=False, default=dbconstants.VAL_STR_DEFAULT, null=True)
    location_longitude = models.CharField(max_length=50, unique=False, default=dbconstants.VAL_STR_DEFAULT, null=True)
    user_language = models.CharField(max_length=3, choices=dbconstants.USER_LANGUAGE, default = dbconstants.USER_LG_ENGLISH)
    user_type = models.CharField(max_length=3, choices=dbconstants.USER_TYPES, default = dbconstants.USER_TYPE_CONSUMER)
    user_status = models.CharField(max_length=2, choices=dbconstants.USER_STATUS, default=dbconstants.USER_STATUS_ACTIVE)
    status = models.CharField(max_length=2, choices=dbconstants.STATUS,  default=dbconstants.STATUS_ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    brand = models.ForeignKey('GEN.BrandBasicInfo', on_delete=models.CASCADE, null=True, blank=True)
    brandbranch = models.ForeignKey('GEN.BrandBranchBasicInfo', on_delete=models.SET_NULL, null=True, blank=True)

    def getUserDisplayName(self):
        return self.user.username

    def __str__(self):
        return str(self.user.username)


class UserLocationLog(models.Model):
    user = models.OneToOneField(UserProfileInfo, on_delete=models.CASCADE)
    landmark_place_google_id = models.TextField(default=dbconstants.VAL_STR_DEFAULT, null=True, blank=True)
    location_latitude = models.CharField(max_length=30, unique=False, default=dbconstants.VAL_STR_DEFAULT)
    location_langitude = models.CharField(max_length=30, unique=False, default=dbconstants.VAL_STR_DEFAULT)
    status = models.CharField(max_length=2, choices=dbconstants.STATUS,  default=dbconstants.STATUS_ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.username)

class BrandBasicInfo(models.Model):

    name = models.CharField(max_length=250, default=dbconstants.VAL_STR_DEFAULT, null=True)
    code = models.CharField(max_length=100, default=dbconstants.VAL_STR_DEFAULT, null=True)
    description = models.TextField(default=dbconstants.VAL_STR_DEFAULT, null=True, blank=True)
    address_text = models.TextField(default=dbconstants.VAL_STR_DEFAULT, null=True, blank=True)
    branch_base_image = models.ImageField(upload_to='brand_images', blank=True)
    # user = models.OneToOneField(UserProfileInfo, on_delete=models.CASCADE)
    location_latitude = models.CharField(max_length=30, unique=False, default=dbconstants.VAL_STR_DEFAULT)
    location_langitude = models.CharField(max_length=30, unique=False, default=dbconstants.VAL_STR_DEFAULT)
    status = models.CharField(max_length=2, choices=dbconstants.STATUS,  default=dbconstants.STATUS_ACTIVE)
    # capacity = models.CharField(max_length=2, choices=dbconstants.STATUS,  default=dbconstants.STATUS_ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)
    is_online = models.BooleanField(default=True)
    is_service_active = models.BooleanField(default=True)
    service_expiry_date = models.DateTimeField(blank=True, null=True)

    def get_is_service_active(self):
        return self.is_service_active

    def get_service_subscription_detials(self):
        return {"is_active":self.is_service_active,"expiratiojn_date":self.service_expiry_date}

    def __str__(self):
        return str(self.name) +" | " + str(self.id)


class ServisableStoreCapacityCriteria(models.Model):
    # brand = models.ForeignKey(BrandBasicInfo, on_delete=models.CASCADE, null=True)
    # brand_branch = models.ForeignKey(BrandBranchBasicInfo, on_delete=models.CASCADE, null=True)
    store_capacity = models.IntegerField(default=GEN_Constants.STORE_CAPCITY_DEF)

class BrandBranchBasicInfo(models.Model):
    brand = models.ForeignKey(BrandBasicInfo, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=250, default=dbconstants.VAL_STR_DEFAULT, null=True)
    description = models.TextField(default=dbconstants.VAL_STR_DEFAULT, null=True, blank=True)
    phone_primary = models.TextField(default=dbconstants.VAL_STR_DEFAULT, null=True, blank=True)
    phone_secondary = models.TextField(default=dbconstants.VAL_STR_DEFAULT, null=True, blank=True)
    address_text = models.TextField(default=dbconstants.VAL_STR_DEFAULT, null=True, blank=True)
    g_address_dump = models.TextField(default=dbconstants.VAL_STR_DEFAULT, null=True, blank=True)
    place_google_id = models.TextField(default=dbconstants.VAL_STR_DEFAULT, null=True, blank=True)
    landmark_place_google_id = models.TextField(default=dbconstants.VAL_STR_DEFAULT, null=True, blank=True)
    branch_base_image = models.ImageField(upload_to='branch_images', blank=True)
    # capacity_criteria = models.OneToOneField(ServisableStoreCapacityCriteria, on_delete=models.CASCADE)
    store_capacity = models.IntegerField(default=GEN_Constants.STORE_CAPCITY_DEF)
    location_latitude = models.CharField(max_length=30, unique=False, default=dbconstants.VAL_STR_DEFAULT)
    location_langitude = models.CharField(max_length=30, unique=False, default=dbconstants.VAL_STR_DEFAULT)
    status = models.CharField(max_length=2, choices=dbconstants.STATUS,  default=dbconstants.STATUS_ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)
    is_online = models.BooleanField(default=True)

    def get_branch_display_details(self):
        return  { "branch_title":self.name, "branch_address":self.description}

    def __str__(self):
        return str(self.name) + " | " + str(self.id)


class ServisableDaysCriteria(models.Model):
    brand = models.ForeignKey(BrandBasicInfo, on_delete=models.CASCADE, null=True, blank=True)
    branch = models.ForeignKey(BrandBranchBasicInfo, on_delete=models.CASCADE, null=True, blank=True)
    service_start_time = models.TimeField(blank=True, null=True)
    service_end_time = models.TimeField(blank=True, null=True)
    day_of_week = models.IntegerField(choices=dbconstants.DAY_OF_WEEK_LIST,  default=dbconstants.DAY_NONE)
    is_available = models.BooleanField(default=True)
    is_online = models.BooleanField(default=True)
    def __str__(self):
        return str(self.branch.id) + " | " + str(self.day_of_week) + " | " + str(self.id)

class BrandBranchServisableCriteria(models.Model):
    brand = models.ForeignKey(BrandBasicInfo, on_delete=models.CASCADE, null=True, blank=True)
    branch = models.ForeignKey(BrandBranchBasicInfo, on_delete=models.CASCADE, null=True, blank=True)


class C19SymptomSet(models.Model):

    # slug = models.SlugField(unique=True, max_length=8)
    name = models.CharField(max_length=50, default=dbconstants.VAL_STR_DEFAULT, null=True)
    name_tamil = models.CharField(max_length=50, default=dbconstants.VAL_STR_DEFAULT, null=True)
    seviarity = models.IntegerField(default=0)
    note = models.CharField(max_length=250)
    # status = models.CharField(max_length=2, choices=dbconstants.STATUS,  default=dbconstants.STATUS_ACTIVE)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)


    def __str__(self):
        return str(self.name)




class UserHealthProfile(models.Model):

    user = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE, null=True)
    symptom = models.ForeignKey(C19SymptomSet, on_delete=models.CASCADE, null=True)
    note = models.CharField(max_length=250, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.note)



class ItemMeasuementUnit(models.Model):

    brand = models.ForeignKey(BrandBasicInfo, on_delete=models.CASCADE, null=True, blank=True)
    # slug = models.SlugField(unique=True, max_length=8)
    name = models.CharField(max_length=50, default=dbconstants.VAL_STR_DEFAULT, null=True)
    note = models.CharField(max_length=250)
    # status = models.CharField(max_length=2, choices=dbconstants.STATUS,  default=dbconstants.STATUS_ACTIVE)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)




    # order = models.ForeignKey(Order, on_delete=models.CASCADE)

class OrderStatus(models.Model):

    name = models.CharField(max_length=200, unique=False)
    code = models.CharField(max_length=200, unique=True)
    sub_text = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    pic = models.ImageField(upload_to='profile_pics', blank=True)
    status_note = models.CharField(max_length=200, unique=False)
    is_available = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(null=True)

    def __str__(self):
            return str(self.name)


class Order(models.Model):

    # slug = models.SlugField(unique=True, max_length=8)
    brand = models.ForeignKey(BrandBasicInfo, on_delete=models.CASCADE, null=True, blank=True)
    branch = models.ForeignKey(BrandBranchBasicInfo, on_delete=models.CASCADE, null=True, blank=True)
    order_id = models.CharField(max_length=15, unique=True)
    order_status = models.ForeignKey(OrderStatus, on_delete=models.SET_NULL, null=True, blank=True)
    user_customer = models.ForeignKey(UserProfileInfo,  related_name='user_customer', on_delete=models.CASCADE)
    # order_create_m
    schedule_requested_time = models.DateTimeField(blank=True, null=True)
    checked_in_time = models.DateTimeField(blank=True, null=True)
    process_intitated_time = models.DateTimeField(blank=True, null=True)
    process_completed_time = models.DateTimeField(blank=True, null=True)
    rejection_reason = models.TextField(default=dbconstants.VAL_STR_DEFAULT, null=True, blank=True)
    # user_delivery_agent = models.ForeignKey(UserProfileInfo, limit_choices_to={'user_type': dbconstants.USER_TYPE_DELIVERY_AGENT},  related_name='user_delivery_agent', on_delete=models.CASCADE)
    delivery_charges = models.FloatField(max_length=5, default=1.0)
    status_note = models.CharField(max_length=200, default=dbconstants.VAL_STR_DEFAULT, null=True)
    order_accepted = models.BooleanField(default=False)
    order_rejected = models.BooleanField(default=False)
    # status = models.CharField(max_length=3, choices=dbconstants.ORDER_STATUS,  default=dbconstants.ORDER_PLACED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_status_title(self):
        status =get_string_value_by_user(value_constant.KEY_D_PENDING_APPROVAL)

        if self.order_status and hasattr(self.order_status, 'code'):
            order_status = self.order_status.code

            if order_status == GEN_Constants.ORDER_STATUS_AGENT_APPROVED:
                status = get_string_value_by_user(value_constant.KEY_D_ORDER_APPROVED)
            elif order_status == GEN_Constants.ORDER_STATUS_INITIATED:
                status = get_string_value_by_user(value_constant.KEY_D_PENDING_APPROVAL)
            elif order_status == GEN_Constants.ORDER_STATUS_AGENT_REJECTED_NO_SLOT:
                status = get_string_value_by_user(value_constant.KEY_D_ORDER_REJECTED)
            elif order_status == GEN_Constants.ORDER_STATUS_AGENT_REJECTED_OTHERS:
                status = get_string_value_by_user(value_constant.KEY_D_ORDER_REJECTED)
            elif order_status == GEN_Constants.ORDER_STATUS_NO_SHOW:
                status = get_string_value_by_user(value_constant.KEY_D_NOT_REACHABLE)
            elif order_status == GEN_Constants.ORDER_STATUS_ONGOING:
                status = get_string_value_by_user(value_constant.KEY_D_ONGOING)
            elif order_status == GEN_Constants.ORDER_STATUS_COMPLETED:
                status = get_string_value_by_user(value_constant.KEY_D_COMPLETED)

        return status

    def get_status_text(self):

        status = get_string_value_by_user(value_constant.KEY_D_PENDING_APPROVAL);
        if self.order_status and hasattr(self.order_status, 'code'):
            order_status = self.order_status.code

            if order_status == GEN_Constants.ORDER_STATUS_AGENT_APPROVED:
                status = get_string_value_by_user(value_constant.KEY_D_SHOW_THE_QR_CODE_CHECK_IN)
            elif order_status == GEN_Constants.ORDER_STATUS_INITIATED:
                status = get_string_value_by_user(value_constant.KEY_D_AGENT_APPROVE)
            elif order_status == GEN_Constants.ORDER_STATUS_AGENT_REJECTED_NO_SLOT:
                status = get_string_value_by_user(value_constant.KEY_D_NO_SLOT_AVAILABLE)
            elif order_status == GEN_Constants.ORDER_STATUS_AGENT_REJECTED_OTHERS:
                status = get_string_value_by_user(value_constant.KEY_D_NOT_OPERATING_REQUESTED_TIME)
            elif order_status == GEN_Constants.ORDER_STATUS_NO_SHOW:
                status = get_string_value_by_user(value_constant.KEY_D_CHECK_IN_APPOINTMENT)
            elif order_status == GEN_Constants.ORDER_STATUS_ONGOING:
                status = get_string_value_by_user(value_constant.KEY_D_APPOINTMENT_MARKED_AS_ONGOING)
            elif order_status == GEN_Constants.ORDER_STATUS_COMPLETED:
                status = get_string_value_by_user(value_constant.KEY_D_BOOKING_MARKED_AS_COMPLETED)

        return status


    def __str__(self):
        return str(self.order_id) +"==="+ str(self.order_status)+"==="+str(self.branch.id)


class ProductCategory(models.Model):
    brand = models.ForeignKey(BrandBasicInfo, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, unique=False)
    name_tamil = models.CharField(max_length=200, unique=False)
    sub_text = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    pic = models.ImageField(upload_to='profile_pics', blank=True)
    status_note = models.CharField(max_length=200, unique=False)
    is_available = models.BooleanField(default=True)
    slug = models.SlugField(null=True)
    has_view = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(ProductCategory, self).save(*args, **kwargs)

    def __str__(self):
            return str(self.name)




class ProductBase(models.Model):
    name = models.CharField(max_length=200, unique=False)
    name_tamil = models.CharField(max_length=200, unique=False)
    sub_text = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    status_note = models.CharField(max_length=200, unique=False)
    is_available = models.BooleanField(default=True)
    has_view = models.BooleanField(default=True)
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    slug = models.SlugField(null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(ProductBase, self).save(*args, **kwargs)

    def __str__(self):
            return str(self.name)




class Product(models.Model):

    name = models.CharField(max_length=200, unique=False)
    name_tamil = models.CharField(max_length=200, unique=False)
    pic = models.ImageField(upload_to='profile_pics', blank=True)
    is_available = models.BooleanField(default=True)
    price = models.FloatField(default=0, blank=True)
    base_measurement_unit = models.ForeignKey(ItemMeasuementUnit, on_delete=models.CASCADE)
    show_price = models.BooleanField(default=False)
    sub_text = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    priority = models.CharField(max_length=3, choices=dbconstants.PRIORITY_LIST,  default=dbconstants.PRIORIT_05)
    status_note = models.CharField(max_length=200, unique=False)
    status_tamil = models.CharField(max_length=200, unique=False)
    product_base = models.ForeignKey(ProductBase, on_delete=models.CASCADE, unique=False, blank=True)
    measurement_unit = models.ManyToManyField(ItemMeasuementUnit,  related_name='mrp_umo', blank=True)
    slug = models.SlugField(null=True)
    has_view = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
            return str(self.name)


class BranchServisableCategory(models.Model):
    branch = models.ForeignKey(BrandBranchBasicInfo, on_delete=models.CASCADE)
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=dbconstants.STATUS,  default=dbconstants.STATUS_ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)
    is_online = models.BooleanField(default=True)

class BranchServisableProductBase(models.Model):
    product_base = models.ForeignKey(ProductBase, on_delete=models.CASCADE)
    branch = models.ForeignKey(BrandBranchBasicInfo, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=dbconstants.STATUS,  default=dbconstants.STATUS_ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)
    is_online = models.BooleanField(default=True)

class BranchServisableProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    branch = models.ForeignKey(BrandBranchBasicInfo, on_delete=models.CASCADE)
    price = models.FloatField(default=0, blank=True)
    status = models.CharField(max_length=2, choices=dbconstants.STATUS,  default=dbconstants.STATUS_ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)
    is_online = models.BooleanField(default=True)



# class PriceLog(models.Model):
#     slug = models.SlugField(null=True)
#     name = models.CharField(max_length=200, unique=False)
#
#     def save(self, *args, **kwargs):
#         self.slug = slugify(self.name)
#         super(Product, self).save(*args, **kwargs)
#
#     def __str__(self):
#             return str(self.name)


class OrderItem(models.Model):

    # slug = models.SlugField(unique=True, max_length=8)
    order_item_id = models.CharField(max_length=15, unique=True)
    item_name = models.CharField(max_length=60)
    brand = models.ForeignKey(BrandBasicInfo, on_delete=models.CASCADE, null=True, blank=True)
    brand_branch = models.ForeignKey(BrandBranchBasicInfo, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    servisable_product = models.ForeignKey(BranchServisableProduct, on_delete=models.CASCADE, null=True, blank=True)
    item_quantity = models.PositiveSmallIntegerField(default=1)
    item_price = models.FloatField(max_length=5, default=1.0)
    status_note = models.CharField(max_length=200, unique=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    measurement_unit = models.ForeignKey(ItemMeasuementUnit, related_name='measurement_unit', on_delete=models.CASCADE, default="", unique=False)
    status = models.CharField(max_length=3, choices=dbconstants.O_ITEM_STATUS, default=dbconstants.O_ITEM_PLACED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.order_item_id)



class OrderItemLog(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    status = models.CharField(max_length=3, choices=dbconstants.O_ITEM_STATUS, default=dbconstants.O_ITEM_PLACED)
    updated_at = models.DateTimeField(auto_now=True)
    status_note = models.CharField(max_length=200, unique=False)

    def __str__(self):
        return str(self.status)

class OrderLog(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.CharField(max_length=3, choices=dbconstants.ORDER_STATUS,  default=dbconstants.ORDER_PLACED)
    updated_at = models.DateTimeField(auto_now=True)
    status_note = models.CharField(max_length=200, unique=False)

    def __str__(self):
        return str(self.status)


# ==========================================

# ==============
# GEN - CMN
# ==============

# ==============
# ==============

# verbose_name = "Place Holder"
# max_length = "max_length"
# help_text = "Data Type"
# max_length=8, help_text=GEN_Constants.MOD_DT_SLUG, verbose_name="verbose_name1"
# def getName():
#     return  'verbose_name="verbose_name3"';


class CMN_CommunicationVirtualModel(models.Model):

    slug = models.SlugField(max_length=element_types.getMaxLength(element_types.MOD_DT_SLUG), help_text=element_types.getDataType(element_types.MOD_DT_SLUG), verbose_name=element_types.getLabel(element_types.MOD_DT_SLUG), unique=True)
    communication_type = models.CharField(max_length=element_types.getMaxLength(element_types.MOD_DT_CHOICE_LIMITED), help_text=element_types.getDataType(element_types.MOD_DT_CHOICE_LIMITED), verbose_name="Communication Type", choices=GEN_Constants.GEN_COMMUNICATION_TYPES, default=GEN_Constants.PERSONAL)
    is_person = models.BooleanField(help_text=element_types.getDataType(element_types.MOD_DT_BOOL), verbose_name="Is actual person", default=True)
    communication_channel_key = models.CharField(max_length=element_types.getMaxLength(element_types.MOD_DT_CHOICE_LIMITED), help_text=element_types.getDataType(element_types.MOD_DT_CHOICE_LIMITED), verbose_name=element_types.getLabel(element_types.MOD_DT_CHOICE_LIMITED), choices=GEN_Constants.GEN_COMMUNICATION_CHANNEL_TYPES, default=GEN_Constants.PHONE)
    communication_channel_value = models.CharField(max_length=element_types.getMaxLength(element_types.MOD_DT_TEXT), help_text=element_types.getDataType(element_types.MOD_DT_TEXT), verbose_name="Details", null=True)
    # ArrayField(
    #     ArrayField(
    #         models.CharField(max_length=element_types.getMaxLength(element_types.MOD_DT_TEXT), help_text=element_types.getDataType(element_types.MOD_DT_TEXT), verbose_name=element_types.getLabel(element_types.MOD_DT_TEXT), blank=True),
    #         size=8,
    #     ),
    #     help_text=element_types.getDataType(element_types.MOD_DT_TEXT), verbose_name="Communication Channel Value",
    #     size=8, blank=True, null=True
    # )


    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
            return str(self.slug)


class CMN_CommunicationPhysicalModel(models.Model):
    slug = models.SlugField(max_length=element_types.getMaxLength(element_types.MOD_DT_SLUG), help_text=element_types.getDataType(element_types.MOD_DT_SLUG), verbose_name=element_types.getLabel(element_types.MOD_DT_SLUG), unique=True)
    communication_type = models.CharField(max_length=element_types.getMaxLength(element_types.MOD_DT_CHOICE_LIMITED), help_text=element_types.getDataType(element_types.MOD_DT_CHOICE_LIMITED), verbose_name="Communication Type", choices=GEN_Constants.GEN_COMMUNICATION_TYPES, default=GEN_Constants.ENTERPRISE)
    is_person = models.BooleanField(help_text=element_types.getDataType(element_types.MOD_DT_BOOL), verbose_name="Is actual person", default=True)
    address_line_01 = models.CharField(max_length=element_types.getMaxLength(element_types.MOD_DT_TEXT), help_text=element_types.getDataType(element_types.MOD_DT_TEXT), verbose_name="Address Line 1")
    address_line_02 =  models.CharField(max_length=element_types.getMaxLength(element_types.MOD_DT_TEXT), help_text=element_types.getDataType(element_types.MOD_DT_TEXT), verbose_name="Address Line 2")
    city = models.CharField(max_length=element_types.getMaxLength(element_types.MOD_DT_TEXT), help_text=element_types.getDataType(element_types.MOD_DT_TEXT), verbose_name="City")
    district = models.CharField(max_length=element_types.getMaxLength(element_types.MOD_DT_TEXT), help_text=element_types.getDataType(element_types.MOD_DT_TEXT), verbose_name="District")
    state = models.CharField(max_length=element_types.getMaxLength(element_types.MOD_DT_TEXT), help_text=element_types.getDataType(element_types.MOD_DT_TEXT), verbose_name="State")
    country = models.CharField(max_length=element_types.getMaxLength(element_types.MOD_DT_TEXT), help_text=element_types.getDataType(element_types.MOD_DT_TEXT), verbose_name="Country")
    pincode = models.CharField(max_length=element_types.getMaxLength(element_types.MOD_DT_PINCODE), help_text=element_types.getDataType(element_types.MOD_DT_PINCODE), verbose_name="Pincode")

    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
            return str(self.slug)

# ==============
# GEN - EPS
# ==============

class EPS_EnterpriseProfileModel(models.Model):
    slug = models.SlugField(max_length=element_types.getMaxLength(element_types.MOD_DT_SLUG), help_text=element_types.getDataType(element_types.MOD_DT_SLUG), verbose_name=element_types.getLabel(element_types.MOD_DT_SLUG), unique=True)
    name = models.CharField(max_length=element_types.getMaxLength(element_types.MOD_DT_NAME), help_text=element_types.getDataType(element_types.MOD_DT_NAME), verbose_name=element_types.getLabel(element_types.MOD_DT_NAME))
    GST_number = models.CharField(max_length=50, help_text=element_types.getDataType(element_types.MOD_DT_TEXT), verbose_name=element_types.getLabel(element_types.MOD_DT_TEXT))
    PAN_number = models.CharField(max_length=50, help_text=element_types.getDataType(element_types.MOD_DT_TEXT), verbose_name=element_types.getLabel(element_types.MOD_DT_TEXT))
    credit_limit = models.IntegerField( help_text=element_types.getDataType(element_types.MOD_DT_NUMBER), verbose_name=element_types.getLabel(element_types.MOD_DT_NUMBER))

    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
            return str(self.slug)

class EPS_EnterpriseMetaModel(models.Model):
    slug = models.SlugField(unique=True, max_length=8)
    enterprise_profile = models.ForeignKey(EPS_EnterpriseProfileModel, related_name='ep', on_delete=models.CASCADE)
    communication_virtual_slugs = models.ForeignKey(CMN_CommunicationVirtualModel, related_name='ecv', on_delete=models.CASCADE)
    communication_physical = models.ForeignKey(CMN_CommunicationPhysicalModel, related_name='ecp', on_delete=models.CASCADE)
    parent_enterprise_meta = models.ForeignKey('self', on_delete=models.CASCADE)

    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
            return str(self.slug)

# enterprise_profile_slug
# communication_virtual_slugs
# communication_physical_slugs
# parent_enterprise_meta_slug
# contact_person_user_meta_slugs
