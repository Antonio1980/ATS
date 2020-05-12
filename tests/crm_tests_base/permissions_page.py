from src.base import logger
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from tests.crm_tests_base import BasePage
from tests.crm_tests_base.locators import permissions_locators


class PermissionsPage(BasePage):

    def __init__(self):
        super(PermissionsPage, self).__init__()
        self.locators = permissions_locators
        self.username = "Permission User"
        self.password = "1Aa@<>12"
        self.permissions_group_id = '24'
        self.local_permissions_group_name = "Permissions Test"

    @automation_logger(logger)
    def set_entity_permissions(self, permissions_group_id, local_permissions_group_name,
                               local_permissions_entity_name, local_sub_module_name):

        query_entity_name = (
                "SELECT * FROM local_permission_entities WHERE permissionGroupId = "
                + permissions_group_id + " AND name = " + local_permissions_entity_name + ";")

        query_insert_view = """INSERT INTO local_permission_entities ('brokerId', 'name', 'moduleId', 'hasView', 
           'hasEdit', 'hasCreate', 'enableEdit', 'enableCreate', 'permissionGroupId', 'submoduleId') 
           VALUES(100001, """ + local_permissions_entity_name + """

           (SELECT id FROM local_modules WHERE name = """ + local_permissions_entity_name + """), 1, 0, 0, 0, 0,

           (SELECT id FROM local_permission_groups WHERE name = """ + local_permissions_group_name + """), 

           (SELECT id FROM local_sub_modules WHERE name = """ + local_sub_module_name + """));"""

        query_update_view = ("UPDATE local_permission_entities SET hasView = 1, hasEdit = 0, hasCreate = 0 WHERE name ="
                             + local_permissions_entity_name + " AND permissionGroupId = " + permissions_group_id + ";")

        try:
            query_entity_name_result = Instruments.run_mysql_query(query_entity_name)
            if query_entity_name_result is None:
                Instruments.run_mysql_query(query_insert_view)
                return True
            else:
                Instruments.run_mysql_query(query_update_view)
                return True
        except Exception as e:
            logger.logger.error("{0} set_entity_permissions failed with error. {1}".format(e.__class__.__name__,
                                                                                           e.__cause__))
            return False

    @automation_logger(logger)
    def update_view_edit_create_permissions(self, local_permissions_entity_name, permissions_group_id, flag=0):
        # flag = 1 : update permissions  to view and edit,
        # flag = 2 : update permissions to view , edit and create
        if flag == 0:
            part = "hasView = 0, hasEdit = 0, hasCreate = 0"
        elif flag == 1:
            part = "hasView = 1, hasEdit = 1, hasCreate = 0"
        elif flag == 2:
            part = "hasView = 1, hasEdit = 1, hasCreate = 1"
        else:
            part = ""
        query_update_view_edit = "UPDATE local_permission_entities SET " + part + " WHERE name = " \
                                 + local_permissions_entity_name + " AND permissionGroupId = " \
                                 + permissions_group_id + ";"
        try:
            Instruments.run_mysql_query(query_update_view_edit)
            return True
        except Exception as e:
            logger.logger.error("{0} update_view_edit_create_permissions failed with error. {1}".format(
                e.__class__.__name__, e.__cause__))
            return False
