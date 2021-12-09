from airgun.entities.base import BaseEntity
from airgun.navigation import NavigateStep
from airgun.navigation import navigator
from airgun.views.ansible_variable import AnsibleVariablesView
from airgun.views.ansible_variable import NewAnsibleVariableView

from navmazing import NavigateToSibling

class AnsibleVariablesEntity(BaseEntity):
    endpoint_path = '/ansible/ansible_variables'

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

    def read_total_variables(self):
        view = self.navigate_to(self, 'All')
        return view.total_variables.read()

    def create(self, values):
        view = self.navigate_to(self, 'New')
        view.fill(values)
        view.submit.click()
        view.flash.assert_no_error()
        view.flash.dismiss()

    def create_with_overrides(self, values):
        view = self.navigate_to(self, 'New')
        view.override.fill(True)
        view.expand()
        view.add_matcher_button.click()
        view.fill(values)
        view.submit.click
        view.flash.assert_no_error()
        view.flash.dismiss()


@navigator.register(AnsibleVariablesEntity, 'All')
class ShowAllVariables(NavigateStep):
    """Navigate to Ansible Variables page"""

    VIEW = AnsibleVariablesView

    def step(self, *args, **kwargs):
        self.view.menu.select('Configure', 'Variables')


@navigator.register(AnsibleVariablesEntity, 'New')
class NewAnsibleVariable(NavigateStep):
    """Navigate to Create Ansible Variable page"""

    VIEW = NewAnsibleVariableView

    prerequisite = NavigateToSibling('All')

    def step(self, *args, **kwargs):
        self.parent.new_variable.click()
