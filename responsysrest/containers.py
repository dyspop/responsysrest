# TODO expose as a class with enums
rules = {
    'merge_or_update_members_in_a_profile_list_table' :
        [
            {
                'recordData' : {
                    'fieldNames' : [
                        'email_address_'
                        #'riid_',
                        #'mobile_number_',
                        #'email_address_'
                    ],
                    'records' : [
                        [
                            'a@b.c'
                            #'0123456', # RIID_
                            #'0123456789', # U.S. Ten-digit format phone number without dashes
                            #'a@b.c' # email address
                        ]
                    ],
                    'mergeTemplateName' : None
                },
                'mergeRule' : {
                    'htmlValue' : {
                        'default' : 'H',
                        'options' : [
                            'H',
                            'h',
                            'HTML',
                            'html',
                            'Html',
                            'HTM',
                            'htm',
                            'Htm'
                        ]
                    },
                    'optinValue' : {
                        'default' : 'I',
                        'options' : [
                            'I',
                            'i',
                            '1'
                        ]
                    },
                    'textValue' : {
                        'default' : 'T',
                        'options' : [
                            'T',
                            't',
                            'TEXT',
                            'text',
                            'Text',
                            'TXT',
                            'txt',
                            'Txt'
                        ]
                    },
                    'insertOnNoMatch' : {
                        'default' : True,
                        'options' : [
                            True,
                            False
                        ]
                    },
                    'updateOnMatch' : {
                        'default' : 'REPLACE_ALL',
                        'options' : [
                            'NO_UPDATE',
                            'REPLACE_ALL'
                        ]
                    },
                    'matchColumnName1' : {
                        'default' : 'RIID_',
                        'options' : [
                            'RIID_',
                            'CUSTOMER_ID_',
                            'EMAIL_ADDRESS_',
                            'MOBILE_NUMBER_',
                            'EMAIL_MD5_HASH_', # this shouldn't be an option!
                            'EMAIL_SHA256_HASH_'
                        ]
                    },
                    'matchColumnName2' : {
                        'default' : None,
                        'options' : [
                            None,
                            'RIID_',
                            'CUSTOMER_ID_',
                            'EMAIL_ADDRESS_',
                            'MOBILE_NUMBER_',
                            'EMAIL_MD5_HASH_', # this shouldn't be an option!
                            'EMAIL_SHA256_HASH_'
                        ]
                    },
                    # 'matchColumnName3' : {
                    #     'default' : None,
                    #     'options' : [
                    #         None
                    #     ] # deprecated
                    # },
                    'matchOperator' : {
                        'default' : 'NONE',
                        'options' : [
                            'NONE',
                            'AND'
                        ]
                    },
                    'optoutValue' : {
                        'default' : 'O',
                        'options' : [
                            'O',
                            'o',
                            '0'
                        ]
                    },
                    'rejectRecordIfChannelEmpty' : {
                        'default' : None,
                        'options' : [
                            None,
                            'E', # Email
                            'M', # Mobile
                            'P', # Postal address
                            'E,M', # Email or Mobile
                            'E,P', # Email or Postal
                            'M,E', # Mobile or Email
                            'M,P', # Mobile or Postal
                            'E,M,P', # Email, Mobile or Postal
                            'E,P,M', # Email, Postal or Mobile
                            'M,E,P', # Mobile, Email or Postal
                            'M,P,E', # Mobile, Postal or Email
                            'P,E,M', # Postal, Email or Postal
                            'P,M,E' # Postal, Mobile or Email
                        ]
                    },
                    'defaultPermissionStatus' : {
                        'default' : 'OPTIN',
                        'options' : [
                            'OPTIN',
                            'OPTOUT'
                        ]
                    }
                }
            }
        ],
        'query_attributes_allowed' : [
            'r', # RIID
            'e', # EMAIL_ADDRESS
            'c', # CUSTOMER_ID
            'm'  # MOBILE_NUMBER
        ]
    }
