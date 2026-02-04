from django.db import models
from django.core.exceptions import ValidationError

class Binder(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

    def clean(self):
        if not self.pk and Binder.objects.count() >= 3:
            raise ValidationError("You can only create a maximum of 3 binders.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class PokemonCard(models.Model):
    binder = models.ForeignKey(Binder, on_delete=models.CASCADE, related_name='cards', null=True, blank=True)
    name = models.CharField(max_length=100)
    card_id = models.CharField(max_length=50, unique=True)
    image_url = models.URLField()
    set_name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name} ({self.set_name})"
