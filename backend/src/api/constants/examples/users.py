get_users_200_example = {
    "count": 10,
    "next": "http://localhost:8000/api/users/?page=3",
    "previous": "http://localhost:8000/api/users/?page=1",
    "results": [
        {
            "id": 5,
            "username": "User4",
            "first_name": "user4",
            "last_name": "user4",
            "email": "user4@yandex.ru",
            "is_subscribed": False
        },
        {
            "id": 6,
            "username": "User5",
            "first_name": "user5",
            "last_name": "user5",
            "email": "user5@yandex.ru",
            "is_subscribed": False
        },
        {
            "id": 7,
            "username": "User6",
            "first_name": "user6",
            "last_name": "user6",
            "email": "user6@yandex.ru",
            "is_subscribed": False
        }
    ]
}
post_user_201_example = {
    "id": 11,
    "username": "User123",
    "first_name": "User123",
    "last_name": "User123",
    "email": "user123@mail.ru",
    "is_subscribed": False
}
get_me_200_example = {
    "id": 1,
    "username": "admin",
    "first_name": "admin",
    "last_name": "admin",
    "email": "admin@admin.ru",
    "is_subscribed": False
}
get_user_by_id_200_example = {
    "id": 2,
    "username": "User1",
    "first_name": "user1",
    "last_name": "user1",
    "email": "user1@yandex.ru",
    "is_subscribed": True
}
