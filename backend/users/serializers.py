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

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer pour le profil utilisateur"""
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'nom_cli', 'numero_cli',
            'adresse_cli', 'ville_cli', 'code_postal_cli', 'pays_cli',
            'commerçant', 'created_at'
        ]
        read_only_fields = ['id', 'username', 'created_at', 'commerçant']


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer pour la mise à jour du profil"""
    class Meta:
        model = User
        fields = [
            'email', 'nom_cli', 'numero_cli',
            'adresse_cli', 'ville_cli', 'code_postal_cli', 'pays_cli'
        ]


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer pour le changement de mot de passe"""
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, min_length=6)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({
                'confirm_password': 'Les mots de passe ne correspondent pas.'
            })
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Mot de passe actuel incorrect.')
        return value