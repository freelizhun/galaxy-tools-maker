from flask import Blueprint, render_template, Response, request
import json, requests, yaml, os, uuid, time
from handlers.tool_shed_api import ToolSheld
from handlers.operation_db import OperationDb
from werkzeug.utils import secure_filename

tools_blue = Blueprint('tools', __name__)

# 根目录
root_path = os.path.dirname(os.path.dirname(__file__))
config_f_path = os.path.join(root_path, 'g-tools-maker.yml')
with open(config_f_path, 'r', encoding='utf-8') as config_f:
    yml_data = config_f.read()
    dic_yml_data = yaml.load(yml_data, Loader=yaml.FullLoader)
# galaxy_toolshed_ipaddress=‘192.168.108.109:9009’
GALAXY_TOOLSHED_IPADDRESS = dic_yml_data['galaxy_tool_shed']['ip_address']


@tools_blue.route('/tools')
def tools():
    return render_template('tools.html')


@tools_blue.route('/tools/')
def toolss():
    return render_template('tools.html')


@tools_blue.route('/api/g/tools/categories')
def tools_categories():
    # 通过向galaxy_toolshed请求获取其tools类别
    g_toolshed_categories_api = '/api/categories'
    g_toolshed_categories_api_instance = ToolSheld(g_toolshed_categories_api)
    g_toolshed_response = g_toolshed_categories_api_instance.tool_shed_api_request_response(GALAXY_TOOLSHED_IPADDRESS)
    categories = []
    operation_category_instance=OperationDb()
    for category in g_toolshed_response.json():
        category_dic = {}
        category_dic['CategoryID'] = category['id']
        category_dic['CategoryName'] = category['name']
        categories.append(category_dic)

    return Response(json.dumps(categories), content_type='application/json')


@tools_blue.route('/api/g/tools', methods=['GET', 'POST'])
def tools_list():
    if request.method == 'GET':
        operation_db_instance = OperationDb()
        values = operation_db_instance.select_tool()
        tools_list = []
        for value in values:
            dic = {}
            dic_version = {}
            tools_versions_list = []
            dic["ToolID"] = value[0]
            dic["ToolName"] = value[1]
            dic["Category"] = value[2]
            dic["ToolDescription"] = value[3]
            # 公开与否，默认公开
            # dic["PublicInd"]=True
            dic["PublicInd"] = value[4]
            dic_version["ToolVersionID"] = value[5]
            dic_version["ToolVersionNum"] = value[6]
            dic_version["DatePublished"] = value[7]
            tools_versions_list.append(dic_version)
            dic["ToolVersions"] = tools_versions_list
            dic["DeletedInd"] = False
            tools_list.append(dic)
        '''tools_list = [{"ToolID": 1, "ToolName": "test", "Category": "2e810b1cd3515059", "ToolDescription": "ddd", "PublicInd": False,
                   "ToolVersions": [{"ToolVersionID": 1, "ToolVersionNum": "dev", "DatePublished": "2021-03-01"}],
                   "DeletedInd": False}]'''

        return Response(json.dumps(tools_list), content_type='application/json')
    else:
        o_uuid = str(uuid.uuid4())
        s_uuid = ''.join(o_uuid.split('-'))
        # print(request.form)
        # ImmutableMultiDict([('{"ToolID":0,"ToolName":"dd","Category":"adb5f5c93f827949","ToolDescription":"dd","User":{"UserID":0,"Username":""},"ToolVersions":[],"UserToolPermissions":[]}', '')])
        # print(request.form.to_dict())
        # {'{"ToolID":0,"ToolName":"dd","Category":"adb5f5c93f827949","ToolDescription":"dd","User":{"UserID":0,"Username":""},"ToolVersions":[],"UserToolPermissions":[]}': ''}
        # print(request.form.to_dict().keys())
        # dict_keys(['{"ToolID":0,"ToolName":"dd","Category":"adb5f5c93f827949","ToolDescription":"dd","User":{"UserID":0,"Username":""},"ToolVersions":[],"UserToolPermissions":[]}'])
        # print(list(request.form.to_dict().keys()))
        # ['{"ToolID":0,"ToolName":"dd","Category":"adb5f5c93f827949","ToolDescription":"dd","User":{"UserID":0,"Username":""},"ToolVersions":[],"UserToolPermissions":[]}']
        # print(eval((list(request.form.to_dict().keys()))[0]))
        # {'ToolID': 0, 'ToolName': 'dd', 'Category': 'adb5f5c93f827949', 'ToolDescription': 'dd', 'User': {'UserID': 0, 'Username': ''}, 'ToolVersions': [], 'UserToolPermissions': []}
        toolname = eval(list(request.form.to_dict().keys())[0])["ToolName"]
        category = eval(list(request.form.to_dict().keys())[0])['Category']
        tool_description = eval(list(request.form.to_dict().keys())[0])['ToolDescription']
        # 公开与否，默认公开
        publicind = True
        tool_version_id = s_uuid
        tool_version_num = "dev"
        date_published = time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime())
        tool_parameters = ""
        expected_outputs = ""
        loog_description = ""
        command = ""
        operation_db_instance = OperationDb()
        operation_db_instance.insert_tool(toolname, category, tool_description, publicind,
                                          tool_version_id, tool_version_num, date_published,
                                          tool_parameters, expected_outputs, loog_description, command)

        ToolVersions = [{"ToolVersionID": s_uuid, "ToolVersionNum": "dev", "DatePublished": date_published}]
        return Response(json.dumps(ToolVersions), content_type='application/json')


