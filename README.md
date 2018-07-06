# Responsys Interact REST API python client #

A python library providing access to the Responsys Interact API. Currently supports version 1.3 Release 6.33 E65150-15.


## Requirements

1. A Responsys Interact account (see How-to).
2. A valid Responsys Interact API user name and password.
3. Python (see How-to)
4. pip (see How-to)

### How-to

Sign up for Responsys Interact at https://www.oracle.com/marketingcloud/products/cross-channel-orchestration/index.html (not free).

Install Python3 and Python Package Index. 
  * OS X: It is recommended to install Python3 this way: http://docs.python-guide.org/en/latest/starting/install3/osx/ which should alias your Python3 to separate command `python3`.

This package is developed for Python3.x but should work on 2.7 if you're so inclined.

## Install ##

### Standard install for using in your application

    pip install git+https://@github.com/dyspop/responsysrest.git@0.1.7

### Development install via repository clone
1. Clone this repo:
    git clone git@github.com:dyspop/responsysrest.git
2. Create Virtual Environment
    cd responsysrest && virtualenv env && source env/bin/activate
2. Install via source package in development mode:
```
    pip install -e .
```

## Usage ##

1. Import the responsysrest package
2. Configure your Interact connection settings and credentials
3. Instantiate the client
4. Use the client

The quickest way to get started is to create a `config.json` file and a `secret.json` file with your configuration and credentials information in them. The package comes with the `config.json` file but you'll need to create your own `secret.json` file. You can call the auto function from the package sub modules `configuration` and `credentials` which will traverse the root looking for the json files.

config.json boilerplate:

    {
        "pod": "5",
        "api_folder": "___api-generated",
        "api_list": "API_testing",
        "profile_extension_table_alias": "_pet",
        "supplemental_table_alias": "_supp",
        "primary_key_alias": "_primary_key",
        "riid_generator_length": 11,
        "test_campaign_name": "test_api_classic",
        "test_content_library_folder": "___api-generated-test",
        "content_library_folder": "___api-generated-cl",
        "api_version": "1.3"
    }

secret.json boilerplate:

    {
        "user_name": "team_member",
        "password": "1!Aa",
        "email_address": "team_member@company.com"
    }

then if they're local to where you're running python from:

    import responsysrest as r
    client = r.Client(r.configuration.auto(), r.credentials.auto())

If not then the package can import them from json files:

    config = r.configuration.from_json('path/to/config.json')
    creds = r.credentials.from_json('path/to/secret.json')

Then instantiate the client:

    client = r.Client(config, creds)

If you're in an application context you can directly configure your client by passing the following values

    client = r.Client(
        pod='2',
        api_folder='folder_name',
        api_list='api_list',
        profile_extension_table_alias='pet_alias',
        supplemental_table_alias='supp_alias',
        primary_key_alias='pk_alias',
        riid_generator_length=11,
        test_campaign_name='testtest',
        content_library_folder='clsubfolder',
        api_version='1.3')

| Property  | Value  |
|---|---|
| pod  | string, `2` or `5`  |
| api_folder  | string  |
| api_list  | string  |
| profile_extension_table_alias  | string  |
| supplemental_table_alias  | string  |
| primary_key_alias  | string  |
| riid_generator_length  | integer  |
| test_campaign_name  | string  |
| content_library_folder  | string  |
| api_version  | string  |


## Client functions usage:

Generally the library wants lists of records per function call where appropriate. To apply a method to a series of records do this:

    imported_csv_data = [
        ['EMAIL_ADDRESS_', 'COUNTRY_'],
        ['hey@test.com', 'US']
    ]
    fields = imported_csv_data[0]
    records = imported_csv_data[1:]
    client.some_method(fields, records)

Don't do this:

    for record in records:
        client.some_method(fields, [record])


### Managing Profile List Tables


#### Retrieving all profile lists for an account

    client.get_profile_lists()
  
