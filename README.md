# marshmallow_more_dot_delimiters

This is a simple python helper module, which allows using more than 2 delimiters, to specify which fields to nest.

# Usage

<h3>get_results</h3>

###
    # Define the model - same as with normal marshmallow usage
    user = User(name="Monty", email="monty@python.org", friends=[...])

    # get results by passing the SchemaClass, the model and a list of fields, where nested entities and properties are separated by dot delimeters
    res = get_results(UserSchema, user, ["name", "friends.user.name", "friends.user.friends.user.name"])
###

<h3>get_results_from_custom_schema</h3>

As get_results does not support any fields to be excluded with using the exlude parameter, you can declare the schema outside, pass the schema instance as an argument.

###
    # Define the model - same as with normal marshmallow usage
    user = User(name="Monty", email="monty@python.org", friends=[...])

    # Declare the schema
    schema = UserSchema(exclude=("friends.user.name"))

    # get results by passing the schama instance, the model and a list of fields, where nested entities and properties are separated by dot delimeters
    res = get_results_from_custom_schema(schema, user, ["name", "friends.user.friends.user.name"])
###

# Results

For example, the following:
###
        res = get_results(UserSchema, user, ["name", "friends.user.name", "friends.user.friends.user.name"])
###

Could return the following:

###
    {
        results: {
            name: "User's Name", 
            friends: [ 
                { 
                    user : { 
                        name : "Friend 1",
                        friends: [
                            { 
                                user : {
                                    name : "Friend11 of Friend1",
                                }
                            },
                            { 
                                user : {
                                    name : "Friend12 of Friend1",
                                }
                            }
                        ]
                    }
                },
                { 
                    user : { 
                        name : "Friend 2",
                        friends: [
                            { 
                                user : {
                                    name : "Friend21 of Friend2",
                                }
                            }
                        ]
                    }
                },
                { 
                    user : { 
                        name : "Friend 3",
                        friends: []
                    }
                }
            ]
        }
    }
###

# Errors

If the query had resulted in an error, then something like this will be returned:

| Code | Description |
|-----| ----------- |
| 1   |  Fields are incorrect       |

###
    {
        results: None,
        errors : [{
            code: 1,
            message : "Fields are incorrect"
        }]
    }
###

Note: currently there is just one error supported, so errors will be an array of a single element. That said, I will be working on more descriptive and informative errors.

Note: this module works with marshmallow, as well as any derivatives of marshmallow, such as Marshmallow-SQLAlchemy.