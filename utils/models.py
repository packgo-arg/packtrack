from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator
from tasks.services import LocationService
import uuid


# Create your models here.

class Package(models.Model):
    
    PACKAGE_FIXED = ( 
    (0, "Fixed"), 
    (1, "Variable"), 
)
    pkg_name = models.CharField(max_length=20, unique=True)
    pkg_code = models.CharField(max_length=2, unique=True)
    pkg_description = models.CharField(max_length=100, null=True, blank=True)
    pkg_fixed = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1)])
    height = models.FloatField(default=0, validators=[MinValueValidator(0)])
    width = models.FloatField(default=0, validators=[MinValueValidator(0)])
    length = models.FloatField(default=0, validators=[MinValueValidator(0)])
    volume = models.FloatField(default=0, validators=[MinValueValidator(0)])
    weight = models.FloatField(default=0, validators=[MinValueValidator(0)])
    pkg_coef = models.FloatField(default=0, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pkg_name
    
    def save(self, *args, **kwargs):
        if (self.height != 0) and (self.width != 0) and (self.length != 0):
            self.volume = self.height * self.width * self.length

        super(Package, self).save(*args, **kwargs)


class Status(models.Model):
    status_name = models.CharField(max_length=50, unique=True)
    status_desc = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status_name


class State(models.Model):
    city = models.CharField(max_length=50, unique=True, null=True)
    province = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=50, null=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    mpoly = models.MultiPolygonField(default='SRID=4326;MULTIPOLYGON (((0 0, 0 1, 1 1, 1 0, 0 0)))')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.city

    def save(self, *args, **kwargs):

        req = LocationService.getLocal('localidades_censales', [dict(nombre=self.city, provincia=self.province)])

        self.city = req.get('nombre')
        self.province = req.get('provincia').get('nombre')
        self.country = 'Argentina'
        self.latitude = req.get('centroide').get('lat')
        self.longitude = req.get('centroide').get('lon')

        super(State, self).save(*args, **kwargs)


class Provider(models.Model):
    # required fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    users = models.ManyToManyField(User)
    prov_name = models.CharField(max_length=20, unique=True)
    prov_code = models.CharField(max_length=2, unique=True)
    state_code = models.ForeignKey(State, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """A string representation of the model."""
        return self.prov_name
    
    def get_packgo():
        """Get packgo object
        Returns:
            object: Pack Go provider object
        """
        return Provider.objects.get(prov_name='Pack GO').id


class Driver(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    driv_name = models.CharField(max_length=20, unique=True)
    vehicle_type = models.CharField(max_length=20)
    vehicle_brand = models.CharField(max_length=30, null=True, blank=True)
    vehicle_model = models.CharField(max_length=30, null=True, blank=True)
    vehicle_year = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(2999)])
    vehicle_plate = models.CharField(max_length=20, unique=True)
    vehicle_capacity = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(200)])
    prov_code = models.ForeignKey(Provider, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """A string representation of the model."""
        return self.driv_name


class Client(models.Model):
    # required fields
    PRICE_CALC = ( 
    (0, "Variable"), 
    (1, "Fixed"), 
)
    PACKAGE_CAPACITY = ( 
    (0, "Volume"), 
    (1, "Weight"), 
)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    users = models.ManyToManyField(User)
    client_name = models.CharField(max_length=20, unique=True)
    client_code = models.CharField(max_length=2, unique=True)
    state_code = models.ForeignKey(State, on_delete=models.CASCADE, null=True)
    price_calc = models.PositiveIntegerField(default=0, choices=PRICE_CALC)
    unit_type = models.PositiveIntegerField(default=0, choices=PACKAGE_CAPACITY)
    base_price = models.FloatField(default=0, validators=[MinValueValidator(0)])
    unit_price = models.FloatField(default=0, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """A string representation of the model."""
        return self.client_name


class MyAccountManager(BaseUserManager):

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have email address')
        if not username:
            raise ValueError('Users must have username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user


class Account(AbstractBaseUser):

    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True