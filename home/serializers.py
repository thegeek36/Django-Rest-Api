from rest_framework import serializers
from .models import Person,Color
from django.contrib.auth.models import User

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self,data):
        if data['username']:
            if User.objects.filter(username = data['username']).exists():
                raise serializers.ValidationError('username is taken')
        if data['email']:
            if User.objects.filter(email = data['email']).exists():
                raise serializers.ValidationError('Email already exists')
        return data
    
    def  create(self,validated_data):
        user = User.objects.create(username = validated_data['username'],email = validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        print(validated_data)
        return validated_data

     
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class ColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Color 
        fields = ['id']
        fields = ['id','color_name']

class PeopleSerializer(serializers.ModelSerializer):

    #color = ColorSerializer()
    #color_info = serializers.SerializerMethodField()

    class Meta:
        model =  Person
        #Eiter way we can serialize the  feilds 
        #feilds = ['name', 'age']
        #to serialize all the fields
        fields = '__all__'
        # depth = 1

    def get_color_info(self,obj):
        color_obj = Color.objects.get(id = obj.color.id)
        return {'color_name' : color_obj.color_name,'hex_code' : '#0000'}
    
    def validate(self,data):
        special = "!@#$%^&*()*+,-./<>?=_~"
        if any(c in special for c in data['name']):
            raise serializers.ValidationError('Name must not contain any special character')
        if data['age'] < 18:
            raise serializers.ValidationError('Age must be greater than 18')
        return data

