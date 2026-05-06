import pytest

from tests.test_base import BaseTest


class TestLogin(BaseTest):

    @pytest.mark.smoke
    def test_login_page_has_title(self):
        pass