@tools_blue.route('/api/g/tools/<int:tool_id>/parameters', methods=['GET', 'POST'])
def add_parameters(tool_id):
    if request.method == 'POST':
        # 先通过tool_id获取TOOLS中的tool_verison_id
        operation_db_instance = OperationDb()
        values = operation_db_instance.select_tool_id(tool_id)
        value = values[0]
        tool_version_id_parameter = value[5]

        # parameter相关参数
        parameter_name = "default"
        context = ""
        parameter_type = ""
        value = ""
        tool_version_id_parameter = tool_version_id_parameter
        operation_db_instancep = OperationDb()
        operation_db_instancep.insert_parameter(parameter_name, context, parameter_type, value,
                                                tool_version_id_parameter)

        # 插入parameter数据后返回查询后的结果tool_parameter_list到前端
        operation_db_instancep2 = OperationDb()
        parameter_values = operation_db_instancep2.select_tool_version_id_parameter(tool_version_id_parameter)
        tool_parameter_list = []
        for parameter_value in parameter_values:
            dicp = {}
            dicp["ParameterID"] = parameter_value[0]
            dicp["ParameterName"] = parameter_value[1]
            dicp["Context"] = parameter_value[2]
            dicp["InputBy"] = "System"
            dicp["ParameterType"] = parameter_value[3]
            dicp['Value']=parameter_value[4]
            dicp["Multiple"] = False
            dicp["Delimiter"] = ""
            dicp["ParentParameter"] = None
            dicp["Optional"] = False
            dicp["ParameterOptions"] = []
            tool_parameter_list.append(dicp)
        tool_parameter_list_last = [tool_parameter_list[-1]]
        return Response(json.dumps(tool_parameter_list_last), content_type='application/json')


@tools_blue.route('/api/g/parameters/<int:parameter_id>', methods=["DELETE"])
def delete_parameters(parameter_id):
    operation_db_instancep = OperationDb()
    operation_db_instancep.delete_parameter(parameter_id)
    return Response(json.dumps([]), content_type='application/json')


