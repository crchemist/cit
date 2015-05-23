import os 

virtenv = os.path.join(os.environ.get('OPENSHIFT_PYTHON_DIR', '.'), 'virtenv')
virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
try:
    execfile(virtualenv, dict(__file__=virtualenv))
except IOError:
    pass

from cit import create_app

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    ip = os.environ['OPENSHIFT_PYTHON_IP']
    port = int(os.getenv('OPENSHIFT_PYTHON_PORT'))
    application = create_app()
    httpd = make_server(ip, port, application)
    #Wait for a single request, serve it and quit.
    httpd.serve_forever()
