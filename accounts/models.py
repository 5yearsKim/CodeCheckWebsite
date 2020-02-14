from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password, is_password_usable


class MyUserManager(BaseUserManager):
    def create_user(self, student_id, nickname, password=None):
        """
        Creates and saves a User with the student_id, nickname
        """
        if not student_id:
            raise ValueError('Users must have an student_id')

        user = self.model(
            student_id=student_id,
            nickname=nickname,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, student_id, nickname, password=None):
        """
        Creates and saves a superuser with the given student_id, nickname, password.
        """
        user = self.create_user(
            student_id=student_id,
            nickname=nickname,
        )
        user.set_password(password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    student_id = models.CharField(
        max_length=10,
        primary_key=True,
    )
    nickname = models.CharField(
        max_length=20,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    total_score = models.FloatField(default=0.)

    objects = MyUserManager()

    USERNAME_FIELD = 'student_id'
    REQUIRED_FIELDS = ['nickname']

    def __str__(self):
        return self.nickname

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

@receiver(pre_save, sender=MyUser)
def password_hashing(instance, **kwargs):
    if not is_password_usable(instance.password):
        instance.password = make_password(instance.password)
