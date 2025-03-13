from rest_framework import serializers
from ..models.player_skill import PlayerSkill, SkillName

class PlayerSkillSerializer(serializers.ModelSerializer):
    skill = serializers.ChoiceField(choices=SkillName.choices)
    value = serializers.IntegerField()

    class Meta:
        model = PlayerSkill
        fields = ['id', 'skill', 'value', 'player']
        extra_kwargs = {'player': {'write_only': True, 'required': False}}

    def validate_value(self, value):
        if value < 0:
            raise serializers.ValidationError("The value must be greater than or equal to 0.")
        if value > 100:
            raise serializers.ValidationError("The value must be less than or equal to 100.")
        return value