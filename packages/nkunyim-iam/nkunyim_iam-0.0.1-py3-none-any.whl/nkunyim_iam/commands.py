from uuid import UUID
from nkunyim_util import Validation


class UserCommand(Validation):
    
    def __init__(self, data: dict):
        super().__init__()
        
        schema = {
            'id': {
                'typ': 'uuid',
            },
            'username': {
                'typ': 'str',
            },
            'nickname': {
                'typ': 'str',
            },
            'phone_number': {
                'typ': 'str',
            },
            'email_address': {
                'typ': 'str',
            }
        }
        
        self.check(schema=schema, data=data)
        
        self.id = UUID(data['id'])
        self.username = data['username']
        self.nickname = data['nickname']
        self.phone_number = data['phone_number']
        self.email_address = data['email_address']
    
    