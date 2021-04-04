import os, sqlite3, time


class OperationDb(object):
    def __init__(self):
        root_path = os.path.dirname(os.path.dirname(__file__))
        db_dir=os.path.join(root_path,'db_dir')
        db_f_path = os.path.join(db_dir, 'galaxy_tools.db')
        self.con = sqlite3.connect(db_f_path)
        self.c = self.con.cursor()

    def insert_tool(self, toolname, category,
                    tool_description, publicind, tool_version_id,
                    tool_version_num, date_published,
                    tool_parameters, expected_outputs,
                    loog_description, command):
        self.c.execute("INSERT INTO TOOLS (ToolName,Category,"
                       "ToolDescription,PublicInd ,ToolVersionID,"
                       "ToolVersionNum,DatePublished,"
                       "ToolParameters,ExpectedOutputs,"
                       "LongDescription,Command) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                       (toolname, category,
                        tool_description, publicind, tool_version_id,
                        tool_version_num, date_published,
                        tool_parameters, expected_outputs,
                        loog_description, command))
        self.c.close()
        self.con.commit()
        self.con.close()

    def select_tool(self):
        self.c.execute('select* from TOOLS')
        values = self.c.fetchall()
        self.c.close()
        self.con.close()
        return values

    def select_tool_id(self, tool_id):
        self.c.execute('select* from TOOLS where ToolID=?', (tool_id,))
        values = self.c.fetchall()
        self.c.close()
        self.con.close()
        return values

    def delete_tool_id(self,tool_id):
        self.c.execute('delete from TOOLS where ToolID=?',(tool_id,))
        self.c.close()
        self.con.commit()
        self.con.close()

    def insert_parameter(self, parameter_name, context, parameter_type, value, tool_version_id):
        self.c.execute("INSERT INTO PARAMETERS (ParameterName,"
                       "Context,"
                       "ParameterType,"
                       "Value,"
                       "ToolVersionID) VALUES(?,?,?,?,?)",
                       (parameter_name, context, parameter_type, value, tool_version_id))
        self.c.close()
        self.con.commit()
        self.con.close()

    def select_tool_version_id_parameter(self, tool_version_id_parameter):
        self.c.execute('select * from PARAMETERS where ToolVersionID=?', (tool_version_id_parameter,))
        values = self.c.fetchall()
        self.c.close()
        self.con.close()
        return values

    def delete_parameter(self, parameter_id):
        self.c.execute('delete from PARAMETERS where ParameterID=?', (parameter_id,))
        self.c.close()
        self.con.commit()
        self.con.close()

    def delete_parameter_toolversion(self,tool_version_id):
        self.c.execute('delete from PARAMETERS where ToolVersionID=?',(tool_version_id,))
        self.c.close()
        self.con.commit()
        self.con.close()

    def insert_file(self, file_name, file_dir, tool_version_id):
        self.c.execute("INSERT INTO FILES (FileName,"
                       "FileDir,ToolVersionID) VALUES (?,?,?)", (file_name, file_dir, tool_version_id))
        self.c.close()
        self.con.commit()
        self.con.close()

    def select_tool_version_id_file(self, tool_version_id_file):
        self.c.execute('select * from FILES where ToolVersionID=?', (tool_version_id_file,))
        values = self.c.fetchall()
        self.c.close()
        self.con.close()
        return values

    def delete_files(self, tool_version_id, file_name):
        self.c.execute('delete from FILES where ToolVersionID=? AND FileName=?', (tool_version_id, file_name))
        self.c.close()
        self.con.commit()
        self.con.close()

    def delete_files_toolversion(self,tool_version_id):
        self.c.execute('delete from FILES where ToolVersionID=?',(tool_version_id,))
        self.c.close()
        self.con.commit()
        self.con.close()

    def search_filedir_need_to_delete(self, tool_version_id, file_name):
        self.c.execute('select * from FILES where ToolVersionID=? AND FileName=?', (tool_version_id, file_name))
        values = self.c.fetchall()
        self.c.close()
        self.con.close()
        return values

    def only_search_filedir_need_to_delete(self,tool_version_id):
        self.c.execute('select * from FILES where ToolVersionID=?',(tool_version_id,))
        values=self.c.fetchall()
        self.c.close()
        self.con.close()
        return values

    # def insert_category(self,category_name,category_version_id):
    #    self.c.execute('INSERT INTO CATEGORY (CategoryName,CategoryVersionID) VALUES (?,?)',
    #                   (category_name,category_version_id))
    #    self.c.close()
    #    self.con.commit()
    #    self.con.close()
    def update_tools(self, tool_id, toolname, category, tool_description, loog_description, command):
        self.c.execute('update TOOLS set ToolName=?,Category=?,ToolDescription=?,LongDescription=?,Command=? where '
                       'ToolID=?', (toolname, category, tool_description, loog_description, command, tool_id))
        self.c.close()
        self.con.commit()
        self.con.close()

    def update_parameters(self,parameter_id,parameter_name,context,parameter_type,value):
        self.c.execute('update PARAMETERS set ParameterName=?,Context=?,ParameterType=?,Value=? where '
                       'ParameterID=?',(parameter_name,context,parameter_type,value,parameter_id))
        self.c.close()
        self.con.commit()
        self.con.close()
