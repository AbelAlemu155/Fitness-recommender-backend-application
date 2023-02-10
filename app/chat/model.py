from app import db
from datetime import datetime


class Group(db.Model):
    __tablename__ = 'group'
    group_id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(50), unique=True)
    # password = db.Column(db.String(100)
    group_members = db.relationship("GroupMembers", back_populates="group")
    group_chat = db.relationship("GroupChat", back_populates="group")
    
    def to_json(self):
        group = {
            "id" : self.group_id,
            "name" : self.group_name,
            "members_count" : len(self.group_members),
        }
        return group
    
    @staticmethod
    def from_json(json_user):
        group_name = json_user.get('name')
        return Group(group_name=group_name)


class GroupMembers(db.Model):
    __tablename__ = 'group_members'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey(
        'group.group_id'))
    group_member_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    group = db.relationship("Group", back_populates="group_members")
    
    def to_json(self):
        member = {
            "group_id" : self.group_id,
            "member_id" : self.group_member_id,
            "name" : self.group.group_name
        }
        return member
        

class GroupChat(db.Model):
    __tablename__ = 'group_chat'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey(
        'group.group_id'), primary_key=True)
    group_member_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    chat_message_data = db.Column(db.String(500))
    chat_message_type = db.Column(db.Integer)
    chat_datetime = db.Column(db.DateTime)
    group = db.relationship("Group", back_populates="group_chat")
    
    def to_json(self):
        group = {
            "member_id" : self.group_member_id,
            "message_data" : self.chat_message_data,
            "message_type" : self.chat_message_type,
            "message_time" : self.chat_datetime
        }
        return group
    
    @staticmethod
    def from_json(json_user):
        group_member_id = json_user.get('id')
        chat_message_data = json_user.get('data')
        chat_datatime = datetime.utcnow
        chat_message_type = MessageDataType.TEXT
        return GroupMembers(
            group_member_id=group_member_id,
            chat_message_type =chat_message_type,
            chat_message_data=chat_message_data,
            chat_datatime=chat_datatime
        )

class MessageDataType:
    TEXT = 0,