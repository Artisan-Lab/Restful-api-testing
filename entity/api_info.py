import random


class DependPoint:

    def __init__(self, api_id: int, path: list, score):
        self._api_id = api_id
        self._path = path
        self._base_score = score
        self._mutate_score = score
        self._time = 0
        self.flag = None

    @property
    def api_id(self):
        return self._api_id

    @property
    def path(self):
        return self._path

    @property
    def score(self):
        return self._base_score

    @property
    def mutate_score(self):
        return self._mutate_score

    @property
    def time(self):
        return self._time

    def add_score(self):
        if self.flag == "base":
            self._base_score += pow((1 - self.score), 2)
        elif self.flag == "mutate":
            self._mutate_score += pow((1 - self.mutate_score), 2)

    def minus_score(self):
        if self.flag == "base":
            self._base_score -= pow(self.score, 2)
        elif self.flag == "mutate":
            self._mutate_score -= pow(self._mutate_score, 2)

    def add_time(self):
        self._time += 1


class FieldInfo:

    def __init__(self, field_name, type_, require, location, max_lenth=None, min_lenth=None, default=None,
                 description=None, enum=None, object=None, array=None, max=None, min=None, format=None):
        self.field_name = field_name
        self.field_type = type_
        self.require = require
        self.default = default
        self.location = location
        self.max_lenth = max_lenth
        self.min_lenth = min_lenth
        self.enum = enum
        self.description = description
        self.object = object
        self.array = array
        self.maximum = max
        self.minimum = min
        self.format = format
        self.depend_list = []  # type: list[DependPoint]
        if self.field_type == 'int' or self.field_type == 'str':
            self.depend_list.append(DependPoint(-1, [], 0.5))

    def get_depend(self, api_id, path):
        for depend in self.depend_list:
            if depend.api_id == api_id and depend.path == path:
                return depend
        return None

    def genetic_algorithm(self) -> DependPoint:
        depend_point = random.choices(self.depend_list,
                                      weights=[point.mutate_score + point.score for point in self.depend_list])[0]
        depend_point.flag = random.choices(["base", "mutate"],
                                           weights=[depend_point.score, depend_point.mutate_score])[0]
        return depend_point


class APIInfo:

    def __init__(self, api_id, base_url, path, req_param, resp_param, http_method):
        self.api_id = api_id
        self.identifier = http_method + " " + path
        self.base_url = base_url
        self.path = path
        self.close_api = []
        self.key_depend_api_list = []
        self.req_param = req_param  # type: list[FieldInfo]
        self.resp_param = resp_param  # type: list[FieldInfo]
        self.http_method = http_method
