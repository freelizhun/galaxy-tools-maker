import requests
class ToolSheld(object):
    def __init__(self,tool_shed_api):
        self.tool_shed_api=tool_shed_api
    def tool_shed_api_request_response(self,g_toolshed_ipaddress):
        g_toolshed_api_url = 'http://' + g_toolshed_ipaddress + self.tool_shed_api
        g_toolshed_response = requests.get(g_toolshed_api_url)
        return g_toolshed_response
