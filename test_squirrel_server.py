import requests
import pytest
SERVER_URL = "http://localhost:8080/squirrels"

@pytest.fixture
def base_setup():
    base_data = {"name": "chippy", "size": "large"}
    response  = requests.post(SERVER_URL, data=base_data)

    assert response.status_code == 201, f"Creation failed: {response.text}"

    yield

    squirrel_response = requests.get(SERVER_URL)

    squirrels = squirrel_response.json()
    for i in range(len(squirrels) - 1, len(squirrels)):
        squirrel = squirrels[i]
        requests.delete(f"{SERVER_URL}/{squirrel['id']}")
@pytest.fixture
def base_setup_two_squirrels():
    base_data = [{"name": "chippy", "size": "large"}, {'name': 'charles', 'size': 'british'}]
    
    for data in base_data:
        response  = requests.post(SERVER_URL, data=data)
        assert response.status_code == 201, f"Creation failed: {response.text}"

    yield

    squirrel_response = requests.get(SERVER_URL)

    squirrels = squirrel_response.json()
    for i in range(len(squirrels) - 2, len(squirrels)):
        squirrel = squirrels[i]
        requests.delete(f"{SERVER_URL}/{squirrel['id']}")

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
            assert data == [{'id' : 1,  'name': 'zippy', 'size': 'small'}, {'id' : 2,  'name': 'chippy', 'size': 'large'}, {'id': 3, 'name': 'charles', 'size': 'british'}]
            #I need to look into how responses are returned from the server
    def describe_handle_squirrels_retrieve_functionality():
        def it_returns_200_on_good_request():
            pass
        def it_returns_correct_headers():
            pass
        def it_returns_a_single_squirrel():
            pass
        def it_returns_404_on_malformed_url_request():
            pass
        def it_returns_404_on_malformed_id_request():
            pass
    def describe_handle_squirrels_create_functionality():
        def it_returns_201_success_code():
            pass
        def it_returns_correct_headers():
            pass
        def it_actually_creates_the_squirrel():
            pass
    def describe_handle_squirrels_update_functionality():
        def it_returns_204_on_good_request():
            pass
        def it_actually_updates_the_squirrel():
            pass
        def it_returns_correct_headers():
            pass
        def it_returns_404_on_malformed_url_request():
            pass
        def it_returns_404_on_malformed_id_request():
            pass
    def describe_handle_squirrels_delete_functionality():
        def it_returns_204_on_good_request():
            pass
        def it_actually_deletes_the_squirrel():
            pass
        def it_returns_correct_headers():
            pass
        def it_returns_404_on_malformed_url_request():
            pass
        def it_returns_404_on_malformed_id_request():
            pass
    def describe_handle_404_functionaltiy():
        def it_returns_404_on_malformed_url_request():
            pass
        def it_returns_404_on_malformed_id_request():
            pass
        def it_returns_correct_headers():
            pass
"""
response = requests.get("http://localhost:8080/squirrels")

print(response.status_code)
print(response.headers)
print(response.text[:200])
"""