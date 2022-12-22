from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
# from django.utils.text import slugify
from geopy import Nominatim
from slugify import slugify


GENDER = [
    ['male', "Мужской"],
    ['female', "Женский"]
]


def user_directory_path1(instance, filename):
    today = datetime.now().date()
    today_path = today.strftime("%Y/%m/%d")
    return f'{instance.author.username}/{today_path}/{filename}'


class Snapshot(models.Model):
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Автор")

    photo = models.FileField(upload_to=user_directory_path1, verbose_name="Фото")
    category = models.ManyToManyField('Category', blank=True, verbose_name="Категория")

    description = models.TextField(max_length=500, null=True, blank=True, verbose_name="Описание")
    person_list = models.CharField(max_length=200, null=True, blank=True, verbose_name="Кто на фото?")
    person = models.ManyToManyField('Person', blank=True, verbose_name="Человек")
    camera = models.ForeignKey('Camera', on_delete=models.PROTECT, verbose_name="Камера")

    city = models.CharField(max_length=30, blank=True, null=True, verbose_name="Город")
    region = models.CharField(max_length=30, blank=True, null=True, verbose_name="Регион")
    country = models.CharField(max_length=30, blank=True, null=True, verbose_name="Страна")

    lon = models.DecimalField(max_digits=9, decimal_places=6, default=0, verbose_name="Longitude")
    lat = models.DecimalField(max_digits=9, decimal_places=6, default=0, verbose_name="Latitude")

    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата")

    def save(self, *args, **kwargs):
        geolocator = Nominatim(user_agent="thomas")
        location = geolocator.reverse(f'{self.lat}, {self.lon}')
        address = location.raw['address']

        self.city = address.get('city', '')
        self.region = address.get('state', '')
        self.country = address.get('country', '')

        super(Snapshot, self).save(*args, **kwargs)

    def __str__(self):
        lss = self.description.split()[:3]
        return " ".join(lss)

    def get_absolute_url(self):
        return reverse('snap', kwargs={'pk': self.pk})

    def categories(self):
        return "\n".join([c.name+',' for c in self.category.all()])

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фотки'
        ordering = ['-timestamp']


class Category(models.Model):
    name = models.CharField(max_length=20, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, null=True, verbose_name="URL")
    snap_count = models.IntegerField(default=0, verbose_name="Всего фотографий")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.snap_count = Snapshot.objects.filter(category=self).count()
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']


class Person(models.Model):
    name = models.CharField(max_length=30, verbose_name="Имя")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, null=True, verbose_name="URL")
    person_in_snap = models.IntegerField(default=1, verbose_name="Присутствие на фото")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.person_in_snap = Snapshot.objects.filter(person=self).count()
        super(Person, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Человек'
        verbose_name_plural = 'Люди'
        ordering = ['name']


class Camera(models.Model):
    brand = models.CharField(max_length=30, verbose_name="Модель камеры")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, blank=True, null=True, verbose_name="URL")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.brand)
        super(Camera, self).save(*args, **kwargs)

    def __str__(self):
        return self.brand

    class Meta:
        verbose_name = 'Камера'
        verbose_name_plural = 'Камеры'
        ordering = ['brand']


def user_directory_path(instance, filename):
    return f'{instance.user.username}/avatar/{filename}'


class Profile(models.Model):
    """ ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")

    nick = models.CharField(max_length=30, blank=True, null=True, verbose_name="Ник")
    avatar = models.FileField(upload_to=user_directory_path, null=True, blank=True, verbose_name="Аватар")
    fio = models.CharField(max_length=50, blank=True, null=True, verbose_name="ФИО")
    city = models.CharField(max_length=30, blank=True, null=True, verbose_name="Город")

    cameras = models.CharField(max_length=200, null=True, blank=True, verbose_name="Камеры")
    gear = models.ManyToManyField(Camera, blank=True, verbose_name="Камера")

    gender = models.CharField(max_length=10, null=True, verbose_name="Пол", choices=GENDER, default="male")
    contacts = models.CharField(max_length=20, blank=True, null=True, verbose_name="Контакты")
    private = models.BooleanField(default=False)

    skill = models.CharField(max_length=50, blank=True, null=True, verbose_name="Скилл")

    def save(self, *args, **kwargs):
        snaps = Snapshot.objects.filter(author=self.user).count()
        if not snaps or snaps < 5:
            self.skill = 'Новичок'
        elif 5 <= snaps < 10:
            self.skill = 'Любитель'
        elif 10 <= snaps < 15:
            self.skill = 'Полупрофессионал'
        elif 15 <= snaps < 20:
            self.skill = 'Профи'
        else:
            self.skill = 'Легенда'

        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return self.nick

    def get_absolute_url(self):
        return reverse('profile', kwargs={'nick': self.nick})

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        ordering = ['id']


class Comment(models.Model):
    datetime = models.DateTimeField(verbose_name="Дата", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор", related_name="comments")
    post = models.ForeignKey(Snapshot, on_delete=models.CASCADE, verbose_name="Пост", related_name="comments")
    text = models.TextField(max_length=1000, null=True, blank=True, verbose_name="Текст")

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ["datetime"]


class SubList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user")
    subscriptions = models.ManyToManyField(Profile, blank=True, related_name="subscriptions")
    categories = models.ManyToManyField(Category, blank=True, related_name="cat_subs")
    cameras = models.ManyToManyField(Camera, blank=True, related_name="cam_subs")

    def __str__(self):
        return self.user.profile.nick + "'s subscriptions"

    def subscribe(self, profile):
        if not profile in self.subscriptions.all():
            self.subscriptions.add(profile)

    def unsubscribe(self, profile=None, category=None):
        if profile:
            if profile in self.subscriptions.all():
                self.subscriptions.remove(profile)
        if category:  # еще камеры
            if category in self.categories.all():
                self.categories.remove(category)

    def cancel_subscription(self, profile=None, category=None):
        subs = self
        if profile:
            subs.unsubscribe(profile)
        elif category:
            subs.unsubscribe(category)

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

