import traceback

from collections import OrderedDict

from django.contrib.auth.base_user import BaseUserManager

from rest_framework import serializers
from rest_framework.utils import model_meta

from api.users.serializers import AccountSerializer
from api.users.models import Account

from .models import Tag, Advice


class TagSerializer(serializers.ModelSerializer):
    """
    Advice tag serializer.
    """

    class Meta:
        model = Tag
        fields = (
            "title",
            "slug",
        )
        read_only_fields = ("slug",)


class UpdateTagsMixin:
    def update_tags(self, manager, values: list):
        for row in values:
            tag, _ = Tag.objects.get_or_create(title=row["title"])
            manager.add(tag)
        return manager


class AccountValidateMixin:
    def validate_author(self, value: OrderedDict):
        email = BaseUserManager.normalize_email(value["email"])
        return Account.objects.get_or_create(email=email)[0]


class AdviceSerializer(
    AccountValidateMixin, UpdateTagsMixin, serializers.ModelSerializer
):
    """Advice model serializer."""

    author = AccountSerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = Advice
        fields = ("title", "slug", "link", "author", "tags", "created")
        read_only_fields = ("slug", "created", )

    def create(self, validated_data):
        """
        We have a bit of extra checking around this in order to provide
        descriptive messages when something goes wrong, but this method is
        essentially just:
            return ExampleModel.objects.create(**validated_data)
        If there are many to many fields present on the instance then they
        cannot be set until the model is instantiated, in which case the
        implementation is like so:
            example_relationship = validated_data.pop('example_relationship')
            instance = ExampleModel.objects.create(**validated_data)
            instance.example_relationship = example_relationship
            return instance
        The default implementation also does not handle nested relationships.
        If you want to support writable nested relationships you'll need
        to write an explicit `.create()` method.
        """
        ModelClass = self.Meta.model

        # Remove many-to-many relationships from validated_data.
        # They are not valid arguments to the default `.create()` method,
        # as they require that the instance has already been saved.
        info = model_meta.get_field_info(ModelClass)
        many_to_many = {}
        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in validated_data):
                many_to_many[field_name] = validated_data.pop(field_name)

        try:
            instance = ModelClass._default_manager.create(**validated_data)
        except TypeError:
            tb = traceback.format_exc()
            msg = (
                "Got a `TypeError` when calling `%s.%s.create()`. "
                "This may be because you have a writable field on the "
                "serializer class that is not a valid argument to "
                "`%s.%s.create()`. You may need to make the field "
                "read-only, or override the %s.create() method to handle "
                "this correctly.\nOriginal exception was:\n %s"
                % (
                    ModelClass.__name__,
                    ModelClass._default_manager.name,
                    ModelClass.__name__,
                    ModelClass._default_manager.name,
                    self.__class__.__name__,
                    tb,
                )
            )
            raise TypeError(msg)

        # Save many-to-many relationships after the instance is created.
        if many_to_many:
            for field_name, value in many_to_many.items():
                field = getattr(instance, field_name)
                # if the field is an instance of a related manager which has Tag model
                if field.model and field.model == Tag:
                    field = self.update_tags(field, value)

        return instance


class ReadOnlyAdviceSerializer(serializers.ModelSerializer):
    """
    Read-only Advice model serializer.
    """

    author = AccountSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True,)

    class Meta:
        model = Advice
        fields = ("title", "slug", "link", "author", "tags", "created")
        read_only_fields = ("title", "slug", "link", "author", "tags", "created")


class UpdateAdviceSerializer(UpdateTagsMixin, serializers.ModelSerializer):
    """Advice model serializer for updating."""

    author = AccountSerializer(read_only=True)
    tags = TagSerializer(many=True,)

    class Meta:
        model = Advice
        fields = ("title", "slug", "link", "author", "tags", "created")
        read_only_fields = ("slug", "link", "created")

    def create(self, validated_data):
        """
        We have a bit of extra checking around this in order to provide
        descriptive messages when something goes wrong, but this method is
        essentially just:
            return ExampleModel.objects.create(**validated_data)
        If there are many to many fields present on the instance then they
        cannot be set until the model is instantiated, in which case the
        implementation is like so:
            example_relationship = validated_data.pop('example_relationship')
            instance = ExampleModel.objects.create(**validated_data)
            instance.example_relationship = example_relationship
            return instance
        The default implementation also does not handle nested relationships.
        If you want to support writable nested relationships you'll need
        to write an explicit `.create()` method.
        """
        ModelClass = self.Meta.model

        # Remove many-to-many relationships from validated_data.
        # They are not valid arguments to the default `.create()` method,
        # as they require that the instance has already been saved.
        info = model_meta.get_field_info(ModelClass)
        many_to_many = {}
        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in validated_data):
                many_to_many[field_name] = validated_data.pop(field_name)

        try:
            instance = ModelClass._default_manager.create(**validated_data)
        except TypeError:
            tb = traceback.format_exc()
            msg = (
                "Got a `TypeError` when calling `%s.%s.create()`. "
                "This may be because you have a writable field on the "
                "serializer class that is not a valid argument to "
                "`%s.%s.create()`. You may need to make the field "
                "read-only, or override the %s.create() method to handle "
                "this correctly.\nOriginal exception was:\n %s"
                % (
                    ModelClass.__name__,
                    ModelClass._default_manager.name,
                    ModelClass.__name__,
                    ModelClass._default_manager.name,
                    self.__class__.__name__,
                    tb,
                )
            )
            raise TypeError(msg)

        # Save many-to-many relationships after the instance is created.
        if many_to_many:
            for field_name, value in many_to_many.items():
                field = getattr(instance, field_name)
                # if the field is an instance of a related manager which has Tag model
                if field.model and field.model == Tag:
                    field = self.get_or_create_tags(field, value)

        return instance

    def update(self, instance, validated_data):
        info = model_meta.get_field_info(instance)

        # Simply set each attribute on the instance, and then save it.
        # Note that unlike `.create()` we don't need to treat many-to-many
        # relationships as being a special case. During updates we already
        # have an instance pk for the relationships to be associated with.
        m2m_fields = []
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)

        instance.save()

        # Note that many-to-many fields are set after updating instance.
        # Setting m2m fields triggers signals which could potentially change
        # updated instance and we do not want it to collide with .update()
        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            # if the field is an instance of a related manager which has Tag model
            if field.model and field.model == Tag:
                field = self.get_or_create_tags(field, value)

        return instance
