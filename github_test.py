import os
import requests
from dotenv import load_dotenv
import time

# Загрузка переменных окружения
load_dotenv()

# Конфигурация (лучше хранить в .env)
GITHUB_USER = os.getenv('GITHUB_USER', 'nana223aaaa')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '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')
REPO_NAME = os.getenv('REPO_NAME', f'test-repo-{int(time.time())}')  # Уникальное имя

# Настройки запросов
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}
BASE_URL = "https://api.github.com"

def create_repository():
    """Создание нового репозитория"""
    print("\n[1/3] Создание репозитория...")
    repo_data = {
        "name": REPO_NAME,
        "description": "Тестовый репозиторий для API",
        "auto_init": True,
        "private": False
    }
    
    response = requests.post(
        f"{BASE_URL}/user/repos",
        json=repo_data,
        headers=headers
    )
    response.raise_for_status()
    print(f"✅ Репозиторий создан: {REPO_NAME}")
    print(f"   URL: https://github.com/{GITHUB_USER}/{REPO_NAME}")
    return response.json()

def verify_repository_exists():
    """Проверка существования репозитория"""
    print("\n[2/3] Проверка репозитория...")
    response = requests.get(
        f"{BASE_URL}/users/{GITHUB_USER}/repos",
        headers=headers
    )
    response.raise_for_status()
    
    repos = [repo["name"] for repo in response.json()]
    if REPO_NAME not in repos:
        raise Exception(f"Репозиторий {REPO_NAME} не найден!")
    print(f"✅ Репозиторий найден в профиле {GITHUB_USER}")

def delete_repository():
    """Удаление репозитория"""
    print("\n[3/3] Удаление репозитория...")
    response = requests.delete(
        f"{BASE_URL}/repos/{GITHUB_USER}/{REPO_NAME}",
        headers=headers
    )
    
    if response.status_code != 204:
        raise Exception(f"Ошибка удаления! Статус: {response.status_code}")
    print("✅ Репозиторий успешно удален")

def test_github_repo_workflow():
    try:
        print("\n" + "="*50)
        print(f"ТЕСТИРОВАНИЕ GITHUB API | Пользователь: {GITHUB_USER}")
        print("="*50)
        
        # Основной workflow
        create_repository()
        verify_repository_exists()
        delete_repository()
        
        print("\n" + "="*50)
        print("ТЕСТ УСПЕШНО ЗАВЕРШЕН!")
        print("="*50)
        
    except requests.exceptions.HTTPError as err:
        print(f"\n❌ Ошибка API: {err}")
        if err.response.status_code == 403:
            print("Проверьте правильность токена и его разрешения!")
        print(f"Детали: {err.response.text}")
    except Exception as e:
        print(f"\n❌ Ошибка: {type(e).__name__}: {e}")
    finally:
        print("\nЗавершение работы...")

if __name__ == "__main__":
    test_github_repo_workflow()
