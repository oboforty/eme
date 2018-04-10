from apps.website.website import Website

if __name__ == "__main__":
    app = Website(environment='dev')

    app.start()
