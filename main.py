from app import app

def main():
    app.get().run_server(debug=True)
    pass


if __name__ == '__main__':
    main()
