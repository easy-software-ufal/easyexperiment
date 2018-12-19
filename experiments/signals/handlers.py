from django.db.models.signals import post_save
from django.dispatch import receiver

from experiments.models import LatinSquare
from experiments.services.generate_latin_square_rows import GenerateLatinSquareRows

@receiver(post_save, sender=LatinSquare)
def my_handler(sender, **kwargs):
  print '========================================================='
  print  "Generating Latin Square to: %s" % kwargs['instance'].experiment
  print '========================================================='

  GenerateLatinSquareRows(kwargs['instance']).call()
