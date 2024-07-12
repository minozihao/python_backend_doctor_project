import json

from fastapi.testclient import TestClient

from src.main import start_app

app = start_app()
client = TestClient(app)

mock_doctor_create_payload = [
    {
        "first_name": "BBBB",
        "last_name": "BABA",
        "first_name_cn": "兆哈",
        "last_name_cn": "哈",
        "consultation_fee": 100,
        "consultation_fee_detail": "inclusive 3 days of western medicine",
        "consultation_fee_detail_cn": "包含3日西药",
        "category": "bone",
        "phone": "28773222,28773888",
        "street": "100 bbbbbbb st",
        "room": "3",
        "district": "futian",
        "city": "shenzhen",
        "street_cn": "商报路",
        "room_cn": "3",
        "district_cn": "福田",
        "city_cn": "深圳",
        "schedule_monday": "5:00-10:00",
        "schedule_tuesday": "5:00-10:00",
        "schedule_wednesday": "5:00-10:00",
        "schedule_thursday": "5:00-10:00",
        "schedule_friday": "5:00-10:00",
        "schedule_saturday": "5:00-10:00",
        "schedule_sunday": "closed",
        "public_holiday": "closed"
    }, {
        "first_name": "HHKKH",
        "last_name": "fdsf",
        "first_name_cn": "你好",
        "last_name_cn": "饿",
        "consultation_fee": 120,
        "consultation_fee_detail": "inclusive 3 days of western medicine",
        "consultation_fee_detail_cn": "包含3日西药",
        "category": "bone",
        "phone": "28773222,28773888",
        "street": "777 gdfgd st",
        "room": "3",
        "district": "futian",
        "city": "shenzhen",
        "street_cn": "商报路",
        "room_cn": "3",
        "district_cn": "福田",
        "city_cn": "深圳",
        "schedule_monday": "5:00-10:00",
        "schedule_tuesday": "5:00-10:00",
        "schedule_wednesday": "5:00-10:00",
        "schedule_thursday": "5:00-10:00",
        "schedule_friday": "5:00-10:00",
        "schedule_saturday": "5:00-10:00",
        "schedule_sunday": "closed",
        "public_holiday": "closed"
    }
]


def test_get_doctor_by_id():
    # general behaviour
    response = client.get("/doctor/1", headers={'env': 'test'})
    assert response.status_code == 200
    assert response.json() == {'data': {'first_name': 'abc', 'last_name': 'efg', 'consultation_fee': 50.0,
                                        'consultation_fee_detail': 'include 3 days medicine', 'phone': '555666777',
                                        'category': {'name': 'bone'},
                                        'schedule': [{'day_in_week': 'monday', 'working_hours': '9:00-12:00'},
                                                     {'day_in_week': 'tuesday', 'working_hours': '9:00-12:00'}],
                                        'address': {'street': '66 qwert st', 'room': 'A3', 'district': 'futian',
                                                    'city': 'shenzhen'}}, 'err_message': ''}

    # id not found
    response = client.get("/doctor/5", headers={'env': 'test'})
    assert response.status_code == 200
    assert response.json()['err_message'] == 'id not found'

    # invalid id
    response = client.get("/doctor/0", headers={'env': 'test'})
    assert response.status_code == 400
    assert response.json()['err_message'] == 'invalid doctor id'

    response = client.get("/doctor/-1", headers={'env': 'test'})
    assert response.status_code == 400
    assert response.json()['err_message'] == 'invalid doctor id'


def test_create_doctors():
    # general behaviour
    payload = json.dumps(mock_doctor_create_payload)
    response = client.post("/doctor", headers={'env': 'test'}, data=payload)
    assert response.status_code == 200

    # create doctors without payload
    response = client.post("/doctor", headers={'env': 'test'})
    assert response.status_code == 422

    # with empty list payload
    payload = json.dumps([])
    response = client.post("/doctor", headers={'env': 'test'}, data=payload)
    assert response.status_code == 400
    assert response.json()['err_message'] == 'no doctors entity found in payload'

    # with more than 500 doctors in payload
    p = [{
        "first_name": f"name_{i}",
        "last_name": "BABA",
        "first_name_cn": "兆哈",
        "last_name_cn": "哈",
        "consultation_fee": 100,
        "consultation_fee_detail": "inclusive 3 days of western medicine",
        "consultation_fee_detail_cn": "包含3日西药",
        "category": "bone",
        "phone": "28773222,28773888",
        "street": "100 bbbbbbb st",
        "room": "3",
        "district": "futian",
        "city": "shenzhen",
        "street_cn": "商报路",
        "room_cn": "3",
        "district_cn": "福田",
        "city_cn": "深圳",
        "schedule_monday": "5:00-10:00",
        "schedule_tuesday": "5:00-10:00",
        "schedule_wednesday": "5:00-10:00",
        "schedule_thursday": "5:00-10:00",
        "schedule_friday": "5:00-10:00",
        "schedule_saturday": "5:00-10:00",
        "schedule_sunday": "closed",
        "public_holiday": "closed"
    } for i in range(501)]
    payload = json.dumps(p)
    response = client.post("/doctor", headers={'env': 'test'}, data=payload)
    assert response.status_code == 400
    assert response.json()['err_message'] == 'limit 500 entity reached'


def test_query_doctors():
    # general behaviour
    response = client.get("/doctor?district=futian&category=bone&language=en", headers={'env': 'test'})
    assert response.status_code == 200
    assert response.json()['rows'] == 2
    assert response.json()['data'] == [{'first_name': 'bob', 'last_name': 'john', 'consultation_fee': 50.0,
                                        'consultation_fee_detail': 'include 3 days medicine', 'phone': '555666777',
                                        'category': {'name': 'bone'},
                                        'schedule': [{'day_in_week': 'monday', 'working_hours': '9:00-12:00'},
                                                     {'day_in_week': 'tuesday', 'working_hours': '9:00-12:00'}],
                                        'address': {'street': '66 qwert st', 'room': 'A3', 'district': 'futian',
                                                    'city': 'shenzhen'}},
                                       {'first_name': 'charlie', 'last_name': 'king', 'consultation_fee': 100.0,
                                        'consultation_fee_detail': 'include 3 days medicine', 'phone': '555666777',
                                        'category': {'name': 'bone'},
                                        'schedule': [{'day_in_week': 'monday', 'working_hours': '9:00-12:00'},
                                                     {'day_in_week': 'tuesday', 'working_hours': '9:00-12:00'}],
                                        'address': {'street': '66 qwert st', 'room': 'A3', 'district': 'futian',
                                                    'city': 'shenzhen'}}]

    # test with no result found
    response = client.get("/doctor?district=some_district", headers={'env': 'test'})
    assert response.status_code == 200
    assert response.json()['rows'] == 0
    assert response.json()['data'] == []

    # test with invalid language code in parameter
    response = client.get("/doctor?language=jp", headers={'env': 'test'})
    assert response.status_code == 400
    assert response.json()['err_message'] == 'unexpected language code'

