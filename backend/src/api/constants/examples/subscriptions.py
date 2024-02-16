get_subscriptions_200_example = {
    "count": 4,
    "next": None,
    "previous": None,
    "results": [
        {
            "id": 3,
            "username": "User2",
            "first_name": "user2",
            "last_name": "user2",
            "email": "user2@yandex.ru",
            "is_subscribed": True,
            "recipes": [],
            "recipes_count": 0
        },
        {
            "id": 4,
            "username": "User3",
            "first_name": "user3",
            "last_name": "user3",
            "email": "user3@yandex.ru",
            "is_subscribed": True,
            "recipes": [],
            "recipes_count": 0
        },
        {
            "id": 5,
            "username": "User4",
            "first_name": "user4",
            "last_name": "user4",
            "email": "user4@yandex.ru",
            "is_subscribed": True,
            "recipes": [],
            "recipes_count": 0
        },
        {
            "id": 2,
            "username": "User1",
            "first_name": "user1",
            "last_name": "user1",
            "email": "user1@yandex.ru",
            "is_subscribed": True,
            "recipes": [
                {
                    "name": "джем",
                    "id": 2,
                    "cooking_time": 1,
                    "image": None
                }
            ],
            "recipes_count": 1
        }
    ]
}
subscribe_user_201_example = {
    "id": 2,
    "username": "User1",
    "first_name": "user1",
    "last_name": "user1",
    "email": "user1@yandex.ru",
    "is_subscribed": True,
    "recipes": [
        {
            "id": 2,
            "name": "джем",
            "image": True,
            "cooking_time": 1
        }
    ],
    "recipes_count": 1
}
