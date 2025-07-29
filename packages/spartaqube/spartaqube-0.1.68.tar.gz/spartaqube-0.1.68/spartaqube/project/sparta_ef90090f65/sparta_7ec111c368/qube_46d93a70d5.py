import os
from project.sparta_ef90090f65.sparta_7ec111c368.qube_caacf6f8e3 import qube_caacf6f8e3
from project.sparta_ef90090f65.sparta_7ec111c368.qube_688ce26e9f import qube_688ce26e9f
from project.sparta_ef90090f65.sparta_7ec111c368.qube_dd4bc33dd5 import qube_dd4bc33dd5
from project.sparta_ef90090f65.sparta_7ec111c368.qube_33363b82a4 import qube_33363b82a4


class db_connection:
    """
    dbType : 
        0 SQLite DEFAULT DATABASE
        1 MySQL DATABASE
        2 Microsoft SQL Server
    """

    def __init__(self, dbType=0):
        self.dbType = dbType
        self.dbCon = None

    def get_db_type(self):
        return self.dbType

    def getConnection(self):
        """

        """
        if self.dbType == 0:
            from django.conf import settings as conf_settings
            if conf_settings.PLATFORM in ['SANDBOX', 'SANDBOX_MYSQL']:
                return None
            self.dbCon = qube_caacf6f8e3()
        elif self.dbType == 1:
            self.dbCon = qube_688ce26e9f()
        elif self.dbType == 2:
            self.dbCon = qube_dd4bc33dd5()
        elif self.dbType == 4:
            self.dbCon = qube_33363b82a4()
        return self.dbCon

#END OF QUBE
