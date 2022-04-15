import reversion
from django.contrib.auth.models import AbstractUser


@reversion.register()
class User(AbstractUser):
    def activate(self, method):
        if method == 'POST':
            if self.is_active:
                self.is_active = True
        elif method == 'DELETE':
            if not self.is_active:
                self.is_active = False
        else:
            pass
        self.save()

    def __str__(self) -> str:
        return str(self.id)

    class Meta:
        db_table = 'users'