Returns a list of dictionaries of all profile lists:

    [
        {
            'fields': [
                {'fieldName': 'RIID_', 'fieldType': 'INTEGER'},
                {'fieldName': 'CREATED_SOURCE_IP_', 'fieldType': 'STR255'},
                {'fieldName': 'CUSTOMER_ID_', 'fieldType': 'STR255'},
                {'fieldName': 'EMAIL_ADDRESS_', 'fieldType': 'STR500'},
                {'fieldName': 'EMAIL_DOMAIN_', 'fieldType': 'STR255'},
                {'fieldName': 'EMAIL_ISP_', 'fieldType': 'STR255'},
                {'fieldName': 'EMAIL_FORMAT_', 'fieldType': 'CHAR'},
                {'fieldName': 'EMAIL_PERMISSION_STATUS_', 'fieldType': 'CHAR'},
                {'fieldName': 'EMAIL_DELIVERABILITY_STATUS_', 'fieldType': 'CHAR'},
                {'fieldName': 'EMAIL_PERMISSION_REASON_', 'fieldType': 'STR255'},
                {'fieldName': 'MOBILE_NUMBER_', 'fieldType': 'STR25'},
                {'fieldName': 'MOBILE_COUNTRY_', 'fieldType': 'STR25'},
                {'fieldName': 'MOBILE_PERMISSION_STATUS_', 'fieldType': 'CHAR'},
                {'fieldName': 'MOBILE_DELIVERABILITY_STATUS_', 'fieldType': 'CHAR'},
                {'fieldName': 'MOBILE_PERMISSION_REASON_', 'fieldType': 'STR255'},
                {'fieldName': 'POSTAL_STREET_1_', 'fieldType': 'STR255'},
                {'fieldName': 'POSTAL_STREET_2_', 'fieldType': 'STR255'},
                {'fieldName': 'CITY_', 'fieldType': 'STR50'},
                {'fieldName': 'STATE_', 'fieldType': 'STR50'},
                {'fieldName': 'POSTAL_CODE_', 'fieldType': 'STR25'},
                {'fieldName': 'COUNTRY_', 'fieldType': 'STR50'},
                {'fieldName': 'POSTAL_PERMISSION_STATUS_', 'fieldType': 'CHAR'},
                {'fieldName': 'POSTAL_DELIVERABILITY_STATUS_', 'fieldType': 'CHAR'},
                {'fieldName': 'POSTAL_PERMISSION_REASON_', 'fieldType': 'STR255'},
                {'fieldName': 'CREATED_DATE_', 'fieldType': 'TIMESTAMP'},
                {'fieldName': 'MODIFIED_DATE_', 'fieldType': 'TIMESTAMP'},
                {'fieldName': 'MY_CUSTOM_FIELD', 'fieldType': 'STR500'}
            ],
            'folderName': 'UIfolderNotContentLibraryFolder',
            'name': 'LIST_NAME'
        },
        {
            'fields': [
                {'fieldName': 'RIID_', 'fieldType': 'INTEGER'},
                {'fieldName': 'CREATED_SOURCE_IP_', 'fieldType': 'STR255'},
                {'fieldName': 'CUSTOMER_ID_', 'fieldType': 'STR255'},
                {'fieldName': 'EMAIL_ADDRESS_', 'fieldType': 'STR500'},
                {'fieldName': 'EMAIL_DOMAIN_', 'fieldType': 'STR255'},
                {'fieldName': 'EMAIL_ISP_', 'fieldType': 'STR255'},
                {'fieldName': 'EMAIL_FORMAT_', 'fieldType': 'CHAR'},
                {'fieldName': 'EMAIL_PERMISSION_STATUS_', 'fieldType': 'CHAR'},
                {'fieldName': 'EMAIL_DELIVERABILITY_STATUS_', 'fieldType': 'CHAR'},
                {'fieldName': 'EMAIL_PERMISSION_REASON_', 'fieldType': 'STR255'},
                {'fieldName': 'MOBILE_NUMBER_', 'fieldType': 'STR25'},
                {'fieldName': 'MOBILE_COUNTRY_', 'fieldType': 'STR25'},
                {'fieldName': 'MOBILE_PERMISSION_STATUS_', 'fieldType': 'CHAR'},
                {'fieldName': 'MOBILE_DELIVERABILITY_STATUS_', 'fieldType': 'CHAR'},
                {'fieldName': 'MOBILE_PERMISSION_REASON_', 'fieldType': 'STR255'},
                {'fieldName': 'POSTAL_STREET_1_', 'fieldType': 'STR255'},
                {'fieldName': 'POSTAL_STREET_2_', 'fieldType': 'STR255'},
                {'fieldName': 'CITY_', 'fieldType': 'STR50'},
                {'fieldName': 'STATE_', 'fieldType': 'STR50'},
                {'fieldName': 'POSTAL_CODE_', 'fieldType': 'STR25'},
                {'fieldName': 'COUNTRY_', 'fieldType': 'STR50'},
                {'fieldName': 'POSTAL_PERMISSION_STATUS_', 'fieldType': 'CHAR'},
                {'fieldName': 'POSTAL_DELIVERABILITY_STATUS_', 'fieldType': 'CHAR'},
                {'fieldName': 'POSTAL_PERMISSION_REASON_', 'fieldType': 'STR255'},
                {'fieldName': 'CREATED_DATE_', 'fieldType': 'TIMESTAMP'},
                {'fieldName': 'MODIFIED_DATE_', 'fieldType': 'TIMESTAMP'},
                {'fieldName': 'MY_CUSTOM_FIELD', 'fieldType': 'STR500'}
            ],
            'folderName': 'UIfolderNotContentLibraryFolder',
            'name': 'LIST_NAME_2'
        }
    ]

