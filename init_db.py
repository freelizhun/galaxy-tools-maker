import os,sqlite3
if __name__=="__main__":
    root_path = os.path.dirname(__file__)
    db_f_path = os.path.join(root_path, 'galaxy_tools.db')
    con = sqlite3.connect(db_f_path)
    c = con.cursor()
    #TOOLS主表
    c.execute("CREATE TABLE IF NOT EXISTS TOOLS (ToolID INTEGER PRIMARY KEY AUTOINCREMENT,"
              "ToolName CHAR(100),"
              "Category CHAR(100),"
              "ToolDescription TEXT,"
              "PublicInd INTEGER,"
              "ToolVersionID TEXT,"
              "ToolVersionNum TEXT,"
              "DatePublished TEXT,"
              "ToolParameters TEXT,"
              "ExpectedOutputs TEXT,"
              "LongDescription TEXT,"
              "Command TEXT)")

    #PARAMETERS从表
    c.execute("CREATE TABLE IF NOT EXISTS PARAMETERS (ParameterID INTEGER PRIMARY KEY AUTOINCREMENT,"
              "ParameterName CHAR(100),"
              "Context CHAR(100),"
              "ParameterType INTEGER,"
              "Value TEXT,"
              "ToolVersionID TEXT,"
              "CONSTRAINT fk_toolversionid FOREIGN KEY (ToolVersionID) REFERENCES TOOLS(ToolVersionID) on delete cascade on update cascade)")

    #FILES从表
    c.execute("CREATE TABLE IF NOT EXISTS FILES (FileID INTEGER PRIMARY KEY AUTOINCREMENT,"
              "FileName CHAR(100),"
              "FileDir CHAR(100),"
              "ToolVersionID TEXT,"
              "CONSTRAINT ffk_toolversionid FOREIGN KEY (ToolVersionID) REFERENCES TOOLS(ToolVersionID) on delete cascade on update cascade)")

    # 类别表
    # c.execute("CREATE TABLE IF NOT EXISTS CATEGORY (CategoryID INTEGER PRIMARY KEY AUTOINCREMENT,"
    #          "CategoryName CHAR(100),"
    #          "CategoryVersionID CHAR(100))")
    # c.close()
    # con.commit()
    # con.close()