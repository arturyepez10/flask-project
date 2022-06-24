# Dictionary with all the routes/endpoints available in the project. This does not take into
# consideration the prefixes for each module. 
routes = {
  "home": "/",
  "auth": {
    "login": '/login',
    "register": '/register',
    "logout": '/logout'
  },
  "admin": {
    "users": "/users",
  },
  "analist": {
    "producers": "/producers",
    "producers-types": "/producers/types",
  }
}