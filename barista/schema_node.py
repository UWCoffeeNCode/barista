from typing import Union
from graphene import ID, ObjectType, Field
from graphene.relay import Node as GrapheneNode, is_node


class Node(GrapheneNode):
    "An object with an ID."

    pass


class NodeField(Field):
    def __init__(self, type: Union[ObjectType, None] = None, **kwargs):
        if type:
            assert issubclass(type, ObjectType), "Object is not an ObjectType."
            assert is_node(type), "Object is not a Node."
        self.__type = type

        super(NodeField, self).__init__(
            type or Node,
            id=ID(required=True, description="The ID of the object."),
            **kwargs,
        )

    def get_resolver(self, parent_resolver):
        def resolver(root, info, id: ID):
            return Node.get_node_from_global_id(info, id, only_type=self.__type)

        return resolver
