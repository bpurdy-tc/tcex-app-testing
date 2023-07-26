"""TcEx App Testing Module"""
# third-party
from tcex_app_testing.validator import Validator

# first-party
from tests.validate import Validate


class ValidateCustom(Validate):
    """Validate for Feature ${feature}

    This file will only be auto-generated once to ensure any changes are not overwritten.
    """

    def __init__(self, validator: Validator):  # pylint: disable=useless-super-delegation
        """Initialize class properties."""
        super().__init__(validator)
