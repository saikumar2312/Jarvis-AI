from config.settings import settings


def main():
    print("=" * 40)
    print(f"      {settings.APP_NAME}")
    print(f"        Version {settings.VERSION}")
    print("=" * 40)
    print("\nInitializing Jarvis...\n")
    print("✅ Configuration Loaded")
    print("🚀 Jarvis is Ready!")


if __name__ == "__main__":
    main()