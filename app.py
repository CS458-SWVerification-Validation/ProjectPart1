from app import create_app

app = create_app()

if __name__ == "__main__":
    print("app runss")
    app.run(host="127.0.0.1", ssl_context="adhoc")