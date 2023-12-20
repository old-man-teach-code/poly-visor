import json
from unittest.mock import MagicMock
import pytest
from datetime import timedelta
from flask_session import Session
from flask import Flask
from flask.testing import FlaskClient
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from polyvisor.controllers.routes import app_routes  

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(app_routes)

    CORS(app)

    # Set the session type and key
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config["SESSION_PERMANENT"] = False
    app.config['SECRET_KEY'] = 'your_secret_key_here'
    # set the token expiration time
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    # Configure JWT for cookies
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_ACCESS_COOKIE_PATH'] = '/api'  # Path to protect with JWT cookies
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False  

    jwt = JWTManager(app)
    # Initialize the session
    session = Session(app)

    return app


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def jwt_token(mocker):
    # Mock the behavior of jwt_required() decorator
    mocker.patch('polyvisor.controllers.utils.jwt_required', MagicMock(return_value=True))

    # Mock a valid JWT access token
    return 'mocked_jwt_access_token'



def test_login_route_without_authentication(client):
    response = client.post('/api/login', data={'supervisor': 'lid002'})
    assert response.status_code == 401
    

def test_login_route_with_authentication_valid_credentials(client):
    # Assuming you have valid credentials for testing
    response = client.post('/api/login', data={'supervisor': 'lid002', 'username': 'test', 'password': 'test'})
    assert response.status_code == 200
    assert 'access_token_cookie' in response.headers['Set-Cookie']
    assert 'message' in response.json['data']
    assert response.json['data']['message'] == 'Login successfully'

def test_login_route_with_authentication_invalid_credentials(client):
    # Assuming you have invalid credentials for testing
    response = client.post('/api/login', data={'supervisor': 'lid002', 'username': 'tet', 'password': 'test'})
    assert response.status_code == 401
    assert 'message' in response.json['data']
    assert response.json['data']['message'] == 'Invalid username or password'


def test_logout_route(client):
    response = client.post('/api/logout')
    assert response.status_code == 200
    assert 'access_token_cookie' in response.headers['Set-Cookie']
    assert 'message' in response.json['data']
    assert response.json['data']['message'] == 'Logout successfully'



# def test_process_log_tail_out(client):
#         # Test when stream is "out"
#         response = client.get('/api/process/out/lid002:demo3:demo3')

#         assert response.status_code == 200
#         # assert type is event stream
        
#         assert 'data' in response.json


def test_create_config_post_success(client):
        # Assuming a successful POST request
        data =  {
            "pid": "4146544",
            "process_full_name": "test1423413",
            "command": "test",
            "numprocs": "1",
            "umask": "022",
            "supervisor_name": "lid002",
            "numprocs_start": "0",
            "priority": "999",
            "autostart": "true",
            "autorestart": "true",
            "startsecs": "1",
            "startretries": "3",
            "exitcodes": "0",
            "stopsignal": "TERM",
            "stopwaitsecs": "10",
            "stopasgroup": "false",
            "killasgroup": "false",
            "redirect_stderr": "false",
            "stdout_logfile_maxbytes": "50MB",
            "stdout_logfile_backups": "10",
            "stdout_capture_maxbytes": "0",
            "stdout_events_enabled": "false",
            "stdout_syslog": "false",
            "stderr_logfile_maxbytes": "50MB",
            "stderr_logfile_backups": "10",
            "stderr_capture_maxbytes": "0",
            "stderr_events_enabled": "false",
            "stderr_syslog": "false",
            "environment": "",
            "serverurl": "AUTO",
            "directory": "/tmp",
            "stdout_logfile": "AUTO",
            "stderr_logfile": "AUTO",
            "edit": "false"
        }
        response = client.post('/api/config/create', json=data)

        # Assuming a successful response should have a status code 200
        assert response.status_code == 200

        # Assuming the response contains a 'message' key in the JSON
        response_data = json.loads(response.get_data(as_text=True))
        # self.assertIn('message', response_data)
        # self.assertEqual(response_data['message'], 'Config file created successfully')
        assert 'message' in response_data
        

        

def test_create_config_post_failure(client):
    # Assuming a failed POST request
    data = {
        "supervisor_name": "lid002",
        "pid": "3382",
        "process_full_name": "test",
        "command": "test",
        "numprocs": "1",
        "umask": "022",
        "numprocs_start": "0",
        "priority": "999",
        "autostart": "true",
        "autorestart": "true",
        "startsecs": "1",
        "startretries": "3",
        "exitcodes": "0",
        "stopsignal": "TERM",
        "stopwaitsecs": "10",
        "stopasgroup": "false",
        "killasgroup": "false",
        "redirect_stderr": "false",
        "stdout_logfile_maxbytes": "50MB",
        "stdout_logfile_backups": "10",
        "stdout_capture_maxbytes": "0",
        "stdout_events_enabled": "false",
        "stdout_syslog": "false",
        "stderr_logfile_maxbytes": "50MB",
        "stderr_logfile_backups": "10",
        "stderr_capture_maxbytes": "0",
        "stderr_events_enabled": "false",
        "stderr_syslog": "false",
        "environment": "",
        "serverurl": "AUTO",
        "directory": "/tmp",
        "stdout_logfile": "AUTO",
        "stderr_logfile": "AUTO",
        "edit": "false"
        
    }

    response = client.post('/api/config/create', json=data)
    assert response.status_code == 500

        
#     response_data = json.loads(response.get_data(as_text=True))
        
#     assert 'message' in response_data

    
def test_set_process_core_index_route(client):
    

    # Act
    response = client.get('/api/cpu/set_affinity/4146590/2')  # Replace with actual pid and core_index values

    # Assert
    assert response.status_code == 200
    assert response.json == {'result': True}



def test_shutdown_supervisor_without_authentication(client):
    response = client.post('/api/supervisors/shutdown', data = {'supervisor': 'lid002'})
    assert response.status_code == 401

def test_restart_supervisor_without_authentication(client):
    response = client.post('/api/supervisors/restart', data = {'supervisor': 'lid002'})
    assert response.status_code == 401

def test_stop_process_without_authentication(client):
    response = client.post('/api/processes/stop', data = {'supervisor': 'lid002', 'process': 'lid002:demo3:demo3'})
    assert response.status_code == 401

def test_start_process_without_authentication(client):
    response = client.post('/api/processes/start', data = {'supervisor': 'lid002', 'process': 'lid002:demo3:demo3'})
    assert response.status_code == 401

def test_restart_process_without_authentication(client):
    response = client.post('/api/processes/restart', data = {'supervisor': 'lid002', 'process': 'lid002:demo3:demo3'})
    assert response.status_code == 401


    

