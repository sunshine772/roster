## /////////////////////////////////////////////////////////////////////////////
## PLEASE DO NOT RENAME OR REMOVE ANY OF THE CODE BELOW. 
## YOU CAN ADD YOUR CODE TO THIS FILE TO EXTEND THE FEATURES TO USE THEM IN YOUR WORK.
## /////////////////////////////////////////////////////////////////////////////

from django.db import models
from .player import Player

class SkillName(models.TextChoices):
    DEFENSE = 'defense', 'Defense'
    ATTACK = 'attack', 'Attack'
    SPEED = 'speed', 'Speed'
    STRENGTH = 'strength', 'Strength'
    STAMINA = 'stamina', 'Stamina'

class PlayerSkill(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_skills')
    skill = models.CharField(max_length=20, choices=SkillName.choices)
    value = models.IntegerField()

    def __str__(self):
        return f"{self.player.name} - {self.skill}: {self.value}"