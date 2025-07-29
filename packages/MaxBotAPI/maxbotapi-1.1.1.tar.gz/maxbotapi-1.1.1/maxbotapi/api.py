import aiohttp
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum


class HTTPMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


@dataclass
class User:
    id: str
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    language_code: Optional[str]
    is_bot: bool
    is_admin: bool

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        return cls(
            id=data['id'],
            username=data.get('username'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            language_code=data.get('language_code'),
            is_bot=data.get('is_bot', False),
            is_admin=data.get('is_admin', False)
        )


@dataclass
class Chat:
    id: str
    type: str
    title: Optional[str]
    description: Optional[str]
    invite_link: Optional[str]
    creator_id: Optional[str]
    created_at: str
    updated_at: str
    members_count: int
    is_member: bool
    is_creator: bool
    is_admin: bool
    pinned_message: Optional['Message']

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Chat':
        pinned_message = Message.from_dict(data['pinned_message']) if data.get('pinned_message') else None
        return cls(
            id=data['id'],
            type=data['type'],
            title=data.get('title'),
            description=data.get('description'),
            invite_link=data.get('invite_link'),
            creator_id=data.get('creator_id'),
            created_at=data['created_at'],
            updated_at=data['updated_at'],
            members_count=data['members_count'],
            is_member=data['is_member'],
            is_creator=data['is_creator'],
            is_admin=data['is_admin'],
            pinned_message=pinned_message
        )


@dataclass
class Message:
    id: str
    chat_id: str
    text: Optional[str]
    sender: Optional[User]
    created_at: str
    updated_at: str
    reply_to_message_id: Optional[str]
    is_edited: bool
    is_pinned: bool
    callback_data: Optional[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        sender = User.from_dict(data['sender']) if data.get('sender') else None
        return cls(
            id=data['id'],
            chat_id=data['chat_id'],
            text=data.get('text'),
            sender=sender,
            created_at=data['created_at'],
            updated_at=data['updated_at'],
            reply_to_message_id=data.get('reply_to_message_id'),
            is_edited=data['is_edited'],
            is_pinned=data['is_pinned'],
            callback_data=data.get('callback_data')
        )


@dataclass
class NewMessageBody:
    chat_id: str
    text: str
    reply_to_message_id: Optional[str] = None
    inline_keyboard: Optional[List[List[Dict[str, Any]]]] = None


@dataclass
class Update:
    update_id: str
    type: str
    message: Optional[Message]
    callback_query: Optional[Dict[str, Any]]
    chat_member: Optional[Dict[str, Any]]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Update':
        message = Message.from_dict(data['message']) if data.get('message') else None
        return cls(
            update_id=data['update_id'],
            type=data['type'],
            message=message,
            callback_query=data.get('callback_query'),
            chat_member=data.get('chat_member')
        )


class MaxAPI:
    def __init__(self, token: str, base_url: str = "https://api.max.ru/v1"):
        self.token = token
        self.base_url = base_url
        self.session = aiohttp.ClientSession()

    async def _make_request(
            self,
            method: HTTPMethod,
            endpoint: str,
            params: Optional[Dict[str, Any]] = None,
            json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        headers = {"Authorization": f"Bearer {self.token}"}
        url = f"{self.base_url}/{endpoint}"

        async with self.session.request(
                method.value,
                url,
                headers=headers,
                params=params,
                json=json_data
        ) as response:
            response.raise_for_status()
            return await response.json()

    async def close(self):
        await self.session.close()

    # Bot methods
    async def get_bot_info(self) -> User:
        """Get current bot information"""
        data = await self._make_request(HTTPMethod.GET, "me")
        return User.from_dict(data)

    async def update_bot_info(self, **kwargs) -> User:
        """Update bot information"""
        data = await self._make_request(HTTPMethod.PATCH, "me", json_data=kwargs)
        return User.from_dict(data)

    # Chats methods
    async def get_chats(self) -> List[Chat]:
        """Get list of all chats"""
        data = await self._make_request(HTTPMethod.GET, "chats")
        return [Chat.from_dict(chat) for chat in data['chats']]

    async def get_chat_by_link(self, chat_link: str) -> Chat:
        """Get chat by invite link"""
        data = await self._make_request(HTTPMethod.GET, f"chats/{chat_link}")
        return Chat.from_dict(data)

    async def get_chat_info(self, chat_id: str) -> Chat:
        """Get chat information"""
        data = await self._make_request(HTTPMethod.GET, f"chats/{chat_id}")
        return Chat.from_dict(data)

    async def update_chat_info(self, chat_id: str, **kwargs) -> Chat:
        """Update chat information"""
        data = await self._make_request(HTTPMethod.PATCH, f"chats/{chat_id}", json_data=kwargs)
        return Chat.from_dict(data)

    async def delete_chat(self, chat_id: str) -> bool:
        """Delete chat"""
        await self._make_request(HTTPMethod.DELETE, f"chats/{chat_id}")
        return True

    async def send_chat_action(self, chat_id: str, action: str) -> bool:
        """Send action to chat"""
        await self._make_request(HTTPMethod.POST, f"chats/{chat_id}/actions", json_data={"action": action})
        return True

    async def get_pinned_message(self, chat_id: str) -> Optional[Message]:
        """Get pinned message in chat"""
        data = await self._make_request(HTTPMethod.GET, f"chats/{chat_id}/pin")
        return Message.from_dict(data) if data else None

    async def pin_message(self, chat_id: str, message_id: str) -> bool:
        """Pin message in chat"""
        await self._make_request(HTTPMethod.PUT, f"chats/{chat_id}/pin", json_data={"message_id": message_id})
        return True

    async def unpin_message(self, chat_id: str) -> bool:
        """Unpin message in chat"""
        await self._make_request(HTTPMethod.DELETE, f"chats/{chat_id}/pin")
        return True

    async def get_chat_membership(self, chat_id: str) -> Dict[str, Any]:
        """Get bot's membership in chat"""
        return await self._make_request(HTTPMethod.GET, f"chats/{chat_id}/members/me")

    async def leave_chat(self, chat_id: str) -> bool:
        """Leave chat"""
        await self._make_request(HTTPMethod.DELETE, f"chats/{chat_id}/members/me")
        return True

    async def get_chat_admins(self, chat_id: str) -> List[User]:
        """Get chat admins"""
        data = await self._make_request(HTTPMethod.GET, f"chats/{chat_id}/members/admins")
        return [User.from_dict(admin) for admin in data['admins']]

    async def promote_to_admin(self, chat_id: str, user_id: str) -> bool:
        """Promote user to admin"""
        await self._make_request(HTTPMethod.POST, f"chats/{chat_id}/members/admins", json_data={"user_id": user_id})
        return True

    async def demote_admin(self, chat_id: str, user_id: str) -> bool:
        """Demote admin"""
        await self._make_request(HTTPMethod.DELETE, f"chats/{chat_id}/members/admins/{user_id}")
        return True

    async def get_chat_members(self, chat_id: str) -> List[User]:
        """Get chat members"""
        data = await self._make_request(HTTPMethod.GET, f"chats/{chat_id}/members")
        return [User.from_dict(member) for member in data['members']]

    async def add_chat_members(self, chat_id: str, user_ids: List[str]) -> bool:
        """Add members to chat"""
        await self._make_request(HTTPMethod.POST, f"chats/{chat_id}/members", json_data={"user_ids": user_ids})
        return True

    async def remove_chat_member(self, chat_id: str, user_id: str) -> bool:
        """Remove member from chat"""
        await self._make_request(HTTPMethod.DELETE, f"chats/{chat_id}/members/{user_id}")
        return True

    # Subscriptions methods
    async def get_subscriptions(self) -> List[Dict[str, Any]]:
        """Get subscriptions"""
        data = await self._make_request(HTTPMethod.GET, "subscriptions")
        return data['subscriptions']

    async def subscribe(self, url: str, events: List[str]) -> Dict[str, Any]:
        """Subscribe to updates"""
        data = await self._make_request(HTTPMethod.POST, "subscriptions", json_data={"url": url, "events": events})
        return data

    async def unsubscribe(self, subscription_id: str) -> bool:
        """Unsubscribe from updates"""
        await self._make_request(HTTPMethod.DELETE, f"subscriptions/{subscription_id}")
        return True

    async def get_updates(self, timeout: Optional[int] = None, limit: Optional[int] = None) -> List[Update]:
        """Get updates"""
        params = {}
        if timeout is not None:
            params['timeout'] = timeout
        if limit is not None:
            params['limit'] = limit

        data = await self._make_request(HTTPMethod.GET, "updates", params=params)
        return [Update.from_dict(update) for update in data['updates']]

    # Uploads methods
    async def get_upload_url(self, file_name: str, file_size: int, content_type: str) -> Dict[str, Any]:
        """Get URL for file upload"""
        data = await self._make_request(
            HTTPMethod.POST,
            "uploads",
            json_data={
                "file_name": file_name,
                "file_size": file_size,
                "content_type": content_type
            }
        )
        return data

    # Messages methods
    async def get_messages(
            self,
            chat_id: Optional[str] = None,
            limit: Optional[int] = None,
            before: Optional[str] = None,
            after: Optional[str] = None
    ) -> List[Message]:
        """Get messages"""
        params = {}
        if chat_id:
            params['chat_id'] = chat_id
        if limit:
            params['limit'] = limit
        if before:
            params['before'] = before
        if after:
            params['after'] = after

        data = await self._make_request(HTTPMethod.GET, "messages", params=params)
        return [Message.from_dict(message) for message in data['messages']]

    async def send_message(
            self,
            chat_id: str,
            text: str,
            reply_to_message_id: Optional[str] = None,
            inline_keyboard: Optional[List[List[Dict[str, Any]]]] = None
    ) -> Message:
        """Send message"""
        payload = {
            "chat_id": chat_id,
            "text": text
        }
        if reply_to_message_id:
            payload['reply_to_message_id'] = reply_to_message_id
        if inline_keyboard:
            payload['inline_keyboard'] = inline_keyboard

        data = await self._make_request(HTTPMethod.POST, "messages", json_data=payload)
        return Message.from_dict(data)

    async def edit_message(
            self,
            message_id: str,
            text: str,
            inline_keyboard: Optional[List[List[Dict[str, Any]]]] = None
    ) -> Message:
        """Edit message"""
        payload = {
            "message_id": message_id,
            "text": text
        }
        if inline_keyboard:
            payload['inline_keyboard'] = inline_keyboard

        data = await self._make_request(HTTPMethod.PUT, "messages", json_data=payload)
        return Message.from_dict(data)

    async def delete_message(self, message_id: str) -> bool:
        """Delete message"""
        await self._make_request(HTTPMethod.DELETE, f"messages/{message_id}")
        return True

    async def get_message(self, message_id: str) -> Message:
        """Get message by ID"""
        data = await self._make_request(HTTPMethod.GET, f"messages/{message_id}")
        return Message.from_dict(data)

    async def get_video_info(self, video_token: str) -> Dict[str, Any]:
        """Get video information"""
        return await self._make_request(HTTPMethod.GET, f"videos/{video_token}")

    async def answer_callback(self, callback_id: str, text: Optional[str] = None) -> bool:
        """Answer to callback"""
        payload = {"callback_id": callback_id}
        if text:
            payload['text'] = text

        await self._make_request(HTTPMethod.POST, "answers", json_data=payload)
        return True