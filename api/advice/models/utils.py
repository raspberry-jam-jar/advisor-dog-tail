def get_default_tag_type():
    """
    Give the default tag type.
    """
    from .tag import TagType

    return TagType.objects.default().pk
