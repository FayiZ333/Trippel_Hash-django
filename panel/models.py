from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.fields import CharField, DateField, TextField, TimeField
from django.urls import reverse


# Create your models here.

class myaccount(BaseUserManager):
    def create_user(self, email, username, phone, password=None, profile_img=None):
        if not email:
            raise ValueError("Users must have an email id")
        if not username:
            raise ValueError("Users must have an username")
        if not phone:
            raise ValueError("Users must have an phone No")

        user  = self.model(
                email=self.normalize_email(email),
                username=username,
                phone=phone,
                profile_img=profile_img,
            )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user  = self.model(
                email=self.normalize_email(email),
                password=password,
                username=username,
            )
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user




class custom(AbstractBaseUser):
    email               = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username            = models.CharField(max_length=33, unique=True)
    phone               = models.CharField(max_length=15)
    gender              = models.CharField(max_length=10,null=True)
    address             = models.TextField(max_length=333,null=True)
    country             = models.CharField(max_length=33,null=True)
    state               = models.CharField(max_length=33,null=True)
    district            = models.CharField(max_length=33, null=True)
    date_joined         = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login          = models.DateTimeField(verbose_name='last login',auto_now=True)
    is_admin            = models.BooleanField(default=False)
    is_active           = models.BooleanField(default=True)
    is_staff            = models.BooleanField(default=False)
    is_superuser        = models.BooleanField(default=False)
    profile_img         = models.ImageField( blank=True, upload_to='profile',null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = myaccount()

    def __str__(self):
        return self.email 

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_Label):
        return True

        
# models of prodects
#####################


class Catagory(models.Model):
    cat_name            = models.CharField(max_length=333, unique=True)
    cat_img             = models.ImageField(upload_to='fz/projects/img 1/prodect', blank=True)
    cat_slug            = models.SlugField(max_length=303,unique=True)
    cat_discription     = models.TextField(max_length=333, blank=TextField)
    cat_date            = models.CharField(max_length=333)


    def get_url(self):
        return reverse('cat_pro',args=[self.cat_slug])

    def __str__(self):
       return self.cat_name


class Brand(models.Model):
    brand_name            = models.CharField(max_length=333, unique=True)
    brand_img             = models.ImageField(upload_to='fz/projects/img 1/brand', blank=True)
    brand_discription     = models.TextField(max_length=333, blank=TextField)
    brand_date            = models.DateField(auto_now_add=True)

    def __str__(self):
       return self.brand_name

class Prodect(models.Model):
    img1                = models.ImageField(upload_to='fz/projects/img 1/prodect')
    img2                = models.ImageField(upload_to='fz/projects/img 1/prodect')
    img3                = models.ImageField(upload_to='fz/projects/img 1/prodect')
    brand               = models.CharField(max_length=33)
    prodectname         = models.CharField(max_length=33)
    gender              = models.CharField(max_length=33, default="Men")
    catagory            = models.ForeignKey(Catagory, on_delete=models.CASCADE)
    price               = models.IntegerField()
    actual_price        = models.IntegerField(null=True)
    offer               = models.IntegerField(null=True)
    model_no            = models.CharField(max_length=33, unique=True)
    stock               = models.IntegerField(default=0)
    slug                = models.SlugField(max_length=303,unique=True)
    discription         = models.TextField()
    date                = models.DateTimeField(auto_now_add=True)
    is_available        = models.BooleanField(default=True)
    modified_date       = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('single',args=[self.catagory.cat_slug, self.slug])

    def __str__(self):
        return self.prodectname



class ReviewRating(models.Model):
    prodect = models.ForeignKey(Prodect, on_delete=models.CASCADE)
    user = models.ForeignKey(custom, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


    def __str__(self) :
        return self.subject
