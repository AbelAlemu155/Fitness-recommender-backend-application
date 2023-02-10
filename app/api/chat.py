from app.api import api
from app.chat.model import Group, GroupMembers, GroupChat
from flask import request, jsonify
from app import db


@api.route('/chat/search')
def searchGroup():
    page = request.args.get('page', 1, type=int)
    search_params = request.args.get('search', type=str, default="a")
    groups = Group.query.filter(
        Group.group_name.like("%" + search_params + "%"),
    ).paginate(page, per_page=4)

    return jsonify({
        "results": [g.to_json() for g in groups.items],
    })

# GET groups that a client is a member for


@api.route('/chat/user/<userID>')
def get_group_for_user(userID):
    page = request.args.get('page', 1, type=int)
    groups = GroupMembers.query.filter_by(
        group_member_id=userID).paginate(page, per_page=4)
    return jsonify([member.to_json() for member in groups.items])


@api.route('/chat', methods=['POST'])
def createGroup():
    data = request.get_json()
    new_group = Group.from_json(data)

    db.session.add(new_group)
    db.session.commit()
    return jsonify(new_group.to_json())


@api.route('/chat/join/<groupID>', methods=['POST'])
def joinGroup(groupID):
    data = request.get_json()
    group = Group.query.get_or_404(groupID)
    
    #Check if a user is already a member
    existing = GroupMembers.query.filter_by(group_id=groupID, group_member_id=data.get('id')).all()
    
    if(existing):
        return jsonify({'message' : 'user exists'}), 400
    
    group.group_members.append(GroupMembers(group_member_id=data.get('id')))
    db.session.add(group)
    db.session.commit()
    return jsonify({'message': 'joined group'})


@api.route('/chat/<groupID>/messages')
def getMessages(groupID):
    data = request.get_json()
    page = request.args.get('page', 1, type=int)
    group = Group.query.get_or_404(groupID)
    return jsonify([message.to_json() for message in group.chat])


@api.route('/chat/<groupID>', methods=['POST'])
def sendMessage(groupID):
    data = request.get_json()
    group = Group.query.get_or_404(groupID)
    message = GroupMembers.from_json(data)
    group.chat.append(message)
    return jsonify({'message': 'message sent'})
