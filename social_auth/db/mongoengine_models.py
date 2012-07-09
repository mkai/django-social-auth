"""
MongoEngine models for Social Auth

Requires MongoEngine 0.6.10
"""
from mongoengine import DictField, Document, IntField, ReferenceField, \
                        StringField
from mongoengine.django.auth import User

from social_auth.db.base import UserSocialAuthMixin, AssociationMixin, \
                                NonceMixin


# TODO make this a complementary config setting to SOCIAL_AUTH_USER_MODEL
USERNAME = 'username'


class UserSocialAuth(Document, UserSocialAuthMixin):
    """Social Auth association model"""
    user = ReferenceField(User)
    provider = StringField(max_length=32)
    uid = StringField(max_length=255, unique_with='provider')
    extra_data = DictField()

    @classmethod
    def get_social_auth_for_user(cls, user):
        return cls.objects(user=user)

    @classmethod
    def create_social_auth(cls, user, uid, provider):
        if not isinstance(type(uid), basestring):
            uid = str(uid)
        return cls.objects.create(user=user, uid=uid, provider=provider)


class Nonce(Document, NonceMixin):
    """One use numbers"""
    server_url = StringField(max_length=255)
    timestamp = IntField()
    salt = StringField(max_length=40)


class Association(Document, AssociationMixin):
    """OpenId account association"""
    server_url = StringField(max_length=255)
    handle = StringField(max_length=255)
    secret = StringField(max_length=255)  # Stored base64 encoded
    issued = IntField()
    lifetime = IntField()
    assoc_type = StringField(max_length=64)
