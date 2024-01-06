import requests
import datetime
import json


# Dados de login
email = input_data['email']
password = input_data['password']
# Função de login
def fazer_login(email, password):
    url = "https://www.gymrats.app/api/tokens"
    
    payload = f"email={email}&password={password}"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',

    }
    
    response = requests.post(url, headers=headers, data=payload)
    
    return response.text

duration_time = int(input_data['duration_sec']) // 60 

# Dados do novo workout a ser adicionado
new_workout_payload = {
    "title": input_data['title'],
    "description": f"strava_id:{input_data['strava_id']}",
    "challenges": [
        {
            "id": input_data['challegend_id'],
            "activity_type_id": None,
            "activity_metric_amount": None
        }
    ],
    "media": [
        {
            "url": "https://d1nab7r3hzzrs7.cloudfront.net/61263d2c-c6b1-496f-b1f4-656d10fc61f4.jpg",
            "thumbnail_url": "https://d1nab7r3hzzrs7.cloudfront.net/61263d2c-c6b1-496f-b1f4-656d10fc61f4.jpg",
            "medium_type": "image/jpg",
            "width": 670,
            "height": 563
        }
    ],
    "duration": duration_time,
    "distance": input_data['distance'],
    "steps": "",
    "calories": input_data['calories'],
    "points": None,
    "occurred_at": input_data['start_date']
}


# Fazer login
resultado_login = fazer_login(email, password)
resultado_login_json = json.loads(resultado_login)
# Verificar se o login foi bem-sucedido
if "token" in resultado_login_json["data"]:
    token = resultado_login_json["data"]["token"]

    # Requisição dos workouts com o token
    headers = {
        'Authorization': token
    }
    
    # Fazer a request dos workouts
    workouts_response = requests.get(f"https://www.gymrats.app/api/accounts/{input_data['gymrats_account']}/workouts", headers=headers)
    # Checar se a request foi bem-sucedida
    if workouts_response.status_code == 200:
        data = workouts_response.json()

        # Obtém a data de hoje
        today = datetime.date.today()

        # Verifica se a atividade já existe
        activity_exists = any(
            workout['challenge_id'] == 142155 and
            datetime.datetime.strptime(workout['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ').date() == today and
            ('description' in workout and f"strava_id:{input_data['strava_id']}" in workout['description'])
            for workout in data['data']
        )

        if not activity_exists:
            url = "https://www.gymrats.app/api/workouts"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': token
            }
            response = requests.post(url, headers=headers, json=new_workout_payload)
            print(response.text)
        else:
            print("Atividade já existe")
    else:
        print("Erro ao obter os workouts")
else:
    print("Login falhou")
