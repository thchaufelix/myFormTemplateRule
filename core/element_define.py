from typing import Literal, get_args

_INPUT_TYPE = Literal["draggable", "input"]


class RuleElement(object):

    def __init__(self, name, element):
        self.name = name
        self.props = element.get_props

    @property
    def get_element(self):
        return vars(self)


class ElementBasicMethod(object):
    item_type = ""
    required = True

    @property
    def get_props(self):
        return vars(self)


class TextElement(ElementBasicMethod):
    def __init__(self, required=True, option=None, default=None):
        self.required = required
        self.item_type = "text"

        if default is not None:
            self.default = default

        if option is not None:
            self.option = option


class NumericElement(ElementBasicMethod):
    def __init__(self, required=True, default=None):
        self.required = required
        self.item_type = "numeric"

        if default is not None:
            self.default = default


class BooleanElement(ElementBasicMethod):
    def __init__(self, required=True, child_element={}, default=None):
        self.required = required
        self.props = child_element

        if default is not None:
            self.default = default


class ColorElement(ElementBasicMethod):
    props = {}

    def __init__(self, required=True, color_options=[]):
        self.item_type = "boolean"
        self.required = required
        self.props = {**TextElement(option=color_options).get_props}


class ListElement(ElementBasicMethod):
    props = {}

    def __init__(self, child_element, required=True, duplicable=True, size=1, input_type: _INPUT_TYPE = "draggable"):
        self.item_type = "list"
        self.required = required
        self.duplicable = duplicable
        self.size = size

        assert input_type in get_args(_INPUT_TYPE), f"'{input_type}' is not in {get_args(_INPUT_TYPE)}"
        self.input_type = input_type

        self.props = child_element.get_props


class ObjectElement(ElementBasicMethod):
    template = {}

    def __init__(self, required=True, rules=[], duplicable=False, duplicable_rules=None):
        self.item_type = "object"
        self.required = required

        self.template = [rule.get_element for rule in rules]

        if duplicable:
            self.duplicable = duplicable
            self.duplicable_rules = duplicable_rules if duplicable_rules is None else {
                "delimiter": "_",
                "initial": 1
            }


if __name__ == "__main__":
    print(ColorElement(color_options=["#FFFCF2", "#EDFFFB", "#F9F5FF"]).get_props)
    print(ListElement(child_element=TextElement(default="none")).get_props)
    print(ObjectElement(
        rules=[
            RuleElement(name="key", element=TextElement()),
            RuleElement(name="title", element=TextElement()),
            RuleElement(name="location", element=ListElement(size=4, child_element=NumericElement()))
        ]
    ).get_props)

    print(ListElement(
        size=1,
        duplicable=False,
        input_type="input",
        child_element=ListElement(
            size=2,
            child_element=NumericElement()
        )
    ).get_props)
