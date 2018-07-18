from rest_framework import serializers
from api.models import Group, User
from api.v1.account.serializers import UserSerializer


class GroupSerializer(serializers.ModelSerializer):
    queryset = User.objects.all()
    users = UserSerializer(queryset, many=True, read_only=True)

    class Meta:
        model = Group
        fields = ('id', 'name', 'created_by', 'created_on', 'users')
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}
        

class MemberSerializer(serializers.Serializer):
    email = serializers.ListField(child = serializers.EmailField(), min_length=1)