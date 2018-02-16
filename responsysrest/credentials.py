import os
import getpass
import json

class Credentials:
    """Load credentials information like passwords."""

    def __init__(
        self,
        mode='',
        user_name='',
        password='',
        email_address=''
    ):
        """Initialize the credentials."""
        self.mode = mode
        self.user_name = user_name
        self.password = password
        self.email_address = email_address

    @property
    def user_name(self):
        """Get Username."""
        return self.__user_name

    @user_name.setter
    def user_name(self, user_name):
        """Set Username."""
        # cli-style
        if self.mode.lower() == 'cli':
            self.__user_name = input('Username:\n')
        # non-cli-style
        else:
            self.__user_name = user_name

    @property
    def password(self):
        """Get Password."""
        return self.__password

    @password.setter
    def password(self, password):
        """Set Username."""
        # cli-style
        if self.mode.lower() == 'cli':
            self.__password = getpass.getpass()
        # non-cli-style
        else:
            self.__password = password

    @property
    def email_address(self):
        """Get Email Address."""
        return self.__email_address

    @email_address.setter
    def email_address(self, email_address):
        """Set Username."""
        # cli-style
        if self.mode.lower() == 'cli':
            self.__email_address = input(
                'Email Address (for account and testing):\n')
        # non-cli-style
        else:
            self.__email_address = email_address


def auto():
    """Load any secret.json file."""
    # traverse root directory looking for credentials
    for root, dirs, files in os.walk("."):
        for file in files:
            if file == 'secret.json':
                try:
                    with open(file) as f:
                        user_config = json.load(f)
                        creds = Credentials(
                            mode='',
                            user_name=user_config['user_name'],
                            password=user_config['password'],
                            email_address=user_config['email_address'])
                        return creds
                except:
                    raise ValueError(f'Could not open {file}')
