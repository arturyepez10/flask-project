from app import create_app

# start the server with the 'run()' method
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)