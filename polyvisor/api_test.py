import pytest
from flask import Flask
from flask.testing import FlaskClient
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from polyvisor.controllers.api import app_api  


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(app_api)
   

    CORS(app)

    app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Replace 'your_secret_key' with an actual secret key
    jwt = JWTManager(app)

    return app


@pytest.fixture
def client(app):
    return app.test_client()




def test_get_system_api(client):
    response = client.get('/api/system')
    assert response.status_code == 200
    data = response.get_json()
    assert 'cpu' in data
    assert 'cores' in data
    assert 'memory' in data
    assert 'machineSpec' in data


def test_render_config_api(client):
    response = client.get('/api/config/render/4146544/lid002:demo3:demo3')
    assert response.status_code == 200
    data = response.get_json()
    # Add assertions based on what your renderConfig function is expected to return
    assert 'command' in data


# def test_render_supervisors_api(client):
#     response = client.get('/api/supervisors')
#     assert response.status_code == 200
#     data = response.get_json()
  
#     # Add assertions based on what your get_supervisors function is expected to return
#     assert 'name' in data[0]
#     assert 'processes' in data[0]
#     assert 'statename' in data[0].get('processes')
   

def test_render_one_supervisor_api(client):
    response = client.get('api/supervisor/lid002/processes')
    assert response.status_code == 200
    data = response.get_json()
    # Add assertions based on what your get_supervisor function is expected to return
    assert 'authentication' in data
    assert 'host' in data
    assert 'pid' in data
    assert 'name' in data
    assert 'processes' in data
    assert 'statename' in data.get('processes').get('lid002:demo3:demo3')
    assert 'pid' in data.get('processes').get('lid002:demo3:demo3')
    assert 'core_index' in data.get('processes').get('lid002:demo3:demo3')
    assert 'stderr_logfile' in data.get('processes').get('lid002:demo3:demo3')
    assert 'stdout_logfile' in data.get('processes').get('lid002:demo3:demo3')
    assert 'supervisor' in data.get('processes').get('lid002:demo3:demo3')
    assert 'uid' in data.get('processes').get('lid002:demo3:demo3')
    
