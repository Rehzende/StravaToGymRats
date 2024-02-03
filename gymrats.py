import requests
import datetime
import json

# Dados de login
email = input_data['email']
password = input_data['password']

# URL da API
base_url = "https://www.gymrats.app/api"

# Função de login
def fazer_login(email, password):
    url = f"{base_url}/tokens"
    
    payload = f"email={email}&password={password}"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    
    response = requests.post(url, headers=headers, data=payload)
    
    return response.json()

def get_id_by_sports_name(sports_name):

    sports_data = [{"id":"63b24d17-185f-4d41-9f42-9a20cf6b5545","name":"Bicicleta Estacionária","strava_sports_type":"VirtualRun"},{"id":"61443906-ab96-4eb9-b0e6-875ea465f644","name":"Elíptica","strava_sports_type":"Elliptical"},{"id":"c28e30db-d6c7-4f15-8671-230a01112388","name":"Trilha","strava_sports_type":"Hike"},{"id":"3b4b6262-38f1-4080-a40e-7d02aed0a99a","name":"Ciclismo","strava_sports_type":"Ride"},{"id":"2380d22a-ff3b-4280-b697-4b25aeb6efbe","name":"Remo","strava_sports_type":"Rowing"},{"id":"72c7f738-bc51-4a6f-889c-a6a79bcb112a","name":"Corrida","strava_sports_type":"Run"},{"id":"d9d551c0-bd6c-4c7d-9019-986a80f24219","name":"Escada","strava_sports_type":"StairStepper"},{"id":"ef653e68-d75e-4377-b928-52cc3d44bf97","name":"Musculação","strava_sports_type":"Workout"},{"id":"07340cb5-c743-4393-94dc-993f12cd4228","name":"Natação","strava_sports_type":"Swim"},{"id":"1d0be572-eb02-47ec-85a4-e567d5021bd0","name":"Caminhada","strava_sports_type":"Walk"},{"id":"a6fb7bd4-c6c3-4cb0-9c3b-addb4e6afaa7","name":"Yoga/Pilates","strava_sports_type":"Pilates"},{"id":"b58a5d49-dc2e-4366-8845-d15f6fc1b63f","name":"Cardio e Força Mistos/ Crossfit","strava_sports_type":"Crossfit"},{"id":"44064633-e6a4-43a2-a99b-696746fdd3f5","name":"Futebol","strava_sports_type":"Soccer"}]

    for sport_data in sports_data:
        if sport_data["strava_sports_type"] == sports_name:
            return sport_data["id"]
    return None 

activity_type_id = get_id_by_sports_name(input_data['strava_sport_type'])

# Dados do novo workout a ser adicionado
new_workout_payload = {
    "title": input_data['title'],
    "description": f"strava:{input_data['strava_url']}",
    "challenges": [
        {
            "id": input_data['challegend_id'],
            "activity_type_id": activity_type_id,
            "activity_metric_amount": None
        }
    ],
    "media": [
        {
            "url": "https://d1nab7r3hzzrs7.cloudfront.net/5793e3a2-880f-4b4c-97a7-23ed7d3258cf.jpg",
            "thumbnail_url": "https://d1nab7r3hzzrs7.cloudfront.net/5793e3a2-880f-4b4c-97a7-23ed7d3258cf.jpg",
            "medium_type": "image/jpg",
            "width": 670,
            "height": 563
        }
    ],
    "duration": int(input_data['duration_sec']) // 60,
    "distance": input_data['distance'],
    "steps": "",
    "calories": input_data['calories'],
    "points": None,
    #"occurred_at": input_data['start_date']
}

# Fazer login
resultado_login = fazer_login(email, password)
# Verificar se o login foi bem-sucedido
if "token" in resultado_login["data"]:
    token = resultado_login["data"]["token"]

    # Requisição dos workouts com o token
    headers = {
        'Authorization': token
    }
    
    today = datetime.date.today()

    url = f"{base_url}/workouts"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': token
    }
    response = requests.post(url, headers=headers, json=new_workout_payload)
    print(response.status_code)


else:
    print("Login falhou")
