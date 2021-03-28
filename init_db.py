import os,sqlite3
if __name__=="__main__":
    root_path = os.path.dirname(__file__)
    db_f_path = os.path.join(root_path, 'galaxy_tools.db')
    con = sqlite3.connect(db_f_path)
    c = con.cursor()
    c.execute("CREATE TABLE TOOLS (ToolID INTEGER PRIMARY KEY AUTOINCREMENT,"
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
    c.close()
    con.commit()
    con.close()