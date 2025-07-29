from enum import Enum

class Language(Enum):
    """Język analizy"""
    ENGLISH = "english"
    POLISH = "polish"
    GERMAN = "german"
    FRENCH = "french"
    SPANISH = "spanish"
    ITALIAN = "italian"
    PORTUGUESE = "portuguese"
    DUTCH = "dutch"
    RUSSIAN = "russian"
    JAPANESE = "japanese"
    KOREAN = "korean"
    CHINESE = "chinese"

    def get_country_code(self) -> str:
        """
        Zwraca kod kraju dla danego języka
        
        Returns:
            Kod kraju
        """
        country_codes = {
            self.ENGLISH: "us",
            self.POLISH: "pl",
            self.GERMAN: "de",
            self.FRENCH: "fr",
            self.SPANISH: "es",
            self.ITALIAN: "it",
            self.PORTUGUESE: "pt",
            self.DUTCH: "nl",
            self.RUSSIAN: "ru",
            self.JAPANESE: "jp",
            self.KOREAN: "kr",
            self.CHINESE: "cn"
        }
        return country_codes[self]

    @staticmethod
    def get_available_languages() -> list[str]:
        """
        Zwraca listę dostępnych języków
        
        Returns:
            Lista dostępnych języków
        """
        return [lang.value for lang in Language] 