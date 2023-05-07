from rest_framework import serializers
from .models import Stream, Image, Object


class StreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stream
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    stream = StreamSerializer(read_only=True)
    class Meta:
        model = Image
        fields = '__all__'

class ObjectSerializer(serializers.ModelSerializer):
    # image = ImageSerializer(read_only=True)
    class Meta:
        model = Object
        fields = '__all__'

class ObjectSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Object
        fields = '__all__'

class ImageWithObjectsSerializer(serializers.ModelSerializer):
    objects = ObjectSerializer(many=True, read_only=True,source='object_set')
    
    class Meta:
        model = Image
        fields = '__all__'
