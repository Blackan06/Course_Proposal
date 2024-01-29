from ..models.data_model import db,Category

class CategoryService:

    @staticmethod
    def get_all_category():
        return Category.query.all()
    
    @staticmethod
    def get_category_by_id(category_id):
        return Category.query.get(category_id)
    
    @staticmethod
    def create_category(category_name):
        newCategory = Category(category_name=category_name)
        db.session.add(newCategory)
        db.session.commit()
        return newCategory
    
    @staticmethod
    def edit_category(category_id,category_name):
        category = Category.query.get(category_id)
        if category:
            category.category_name = category_name
            db.session.commit()
            return category
        return None
    @staticmethod
    def delete_category(category_id):
        category = Category.query.get(category_id)
        if category:
            db.session.delete(category)
            db.session.commit()
            return True
        return False
        
