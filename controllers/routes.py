# Dictionary with all the routes/endpoints available in the project. This does not take into
# consideration the prefixes for each module. 
routes = {
  "home": "/",
  "auth": {
    "login": '/login',
    "register": '/register',
    "change": '/change-password',
    "logout": '/logout'
  },
  "admin": {
    "users": "/users",
    "logger": "/logger",
  },
  "analist": {
    "producers": "/producers",
    "producers-types": "/producers/types",
  },
  "harvests": {
    "portfolio": "/harvests",
    "purchases": "/purchases",
    "products": "/products",
  }
}