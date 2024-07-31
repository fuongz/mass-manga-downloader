from src.providers import ProviderFactory

if __name__ == "__main__":
    provider = ProviderFactory("nettruyenviet")
    provider.download("conan")
