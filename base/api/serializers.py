from rest_framework.serializers import ModelSerializer
from base.models import Room

# serializer converts our objects into JSON
class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'