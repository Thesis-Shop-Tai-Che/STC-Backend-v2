from fastapi import Depends, Request
from sqladmin import ModelView
from tag.models.tag_model import Tag

class TagAdmin(ModelView, model=Tag):
    name = "Tag"
    icon = "fa-solid fa-language"
    page_size_options = [25, 50, 100, 200]
    category = "PRODUCT"

    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    can_export = False
    
    column_labels = {
        'id': 'ID',
        'name': 'Name'
    }

