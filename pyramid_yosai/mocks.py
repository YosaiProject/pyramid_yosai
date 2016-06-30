#
#
#   This file is only for prototyping designs and will be removed shortly
#
#
#
import uuid


class MockYosai:

    def __init__(self):
        self.subject = None

    def __enter__(self):
        return self

    def __exit__(self):
        self.subject = None

    def __call__(self, web_registry):
        self.subject = MockSubject(web_registry) 
        return self


class MockSubject:
    
    def __init__(self, web_registry):
        self.subject_id = 'SubjectID_' + str(uuid.uuid())
        self.set_session_cookie(web_registry)

    def get_session(self):
        return MockSession()

    def set_session_cookie(self, web_registry):
        web_registry.session_id = self.get_session().session_id 


class MockSession:

    def __init__(self):
        self.session_id = 'SessionID_' + str(uuid.uuid())
    

class PyramidWebRegistry:

    @property
    def session_id(self):
        pass

    @session_id.setter
    def session_id(self, sessionid):
        pass

