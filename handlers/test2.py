import yaml,requests,os,time
import sqlite3,uuid
if __name__=="__main__":
    root_path = os.path.dirname(os.path.dirname(__file__))
    db_f_path = os.path.join(root_path, 'galaxy_tools.db')
    #con=sqlite3.connect(db_f_path)
    #c=con.cursor()
    #tool_id=1
    #c.execute('select* from TOOLS where ToolID=?',(tool_id,))
    #c.execute('select * from TOOLS')
    #c.execute('select * from PARAMETERS')
    #c.execute('select * from FILES')
    #values=c.fetchall()
    #print(values)
    #print(values[0][1])
    #con.close()
    tool_name_ch='mpirun'
    tool_name='\'%s\'' % tool_name_ch
    o_uuid = str(uuid.uuid4())
    s_uuid = ''.join(o_uuid.split('-'))
    tool_id = '\'%s_%s\''% (s_uuid,tool_name_ch)
    command='mpirun'
    list_args=[['-n','1'],['-p','6'],['--force','True'],['--d','/home/do']]
    example_command=''
    example_input=' --example_input'
    real_example_input = ''
    for value in list_args:
        example_command=example_command+value[0] +' '+value[1] + ' '
        example_input_mid=example_input+' '+'\'%s\''% value[1]
        real_example_input=real_example_input+example_input_mid
    real_example_command='\'%s %s\''% (command,example_command.strip())
    help_text='\'this is a tool for %s\'' % tool_name_ch
    first_planemo_command ='planemo tool_init --force' +\
                           ' --id '+tool_id+\
                           ' --name '+tool_name+\
                           ' --example_command '+real_example_command+\
                           real_example_input+\
                           ' --help_text '+help_text
    owner_ch='planemo'
    owner='\'%s\'' % owner_ch
    description_ch='short description for mpirun'
    description='\'%s\'' % description_ch
    long_description_ch='this is a long description'
    long_description='\'%s\'' % long_description_ch
    category_ch='Web Service'
    category='\'%s\'' % category_ch
    second_planemo_command='planemo shed_init'+\
                           ' --name '+tool_name +\
                           ' --owner '+owner+\
                           ' --description '+description+\
                           ' --long_description '+description+\
                           ' --category '+category
    shed_email_ch='planemo@test.com'
    shed_email='\'%s\'' % shed_email_ch
    shed_password_ch='planemo'
    shed_password='\'%s\'' % shed_password_ch
    tool_shed_url_ch='http://192.168.0.9:9009/'
    tool_shed_url='\'%s\'' % tool_shed_url_ch
    third_planmo_command='planemo shed_create'+\
                         ' --shed_email '+shed_email+\
                         ' --shed_password '+shed_password+\
                         ' -t '+tool_shed_url

    print(first_planemo_command)
    print(second_planemo_command)
    print(third_planmo_command)