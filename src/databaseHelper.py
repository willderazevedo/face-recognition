import sqlite3

class DbHelper:

    def getIdByName(self, name):
        connection = sqlite3.connect('../database/FaceDetection.db');
        query      = "SELECT DISTINCT * FROM USER WHERE NAME LIKE '%" + name + "%'";
        cursor     = connection.execute(query);
        hasRows    = False;
        userId     = 0;

        for rows in cursor:
            userId = rows[0];

        connection.close();

        return userId;

    def getNameById(self, userId):
        connection = sqlite3.connect('../database/FaceDetection.db');
        query      = "SELECT NAME FROM USER WHERE ID = " + str(userId) + "";
        cursor     = connection.execute(query);
        hasRows    = False;
        name       = '';

        for rows in cursor:
            name = rows[0];

        connection.close();

        return name;

    def firstOrUpdate(self, name):
        connection = sqlite3.connect('../database/FaceDetection.db');
        query      = "SELECT DISTINCT * FROM USER WHERE NAME LIKE '%" + name + "%'";
        cursor     = connection.execute(query);
        hasRows    = False;

        for rows in cursor:
            hasRows = True;
                    
        if(hasRows):
            query = "UPDATE USER SET NAME = '" + name + "' WHERE NAME LIKE '%" + name + "%'";
        else:
            query = "INSERT INTO USER(id, name) VALUES(null, '" + name + "')";

        connection.execute(query);
        connection.commit();
        connection.close();
