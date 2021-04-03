import yaml,requests,os,time
import sqlite3,uuid
from handlers.shed_tools import install_tool_from_toolshed
if __name__=="__main__":
    '''root_path = os.path.dirname(os.path.dirname(__file__))
    config_f_path = os.path.join(root_path, 'g-tools-maker.yml')
    with open(config_f_path,'r',encoding='utf-8') as config_f:
        yml_data=config_f.read()
        dic_yml_data=yaml.load(yml_data,Loader=yaml.FullLoader)
    galaxy_toolshed_ipaddress=dic_yml_data['galaxy_tool_shed']['ip_address']
    print(galaxy_toolshed_ipaddress)
    # 通过向galaxy_toolshed请求获取其tools类别
    galaxy_toolshed_categories_url='http://'+galaxy_toolshed_ipaddress+'/api/categories'
    galaxy_toolshed_response=requests.get(galaxy_toolshed_categories_url)

    categories =[]
    for category in galaxy_toolshed_response.json():
        category_dic={}
        category_dic['CategoryID']=category['id']
        category_dic['CategoryName']=category['name']
        categories.append(category_dic)
    print(categories)'''
    '''toolname="lammps_k8s"
        category="2e810b1cd3515059"
        tool_description="test-lammps-in-k8s"
        publicind="true"
        tool_version_id=1
        tool_version_num='dev'
        date_published=time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime())
        tool_parameters="-n 4 -p 6"
        expected_outputs=""
        loog_description="lammps for k8s"
        command="mpirun"
        values=(toolname,
                category,
                tool_description,
                publicind,
                tool_version_id,
                tool_version_num,
                date_published,
                tool_parameters,
                expected_outputs,
                loog_description,
                command)'''
    '''for i in [1,2,3]:
        o_uuid=str(uuid.uuid4())
        s_uuid=''.join(o_uuid.split('-'))
        print(s_uuid)'''
    root_path = os.path.dirname(os.path.dirname(__file__))
    config_f_path = os.path.join(root_path, 'g-tools-maker.yml')
    tool_name='test_tools_maker'
    install_tool_from_toolshed(config_f_path,tool_name)

