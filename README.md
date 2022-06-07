

To run project, use the following command from the source directory:

```
python run.py
```

----------------
TODO: 
- complete the database models
- later implementation of jwt authentication
- look for a way to use envars
- create first view in admin panel
- look about the deprecation errors
- create decorators for authentication (login_required)
- enhance the documentation, especially the README
    - add recommendations to create a env


----------------
temporary solution:
    The authentication what does is to instead of getting the jwt token, uses the password as token and checks if the user id corresponds to the user passwords in the header.