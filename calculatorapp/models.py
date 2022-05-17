from django.db import models
import re


class Calculation(models.Model):
    calc_values = models.CharField(max_length=255, default='null')
    calc_results = models.CharField(max_length=255, default='null')
    created_at = models.DateTimeField(auto_now_add = True)
