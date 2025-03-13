## /////////////////////////////////////////////////////////////////////////////
## PLEASE DO NOT RENAME OR REMOVE ANY OF THE CODE BELOW. 
## YOU CAN ADD YOUR CODE TO THIS FILE TO EXTEND THE FEATURES TO USE THEM IN YOUR WORK.
## /////////////////////////////////////////////////////////////////////////////

from django.db import models

class Position(models.TextChoices):
    DEFENDER = 'defender', 'Defender'
    MIDFIELDER = 'midfielder', 'Midfielder'
    FORWARD = 'forward', 'Forward'

class Player(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=20, choices=Position.choices)

    def __str__(self):
        return self.name