class PyramidWebRegistry:

    def __init__(self, request):
        self.request = request

    @property
    def session_id(self):
        self.request.cookies.get('session_id')

    @session_id.setter
    def session_id(self, sessionid):
        pass
