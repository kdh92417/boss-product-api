from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models, transaction


class UserManager(BaseUserManager):
    def create_user(self, phone_number=None, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("phone_number is not provided")

        if not password:
            raise ValueError("password is not provided")

        with transaction.atomic():
            user = self.model(phone_number=phone_number, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    phone_number = models.CharField("핸드폰 번호", max_length=255, unique=True)

    objects = UserManager()

    USERNAME_FIELD = "phone_number"

    class Meta:
        verbose_name = verbose_name_plural = "사장님"
