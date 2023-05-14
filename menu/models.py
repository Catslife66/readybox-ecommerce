from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet
from django.utils.text import slugify

# Create your models here.
class Cuisine(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title
    
    
class FeatureTag(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class MenuSearchQuerySet(models.QuerySet):
    def search(self, query):
        if query is None or query == '':
            return self.none()
        lookups = Q(title__icontains=query) | Q(feature__title__icontains=query)
        return self.filter(lookups)
    

class MenuManager(models.Manager):
    def get_queryset(self):
        return MenuSearchQuerySet(self.model, using=self._db)
    
    def search(self, query):
        return self.get_queryset().search(query)


class Menu(models.Model):
    DISHTYPE = [
        ('Starter', 'starter'),
        ('Main', 'main'),
        ('Dessert', 'dessert')
    ]
    type = models.CharField(max_length=10, choices=DISHTYPE)
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    image = models.ImageField(upload_to='menu')
    description = models.TextField()
    cuisine = models.ForeignKey(Cuisine, on_delete=models.SET_NULL, null=True)
    feature = models.ManyToManyField(FeatureTag)
    
    objects = MenuManager()

    def __str__(self):
        return self.title
    
    def get_ingredients(self):
        return self.ingredient_set.all()
    
    def get_nutritions(self):
        return self.nutrition_set.all()
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Menu, self).save(*args, **kwargs)


class Serving(models.Model):
    SERVING_OPTIONS = [
        ('SINGLE', '1 adult'),
        ('COUPLE', '2 adults'),
        ('FAMILY', '2 adults & 2 children') ,
        ('BIG_FAMILY', '4 adults')
    ]
    title = models.CharField(max_length=10, choices=SERVING_OPTIONS, default='COUPLE')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='servings')
    price = models.DecimalField(max_digits=5, decimal_places=2)
 

class NutritionOptions(models.TextChoices):
    ENERGYC = 'Energy(kcal)', 'calories'
    ENERGJ = 'Energy(kJ)', 'joules'
    FAT = 'Fat', 'fat'
    CARBOHYDRATE = 'Carbohydrate', 'carbohydrate'
    SUGARS = 'of which sugars', 'sugars'
    PROTEIN = 'Protein', 'protein'
    SALT = 'Salt', 'salt'


class NutriUnitOptions(models.TextChoices):
    KCAL = 'kcal', 'kilocalorie'
    KJ = 'kj', 'kilojoule'
    G = 'g', 'gram'


class Nutrition(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    title = models.CharField(max_length=20, choices=NutritionOptions.choices)
    figure = models.FloatField()
    unit = models.CharField(max_length=5, choices=NutriUnitOptions.choices)
    
    def save(self, *args, **kwargs):
        if self.title == NutritionOptions.ENERGYC:
            self.unit = NutriUnitOptions.KCAL
        elif self.title == NutritionOptions.ENERGJ:
            self.unit = NutriUnitOptions.KJ
        else:
            self.unit = NutriUnitOptions.G
        super().save(*args, **kwargs)


class Ingredient(models.Model):
    menu = models.ManyToManyField(Menu)
    title = models.CharField(max_length=20)
    image = models.ImageField(upload_to='ingredient')

    def __str__(self):
        return self.title
    