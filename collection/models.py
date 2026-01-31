from django.db import models

class Binder(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class PokemonCard(models.Model):
    binder = models.ForeignKey(Binder, on_delete=models.CASCADE, related_name='cards', null=True, blank=True)
    name = models.CharField(max_length=100)
    card_id = models.CharField(max_length=50, unique=True)
    image_url = models.URLField()
    set_name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name} ({self.set_name})"