This comes bundled with the folder location and all of the field names too, so to retrieve just a list of the lists:

    profile_lists = client.get_profile_lists()
    [list["name"] for list in profile_lists] 

returns: 

    ['LIST_NAME', 'LIST_NAME_2']

or a list of the lists with their respective folders:

    [(list["name"], list["folderName"]) for list in profile_lists]

returns:

    [('LIST_NAME', 'UIfolderNotContentLibraryFolder'), ('LIST_NAME_2', 'UIfolderNotContentLibraryFolder')]


#### Update profile list

This is the "Merge or update members in a profile list table" feature. 

    list_name = 'myTestList'
    fields = ['EMAIL_ADDRESS_', 'FIRST_NAME']
    records = ['bob@somesite.com', 'bob']
    client.update_profile_list(list_name, fields, records)

It requires three positional arguments: `list_name`, `fields`, and `records`. The library doesn't do any checking on the input. If the client can connect to Responsys you'll get a somewhat helpful error from the API:

```
client.update_profile_list(
    'fakelist', ['notafield'], ['notarecord'])
```
```
{
    'type': '', 
    'title': 'List not found', 
    'errorCode': 'LIST_NOT_FOUND', 
    'detail': 'fakelist List Not Found', 
    'errorDetails': []
}
```

Responsys wants a lot of contextual information to merge records into an existing list, so this library has chosen defaults for you. 

These can be changed with keyword arguments. Here are all the keyword arguments with all of the default values passed in redundantly. You don't need to set any of these unless you're changing them from the default values below:

    client.update_profile_list(
        list_name,
        fields,
        records)
        html_value='H',
        optin_value='I',
        text_value='T',
        insert_on_no_match=True,
        insert_on_match='REPLACE_ALL',
        match_column_name1='RIID_',
        match_column_name2=None,
        match_operator='NONE',
        opt_out_value='O',
        reject_records_if_channel_empty=None,
        default_permission_status='OPTIN')

Note that whatever records you send in must contain a field in the fields list equal to the `match_column_name1` value (`RIID_` by default). For that reason a common profile list update might look like:

    client.update_profile_list(
        list_name,
        fields,
        records,
        match_column_name1='EMAIL_ADDRESS_')

or

    client.update_profile_list(
        list_name,
        fields,
        records,
        match_column_name1='CUSTOMER_ID_')    


#### Retrieve a member of a profile list using RIID

    client.get_member_of_list_by_riid(list_name, riid)

Returns a full record if it's in the list.


#### Retrieve a member of a profile list based on query attribute

    client.get_member_of_list_by_attribute(
        list_name, record_id, query_attribute, fields)

Returns the record data for the record provided. Requires `list_name`, `record_id`. The list name is that which you want to find the record from within your Responsys Interact instance. The record id is the specific id you wish to use to identify the record. The query attribute is the type of id that you are using to retreive the record. If you don't specify it's assumed to be Customer ID. The available options are:

| Option  | Meaning  |
|---|---|
| r  | RIID  |
| e  | Email Address  |
| c  | Customer ID  |
| m  | Mobile Number  |

The fields to return should be a python list data object, if left blank it will return all the fields:

    fields = ['EMAIL_DOMAIN_, FIRST_NAME']
    query_attribute = 'e'
    record_id = 'test@test.com'
    client.get_member_of_list_by_attribute(
        list_name, record_id, query_attribute, fields)



#### Delete Profile List Recipients based on RIID

    client.delete_from_profile_list(list_name, riid)

Delets a record from a profile list. Examples:

    client.delete_from_profile_list('CONTACTS_LIST', 'a@b.c')



