from rest_framework import serializers

def create_shallow_serializer(cls, view_name, many=False):

    class LocalSerializer(serializers.HyperlinkedModelSerializer):

        url = serializers.HyperlinkedIdentityField(view_name=view_name)
        
        class Meta:
            model = cls
            fields = ('url', 'name', 'id',)
            extra_kwargs = { "id": {"read_only": False} }
    return LocalSerializer(many=many)