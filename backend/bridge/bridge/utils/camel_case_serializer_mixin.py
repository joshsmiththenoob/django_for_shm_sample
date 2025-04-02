import re



def camelize(key):
    """
    Utilize camelize function to convert snake case of representation into camel case
    """
    return re.sub(r'_([a-z])', lambda m: m.group(1).upper(), key)

class CamelCaseSerializerMixin:
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return {camelize(k): v for k, v in rep.items()}