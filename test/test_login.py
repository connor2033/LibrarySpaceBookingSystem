from unittest.mock import patch, MagicMock


import mainMenu
from user import User

# test validateUser function to make sure it is verifying credentials correctly
def test_validateUser():
    patch_open = patch("builtins.open", MagicMock())
    expected_data = MagicMock(return_value=[{
        "email": "fake email", "password": "pwd", "isLibrarian": False, "firstName": "fname", "lastName": "lname"
    }])
    patch_json_load = patch("json.load", expected_data)

    with patch_open as p_open:
        with patch_json_load as p_json:
            # check when password is valid
            isValid, user = mainMenu.validateUser("fake email", "pwd")
            assert isValid is True
            assert type(user) is User

            # check when password is invalid
            isValid, user = mainMenu.validateUser("fake email", "wrong pwd")
            assert isValid is False
            assert user is None

            # check when username is invalid
            isValid, user = mainMenu.validateUser("wrong email", "pwd")
            assert isValid is False
            assert user is None
        

