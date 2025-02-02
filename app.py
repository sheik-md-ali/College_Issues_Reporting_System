from website import create_app  # Import from the app package

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
