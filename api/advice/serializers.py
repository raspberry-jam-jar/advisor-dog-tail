from rest_framework import serializers
from rest_framework.utils import model_meta

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


class AdviceSerializer(serializers.ModelSerializer):
    """
    Advice model serializer.
    """

    tags = TagSerializer(many=True,)

    class Meta:
        model = Advice
        fields = ("title", "slug", "tags", "link", "created")
        read_only_fields = ("slug", "created")

    def update_tags(sefl, manager, values: list):
        for row in values:
            tag, _ = Tag.objects.get_or_create(title=row["title"])
            manager.add(tag)
        return manager

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
                field = self.update_tags(field, value)

        return instance
