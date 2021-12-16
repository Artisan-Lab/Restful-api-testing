from tool.tools import sno
from module.string_march import StringMatch

class Resource:

    def __init__(self, resource_id, api_id, resource_name, resource_data, resource_request):
        self.__resource_id = resource_id
        self.__resource_api_id = api_id
        self.__resource_name = sno.stem(resource_name)
        self.resource_data = resource_data
        self.__resource_request = resource_request
        self.__parent_resource = []
        self.__children_resource = []

    @property
    def get_resource_request(self):
        return self.__resource_request

    @property
    def resource_id(self):
        return self.__resource_id

    @property
    def resource_name(self):
        return self.__resource_name

    @property
    def resource_api_id(self):
        return self.__resource_api_id

    @property
    def parent_resource(self):
        return self.__parent_resource

    @parent_resource.setter
    def parent_resource(self, parent_resource):
        self.__parent_resource.append(parent_resource)

    @property
    def children_resource(self):
        return self.__children_resource

    @children_resource.setter
    def children_resource(self, children_resource):
        self.__children_resource.append(children_resource)

    def find_field_in_resource(self, field_name, field_type):
        value = StringMatch.find_field_in_dic(self.resource_data, field_name, field_type)
        if value: return value
        value
        field_name_list = field_name.split('_')
        for i in range(len(field_name_list)):
            field_name_list[i] =
        if len(field_name_list) > 1:
            if self.resource_name


