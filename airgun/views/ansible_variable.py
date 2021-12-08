from widgetastic.widget import Checkbox
from widgetastic.widget import Text
from widgetastic.widget import TextInput
from widgetastic_patternfly import BreadCrumb

from airgun.views.common import BaseLoggedInView
from airgun.views.common import SatTable
from airgun.views.common import SearchableViewMixin
from airgun.widgets import FilteredDropdown
from airgun.widgets import Pagination
from airgun.widgets import SatSelect


class AnsibleVariablesView(BaseLoggedInView, SearchableViewMixin):
    """Main Ansible Variables view."""

    title = Text("//h1[contains(., text()='Ansible Variables')")
    new_variable = Text("//a[contains(@href, '/ansible/ansible_variables/new')]")
    total_variables = Text("//span[@class='pagination-pf-items-total']")
    table = SatTable(
        './/table',
        column_widgets={
            'Name': Text("./a"),
            'Role': Text("./a"),
            'Type': Text("./a"),
            'Imported?': Text("./a"),
            'Actions': Text("./a[contains(., text()='Delete')]"),
        },
    )
    pagination = Pagination()

    @property
    def is_displayed(self):
        return self.browser.wait_for_element(
            self.title, exception=False
        ) is not None and self.browser.url.endswith('ansible_roles')

class NewAnsibleVariableView(BaseLoggedInView):
    """View while creating a new Ansible Variable"""

    breadcrumb = BreadCrumb()
    key = TextInput(id='ansible_variable_key')
    description = TextInput(id='ansible_variable_description')
    ansible_role = FilteredDropdown(id='ansible_variable_ansible_role_id')
    override = Checkbox(id='ansible_variable_override')

    # Accessing all widgets except the ones above requires that the `override` checkbox is filled
    parameter_type = SatSelect(id='ansible_variable_parameter_type')
    default_value = TextInput(id='ansible_variable_default_value')
    hidden_value = Checkbox(id='ansible_variable_hidden_value')
    expand_input_validator = Text("//h2[@class='expander collapsed']")
    required = Checkbox(id='ansible_variable_required')
    validator_type = SatSelect(id='ansible_variable_validator_type')
    validator_rule = TextInput(id='ansible_variable_validator_rule')
    # the below attribute_order widget throws an error when a string value is passed to it
    attribute_order = TextInput(id='order')
    merge_overrides = Checkbox(id='ansible_variable_merge_overrides')
    merge_default = Checkbox(id='ansible_variable_merge_default')
    avoid_duplicates = Checkbox(id='ansible_variable_avoid_duplicates')
    add_matcher_button = Text("//a[contains(@class, 'add_nested_fields')]")
    attribute_type = SatSelect("//div[@class='matcher-group']/select[1]")
    # the below attribute_value widget is not locating the element correctly as currently written
    attribute_value = Text("//div[@class='matcher-group']/input[1]")
    matcher_value = TextInput(id='new_lookup_value_value')
    submit = Text('//input[@value="Submit"]')
    cancel = Text("//a[contains(., text()='Cancel']")

    @property
    def expand_button(self):
        """Return the Optional Input Validator section expander element."""
        return self.browser.element(self.expand_input_validator, parent=self)

    @property
    def expanded(self):
        """Check whether this section is expanded."""
        return 'active' in self.browser.get_attribute('class', self.expand_input_validator)

    def expand(self):
        """Expand the Optional Input Validator section."""
        if not self.expanded:
            self.browser.click(self.expand_input_validator, parent=self)

    @property
    def is_displayed(self):
        breadcrumb_loaded = self.browser.wait_for_element(self.breadcrumb, exception=False)
        return (
            breadcrumb_loaded
            and self.breadcrumb.locations[0] == 'Ansible Variables'
            and self.breadcrumb.read() == 'Create Ansible Variable'
        )