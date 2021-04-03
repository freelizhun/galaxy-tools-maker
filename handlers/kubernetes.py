from kubernetes import client, config
from handlers import check_url
import time, re, os, sys, uuid
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream


# kubernetes 12.0.1
def exec_commands(api_instance, pod_name, namespace,
                  log,
                  first_planemo_command,
                  second_planemo_command,
                  third_planemo_command):
    name = pod_name
    exec_namespace = namespace
    resp = None
    try:
        resp = api_instance.read_namespaced_pod(name=name,
                                                namespace=exec_namespace)
    except ApiException as e:
        if e.status != 404:
            log.error("Unknown error: %s" % e)
            exit(1)
    if not resp:
        log.error("Pod %s does not exist. Please creating it..." % name)
        exit(1)
    # Begining to exec cmd in planemo-pod
    o_uuid = str(uuid.uuid4())
    s_uuid = ''.join(o_uuid.split('-'))
    cmd='mkdir -p /home/%s; cd /home/%s; %s; %s; %s' % (s_uuid,s_uuid,
                                                        first_planemo_command,
                                                        second_planemo_command,
                                                        third_planemo_command)
    #cmd = 'cd /test-data; source /etc/profile; mpirun -np 4 /home/test/lmp_mpi -in /test-data/%s' % input_file_name
    exec_command = [
        '/bin/sh',
        '-c', cmd]
    resp = stream(api_instance.connect_get_namespaced_pod_exec,
                  name,
                  exec_namespace,
                  command=exec_command,
                  stderr=True, stdin=False,
                  stdout=True, tty=False)
    log.info("Response: " + resp)


def prod_xml_to_shed(log,tool_name, command, list_args,
                     owner, description, long_description, category,
                     shed_email, shed_password, tool_shed_url):
    global pod_name
    if not os.path.exists('/galaxy/server/data-cache'):
        os.makedirs('/galaxy/server/data-cache')
    # 集群内部即pod内使用，加载config配置文件
    config.load_incluster_config()
    v1 = client.CoreV1Api()
    log.info("Listing pods with their names:")
    # 匹配找到planemo-deploy这个pod的名字
    namespace = 'galaxy2'
    ret = v1.list_namespaced_pod(namespace)
    for i in ret.items:
        # print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
        if re.match(r'planemo-deploy-*', i.metadata.name):
            pod_name = i.metadata.name
            log.info('the pod_name is %s' % pod_name)
            break
    core_v1 = client.CoreV1Api()

    # 开始构建到planemo中去执行的三个命令
    tool_name_ch = tool_name
    tool_name = '\'%s\'' % tool_name_ch
    o_uuid = str(uuid.uuid4())
    s_uuid = ''.join(o_uuid.split('-'))
    tool_id = '\'%s_%s\'' % (s_uuid, tool_name_ch)
    command = command
    # list_args=[['-n','1'],['-p','6'],['--force','True'],['--d','/home/do']]
    list_args = list_args
    example_command = ''
    example_input = ' --example_input'
    real_example_input = ''
    for value in list_args:
        example_command = example_command + value[0] + ' ' + value[1] + ' '
        example_input_mid = example_input + ' ' + '\'%s\'' % value[1]
        real_example_input = real_example_input + example_input_mid
    real_example_command = '\'%s %s\'' % (command, example_command.strip())
    help_text = '\'this is a tool for %s\'' % tool_name_ch

    first_planemo_command = 'planemo tool_init --force' + \
                            ' --id ' + tool_id + \
                            ' --name ' + tool_name + \
                            ' --example_command ' + real_example_command + \
                            real_example_input + \
                            ' --help_text ' + help_text
    owner_ch = owner
    owner = '\'%s\'' % owner_ch
    description_ch = description
    description = '\'%s\'' % description_ch
    long_description_ch = long_description
    long_description = '\'%s\'' % long_description_ch
    category_ch = category
    category = '\'%s\'' % category_ch

    second_planemo_command = 'planemo shed_init' + \
                             ' --name ' + tool_name + \
                             ' --owner ' + owner + \
                             ' --description ' + description + \
                             ' --long_description ' + description + \
                             ' --category ' + category
    shed_email_ch = shed_email
    shed_email = '\'%s\'' % shed_email_ch
    shed_password_ch = shed_password
    shed_password = '\'%s\'' % shed_password_ch
    tool_shed_url_ch = check_url(tool_shed_url, log=log)
    tool_shed_url = '\'%s\'' % tool_shed_url_ch

    third_planemo_command = 'planemo shed_create' + \
                           ' --shed_email ' + shed_email + \
                           ' --shed_password ' + shed_password + \
                           ' -t ' + tool_shed_url
    log.info('The planemo tool_init command is:  %s' % first_planemo_command)
    log.info('The planemo shed_init command is: %s' % second_planemo_command)
    log.info('The planemo shed_create command is: %s' % third_planemo_command)
    # 开始在pod即lammps-deploy-***中执行生成tools xml文件、上传tools到shed的命令
    try:
        exec_commands(core_v1, pod_name, namespace,
                  log,
                  first_planemo_command,
                  second_planemo_command,
                  third_planemo_command)
        log.info('Produce tools: %s to tool_shed successful !' % tool_name_ch)
        return 'success'
    except Exception as e:
        log.error('Produce tools: %s to tool_shed failed ! and the reason is: %s' % (tool_name_ch,e))
        return 'failed'
