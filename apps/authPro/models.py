from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):
    def _create_user(self, username, telephone, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        user = self.model(username=username, telephone=telephone, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, telephone, password, **extra_fields):
        extra_fields['is_superuser'] = False
        extra_fields['is_staff'] = False
        return self._create_user(username, telephone, password, **extra_fields)

    def create_superuser(self, username, telephone, password, **extra_fields):
        extra_fields['is_superuser'] = True
        extra_fields['is_staff'] = True
        return self._create_user(username, telephone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    # User
    telephone = models.CharField(max_length=11, unique=True)
    username = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    # 是否活跃
    is_active = models.BooleanField(default=True)
    # 创建时间
    join_date = models.DateTimeField(auto_now_add=True)
    # 是否员工
    is_staff = models.BooleanField(blank=True)

    # 发送邮件
    EMAIL_FIELD = 'email'
    # 创建用户
    USERNAME_FIELD = 'telephone'
    REQUIRED_FIELDS = ['username', 'email']
    # 把UserManages里面内容拿过来
    objects = UserManager()



