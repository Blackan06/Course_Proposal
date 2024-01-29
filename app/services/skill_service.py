from ..models.data_model import Skill
from ..models.db import db

class SkillService:

    @staticmethod
    def get_all_skill():
        return Skill.query.all()
    
    @staticmethod
    def get_skill_by_id(skill_id):
        return Skill.query.get(skill_id)
    
    @staticmethod
    def create_skill(skill_name,category_id):
        new_skill = Skill(skill_name=skill_name,category_id=category_id)
        db.session.add(new_skill)
        db.session.commit()
        return new_skill
    
    @staticmethod
    def edit_skill(skill_id,skill_name,category_id):
        skill = Skill.query.get(skill_id)
        if skill:
            skill.skill_name = skill_name
            skill.category_id = category_id
            db.session.commit()
            return skill
        return None
    @staticmethod
    def delete_skill(skill_id):
        skill = Skill.query.get(skill_id)
        if skill:
            db.session.delete(skill)
            db.session.commit()
            return True
        return False
        