### Managing Profile Extension Tables


#### Retrieve all profile extentions of a profile list

    client.get_profile_extensions_for_list(list_name)

Returns the profile extension tables (also known as profile extensions, profile extenion lists, or PETs) associated with a given list. This comes bundled with the folder location and all of the field names too, so to retrieve just a list of the lists, or a list of the lists with their respective folders use:

    pets = client.get_profile_extensions_for_list(list_name)
    [list['profileExtension']['objectName'] for list in pets]
    [(list['profileExtension']['objectName'],
        list['profileExtension']['folderName']) for list in pets]


#### Create a new profile extension table

Creates a new profile extension table. Requires only the list name you wish to extend, but this will create a blank profile extension table using default a folder locations and name (from on your client configuration).

    client.create_profile_extension(list_name)

Examples:

    client.create_profile_extension('CONTACTS_LIST')

If you've used the defaults from the boilerplate config this creates a `CONTACTS_LIST_pet` profile extension table extending `CONTACTS_LIST` in the UIfolder specified by your client configuration (default is `___api-generated`) with no records and no non-default fields.

You can also specify the extension you want to use, but this function is opinionated and will only let you create a profile extension table that begins with the name of the profile list that is being extended.

This example will create an empty profile extension table extending `CONTACTS_LIST` called `CONTACTS_LIST-Profile_Extension`:

    client.create_profile_extension(
        'CONTACTS_LIST', extension_name='-Profile_Extension')

You can specify the folder to place it in to override your client configuration:

    client.create_profile_extension(
        'CONTACTS_LIST', folder_name='OtherFolder')

Additionally you can supply fields as a list:

    client.create_profile_extension(
        'CONTACTS_LIST', fields=['LTV_v1', 'LTV_v2', 'decile'])

If you don't specify a (Responsys Interact) data type for each it will default to `STR4000`. This default data type can be overridden with one of `STR500`, `STR4000`, `INTEGER`, `NUMBER`, or `TIMESTAMP`:

    fields = ['last_purchased_date', 'first_purchased_date']
    client.create_profile_extension(
        'CONTACTS_LIST', fields=fields, default_field_type='TIMESTAMP')

You can also specify the field type of each within the list if you supply it as a list or tuple:

    fields = [
        ('last_purchased_date','TIMESTAMP'),
        ('lifetime_purchases', 'INTEGER')
    ]
    client.create_profile_extension(
        'CONTACTS_LIST', fields=fields)

The default field type override can be supplied alongside individual fields without their own field type specifications:

    fields = [
        ('probability_of_login', 'NUMBER'),
        'CUSTOMER_ID_',
        ('ARTICLE_CONTENTS','STR4000')
    ]
    client.create_profile_extension(
        'CONTACTS_LIST', fields=fields, default_field_type='STR500')



#### Retrieve a member of a profile extension table based on RIID

Returns a full record if it's in the profile extension table.

    client.get_member_of_profile_extension_by_riid(
        list_name, pet_name, riid)

Also takes an optional argument `fields` which defaults to `all` if not specified. Examples:

    client.get_member_of_profile_extension_by_riid(
        'CONTACTS_LIST', 'CONTACTS_LIST_pet', '101234567890')

or

    client.get_member_of_profile_extension_by_riid(
        'CONTACTS_LIST',
        'CONTACTS_LIST_pet',
        '101234567890',
        fields='FIRST_NAME, LAST_PURCHASE_DATE')


#### Retrieve a member of a profile extension table based on a query attribute

    client.get_member_of_profile_extension_by_attribute(
        list_name, pet_name record_id, query_attribute, fields)

Takes five arguments, but requires `list_name`, `pet_name` and `record_id`. The list name is that which you want to find the record from in your Responsys Interact instance. The record id is the specific id you wish to use to identify the record. The query attribute is the type of id that you are using to retreive the record. The available options are `r` for RIID, `e` for EMAIL_ADDRESS, `c` for CUSTOMER_ID and `m` for MOBILE_NUMBER. The fields to return python list data object of the fields in the list, if left blank it will return all the fields.

Examples:

    client.get_member_of_profile_extension_by_attribute(
        'AFFILIATES', '1234251', 'c', ['email_address_', 'first_name'])


#### Delete a member of a profile extension table based on RIID

Deletes a member of a profile extension table based on RIID if it exists.

    client.delete_member_of_profile_extension_by_riid(
        list_name, pet_name, riid):



