# Run a test server.

from cit import create_app

# choose correct config depending on mode (Development or Production)
# you are in
config = 'config.DevelopmentConfig'
#config = 'config.ProductionConfig'
app = create_app(config)
app.run(host='0.0.0.0', port=8080, debug=True)
