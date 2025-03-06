import httpx
import asyncio

# Адреса твоих сервисов
USER_SERVICE_URL = "http://localhost:8000/users/"
ORDER_SERVICE_URL = "http://localhost:8001/orders/"

# Пример данных для запросов
user_data = {"name": "Alex", "age": 25}
updated_user_data = {"name": "Alexander", "age": 26}  # Обновлённые данные пользователя

order_data = {"user_id": 1, "product": "Laptop", "quantity": 1}
updated_order_data = {"user_id": 1, "product": "Smartphone", "quantity": 2}  # Обновлённые данные заказа


# Асинхронная функция для работы с API
async def create_user():
    async with httpx.AsyncClient() as client:
        response = await client.post(USER_SERVICE_URL[:-1], json=user_data)

        # Выводим статус и содержимое ответа
        print(f"Статус ответа при создании пользователя: {response.status_code}")
        print(f"Ответ: {response.text}")  # Содержимое ответа в текстовом виде

        if response.status_code == 200:  # Успешное создание
            user = response.json()
            print(f"Создан пользователь: {user}")
            return user['id']  # Возвращаем ID пользователя
        else:
            print(f"Ошибка при создании пользователя: {response.status_code}")
            return None


async def update_user(user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{USER_SERVICE_URL}{user_id}", json=updated_user_data)
        if response.status_code == 200:
            print(f"Обновлён пользователь {user_id}:", response.json())
        else:
            print(f"Ошибка при обновлении пользователя {user_id}:", response.status_code)


async def delete_user(user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{USER_SERVICE_URL}{user_id}")
        print(f"Удалён пользователь {user_id}:", response.json())


async def create_order(user_id: int):
    async with httpx.AsyncClient() as client:
        order_data_with_user = {**order_data, "user_id": user_id}  # Подставляем ID пользователя в данные заказа
        response = await client.post(ORDER_SERVICE_URL[:-1], json=order_data_with_user)
        if response.status_code == 200:
            order = response.json()
            print("Создан заказ:", order)
            return order['id']  # Возвращаем ID заказа
        else:
            print(f"Ошибка при создании заказа: {response}")
            return None


async def update_order(order_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{ORDER_SERVICE_URL}{order_id}", json=updated_order_data)
        if response.status_code == 200:
            print(f"Обновлён заказ {order_id}:", response.json())
        else:
            print(f"Ошибка при обновлении заказа {order_id}:", response)


async def delete_order(order_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{ORDER_SERVICE_URL}{order_id}")
        if response.status_code == 200:
            print(f"Удалён заказ {order_id}:", response.json())
        else:
            print(f"Ошибка при удалении заказа {order_id}:", response)


async def get_user(user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{USER_SERVICE_URL}{user_id}")
        if response.status_code == 200:
            print("Получен пользователь:", response.json())
        else:
            print(f"Ошибка при получении пользователя {user_id}: {response}")


async def get_order(order_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{ORDER_SERVICE_URL}{order_id}")
        if response.status_code == 200:
            print("Получен заказ:", response.json())
        else:
            print(f"Ошибка при получении заказа {order_id}: {response}")


async def main():
    # Создаём пользователя
    user_id = await create_user()

    if user_id is None:
        print("Не удалось создать пользователя")
        return

    # Создаём заказ для этого пользователя
    order_id = await create_order(user_id)

    if order_id is None:
        print("Не удалось создать заказ")
        return

    # Получаем пользователя по ID
    await get_user(user_id)

    # Обновляем пользователя
    await update_user(user_id)

    # Получаем обновленного пользователя
    await get_user(user_id)

    # Получаем заказ по ID
    await get_order(order_id)

    # Обновляем заказ
    await update_order(order_id)

    # Получаем обновлённый заказ
    await get_order(order_id)

    # Удаляем заказ
    await delete_order(order_id)

    # Удаляем пользователя
    await delete_user(user_id)


# Запуск асинхронных задач
if __name__ == "__main__":
    asyncio.run(main())
