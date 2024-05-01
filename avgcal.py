from flask import Flask, jsonify, request
import requests
import time

app = Flask(__name__)

window_size = 10
stored_numbers = []

def fetch_numbers(api_url, headers):
    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            return response.json().get('numbers', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching numbers: {e}")
    return []

def calculate_average(numbers):
    return sum(numbers) / len(numbers) if numbers else 0

@app.route('/numbers/<numberid>', methods=['GET'])
def process_number_request(numberid):
    global stored_numbers
    start_time = time.time()

    if numberid == 'p':
        api_url = 'http://20.244.56.144/test/primes'
    elif numberid == 'f':
        api_url = 'http://20.244.56.144/test/fibo'
    elif numberid == 'e':
        api_url = 'http://20.244.56.144/test/even'
    elif numberid == 'r':
        api_url = 'http://20.244.56.144/test/random'
    else:
        return jsonify({'error': 'Invalid number ID.'}), 400

    access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzE0NTQ3MTc0LCJpYXQiOjE3MTQ1NDY4NzQsImlzcyI6IkFmZm9yZG1lZCIsImp0aSI6IjIzODQ4NDUxLTdkNDgtNGQ4Mi05Y2NhLTgxNDU4MjljMGI2NyIsInN1YiI6InZ0dTE5Mjk2QHZlbHRlY2guZWR1LmluIn0sImNvbXBhbnlOYW1lIjoiZ29NYXJ0IiwiY2xpZW50SUQiOiIyMzg0ODQ1MS03ZDQ4LTRkODItOWNjYS04MTQ1ODI5YzBiNjciLCJjbGllbnRTZWNyZXQiOiJmWWRhWWdQc05lcHV6ZHVUIiwib3duZXJOYW1lIjoidnR1MTkyOTYifQ.nYvDBcKg5i9nqNzphzO7yVCSeXKGIDQrSX9A5vKMEJY"
    headers = {'Authorization': f'{access_token}'}

    numbers_from_server = fetch_numbers(api_url, headers)
    elapsed_time = time.time() - start_time

    if elapsed_time > 0.5:
        return jsonify({'error': 'Response time exceeded 500 ms.'}), 400
    stored_numbers.extend(set(numbers_from_server) - set(stored_numbers))
    stored_numbers = stored_numbers[-window_size:]
    if len(stored_numbers) >= window_size:
        average = calculate_average(stored_numbers)
    else:
        average = None

    response_data = {
        'windowPrevState': stored_numbers[:-len(numbers_from_server)],
        'windowCurrState': stored_numbers,
        'numbers': numbers_from_server,
        'avg': average
    }
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9876)
