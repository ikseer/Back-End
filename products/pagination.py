from rest_framework.pagination import PageNumberPagination


class ProductPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'limit'

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        has_next_page = self.get_next_link() is not None
        has_previous_page = self.get_previous_link() is not None
        response.data['hasNextPage'] = has_next_page
        response.data['hasPreviousPage'] = has_previous_page
        return response

        # return Response(OrderedDict([
        #     ('count', self.count),
        #     ('hasNextPage', True if self.offset + self.limit < self.count else False),  # self.get_next_link()),
        #     ('hasPreviousPage', True if self.offset > 0 else False),
        #     ('next', self.get_next_link()),
        #     ('previous', self.get_previous_link()),
        #     ('results', data)
        # ]))
    # def get_schema_operation_parameters(self, view):
    #     parameters = [
    #         {
    #             'name': self.limit_query_param,
    #             'required': False,
    #             'in': 'query',
    #             'description': force_str(self.limit_query_description),
    #             'schema': {
    #                 'type': 'integer',
    #             },
    #         },
    #         {
    #             'name': self.offset_query_param,
    #             'required': False,
    #             'in': 'query',
    #             'description': force_str(self.offset_query_description),
    #             'schema': {
    #                 'type': 'integer',
    #             },
    #         },
    #     ]
    #     return parameters