import os
import requests
from dotenv import load_dotenv
import time

# Загрузка переменных окружения
load_dotenv()

# Настройки
GITHUB_USER = "nana223aaaa"  # Ваш GitHub ник
GITHUB_TOKEN = "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"  # Ваш токен
REPO_NAME = "---"  # Название тестового репозитория

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def test_github_repo_workflow():
    try:
        print("\n" + "="*50)
        print("НАЧАЛО ТЕСТИРОВАНИЯ GITHUB API")
        print("="*50 + "\n")

        # 1. Создание репозитория
        print("[1/3] Создание репозитория...")
        repo_data = {
            "name": REPO_NAME,
            "description": "Тестовый репозиторий",
            "auto_init": True,
            "private": False
        }
        
        response = requests.post(
            "https://api.github.com/user/repos",
            json=repo_data,
            headers=headers
        )
        response.raise_for_status()
        print(f"✅ Успешно создан репозиторий: {REPO_NAME}")
        print(f"   Ссылка: https://github.com/{GITHUB_USER}/{REPO_NAME}")

        # 2. Проверка существования
        print("\n[2/3] Проверка существования репозитория...")
        response = requests.get(
            f"https://api.github.com/users/{GITHUB_USER}/repos",
            headers=headers
        )
        response.raise_for_status()
        
        repos = [repo["name"] for repo in response.json()]
        if REPO_NAME in repos:
            print(f"✅ Репозиторий {REPO_NAME} найден в вашем профиле")
        else:
            raise Exception("Репозиторий не найден в списке!")

        # 3. Удаление репозитория
        print("\n[3/3] Удаление репозитория...")
        response = requests.delete(
            f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}",
            headers=headers
        )
        
        if response.status_code == 204:
            print("✅ Репозиторий успешно удален")
        else:
            raise Exception(f"Ошибка удаления! Код статуса: {response.status_code}")

        print("\n" + "="*50)
        print("ТЕСТИРОВАНИЕ УСПЕШНО ЗАВЕРШЕНО!")
        print("="*50)

    except requests.exceptions.HTTPError as err:
        print(f"\n❌ Ошибка HTTP: {err}")
        print(f"   Ответ сервера: {err.response.text}")
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
    finally:
        print("\nОчистка завершена.")

if __name__ == "__main__":
    test_github_repo_workflow()
