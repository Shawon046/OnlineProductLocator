from django.db import models

# Create your models here.

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.OneToOneField(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


#our models start here

class Shop(models.Model):
    ShopID = models.AutoField(primary_key=True)
    ShopName = models.CharField(max_length=45)
    UserName = models.CharField(max_length=45)
    Location = models.CharField(max_length=45)
    Latitude = models.FloatField()
    Longitude = models.FloatField()
    ContactNumber = models.CharField(max_length=11)
    Email = models.EmailField()
        #CharField(max_length=45)

    def __str__(self):
        return self.ShopName

    class Meta:
        managed = False
        db_table = 'shop'



class Discount(models.Model):
    DiscountID = models.AutoField(primary_key=True)
    Percentage = models.FloatField()
    DiscountAmount = models.FloatField()
    MaxAmount = models.IntegerField()

    def __str__(self):
        if self.DiscountAmount is None or self.DiscountAmount==0:
            return str(self.Percentage)+' Percent''(Max '+str(self.MaxAmount)+')'
        else:
            return str(self.DiscountAmount)+' Total'

    class Meta:
        managed = False
        db_table = 'discount'





class Product(models.Model):
    ProductID = models.AutoField(primary_key=True)
    ProductName = models.CharField(max_length=45)  # Field name made lowercase.
    BuyingPrice = models.FloatField()  # Field name made lowercase.
    SellingPrice = models.FloatField()  # Field name made lowercase.
    shop = models.ForeignKey(Shop, models.DO_NOTHING)
    Quantity = models.IntegerField()
    discount = models.ForeignKey(Discount, models.DO_NOTHING, null=True)
    image = models.ImageField(max_length=1000, blank=True, null=True)
    Mfg = models.DateField()
    Exp = models.DateField()

    def __str__(self):
        return self.ProductName

    class Meta:
        managed = False
        db_table = 'product'





class Log(models.Model):
    LogID = models.AutoField(primary_key=True)  # Field name made lowercase.
    product = models.ForeignKey(Product, models.DO_NOTHING)
    shop = models.ForeignKey(Shop, models.DO_NOTHING)
    Time = models.DateTimeField(auto_now=True)
    Buyer_Name = models.CharField(max_length=45)
    Buyer_Mobile_No = models.CharField(max_length=45)
    Net_Price = models.FloatField()
    Profit = models.FloatField()
    Buyer_Email = models.EmailField()#CharField(max_length=45)
    No_of_prods = models.IntegerField()

    def __str__(self):
        return self.shop.ShopName + ' ' + self.product.ProductName +' ' + self.Buyer_Name

    class Meta:
        managed = False
        db_table = 'log'



class User(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Shop, models.DO_NOTHING)
    username = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    Mobile = models.CharField(max_length=11)
    status = models.CharField(max_length=10)

    def __str__(self):
        return self.username + self.user.ShopName

    class Meta:
        managed = False
        db_table = 'user'


