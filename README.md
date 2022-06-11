
To install the project, run:

```
pip install -r requirements.txt
```

To run project, use the following command from the source directory:

```
python run.py
```

If we want to run the tests of the project, use the following command:

```
python run.py --testing
```

----------------
TODO: 
- complete the database models
- later implementation of jwt authentication
- look for a way to use envars
- look about the deprecation errors
- enhance the documentation, especially the README
    - add recommendations to create a env
- in /admin/users/:
    - use disabled in all users if not admin, except for the current_user for fields that are not id or role
    - create FE and BE guard
    - form validation
- with the testing, see if there is concurrency problems and race conditions with server calls.
    - if such thing happens, use `sleep()` to avoid it
    - test if the logger is disabled
    - set a header for tests before starting


----------------
temporary solution:
    The authentication what does is to instead of getting the jwt token, uses the password and username as token