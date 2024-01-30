from ..models.data_model import db, Provider

class ProviderService:

    @staticmethod
    def get_all_provider():
        return Provider.query.all()
    
    @staticmethod
    def get_provider_by_id(provider_id):
        return Provider.query.get(provider_id)
    
    @staticmethod
    def create_provider(provider_name):
        new_provider = Provider(provider_name=provider_name)
        db.session.add(new_provider)
        db.session.commit()
        return new_provider
    
    @staticmethod
    def edit_provider(provider_id,provider_name):
        provider = Provider.query.get(provider_id)
        if provider:
            provider.provider_name = provider_name
            db.session.commit()
            return provider
        return None
    
    @staticmethod
    def delete_provider(provider_id):
        provider = Provider.query.get(provider_id)
        if provider:
            db.session.delete(provider)
            db.session.commit()
            return True
        return False
        
