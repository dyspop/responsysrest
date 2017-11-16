containers = {
    "merge_or_update_members_in_a_profile_list_table" :
        [{
            "recordData" : {
                "fieldNames" : [
                    #"riid_",
                    #"mobile_number_",
                    #"email_address_"
                ],
                "records" : [
                    [
                        #"0123456",
                        #"0123456789",
                        #"a@b.c"
                    ],
                    [
                        #"0123456",
                        #"0123456789",
                        #"a@b.c"
                    ]
                ],
                "mergeTemplateName" : None
            },
            "mergeRule" : {
                "htmlValue" : "H",
                "optinValue" : "I",
                "textValue" : "T",
                "insertOnNoMatch" : True,
                "updateOnMatch" : "REPLACE_ALL",
                "matchColumnName1" : "RIID_",
                "matchColumnName2" : None,
                "matchOperator" : "NONE",
                "optoutValue" : "O",
                "rejectRecordIfChannelEmpty" : None,
                "defaultPermissionStatus" : "OPTIN"
            }

        }]
}