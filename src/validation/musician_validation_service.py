class MusicianValidationService:

    @staticmethod
    def validate_name(name: str):
        if not name.isalpha():
            raise Exception('Name is invalid.')
