import pulumi


def get_resource_name(resource_id):
    return "%s-%s-%s" % (pulumi.get_project(), pulumi.get_stack(), resource_id)
