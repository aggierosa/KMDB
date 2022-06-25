from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):    
    def _create_user(self, email, first_name, last_name, password, is_staff ,is_superuser, **extra_fields):
        if not email:
            raise ValueError("Informe um email")
        
        email = self.normalize_email(email)

        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_staff=is_staff, 
            is_superuser=is_superuser, 
            **extra_fields
            )

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_user(self, email, first_name, last_name, password, **extra_fields):
        return self._create_user(email=email, first_name=first_name, last_name=last_name, password=password, is_staff=True, is_superuser=True, **extra_fields)

    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        return self._create_user(email=email, first_name=first_name, last_name=last_name, password=password, is_staff=True, is_superuser=True, **extra_fields)

