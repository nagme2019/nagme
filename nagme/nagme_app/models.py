import redis
import pytz
import arrow

from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from timezone_field import TimeZoneField
from django.urls import reverse
from django.core.exceptions import ValidationError


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True, primary_key=True)
    top = models.ForeignKey('Nag', on_delete=models.SET_NULL, related_name='top', null=True)  # change the on_delete to the next most liked nag
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'
        app_label = '_nagme'

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    phonenumber = PhoneNumberField(null=False, blank=False, unique=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    isauthor = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        app_label = '_nagme'


class Nag(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='author', null=True)
    text = models.CharField(max_length=140, unique=True)
    likes = models.PositiveIntegerField(default=0)
    subscriber = models.ManyToManyField(User, related_name='subscribe')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        app_label = '_nagme'


class Reminder(models.Model):
    task_id = models.AutoField(primary_key=True)
    name = models.ForeignKey('UserProfile', default='00000', on_delete=models.CASCADE, related_name='subscriber', null=True)
    phonenumber = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='number', null=True)  # this should be automatically set to the user's number
    time = models.DateTimeField()
    time_zone = TimeZoneField(default='GMT')
    text = models.ForeignKey('Nag', null=True, on_delete=models.CASCADE,)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return 'Reminder for' + self.name + ': ' + self.text

    def get_absolute_url(self):
        return reverse('view_reminder', args=[str(self.id)])

    def clean(self):
        """Checks appointments are not scheduled in the past"""
        reminder_time = arrow.get(self.time, self.time_zone.zone)

        if reminder_time < arrow.utcnow():
            raise ValidationError(
                'You cannot schedule an appointment for the past. '
                'Please check your time and time_zone')

    def schedule_reminder(self):
        """Schedule a Dramatiq task to send a reminder for this appointment"""
        # Calculate the correct time to send this reminder
        reminder_time = arrow.get(self.time, self.time_zone.zone)
        now = arrow.now(self.time_zone.zone)
        milli_to_wait = int(
            (reminder_time - now).total_seconds()) * 1000

        # Schedule the Dramatiq task
        from .tasks import send_sms_reminder
        result = send_sms_reminder.send_with_options(
            args=(self.pk,),
            delay=milli_to_wait)

        return result.options['redis_message_id']

    def save(self, *args, **kwargs):
        """Custom save method which also schedules a reminder"""
        self.slug = slugify(self.name)

        # Check if we have scheduled a reminder for this appointment before
        if self.task_id:
            # Revoke that task in case its time has changed
            self.cancel_task()

        # Save our appointment, which populates self.pk,
        # which is used in schedule_reminder
        super(Reminder, self).save(*args, **kwargs)

        # Schedule a new reminder task for this appointment
        self.task_id = self.schedule_reminder()

        # Save our appointment again, with the new task_id
        super(Reminder, self).save(*args, **kwargs)

    def cancel_task(self):
        redis_client = redis.Redis(host='localhost', port=6379, db=0)
        redis_client.hdel("dramatiq:default.DQ.msgs", self.task_id)

    class Meta:
        app_label = '_nagme'
