## /////////////////////////////////////////////////////////////////////////////
## YOU CAN FREELY MODIFY THE CODE BELOW IN ORDER TO COMPLETE THE TASK
## /////////////////////////////////////////////////////////////////////////////

from rest_framework.response import Response
from rest_framework import status
from ...serializers.player import PlayerSerializer

def create_player_handler(request):
    serializer = PlayerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    errors = serializer.errors
    if isinstance(errors, dict):
        for field, error_list in errors.items():
            if field != 'playerSkills' and isinstance(error_list, list) and error_list:
                for error in error_list:
                    if 'Duplicate skill' in str(error) or 'at least one skill' in str(error):
                        return Response({"message": str(error)}, status=status.HTTP_400_BAD_REQUEST)
                    elif 'is not a valid choice' in str(error):
                        value = request.data.get(field, 'unknown')
                        return Response({"message": f"Invalid value for {field}: {value}"}, status=status.HTTP_400_BAD_REQUEST)
            elif field == 'playerSkills' and isinstance(error_list, list):
                for index, error in enumerate(error_list):
                    if isinstance(error, dict):
                        for sub_field, sub_error_list in error.items():
                            if isinstance(sub_error_list, list) and sub_error_list:
                                for sub_error in sub_error_list:
                                    if 'is not a valid choice' in str(sub_error):
                                        skills = request.data.get('playerSkills', [])
                                        value = skills[index].get(sub_field, 'unknown') if index < len(skills) else 'unknown'
                                        return Response({"message": f"Invalid value for {sub_field}: {value}"}, status=status.HTTP_400_BAD_REQUEST)
                                    elif 'greater than or equal to' in str(sub_error) or 'less than or equal to' in str(sub_error):
                                        skills = request.data.get('playerSkills', [])
                                        value = skills[index].get(sub_field, 'unknown') if index < len(skills) else 'unknown'
                                        return Response({"message": f"Invalid value for {sub_field}: {value}"}, status=status.HTTP_400_BAD_REQUEST)
                    elif isinstance(error, str) and ('Duplicate skill' in error or 'at least one skill' in error):
                        return Response({"message": str(error)}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "Unknown validation error"}, status=status.HTTP_400_BAD_REQUEST)