from controllers import index

def configure_routes(app):
    app.add_url_rule("/", view_func=index, methods=["GET", "POST"])
