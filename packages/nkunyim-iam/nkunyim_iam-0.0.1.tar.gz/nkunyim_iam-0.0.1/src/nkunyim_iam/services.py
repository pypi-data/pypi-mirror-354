from uuid import UUID, uuid4
from typing import Union
from .models import User
from .commands import UserCommand


class UserService:

    def login(self, command: UserCommand) -> User:
        
        user = User.objects.filter(id=command.id).first()
        
        if user:
            user.username = command.username
            user.nickname = command.nickname
            user.phone_number = command.phone_number
            user.email_address = command.email_address
        else:
            user = User(
                id=command.id,
                username=command.username,
                nickname=command.nickname,
                phone_number=command.phone_number,
                email_address=command.email_address
            )

        password = str(uuid4())
        user.set_password(password)
        user.save()
            
        return user

