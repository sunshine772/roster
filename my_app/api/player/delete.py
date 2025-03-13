## /////////////////////////////////////////////////////////////////////////////
## YOU CAN FREELY MODIFY THE CODE BELOW IN ORDER TO COMPLETE THE TASK
## /////////////////////////////////////////////////////////////////////////////

from rest_framework.response import Response
from rest_framework import status
from ...models.player import Player
from ...serializers.player import PlayerSerializer

DELETE_TOKEN = "SkFabTZibXE1aE14ckpQUUxHc2dnQ2RzdlFRTTM2NFE2cGI4d3RQNjZmdEFITmdBQkE="

def delete_player_handler(request, id):
    auth_header = request.headers.get('Authorization')
    if auth_header != f"Bearer {DELETE_TOKEN}":
        return Response({"message": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
    try:
        player = Player.objects.get(id=id)
        serializer = PlayerSerializer(player)
        data = serializer.data
        player.delete()
        return Response(data, status=status.HTTP_200_OK)
    except Player.DoesNotExist:
        return Response({"message": f"Resource not found for id: {id}"}, status=status.HTTP_404_NOT_FOUND)