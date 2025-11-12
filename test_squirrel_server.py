import http.client
import json
import os
import pytest
import shutil
import subprocess
import time
import urllib
import requests
import sys
import signal
from squirrel_db import SquirrelDB


SERVER_URL = "http://localhost:8081/squirrels"

def kill_existing_server():
    try:
        subprocess.run(["fuser", "-k", "8081/tcp"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        subprocess.run("lsof -t -i:8081 | xargs kill -9", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

@pytest.fixture(autouse=True)
def setup_database():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    empty_db = os.path.join(base_dir, "empty_squirrel_db.db")
    target_db = os.path.join(base_dir, "squirrel_db.db")

    if os.path.exists(target_db):
        os.remove(target_db)
    shutil.copy(empty_db, target_db)
    yield

@pytest.fixture(scope="session", autouse=True)
def manage_server_starting():
    kill_existing_server()
    time.sleep(.5)
    try:
        requests.get(SERVER_URL, timeout=1)
        print("Squirrel server already running")
        yield
        return
    except requests.ConnectionError:
        pass

    server_process = subprocess.Popen(
        [sys.executable, "squirrel_server.py"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        preexec_fn=os.setsid
    )

    for _ in range(10):
        try:
            r = requests.get(SERVER_URL, timeout=1)
            if r.status_code == 200:
                print("Squirrel server started successfully")
                break
        except requests.ConnectionError:
            time.sleep(0.5)
    else:
        server_process.terminate()
        pytest.fail("Failed to start squirrel server.")
    yield

    print("Stopping squirrel server")
    try:
        os.killpg(os.getpgid(server_process.pid), signal.SIGTERM)
    except ProcessLookupError:
        pass

@pytest.fixture
def base_setup():
    base_data = {"name": "chippy", "size": "large"}
    response  = requests.post(SERVER_URL, data=base_data)

    assert response.status_code == 201, f"Creation failed: {response.text}"

    yield
@pytest.fixture
def base_setup_two_squirrels():
    base_data = [{"name": "chippy", "size": "large"}, {'name': 'charles', 'size': 'british'}]
    
    for data in base_data:
        response  = requests.post(SERVER_URL, data=data)
        assert response.status_code == 201, f"Creation failed: {response.text}"

    yield

def describe_squirrel_server_functionality():
    def describe_handle_squirrels_index_functionality():
        def it_returns_200_success_code():
            response = requests.get(SERVER_URL)

            assert response.status_code == 200
        def it_returns_correct_headers():
            response = requests.get(SERVER_URL)

            assert response.headers["Content-Type"] == "application/json"
        def it_sends_squirrels_list(base_setup_two_squirrels):
            response = requests.get(SERVER_URL)
            data = response.json()
            for i in range(len(data)):
                squirrel = data[i]
                assert squirrel['name'] in ['chippy', 'charles']
                assert squirrel['size'] in ['large', 'british']
    def describe_handle_squirrels_retrieve_functionality():
        def it_returns_200_on_good_request(base_setup):
            response = requests.get(f'{SERVER_URL}/1')

            assert response.status_code == 200
        def it_returns_correct_headers(base_setup):
            response = requests.get(f'{SERVER_URL}/1')

            assert response.headers['Content-Type'] == "application/json"
        def it_returns_a_single_squirrel(base_setup):
            squirrels = requests.get(SERVER_URL).json()

            response = requests.get(f'{SERVER_URL}/{len(squirrels)}')
            data = response.json()

            assert (
                data["name"] == "chippy" and data["size"] == "large"
                ) 
        def it_returns_404_on_malformed_url_request():
            response = requests.get(f'{SERVER_URL}s/1')

            assert response.status_code == 404
        def it_returns_404_on_malformed_id_request():
            response = requests.get(f'{SERVER_URL}/402')

            assert response.status_code == 404
    def describe_handle_squirrels_create_functionality():
        def it_returns_201_success_code():
            data = {"name": "bob", "size": "human"}
            response = requests.post(SERVER_URL, data=data)

            assert response.status_code == 201

        def it_returns_correct_headers():
            data = {"name": "bob", "size": "human"}
            response = requests.post(SERVER_URL, data=data)
            assert "Content-Type" not in response.headers

        def it_actually_creates_the_squirrel():
            data = {"name": "bob", "size": "human"}
            response = requests.post(SERVER_URL, data=data)

            squirrels_request = requests.get(SERVER_URL)

            assert squirrels_request.status_code == 200, "Error getting squirrels to teardown in squirrel creation"

            squirrels = squirrels_request.json()

            squirrel = squirrels[len(squirrels) - 1]
            assert squirrel['name'] == 'bob'
            assert squirrel['size'] == 'human'
        def it_returns_400_on_bad_post():
            data = {"name": "bob", "size": None}
            response = requests.post(SERVER_URL, data=data)

            assert response.status_code == 400, "Error in getting correct response on post request"
    def describe_handle_squirrels_update_functionality():
        def it_returns_204_on_good_request(base_setup):
            existing_squirrels = requests.get(SERVER_URL)
            squirrel = existing_squirrels.json()[-1]

            updated_squirrel = {"name": "jimmy", "size": "tiny"}
            update_request = requests.put(f'{SERVER_URL}/{squirrel['id']}', data=updated_squirrel)

            assert update_request.status_code == 204
        def it_actually_updates_the_squirrel(base_setup):
            existing_squirrels = requests.get(SERVER_URL)
            squirrel = existing_squirrels.json()[-1]
            
            updated_squirrel = {"name": "jimmy", "size": "tiny"}
            update_request = requests.put(f'{SERVER_URL}/{squirrel['id']}', data=updated_squirrel)

            assert update_request.status_code == 204
        def it_returns_correct_headers(base_setup):
            existing_squirrels = requests.get(SERVER_URL)
            squirrel = existing_squirrels.json()[-1]
            
            updated_squirrel = {"name": "jimmy", "size": "tiny"}
            update_request = requests.put(f'{SERVER_URL}/{squirrel['id']}', data=updated_squirrel)

            assert "Content-Type" not in update_request.headers
        def it_returns_404_on_malformed_url_request(base_setup):
            existing_squirrels = requests.get(SERVER_URL)
            squirrel = existing_squirrels.json()[-1]
            
            updated_squirrel = {"name": "jimmy", "size": "tiny"}
            update_request = requests.put(f'{SERVER_URL}s/{squirrel['id']}', data=updated_squirrel)

            assert update_request.status_code == 404
        def it_returns_404_on_malformed_id_request(base_setup):
            existing_squirrels = requests.get(SERVER_URL)
            squirrel = existing_squirrels.json()[-1]
            
            updated_squirrel = {"name": "jimmy", "size": "tiny"}
            update_request = requests.put(f'{SERVER_URL}s/{squirrel['id'] + 200}', data=updated_squirrel)

            assert update_request.status_code == 404
        def it_returns_400_on_bad_post():
            data = {"name": "bob", "size": None}
            response = requests.post(SERVER_URL, data=data)

            assert response.status_code == 400, "Error in getting correct response on post request"
    def describe_handle_squirrels_delete_functionality():
        def it_returns_204_on_good_request():
            new_squirrel = {"name": "bill", "size": "lumberjack"}
            requests.post(SERVER_URL, data=new_squirrel)
            existing_squirrels = requests.get(SERVER_URL)
            squirrel = existing_squirrels.json()[-1]

            delete_request = requests.delete(f'{SERVER_URL}/{squirrel['id']}')

            assert delete_request.status_code == 204
        def it_actually_deletes_the_squirrel():
            new_squirrel = {"name": "bill", "size": "lumberjack"}
            requests.post(SERVER_URL, data=new_squirrel)
            existing_squirrels = requests.get(SERVER_URL)
            squirrel = existing_squirrels.json()[-1]

            delete_request = requests.delete(f'{SERVER_URL}/{squirrel['id']}')

            post_delete_squirrels = requests.get(SERVER_URL)

            for squirrel in post_delete_squirrels.json():
                assert squirrel['name'] != "bill" and squirrel['size'] != "lumberjack"
        def it_returns_correct_headers():
            new_squirrel = {"name": "bill", "size": "lumberjack"}
            requests.post(SERVER_URL, data=new_squirrel)
            existing_squirrels = requests.get(SERVER_URL)
            squirrel = existing_squirrels.json()[-1]

            delete_request = requests.delete(f'{SERVER_URL}/{squirrel['id']}')

            assert "Content-Type" not in delete_request.headers
        def it_returns_404_on_malformed_url_request(base_setup):
            existing_squirrels = requests.get(SERVER_URL)
            squirrel = existing_squirrels.json()[-1]

            delete_request = requests.delete(f'{SERVER_URL}s/{squirrel['id']}')

            assert delete_request.status_code == 404
        def it_returns_404_on_malformed_id_request(base_setup):
            existing_squirrels = requests.get(SERVER_URL)
            squirrel = existing_squirrels.json()[-1]

            delete_request = requests.delete(f'{SERVER_URL}s/{squirrel['id'] + 200}')

            assert delete_request.status_code == 404
    def describe_handle_404_functionality():
        def it_returns_404_on_malformed_url_request():
            request = requests.get(f'{SERVER_URL}ss')

            assert request.status_code == 404
        def it_returns_404_on_malformed_id_request():
            request = requests.get(f'{SERVER_URL}/-1')

            assert request.status_code == 404
        def it_returns_correct_headers():
            request = requests.get(f'{SERVER_URL}ss')

            assert request.headers['Content-Type'] == "text/plain"