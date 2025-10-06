import requests

def describe_squirrel_server_functionality():
    def describe_handle_squirrels_index_functionality():
        def it_returns_200_success_code():
            pass
        def it_returns_correct_headers():
            pass
        def it_sends_squirrels_list():
            pass
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