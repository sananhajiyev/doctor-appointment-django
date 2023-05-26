from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, first_name, last_name, password, age, phone_number, gender, **extra_fields):
        if email is None or first_name is None or last_name is None or gender is None:
            raise ValueError(_('There is an empty field'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, age=age, phone_number=phone_number, gender=gender, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_user(self, email, first_name, last_name, password, age, phone_number, gender, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, first_name, last_name, password, age, phone_number, gender, **extra_fields)
    
    def create_superuser(self, email, first_name, last_name, password, age, gender, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is False:
            raise ValueError(_('Superuser must have is_stuff as True'))
        if extra_fields.get('is_superuser') is False:
            raise ValueError(_('Superuser is_superuser as True'))

        return self._create_user(email, first_name, last_name, password, age, '', 'non-binary', **extra_fields)