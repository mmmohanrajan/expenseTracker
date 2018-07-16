from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework import serializers

from django.db.models import Q

from api.models import Group, User, Activity, Account
from api.v1.account.serializers import UserSerializer
from api.v1.activity.serializers import ActivitySerializer, AccountSerializer
from api.v1.group.serializers import GroupSerializer, MemberSerializer
from api.permissions import IsOwnerOrReadOnly, IsGroupAccessable


class ActivityViewSet(viewsets.ModelViewSet):
    serializer_class = ActivitySerializer
    permission_classes = (IsOwnerOrReadOnly, IsGroupAccessable)

    def get_queryset(self, pk=None, gid=None):
        user = self.request.user
        if pk:
            return Activity.objects.get(pk=pk)
        if gid:
            return Activity.objects.filter(gid=gid)
        groups = Group.objects.filter(users__in=[user])
        return Activity.objects.filter(gid__in=groups)    

    def list(self, request):
        gid = self.request.GET.get('gid')
        activities = self.get_queryset(gid)
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            activity = self.get_queryset(pk)
            serializer = self.get_serializer(activity)
            if serializer.data:
                return Response(serializer.data)
        except Activity.DoesNotExist:
            return Response(dict(detail='Not found.'), status=status.HTTP_404_NOT_FOUND)

    def perform_create(self, serializer):
        user = self.request.user
        amount = round(serializer.validated_data.get('amount', 0))
        owner = serializer.validated_data.get('owner')
        except_users = serializer.validated_data.get('except_users')
        if owner in except_users:
            raise serializers.ValidationError(dict(detail='owner should\'t be in except list'))
        group = serializer.validated_data.get('gid')
        users = group.users
        if not all([users.filter(pk=u.pk).exists() for u in [user, owner]]):
            raise NotFound(detail='user or owner should blongs to the group')
        users = users.filter(~Q(pk__in=[u.pk for u in except_users]))
        if users:
            per_head = round(amount/len(users), 2)
        for usr in users:
            account, created = Account.objects.get_or_create(user=usr, group=group)
            if usr == owner:
                account.total += (amount-per_head)
            else:
                account.total -= per_head
            account.save() 
        serializer.save()

    def update(self, request, pk=None):
        oActivity = self.get_queryset(pk)
        self.perform_destroy(oActivity, dont_delete=True)
        data = request.data
        group = oActivity.gid
        if str(group.pk) != data.get('gid'):
            raise serializers.ValidationError(dict(detail='group should not be changed'))
        serializer = self.get_serializer(oActivity, data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_destroy(self, instance, **kwargs):
        group = instance.gid
        amount = instance.amount
        owner = instance.owner
        users = group.users
        except_users = instance.except_users
        per_head = round(amount/(users.count()-except_users.count()), 2)
        for usr in users.filter(~Q(pk__in=except_users.all())):
            account = Account.objects.get(user=usr, group=group)
            if usr == owner:
                account.total -= round(amount-per_head, 2)
            else:
                account.total += per_head
            account.save()
        if not kwargs.get('dont_delete'):
            instance.delete()


class AccountView(generics.ListAPIView):
    '''
    '''
    serializer_class = AccountSerializer

    def get_queryset(self):
        grps = Group.objects.filter(users__in=[self.request.user])
        return Account.objects.filter(group__in=grps)

    def list(self, request):
        user = request.user
        gid = self.request.GET.get('gid')
        uid = self.request.GET.get('uid')
        queryset = self.get_queryset()
        if gid and uid:
            queryset = queryset.filter(group=gid, user=uid)
        elif gid:
            queryset = queryset.filter(group=gid)
        elif uid:
            queryset = queryset.filter(user=uid)
        else:
            queryset = queryset.filter(user=user)

        serializer = self.get_serializer(queryset, many=True)    
        if serializer.data:
            return Response(serializer.data)
        return Response(dict(details='account details are not found'))


