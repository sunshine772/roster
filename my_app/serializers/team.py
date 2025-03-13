from rest_framework import serializers
from ..models.player import Player, Position
from ..models.player_skill import SkillName

class TeamRequirementSerializer(serializers.Serializer):
    position = serializers.ChoiceField(choices=Position.choices)
    mainSkill = serializers.ChoiceField(choices=SkillName.choices)
    numberOfPlayers = serializers.IntegerField(min_value=1)

class TeamPlayerSerializer(serializers.ModelSerializer):
    position = serializers.ChoiceField(choices=Position.choices)
    playerSkills = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = ['name', 'position', 'playerSkills']

    def get_playerSkills(self, obj):
        return [{'skill': skill.skill, 'value': skill.value} for skill in obj.player_skills.all()]