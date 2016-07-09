__author__ = 'tingxxu'


class SProperty:

    # Type:0 -> number   Range -> array{min,max} or None
    # Type:1 -> string   Range -> array{item1, item2,item3} or None
    # Type:2 -> bool     Range -> None
    # Type:3 -> color    Range -> None
    def __init__(self, s_name, s_type, s_range, s_value):
        self.name = s_name
        self.type = s_type
        self.range = s_range
        self.value = s_value
        self.description = "the %s property" % self.name