@tools_blue.route('/api/g/tools/<int:tool_id>/files', methods=['POST', 'GET', 'DELETE'])
def upload_files(tool_id):
    if request.method == 'POST':
        file = request.files['file']
        # secure_filename方法会去掉文件名中的中文
        secure_file_name = secure_filename(file.filename)
        # 使用uuid防止文件名重复
        file_name = str(uuid.uuid4()) + '.' + secure_file_name
        upload_folder = os.path.join(root_path, 'filedata')
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        # 文件存储目录
        file_dir = os.path.join(upload_folder, file_name)
        file.save(file_dir)
        # 真实文件名称
        real_filename = file.filename
        # 获取对应tool的tool_version_id
        operation_db_instance = OperationDb()
        values = operation_db_instance.select_tool_id(tool_id)
        value = values[0]
        tool_version_id_file = value[5]

        # 将文件信息保存到文件数据库
        operation_db_instancef = OperationDb()
        operation_db_instancef.insert_file(real_filename, file_dir, tool_version_id_file)

        # 插入file数据后返回查询后的结果tool_file_list到前端
        operation_db_instancef2 = OperationDb()
        file_values = operation_db_instancef2.select_tool_version_id_file(tool_version_id_file)
        tool_file_list = []
        for file_value in file_values:
            file_value_name = file_value[1]
            tool_file_list.append(file_value_name)
        return Response(json.dumps(tool_file_list), content_type='application/json')
    elif request.method == 'GET':
        # 获取对应tool的tool_version_id
        operation_db_instancec = OperationDb()
        valuesc = operation_db_instancec.select_tool_id(tool_id)
        valuec = valuesc[0]
        tool_version_id_filec = valuec[5]
        # 插入file数据后返回查询后的结果tool_file_list到前端
        operation_db_instancefc2 = OperationDb()
        file_valuesc = operation_db_instancefc2.select_tool_version_id_file(tool_version_id_filec)
        tool_file_listc = []
        for file_valuec in file_valuesc:
            file_valuec_name = file_valuec[1]
            tool_file_listc.append(file_valuec_name)
        return Response(json.dumps(tool_file_listc), content_type='application/json')
    else:
        delete_file_name = eval(list(request.form.to_dict().keys())[0])
        # 获取对应tool的tool_version_id
        operation_db_instancedv = OperationDb()
        delete_tool_version_values = operation_db_instancedv.select_tool_id(tool_id)
        delete_tool_version_value = delete_tool_version_values[0]
        delete_tool_version_id = delete_tool_version_value[5]
        # 删除数据库中存储的文件前，先实际删除存储在filedata目录上的文件
        delete_filedir_instance = OperationDb()
        file_dirs = delete_filedir_instance.search_filedir_need_to_delete(delete_tool_version_id, delete_file_name)
        for file_dir in file_dirs:
            if os.path.exists(file_dir[2]):
                os.remove(file_dir[2])
        operation_db_delete = OperationDb()
        operation_db_delete.delete_files(delete_tool_version_id, delete_file_name)
        return Response(json.dumps([]), content_type='application/json')


@tools_blue.route('/api/g/tools/<int:tool_id>', methods=['PUT','DELETE'])
def save_delete_tool(tool_id):
    if request.method=='PUT':
        tools_data=eval(list(request.form.to_dict().keys())[0])
        tool_id=tool_id

        # 更新保存tools相关参数
        toolname=tools_data['Tool']['ToolName']
        category=tools_data['Tool']['CategoryID']
        tool_description=tools_data['ShortDescription']
        # publicind = True
        tool_version_id=tools_data['ToolVersionID']
        # tool_version_num = "dev"
        # date_published=
        # tool_parameters = ""
        # expected_outputs = ""
        loog_description = tools_data['LongDescription']
        command = tools_data['Command']
        operation_db_instance = OperationDb()
        operation_db_instance.update_tools(tool_id,toolname,category,tool_description,loog_description,command)

        # 更新保存parameter相关参数
        parameters=tools_data['Parameters']
        for parameter in parameters:
            parameter_id=parameter['ParameterID']
            parameter_name=parameter['ParameterName']
            context=parameter['Context']
            parameter_type=parameter['ParameterType']
            value=parameter['Value']
            # tool_version_id_parameter = tool_version_id
            operation_db_instancep = OperationDb()
            operation_db_instancep.update_parameters(parameter_id,parameter_name,context,parameter_type,value)
        return Response(json.dumps([]), content_type='application/json')
    else:
        tool_id=tool_id
        # 获取对应tool的tool_version_id
        operation_db_instancedv = OperationDb()
        delete_tool_version_values = operation_db_instancedv.select_tool_id(tool_id)
        delete_tool_version_value = delete_tool_version_values[0]
        delete_tool_version_id = delete_tool_version_value[5]
        # 先删除存储在filedata目录上的文件，再清除数据库TOOLS数据,然后删除PRAMETERS,FILES数据库中的数据
        delete_filedir_instance = OperationDb()
        file_dirs = delete_filedir_instance.only_search_filedir_need_to_delete(delete_tool_version_id)
        for file_dir in file_dirs:
            if os.path.exists(file_dir[2]):
                os.remove(file_dir[2])
        operation_delete_tool=OperationDb()
        operation_delete_tool.delete_tool_id(tool_id)
        # 删除PRAMETERS相关参数
        operation_db_instancep = OperationDb()
        operation_db_instancep.delete_parameter_toolversion(delete_tool_version_id)
        # 删除FILES相关参数
        operation_db_instancef=OperationDb()
        operation_db_instancef.delete_files_toolversion(delete_tool_version_id)
        return Response(json.dumps([]), content_type='application/json')


