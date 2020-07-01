from rest_framework.response import Response


class APIResponse(Response):

    def __init__(self, status=200, message=0, results=None,*arge, **kwargs):
        data = {
            "status": status,
            "message": message
        }
        if results is not None:
            data['results'] = results

        super().__init__(data=data)
