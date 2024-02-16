get_recipes_200_example = {
    "count": 2,
    "next": None,
    "previous": "http://localhost:8000/api/recipes/?page=1",
    "results": [
        {
            "id": 2,
            "name": "джем",
            "text": "нямням",
            "cooking_time": 1,
            "image": None,
            "author": {
                "id": 2,
                "username": "User1",
                "first_name": "user1",
                "last_name": "user1",
                "email": "user1@yandex.ru",
                "is_subscribed": True
            },
            "tags": [
                {
                    "id": 51,
                    "name": "Ужин",
                    "slug": "supper",
                    "color": "#FF4500"
                }
            ],
            "ingredients": [
                {
                    "id": 177,
                    "name": "абрикосовый джем",
                    "measurement_unit": "г",
                    "amount": 1
                }
            ],
            "is_favorited": False,
            "is_in_shopping_cart": False
        }
    ]
}
post_recipe_201_example = {
    "id": 11,
    "username": "User123",
    "first_name": "User123",
    "last_name": "User123",
    "email": "user123@mail.ru",
    "is_subscribed": False
}
get_recipe_by_id_200_example = {
    "id": 1,
    "username": "admin",
    "first_name": "admin",
    "last_name": "admin",
    "email": "admin@admin.ru",
    "is_subscribed": False
}
patch_recipe_by_id_200_example = {
    "id": 2,
    "username": "User1",
    "first_name": "user1",
    "last_name": "user1",
    "email": "user1@yandex.ru",
    "is_subscribed": True
}