@tools_blue.route('/api/g/tools/<int:tool_id>/versions/dev')
def tools_edit_show(tool_id):
    # PublicInd默认为True全部公开
    operation_db_instance = OperationDb()
    values = operation_db_instance.select_tool_id(tool_id)
    value = values[0]
    tools_edit_dic = {}
    tools_edit_dic_dic = {}

    tools_edit_dic_dic["ToolID"] = tool_id
    tools_edit_dic_dic["ToolName"] = value[1]
    tools_edit_dic_dic["Category"] = value[2]
    tools_edit_dic_dic["ToolDescription"] = value[3]
    tools_edit_dic_dic["PublicInd"] = value[4]
    tools_edit_dic_dic["ToolVersions"] = [{"ToolVersionID": value[5],
                                           "ToolVersionNum": value[6], "DatePublished": value[7]}]

    tools_edit_dic["Tool"] = tools_edit_dic_dic

    tool_version_id_parameter = value[5]
    operation_db_instancep = OperationDb()
    parameter_values = operation_db_instancep.select_tool_version_id_parameter(tool_version_id_parameter)
    tool_parameter_list = []
    for parameter_value in parameter_values:
        dicp = {}
        dicp["ParameterID"] = parameter_value[0]
        dicp["ParameterName"] = parameter_value[1]
        dicp["Context"] = parameter_value[2]
        dicp["InputBy"] = "System"
        dicp["ParameterType"] = parameter_value[3]
        dicp["Value"]=parameter_value[4]
        dicp["Multiple"] = False
        dicp["Delimiter"] = ""
        dicp["ParentParameter"] = None
        dicp["Optional"] = False
        dicp["ParameterOptions"] = []
        tool_parameter_list.append(dicp)

    tools_edit_dic["ToolParameters"] = tool_parameter_list
    '''[{"ParameterID":1,"ParameterName":"first","Context":"","InputBy":"System",
         "ParameterType":"","Multiple":False,"Value":"","Delimiter":"",
         "ParentParameter":None,"Optional":False,"ParameterOptions":[]},
         
        {"ParameterID": 2, "ParameterName": "second", "Context": "", "InputBy": "System",
         "ParameterType": "", "Multiple": False, "Value": "", "Delimiter": "",
         "ParentParameter": None, "Optional": False, "ParameterOptions": []}]'''

    tools_edit_dic["ExpectedOutputs"] = []
    tools_edit_dic["Resources"] = []
    tools_edit_dic["ToolVersionID"] = value[5]
    tools_edit_dic["ToolVersionNum"] = value[6]
    tools_edit_dic["ShortDescription"] = value[3]
    tools_edit_dic["LongDescription"] = value[10]
    tools_edit_dic["Command"] = value[11]
    tools_edit_dic["DatePublished"] = value[7]
    tools_edit_dic["DeletedInd"] = False
    '''tools_edit_dic_test = {"Tool":
                       {"ToolID": tool_id,
                        "ToolName": "test",
                        "Category": 1,
                        "ToolDescription": "ddd",
                        "PublicInd": True,
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
                       "DeletedInd": False}'''
    return Response(json.dumps(tools_edit_dic), content_type='application/json')


@tools_blue.route('/api/g/tools/<int:tool_id>/versions')
def tools_versions(tool_id):
    operation_db_instance = OperationDb()
    values = operation_db_instance.select_tool_id(tool_id)
    value = values[0]
    tools_versions = [{"ToolVersionID": value[5], "ToolVersionNum": value[6], "DatePublished": value[7]}]
    return Response(json.dumps(tools_versions), content_type='application/json')


@tools_blue.route('/api/jms/tools/<int:tool_id>/files')
def tools_files(tool_id):
    tools_files = []
    return Response(json.dumps(tools_files), content_type='application/json')
