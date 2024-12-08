from website import create_app
from waitress import serve
from werkzeug.middleware.proxy_fix import ProxyFix

app = create_app()

app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

if __name__ == '__main__':
    #app.run(debug=True)
    serve(app, host='127.0.0.1', port=5000)