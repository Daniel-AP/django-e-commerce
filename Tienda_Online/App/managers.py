from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self,username,email,password,**extra):

        email = self.normalize_email(email)
        user = self.model(username=username,email=email,**extra)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self,username,email,password,**extra):

        extra.setdefault('is_staff', True)
        extra.setdefault('is_superuser', True)
        extra.setdefault('is_active', True)

        return self.create_user(username,email, password, **extra)