### Managing Supplemental Tables


#### Create a new supplemental table


Creates a new supplemental table. Requires only a table name, but this will create a blank supplemental table using default a folder location and name.

Examples:

    client.create_supplemental_table(
        'CONTACTS_LIST', fields=['field1','field2'])

This creates a `CONTACTS_LIST_supp` supplemental table in a folder named from your client configuration (default is `___api-generated`) with no records and no non-default fields. You must specify either a list with at least one field or a primary key that is one of the Responsys internal field names. If you do not specify a primary key the wrapper will use the first field in the input list because the API requires a primary key field. You can also specify an optional data extraction key.

    client.create_supplemental_table(
        supplemental_table_name, folder_name, fields=fields)

or

    client.create_supplemental_table(
        supplemental_table_name, folder_name, primary_key=primary_key)

The wrapper writes all fields with a default field type, which is `STR500` unless another type is specified. If the default type is specified it will use that type for all fields.

Examples:

    client.create_supplemental_table(
        'my_supp_table',
        'API_testing',
        fields=['field1', 'field2'],
        default_field_type='STR25',
        data_extraction_key='field2',
        primary_key='field1')




### Managing Campaigns


#### Get all EMD Campaigns

    client.get_campaigns()

Returns a dictionary of campaigns and their data, along with links and their data:

    'campaigns': [
        {
            'id': 12345678, 
            'name': 'API_Test', 
            'folderName': '___api-generated-cl', 
            'type': 'EMAIL', 
            'purpose': 'PROMOTIONAL', 
            'listName': 'CONTACTS_LIST', 
            'proofListPath': 'testing/Prooflist', 
            'seedListPath': 'testing/Seedlist', 
            'htmlMessagePath': '/contentlibrary/campaigns/___api-generated-cl/document.htm', 
            'enableLinkTracking': False, 
            'enableExternalTracking': False, 
            'subject': 'This is a test message', 
            'fromName': 'Company', 
            'fromEmail': 'email@company.com', 
            'replyToEmail': 'support@company.com', 
            'useUTF8': True, 
            'locale': 'en', 
            'trackHTMLOpens': True, 
            'trackConversions': True, 
            'sendTextIfHTMLUnknown': False, 
            'unsubscribeOption': 'OPTOUT_SINGLE_CLICK', 
            'autoCloseOption': 'AUTO_CLOSE_X_DAYS_AFTER_LAST_RESPONSE', 
            'autoCloseValue': '30', 
            'links': [
                {
                'rel': 'self', 
                'href': '/rest/api/v1.3/campaigns/API_Test', 
                'method': 'GET'
                }
                , 
                {
                'rel': 'update', 
                'href': '/rest/api/v1.3/campaigns/API_Test', 
                'method': 'PUT'
                }
                , 
                {
                'rel': 'create', 
                'href': '/rest/api/v1.3/API_Test', 
                'method': 'POST'
                }
            ]
        }
    ]


To see a list of just campaigns:

    campaigns = client.get_campaigns()['campaigns']
    [campaign['name'] for campaign in campaigns]


or a list of campaigns and their respective folders:
    campaigns = client.get_campaigns()['campaigns']
    [(campaign['name'], campaign['folderName']) for campaign in campaigns]

#### Get all Push Campaigns

    client.get_push_campaigns()

Returns a list of push campaigns and their associated data.


### Managing Content

You'll notice the files we use are `.htm`. It is Responsys's nature to change `.html` to `.htm` silently on upload. It is recommended to simply create all of your files with `.htm` to comply, otherwise you might end up with duplicates in your local copies if you're pulling files out. In fact, the wrapper won't allow .html files. 



#### Create Folder

Creates a folder in the content library (`/contentlibary/`).

    client.create_folder('new_folder')

Creates a folder `/contentlibarary/new_folder` in the Content Library.

If you don't specify a folder the wrapper will default to the API folder name configured for your client. The boilerplate default is `___api-generated`. 


#### Create Content Library Document

Creates a document in the content library (`/contentlibary/`). Takes a document system path, not document data or other protocol path.

    client.create_document('path/to/document.htm')

You can specify a folder but it will become a content library subfolder:

    client.create_document('local/path/to/document.htm', 'arbitrary/folder/path')

