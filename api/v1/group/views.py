from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from itertools import chain

from api.models import Group, User
from api.v1.account.serializers import UserSerializer
from api.v1.group.serializers import GroupSerializer, MemberSerializer
from api.permissions import IsOwnerOrReadOnly, IsGroupAccessable


class GroupViewSet(ModelViewSet):
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    queryset = Group.objects.all()

    def list(self, request):
        user = self.request.user
        print(user)
        belongs_to_group = Group.objects.filter(users__in=[user])
        serializer = GroupSerializer(belongs_to_group, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        user = User.objects.filter(pk=self.request.user.pk)
        serializer.save(users=user)

    def retrieve(self, request, pk=None):
        user = self.request.user
        belongs_to_group = Group.objects.filter(pk=pk, users__in=[user])
        serializer_data = GroupSerializer(belongs_to_group, many=True).data
        if serializer_data:
            return Response(serializer_data)
        return Response(dict(detail='Not found.'), status=status.HTTP_404_NOT_FOUND)


class MemberListView(generics.ListCreateAPIView):
    serializer_class = MemberSerializer
    permission_classes = (IsAuthenticated, IsGroupAccessable, IsOwnerOrReadOnly)

    def get_queryset(self):
        gid = self.kwargs.get('gid')
        return Group.objects.get(id=gid)

    def list(self, request, **kwargs):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset.users, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        group = self.get_queryset()
        self.check_object_permissions(request, group)
        not_a_valid_user = []
        for id_ in email:
            try:
                usr = User.objects.get(email=id_)
                group.users.add(usr)
            except:
                not_a_valid_user.append(id_)  
        group.save()
        if not_a_valid_user:
            return Response({'detail': "can't find valid user", 'data': not_a_valid_user})
        return Response({'detail': 'successfully added members to the group'})


class MemberDeleteView(APIView):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        return Group.objects.get(pk=self.kwargs.get('gid'))

    def delete(self, request, format=None, **kwargs):
        group = self.get_queryset()
        self.check_object_permissions(request, group)
        user = User.objects.get(pk=kwargs.get('mid'))
        if user == group.users.get(pk=request.user.pk):
            return Response(dict(detail='you can\'t remove yourself'))
        group.users.remove(user)
        group.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


