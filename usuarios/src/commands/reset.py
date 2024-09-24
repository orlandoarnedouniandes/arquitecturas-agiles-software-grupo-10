from .base_command import BaseCommannd
from ..models import  db
    
class Reset(BaseCommannd):
  def __init__(self):
    print("Reset Database")   
  
  def execute(self):
    db.drop_all()
    db.create_all()