This should create (if you're on pod 5):

    https://interact5.responsys.net/suite/c#!liveViewEditor/%2Fcontentlibrary%2Farbitrary%2Ffolder%2Fpath/document%2Ehtm

If you don't specify a folder the wrapper will default to the API folder name configured for your client. The boilerplate default is `___api-generated-cl`. 


#### Get Content Library Document

Gets the document path, content, and REST CRUD links for a content library document:

    client.get_document('document.htm')

returns:

    {
        'documentPath': '/contentlibrary/___api-generated-cl/document.htm', 
        'content': '<html>\n    <head>\n        <title>Test Document</title>\n    </head>\n    <body>\n        <h1>Test Document</h1>\n    </body>\n</html>\n', 
        'links': [
            {
                'rel': 'self', 
                'href': '/rest/api/v1.3/clDocs/contentlibrary/___api-generated-cl/document.htm', 
                'method': 'GET'
            }, 
            {
                'rel': 'deleteDocument', 
                'href': '/rest/api/v1.3/clDocs/contentlibrary/___api-generated-cl/document.htm', 
                'method': 'DELETE'
            }, 
            {
                'rel': 'setDocumentContent', 
                'href': '/rest/api/v1.3/clDocs/contentlibrary/___api-generated-cl/document.htm', 
                'method': 'POST'
            }, 
            {
                'rel': 'createDocument', 
                'href': '/rest/api/v1.3/clDocs', 
                'method': 'POST'
            }
        ]
    }


#### Update Content Library Document

Updates a document in `/contentlibrary/` if it's already there. Takes a document system path, not document data or other protocol path.

    client.update_document('local/path/to/document.htm')

returns:

    {
        'documentPath': '/contentlibrary/__api-generated-cl/document.htm', 
        'content': None, 
        'links': [
            {
                'rel': 'self', 
                'href': '/rest/api/v1.3/clDocs/contentlibrary/__api-generated-cl/document.htm',
                'method': 'POST'
            },
            {
                'rel': 'getDocumentContent',
                'href': '/rest/api/v1.3/clDocs/contentlibrary/__api-generated-cl/document.htm',
                'method': 'GET'
            },
            {
                'rel': 'deleteDocument',
                'href': '/rest/api/v1.3/clDocs/contentlibrary/__api-generated-cl/document.htm',
                'method': 'DELETE'
            },
            {
                'rel': 'createDocument',
                'href': '/rest/api/v1.3/clDocs',
                'method': 'POST'
            }
        ]
    }

You can also specify the destination contentlibrary subfolder:

    client.update_document(
        'local/path/to/document.htm',
        'path/to/interact/contentlibrary/subfolder')

    {
        'documentPath': '/contentlibrary/path/to/interact/contentlibrary/subfolder/document.htm', 
        'content': None, 
        'links': [
            {
                'rel': 'self', 
                'href': '/rest/api/v1.3/clDocs/contentlibrary/path/to/interact/contentlibrary/subfolder/document.htm',
                'method': 'POST'
            },
            {
                'rel': 'getDocumentContent',
                'href': '/rest/api/v1.3/clDocs/contentlibrary/path/to/interact/contentlibrary/subfolder/document.htm',
                'method': 'GET'
            },
            {
                'rel': 'deleteDocument',
                'href': '/rest/api/v1.3/clDocs/contentlibrary/path/to/interact/contentlibrary/subfolder/document.htm',
                'method': 'DELETE'
            },
            {
                'rel': 'createDocument',
                'href': '/rest/api/v1.3/clDocs',
                'method': 'POST'
            }
        ]
    }

This method's response from Responsys notably omits the content, you must call the `get_document()` method to get the content.



#### Delete Content Library Document

Try to delete a document from `/contentlibrary/`. Takes only a full path with the document file name in it. The path is the path of the document in Interact, not a local file path:

    client.delete_document(
        'interact/contentlibrary/external/path/to/document.html')

Unlike the opinionated create and get and update methods, you can try to delete anything from the content library even at the (content library) root. If you've managed to load a file into the content library you should be able to delete it.



### Sending Messages

There are a number of types of messages you can send with Responsys via API and methods available. For now we just implement Send Email Message.


#### Send Email Message

This wrapper requires each call to this function to target a single message but allow for any number of recipients and any amount of optional data to be passed along with each recipient. It only accepts email address as the ID type.

    client.send_email_message(
        recipients, responsys_target_folder, responsys_target_campaign_name)

`recipients` can be either a string or a list of strings. The wrapper will take any but Responsys will fail/reject invalid addresses. The following are all valid as the `recipients` argument (as far as the wrapper is concerned), but the third example should return an error from the Responsys response:

    'team_member@company.com'
    ['team_member@company.com', 'team_member2@company.com']
    ['team_member@company.com', 'team_member2@company.com', 42]

Messages will only be sent if the recipient exists in the target list. The target list must be configured from the campaign dashboard in the Responsys UI. If the recipient doesn't exist in the target list for the target campaign then a failure response will be returned from the Responsys API for that item in the list.

You can also pass optional data to be used within the campaign build, whether it be used in classic or EMD campaigns. This is done with a dictionary for one recipient:

    client.send_email_message(
        'team_member@company.com',
        'myfolder',
        'mycampaign',
        {
            'FIELD1': 'Value1',
            'FIELD2': 'Value2'
        }
    )

or a list of dictionaries for multiple recipients:

    recipients = ['team_member@company.com', 'team_member2@company.com']
    optional_data = [
        {
            'FIELD1': 'foo',
            'FIELD2': 'bar'
        },
        {
            'FIELD1': 'ham',
            'FIELD2': 'eggs'
        }
    ]

The length of the recipients list and the optional data key/value pairs must match or the wrapper will return an error.

Note that the key don't need to match:

    recipients = ['team_member@company.com', 'team_member2@company.com']
    optional_data = [
        {
            'FIELD1': 'foo',
            'FIELD2': 'bar'
        },
        {
            'FIELD1': 'ham',
            'OTHER_FIELD': 'bazinga'
            'YET_ANOTHER_FIELD': 'Batman!'
        }
    ]

But be careful, you'll need to pass an empty dictionary if you have a recipient to receive no optional data mixed in with recipients who do receive optional data:

    recipients = [
        'team_member@company.com',
        'team_member2@company.com',
        'otherperson@othercompany.net',
        'someonesfriend@friendlypeople.biz'
        ]
        optional_data = [
            {
                'FIELD1': 'foo',
                'FIELD2': 'bar'
            },
            {
                'FIELD1': 'baz',
                'FIELD2': 'bazoink'
            },
            {},
            {
                'FIELD1': 'spam',
                'FIELD2': 'bacon'
            },
        ]

It can sometimes be easier to pass in `None` or an empty string:

    recipients = [
        'team_member@company.com',
        'team_member2@company.com',
        'otherperson@othercompany.net',
        'someonesfriend@friendlypeople.biz'
        ]
        optional_data = [
            {
                'FIELD1': 'foo',
                'FIELD2': 'bar'
                'FIELD3': None
            },
            {
                'FIELD1': 'baz',
                'FIELD2': None,
                'FIELD3': 'flamingo'
            },
            {
                'FIELD1': None,
                'FIELD2': None,
                'FIELD3': None
            },
            {
                'FIELD1': '',
                'FIELD2': 'bacon',
                'FIELD3': 'flamenco'
            },
        ]



### Non-native features

There are a few things you might want to do with the API that are a little hard based on arbitrary endpoint calls. The wrapper provides you this piece of candy.


#### Get lists for record

    client.get_lists_for_record(riid)

Loops through every list and checks to see if the record is in the list. If the record is in the list it adds it to the returned object. This is very slow, but sometimes you want to know what lists a member is in.



## Development/Testing ##

If you're looking to contribute then your best best is to get your client configured properly (get `tests/test_1user_configs.py` passing) then get a list of missing features from:
    python3 -m pytest responsysrest/tests/test_2client.py

Currently there are 25/52 features implemented. 

Running all tests or just the client tests will attempt to fire a test message to the client's credentials email address. The test message must be configured manually in the Interact UI. It can be any content and the name for it is configured in the `config.json` file:

    {
        ...
        "test_campaign_name": "test_api_classic",
        ...
    }


To run configuration and integration tests:

    pytest

To run configuration tests:

    python -m pytest responsysrest/tests/test_1user_configs.py

To run client/API integration tests only:

    python -m pytest responsysrest/tests/test_2client.py

To run extra features tests only:

    python -m pytest responsysrest/tests/test_3extras.py


## Acknowledgements ##

This library was developed inspired by the SOAP client on pypi as ```responsys```. 
🙇 Oracle for the heavy lifting building and maintaining their API.

## Legal ##

This code is neither officially supported nor endorsed by Oracle, Responsys, or any related entities.
