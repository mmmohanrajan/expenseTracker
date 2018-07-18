from rest_framework import serializers
from api.models import Group, User, Activity, Account, Comment
from api.v1.account.serializers import UserSerializer


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('id', 'name', 'date', 'description', 'amount', 'gid', 'owner', 'created_by', 'created_on', 'except_users',)
        extra_kwargs = {
                        'created_by': {'default': serializers.CurrentUserDefault()},
                        'owner': {'default': serializers.CurrentUserDefault()}
                    }


class CommentSerializer(serializers.ModelSerializer):
    '''
    '''
    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {
                'created_by': {'default': serializers.CurrentUserDefault()},
            }


class AccountSerializer(serializers.ModelSerializer):
    '''
    '''
    class Meta:
        model = Account
        fields = ('total', 'user', 'group',)
