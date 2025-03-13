from rest_framework import serializers
from ..models.player import Player, Position
from ..models.player_skill import PlayerSkill
from .player_skill import PlayerSkillSerializer

class PlayerSerializer(serializers.ModelSerializer):
    position = serializers.ChoiceField(choices=Position.choices)
    playerSkills = PlayerSkillSerializer(many=True, source='player_skills')

    class Meta:
        model = Player
        fields = ['id', 'name', 'position', 'playerSkills']

    def validate(self, data):
        player_skills = data.get('player_skills')
        if not player_skills:
            raise serializers.ValidationError("Player must have at least one skill")
        seen = set()
        for skill in player_skills:
            s = skill.get('skill')
            if s in seen:
                raise serializers.ValidationError(f"Duplicate skill: {s}")
            seen.add(s)
        return data

    def create(self, validated_data):
        skills_data = validated_data.pop('player_skills')
        player = Player.objects.create(**validated_data)
        PlayerSkill.objects.bulk_create([PlayerSkill(player=player, **skill) for skill in skills_data])
        return player

    def update(self, instance, validated_data):
        skills_data = validated_data.pop('player_skills')
        instance.name = validated_data.get('name', instance.name)
        instance.position = validated_data.get('position', instance.position)
        instance.save()
        instance.player_skills.all().delete()
        PlayerSkill.objects.bulk_create([PlayerSkill(player=instance, **skill) for skill in skills_data])
        return instance