from app.application import Application
from config.settings import settings


def banner():
    print("=" * 45)
    print(f"        {settings.APP_NAME}")
    print(f"          Version {settings.VERSION}")
    print("=" * 45)
    print()


if __name__ == "__main__":
    banner()

    app = Application()
    app.run()