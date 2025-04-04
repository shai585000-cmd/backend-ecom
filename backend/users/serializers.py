from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    nom_cli = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        nom_cli = attrs.get('nom_cli')
        password = attrs.get('password')

        if nom_cli and password:
            try:
                user = User.objects.get(username=nom_cli)
                if user.check_password(password):
                    if user.is_active:
                        attrs['user'] = user
                        return attrs
                    raise serializers.ValidationError({
                        'error': 'Ce compte est désactivé.'
                    })
                raise serializers.ValidationError({
                    'error': 'Mot de passe incorrect.'
                })
            except User.DoesNotExist:
                raise serializers.ValidationError({
                    'error': 'Aucun utilisateur trouvé avec ce nom.'
                })
        raise serializers.ValidationError({
            'error': 'Les champs nom_cli et password sont requis.'
        })


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'nom_cli', 'commerçant', 'numero_cli', 'adresse_cli', 'ville_cli', 'code_postal_cli', 'pays_cli', 'email', 'password']
    
    def create(self, validated_data):
        # Créer l'utilisateur avec les données validées
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)  # Crypter le mot de passe
        user.save()
        return user


class vendeurSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'nom_cli', 'commerçant', 'numero_cli', 'adresse_cli', 'ville_cli', 'code_postal_cli', 'pays_cli', 'email', 'password']
    
    def create(self, validated_data):
        # Créer l'utilisateur avec les données validées
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)  # Crypter le mot de passe
        user.save()
        return user

class DashboardSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'