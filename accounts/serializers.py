from dj_rest_auth.registration.serializers import RegisterSerializer
from pkg_resources import require
from rest_framework import serializers
from .models import Profile

from dj_rest_auth.serializers import UserDetailsSerializer




# def get_if_complete_profile(user):
#     if Profile.objects.filter(user=user).exists():
#         return True
#     else:
#         return False

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        # fields = ('user','first_name', 'last_name', 'bio', 'image', 'date_of_birth', 'gender')
    first_name= serializers.CharField(required=True)
    last_name= serializers.CharField(required=True)
    date_of_birth= serializers.DateField(required=True)
    gender= serializers.CharField(required=True)
    is_complete= serializers.BooleanField(read_only=True)


from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers

class CustomUserSerializer(UserDetailsSerializer):
    # Add any additional fields or override existing fields as needed
    profile = ProfileSerializer()  # Replace with your actual profile serializer

    class Meta(UserDetailsSerializer.Meta):
        # Include additional fields in the 'fields' list if needed
        # exclude the 'password' field from the 'fields' list
        # fields = UserDetailsSerializer.Meta.fields 
        # exclude = ['username']
        fields = ('pk',  'email')+ ('profile', )


from dj_rest_auth.serializers import LoginSerializer

class loginSerializer(LoginSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


        # add the 'profile' field to the 'fields' list
        # fields.append('profile')

    # validate email verification status
    def validate_email(self, value):
        user = self.context['request'].user
        if not user.emailaddress_set.filter(email=value, verified=True).exists():
            raise serializers.ValidationError(_('E-mail is not verified.'))
        return value
    
class OtpByEmailSerializer(serializers.Serializer):
    email = serializers.EmailField( required=True)
class VerifyEmailOtpSerializer(serializers.Serializer):
    otp = serializers.CharField( required=True)