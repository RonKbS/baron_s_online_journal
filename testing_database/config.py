from configparser import ConfigParser
import os
# from mydiary import app
 
 
def config(filename="C:\\Users\\Ron\\Desktop\\baron_s_o_dear\\testing_database\\database.ini", section='postgresql'):
    if os.environ.get('DATABASE_URL'):
        db = os.environ.get('DATABASE_URL')
        return db

    parser = ConfigParser()
    # read config file
    parser.read(filename)
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
 
    return db