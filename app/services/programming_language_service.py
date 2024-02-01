from ..models.data_model import db,ProgrammingLanguage

class ProgrammingLanguageService:

    @staticmethod
    def get_all_programming_language():
        return ProgrammingLanguage.query.all()
    
    @staticmethod
    def get_programming_language_by_id(language_id):
        return ProgrammingLanguage.query.get(language_id)
        
    @staticmethod
    def get_language_by_name(language_name):
        language = ProgrammingLanguage.query.filter_by(language_name=language_name).first()
        if language:
            return language.language_id
        else:
            return None 

    @staticmethod
    def create_programming_language(language_name):
        new_programming_language = ProgrammingLanguage(language_name=language_name)
        db.session.add(new_programming_language)
        db.session.commit()
        return new_programming_language
    
    @staticmethod
    def edit_programming_language(language_id,language_name):
        programming_language = ProgrammingLanguage.query.get(language_id)
        if programming_language:
            programming_language.language_name = language_name
            db.session.commit()
            return programming_language
        return None
    @staticmethod
    def delete_programming_language(language_id):
        programming_language = ProgrammingLanguage.query.get(language_id)
        if programming_language:
            db.session.delete(programming_language)
            db.session.commit()
            return True
        return False
        
