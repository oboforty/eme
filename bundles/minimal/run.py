from webapp.website import ExampleWebsite

# this can be used for Gunicorn as well
app = ExampleWebsite()


if __name__ == "__main__":
    # run it manually:
    app.start()
