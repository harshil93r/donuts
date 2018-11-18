form = {
    'formA': {
        'status': "",
        'formFields': {
            'options': [
                {
                    'name': "painChart",
                    'label': "Pain Scale(1-5)",
                    'placeholder': "(1-5)",
                    'type': "TextInput",
                    'keyboardType': "phone-pad",
                    'validations': [
                        {
                            'type': "isRequired",
                            'errorMsg': "Party name is required"
                        },
                        {
                            'type': "isNumber",
                            'errorMsg': "Party name should be number"
                        }
                    ]
                },
                {
                    'name': "familyHistory",
                    'label': "Family Description",
                    'placeholder': "Family History of Diseases",
                    'type': "TextInput"
                },
                {
                    'name': "painHistory",
                    'label': "Days of Facing Pain",
                    'placeholder': 2,
                    'type': "TextInput",
                    'keyboardType': "phone-pad"
                }
            ]
        },
        'buttonList': {
            'options': [
                {
                    'name': "submit",
                    'label': "Submit",
                    'color': "#841584"
                }
            ]
        }
    }}