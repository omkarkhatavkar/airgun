from airgun.entities.base import BaseEntity
from airgun.navigation import NavigateStep
from airgun.navigation import navigator
from airgun.views.ansible_role import AnsibleRolesImportView
from airgun.views.ansible_role import AnsibleRolesView

from navmazing import NavigateToSibling


class AnsibleRolesEntity(BaseEntity):
    endpoint_path = '/ansible/ansible_roles'

    def search(self, value):
        """Search for existing Ansible Role"""
        view = self.navigate_to(self, 'All')
        return view.search(value)

    def delete(self, entity_name, values):
        """Delete Ansible Role from Satellite"""
        view = self.navigate_to(self, 'All')
        view.search(entity_name)
        view.table.row(name=entity_name)['Actions'].widget.fill('Delete')
        self.browser.handle_alert()
        view.flash.assert_no_error()
        view.flash.dismiss()

    def count_imported_roles(self):
        view = self.navigate_to(self, 'All')
        return view.total_imported_roles.read()

    def import_all_roles(self):
        view = self.navigate_to(self, 'Import')
        available_roles_count = view.total_available_roles.read()
        view.select_all.fill(True)
        view.submit.click()
        return available_roles_count


@navigator.register(AnsibleRolesEntity, 'All')
class ShowAllRoles(NavigateStep):

    VIEW = AnsibleRolesView

    def step(self, *args, **kwargs):
        self.view.menu.select('Configure', 'Roles')


@navigator.register(AnsibleRolesEntity, 'Import')
class ImportAnsibleRole(NavigateStep):
    """Navigate to the Import Roles page"""

    VIEW = AnsibleRolesImportView

    prerequisite = NavigateToSibling('All')

    def step(self, *args, **kwargs):
        self.parent.import_button.click()
