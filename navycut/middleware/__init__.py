from ..core.helper_decorators import _get_req_res_view

class MiddlewareMixin(object):
    """
    The default middleware mixin class to provide the default
    middleware service for navycut app.
    """
    def before_request(req, res):
        pass

    def before_first_request(req, res):
        pass

    def after_request(req, res):
        pass

    @classmethod
    def __maker__(cls):
        _before_request = _get_req_res_view(cls.before_request)
        _before_first_request = _get_req_res_view(cls.before_first_request)
        _after_request = _get_req_res_view(cls.after_request)

        return (_before_request, _before_first_request, _after_request)