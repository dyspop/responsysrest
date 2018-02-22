"""How we configure our Interact Client connection."""
import os
import json

class Configuration:
    """How our client is configured."""

    def __init__(
            self,
            pod,
            api_folder,
            api_list,
            profile_extension_table_alias,
            supplemental_table_alias,
            primary_key_alias,
            riid_generator_length,
            test_campaign_name,
            content_library_folder,
            api_version,
            login_url=''
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

    def __repre__(self):
        """Text representation."""
        return "Configuration"

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


def from_json(f):
    """Load configuration from json."""
    with open(f) as f:
        user_config = json.load(f)
        config = Configuration(
            pod=user_config['pod'],
            api_folder=user_config['api_folder'],
            api_list=user_config['api_list'],
            profile_extension_table_alias=user_config['profile_extension_table_alias'],
            supplemental_table_alias=user_config['supplemental_table_alias'],
            primary_key_alias=user_config['primary_key_alias'],
            riid_generator_length=user_config['riid_generator_length'],
            test_campaign_name=user_config['test_campaign_name'],
            content_library_folder=user_config['content_library_folder'],
            api_version=user_config['api_version']
        )
        return config


def auto():
    """Load any config.json file."""
    # traverse root directory looking for credentials
    for root, dirs, files in os.walk("."):
        for f in files:
            if f == 'config.json':
                try:
                    return from_json(f)
                except(ValueError):
                    raise ValueError(f'Could not open {f}')
                break
