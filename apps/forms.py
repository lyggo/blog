class FormMixin:
    def get_error(self):
        if hasattr(self, "errors"):
            """
            {
                'telephone': [
                    {'message': '手机号长度有误', 'code': 'min_length'}
                ],
                 'password': [
                    {'message': '最小长度不能小于6', 'code': 'min_length'}
                 ]
            }
            """
            error_dict = self.errors.get_json_data().popitem()[1][0]
            message = error_dict["message"]
            return message
        return None
