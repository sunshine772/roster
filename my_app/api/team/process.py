## /////////////////////////////////////////////////////////////////////////////
## YOU CAN FREELY MODIFY THE CODE BELOW IN ORDER TO COMPLETE THE TASK
## /////////////////////////////////////////////////////////////////////////////

from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from ...models.player import Player
from ...serializers.team import TeamRequirementSerializer, TeamPlayerSerializer

def team_process_handler(request):
    serializer = TeamRequirementSerializer(data=request.data, many=True)
    if not serializer.is_valid():
        errors = serializer.errors
        if isinstance(request.data, list) and isinstance(errors, list):
            for index, item in enumerate(request.data):
                if index < len(errors) and errors[index]:
                    for field, error_list in errors[index].items():
                        if isinstance(error_list, list) and error_list:
                            for error in error_list:
                                if 'is not a valid choice' in str(error):
                                    value = item.get(field, 'unknown')
                                    return Response({"message": f"Invalid value for {field}: {value}"}, status=status.HTTP_400_BAD_REQUEST)
                                elif 'greater than or equal to' in str(error):
                                    value = item.get(field, 'unknown')
                                    return Response({"message": f"Invalid value for {field}: {value}"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Unknown validation error"}, status=status.HTTP_400_BAD_REQUEST)
    
    requirements = serializer.validated_data
    team = []
    used_player_ids = set()
    seen_positions_skills = set()

    with transaction.atomic():
        for req in requirements:
            position = req['position']
            main_skill = req['mainSkill']
            num_players = req['numberOfPlayers']
            key = (position, main_skill)
            if key in seen_positions_skills:
                return Response({"message": f"Duplicate requirement for position: {position} and skill: {main_skill}"}, 
                                status=status.HTTP_400_BAD_REQUEST)
            seen_positions_skills.add(key)

            players = Player.objects.filter(position=position).exclude(id__in=used_player_ids).prefetch_related('player_skills')
            if players.count() < num_players:
                return Response({"message": f"Insufficient number of players for position: {position}"}, 
                                status=status.HTTP_400_BAD_REQUEST)

            player_scores = []
            for player in players:
                skill_value = next((skill.value for skill in player.player_skills.all() if skill.skill == main_skill), None)
                if skill_value is None:
                    skill_value = max((skill.value for skill in player.player_skills.all()), default=0)
                player_scores.append((player, skill_value))

            sorted_players = sorted(player_scores, key=lambda x: x[1], reverse=True)[:num_players]
            selected_players = [p[0] for p in sorted_players]
            team.extend(selected_players)
            used_player_ids.update(p.id for p in selected_players)

    return Response(TeamPlayerSerializer(team, many=True).data)