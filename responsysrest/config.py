"""How we configure our Interact Client connection."""

import os
import getpass
import json

class Credentials:
    """Load credentials information like passwords."""

    def __init__(
        self,
        mode='',
        user_name=None,
        password=None,
        email_address=None
    ):
        """Initialize the secrets."""
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


class Interact:
    """How our client is configured."""

    def __init__(
            self,
            pod='5',
            api_folder='___api-generated',
            api_list='___api-list',
            profile_extension_table_alias='_pet',
            supplemental_table_alias='_supp',
            primary_key_alias='_primary_key',
            riid_generator_length=11,
            test_campaign_name='___api-testing-campaign',
            content_library_folder='___api-generated-cl',
            api_version='1.3',
            login_url=None
    ):
        """Initialize the Interact Configuration."""
        self.pod = pod
        self.api_folder = api_folder
        self.api_list = api_list
        self.profile_extension_table_alias = profile_extension_table_alias
        self.supplemental_table_alias = supplemental_table_alias
        self.primary_key_alias = primary_key_alias
        self.riid_generator_length = riid_generator_length
        self.test_campaign_name = test_campaign_name
        self.content_library_folder = content_library_folder
        self.api_version = api_version
        self.login_url = login_url

    @property
    def pod(self):
        """Get pod."""
        return self.__pod

    @pod.setter
    def pod(self, pod):
        """Set the pod.

        Only known pods are 2 and 5.
        """
        if str(int(pod)) in ['2', '5']:
            self.__pod = pod
        else:
            raise ValueError('Only pods 2 and 5 are supported.')

    @property
    def api_folder(self):
        """Get API folder."""
        return self.__api_folder

    @api_folder.setter
    def api_folder(self, api_folder):
        """Set the API folder."""
        self.__api_folder = api_folder

    @property
    def api_list(self):
        """Get API list."""
        return self.__api_list

    @api_list.setter
    def api_list(self, api_list):
        """Set API list."""
        self.__api_list = api_list

    @property
    def profile_extension_table_alias(self):
        """Get profile extension table alias."""
        return self.__profile_extension_table_alias

    @profile_extension_table_alias.setter
    def profile_extension_table_alias(self, profile_extension_table_alias):
        """Set profile extension table alias."""
        self.__profile_extension_table_alias = profile_extension_table_alias

    @property
    def supplemental_table_alias(self):
        """Get supplemental table alias."""
        return self.__supplemental_table_alias

    @supplemental_table_alias.setter
    def supplemental_table_alias(self, supplemental_table_alias):
        """Set supplemental table alias."""
        self.__supplemental_table_alias = supplemental_table_alias

    @property
    def primary_key_alias(self):
        """Get primary key alias."""
        return self.__primary_key_alias

    @primary_key_alias.setter
    def primary_key_alias(self, primary_key_alias):
        """Set primary key alias."""
        self.__primary_key_alias = primary_key_alias

    @property
    def riid_generator_length(self):
        """Get riid generator length."""
        return self.__riid_generator_length

    @riid_generator_length.setter
    def riid_generator_length(self, riid_generator_length):
        """Set riid generator length."""
        self.__riid_generator_length = riid_generator_length

    @property
    def test_email_address(self):
        """Get test email address."""
        return self.__test_email_address

    @test_email_address.setter
    def test_email_address(self, test_email_address):
        """Set test email address."""
        self.__test_email_address = test_email_address

    @property
    def test_campaign_name(self):
        """Get test campaign name."""
        return self.__test_campaign_name

    @test_campaign_name.setter
    def test_campaign_name(self, test_campaign_name):
        """Set test campaign name."""
        self.__test_campaign_name = test_campaign_name

    @property
    def content_library_folder(self):
        """Get content library folder."""
        return self.__content_library_folder

    @content_library_folder.setter
    def content_library_folder(self, content_library_folder):
        """Set content library folder."""
        self.__content_library_folder = content_library_folder

    @property
    def login_url(self):
        """Get the login URL."""
        return self.__login_url

    @login_url.setter
    def login_url(self, login_url):
        """Set the login URL."""
        self.__login_url = f'http://login{self.pod}.responsys.net/rest/api/v{self.api_version}/auth/token'

    @property
    def api_url(self):
        """API url partial."""
        return f'rest/api/v{self.api_version}'

    @api_url.setter
    def api_url(self, api_url):
        """API url partial setter."""
        return self.__api_url

    @property
    def api_version(self):
        """Get the API version."""
        return self.__api_version

    @api_version.setter
    def api_version(self, api_version):
        """Set the API version."""
        self.__api_version = api_version

    # login_url = f'http://login{pod}.responsys.net/rest/api/v{api_version}/'


def auto():
    """Load any secret.json file."""
    # traverse root directory looking for credentials
    for root, dirs, files in os.walk("."):
        for file in files:
            if file == 'secret.json':
                try:
                    with open(file) as f:
                        user_config = json.load(f)[0]
                        creds = Credentials(
                            user_name=user_config['user_name'],
                            password=user_config['password'],
                            email_address=user_config['email_address'])
                        return creds
                except:
                    raise ValueError(f'Could not open {file}')
