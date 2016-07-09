__author__ = 'tingxxu'


from .sproperty import SProperty


class SSetting(SProperty):

    def __init__(self, s_name, s_type, s_range, s_value, s_required=False):
        SProperty.__init__(self, s_name, s_type, s_range, s_value)
        self.required = s_required