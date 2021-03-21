from flask import Blueprint,render_template,Response
import json

tools_blue=Blueprint('tools',__name__)

@tools_blue.route('/tools')
def tools():
    return render_template('tools.html')
@tools_blue.route('/tools/')
def toolss():
    return render_template('tools.html')

@tools_blue.route('/api/jms/tools/categories')
def tools_categories():
    categories=[{"CategoryID": 1, "CategoryName": "cae"}, {"CategoryID": 2, "CategoryName": "cae"}]
    return Response(json.dumps(categories),content_type='application/json')
@tools_blue.route('/api/jms/tools')
def tools_list():
    tools_list=[{"ToolID": 1, "ToolName": "test", "Category": 1, "ToolDescription": "ddd", "PublicInd": False,
                 "ToolVersions": [{"ToolVersionID": 1, "ToolVersionNum": "dev", "DatePublished": "2021-03-01"}],
                 "DeletedInd": False}]
    return Response(json.dumps(tools_list), content_type='application/json')

@tools_blue.route('/api/jms/tools/<int:tool_id>/versions/dev')
def tools_edit_show(tool_id):
    tools_edit_list={"Tool":
                      {"ToolID":tool_id,
                        "ToolName": "test",
                        "Category": 1,
                        "ToolDescription": "ddd",
                        "PublicInd":False,
                        "ToolVersions": [{"ToolVersionID": 1, "ToolVersionNum": "dev", "DatePublished": "2021-03-01"}],
                        "DeletedInd": False},
                     "ToolParameters": [],
                     "ExpectedOutputs": [],
                     "Resources": [],
                     "ToolVersionID": 1,
                     "ToolVersionNum": "dev",
                     "ShortDescription": "ddd",
                     "LongDescription": "",
                     "Command": "",
                     "DatePublished": "2021-03-01",
                     "DeletedInd": False}
    return Response(json.dumps(tools_edit_list),content_type='application/json')
@tools_blue.route('/api/jms/tools/<int:tool_id>/versions')
def tools_versions(tool_id):
    tools_versions=[{"ToolVersionID": tool_id, "ToolVersionNum": "dev", "DatePublished": "2021-03-01"}]
    return Response(json.dumps(tools_versions),content_type='application/json')

@tools_blue.route('/api/jms/tools/<int:tool_id>/files')
def tools_files(tool_id):
    tools_files=[]
    return Response(json.dumps(tools_files), content_type='application/json')

