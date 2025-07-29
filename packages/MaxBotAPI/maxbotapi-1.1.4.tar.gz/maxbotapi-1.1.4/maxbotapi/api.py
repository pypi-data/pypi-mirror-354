import aiohttp
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum


class MessageType(Enum):
    TEXT = "text"
    PHOTO = "photo"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"
    LOCATION = "location"
    CONTACT = "contact"
    STICKER = "sticker"
    VOICE = "voice"


class ChatAction(Enum):
    TYPING = "typing"
    UPLOAD_PHOTO = "upload_photo"
    RECORD_VIDEO = "record_video"
    UPLOAD_VIDEO = "upload_video"
    RECORD_VOICE = "record_voice"
    UPLOAD_VOICE = "upload_voice"
    UPLOAD_DOCUMENT = "upload_document"
    FIND_LOCATION = "find_location"
    RECORD_VIDEO_NOTE = "record_video_note"
    UPLOAD_VIDEO_NOTE = "upload_video_note"


@dataclass
class User:
    user_id: int
    first_name: str
    username: Optional[str] = None
    is_bot: Optional[bool] = None
    last_activity_time: Optional[int] = None
    name: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        return cls(
            user_id=data['user_id'],
            first_name=data['first_name'],
            username=data.get('username'),
            is_bot=data.get('is_bot'),
            last_activity_time=data.get('last_activity_time'),
            name=data.get('name')
        )


@dataclass
class Chat:
    chat_id: str
    title: str
    type: str
    link: Optional[str] = None
    description: Optional[str] = None
    photo_id: Optional[str] = None
    pinned_message_id: Optional[str] = None
    members_count: Optional[int] = None
    created_at: Optional[int] = None
    updated_at: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Chat':
        return cls(
            chat_id=data['chat_id'],
            title=data['title'],
            type=data['type'],
            link=data.get('link'),
            description=data.get('description'),
            photo_id=data.get('photo_id'),
            pinned_message_id=data.get('pinned_message_id'),
            members_count=data.get('members_count'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )


@dataclass
class Message:
    message_id: str
    chat_id: str
    sender: User
    type: MessageType
    text: Optional[str] = None
    photo_id: Optional[str] = None
    video_token: Optional[str] = None
    audio_id: Optional[str] = None
    document_id: Optional[str] = None
    created_at: Optional[int] = None
    edited_at: Optional[int] = None
    reply_to_message_id: Optional[str] = None
    forward_from: Optional[User] = None
    forward_from_chat: Optional[Chat] = None
    forward_from_message_id: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        return cls(
            message_id=data['message_id'],
            chat_id=data['chat_id'],
            sender=User.from_dict(data['sender']),
            type=MessageType(data['type']),
            text=data.get('text'),
            photo_id=data.get('photo_id'),
            video_token=data.get('video_token'),
            audio_id=data.get('audio_id'),
            document_id=data.get('document_id'),
            created_at=data.get('created_at'),
            edited_at=data.get('edited_at'),
            reply_to_message_id=data.get('reply_to_message_id'),
            forward_from=User.from_dict(data['forward_from']) if 'forward_from' in data else None,
            forward_from_chat=Chat.from_dict(data['forward_from_chat']) if 'forward_from_chat' in data else None,
            forward_from_message_id=data.get('forward_from_message_id')
        )


@dataclass
class NewMessageBody:
    chat_id: str
    text: str
    reply_to_message_id: Optional[str] = None
    inline_keyboard: Optional[List[List[Dict[str, Any]]]] = None

    def to_dict(self) -> Dict[str, Any]:
        data = {
            'chat_id': self.chat_id,
            'text': self.text
        }
        if self.reply_to_message_id:
            data['reply_to_message_id'] = self.reply_to_message_id
        if self.inline_keyboard:
            data['inline_keyboard'] = self.inline_keyboard
        return data


@dataclass
class Update:
    update_id: int
    message: Optional[Message] = None
    edited_message: Optional[Message] = None
    channel_post: Optional[Message] = None
    edited_channel_post: Optional[Message] = None
    callback_query: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Update':
        message = None
        if 'message' in data:
            message = Message.from_dict(data['message'])

        edited_message = None
        if 'edited_message' in data:
            edited_message = Message.from_dict(data['edited_message'])

        channel_post = None
        if 'channel_post' in data:
            channel_post = Message.from_dict(data['channel_post'])

        edited_channel_post = None
        if 'edited_channel_post' in data:
            edited_channel_post = Message.from_dict(data['edited_channel_post'])

        return cls(
            update_id=data['update_id'],
            message=message,
            edited_message=edited_message,
            channel_post=channel_post,
            edited_channel_post=edited_channel_post,
            callback_query=data.get('callback_query')
        )


class Bot:
    BASE_URL = "https://botapi.max.ru"

    def __init__(self, token: str):
        self.token = token
        self.session = aiohttp.ClientSession()

    async def close(self):
        await self.session.close()

    async def _make_request(
            self,
            method: str,
            endpoint: str,
            params: Optional[Dict[str, Any]] = None,
            data: Optional[Dict[str, Any]] = None,
            json: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        url = f"{self.BASE_URL}{endpoint}"
        params = params or {}
        params['access_token'] = self.token

        async with self.session.request(
                method,
                url,
                params=params,
                data=data,
                json=json
        ) as response:
            response.raise_for_status()
            return await response.json()

    # Bot methods
    async def get_bot_info(self) -> User:
        """Get information about the current bot"""
        data = await self._make_request("GET", "/me")
        return User.from_dict(data)

    async def update_bot_info(
            self,
            first_name: Optional[str] = None,
            username: Optional[str] = None,
            name: Optional[str] = None
    ) -> User:
        """Update information about the current bot"""
        payload = {}
        if first_name is not None:
            payload['first_name'] = first_name
        if username is not None:
            payload['username'] = username
        if name is not None:
            payload['name'] = name

        data = await self._make_request("PATCH", "/me", json=payload)
        return User.from_dict(data)

    # Chats methods
    async def get_chats(self) -> List[Chat]:
        """Get list of all chats"""
        data = await self._make_request("GET", "/chats")
        return [Chat.from_dict(chat) for chat in data.get('chats', [])]

    async def get_chat_by_link(self, chat_link: str) -> Chat:
        """Get chat by link"""
        data = await self._make_request("GET", f"/chats/{chat_link}")
        return Chat.from_dict(data)

    async def get_chat_info(self, chat_id: str) -> Chat:
        """Get information about a chat"""
        data = await self._make_request("GET", f"/chats/{chat_id}")
        return Chat.from_dict(data)

    async def update_chat_info(
            self,
            chat_id: str,
            title: Optional[str] = None,
            description: Optional[str] = None,
            photo_id: Optional[str] = None
    ) -> Chat:
        """Update information about a chat"""
        payload = {}
        if title is not None:
            payload['title'] = title
        if description is not None:
            payload['description'] = description
        if photo_id is not None:
            payload['photo_id'] = photo_id

        data = await self._make_request("PATCH", f"/chats/{chat_id}", json=payload)
        return Chat.from_dict(data)

    async def delete_chat(self, chat_id: str) -> bool:
        """Delete a chat"""
        await self._make_request("DELETE", f"/chats/{chat_id}")
        return True

    async def send_chat_action(self, chat_id: str, action: ChatAction) -> bool:
        """Send action to a chat"""
        await self._make_request("POST", f"/chats/{chat_id}/actions", json={'action': action.value})
        return True

    async def get_pinned_message(self, chat_id: str) -> Optional[Message]:
        """Get pinned message in a chat"""
        data = await self._make_request("GET", f"/chats/{chat_id}/pin")
        return Message.from_dict(data) if data else None

    async def pin_message(self, chat_id: str, message_id: str) -> bool:
        """Pin a message in a chat"""
        await self._make_request("PUT", f"/chats/{chat_id}/pin", json={'message_id': message_id})
        return True

    async def unpin_message(self, chat_id: str) -> bool:
        """Unpin message in a chat"""
        await self._make_request("DELETE", f"/chats/{chat_id}/pin")
        return True

    async def get_chat_membership(self, chat_id: str) -> Dict[str, Any]:
        """Get information about bot's membership in a chat"""
        return await self._make_request("GET", f"/chats/{chat_id}/members/me")

    async def leave_chat(self, chat_id: str) -> bool:
        """Remove bot from a chat"""
        await self._make_request("DELETE", f"/chats/{chat_id}/members/me")
        return True

    async def get_chat_admins(self, chat_id: str) -> List[User]:
        """Get list of chat administrators"""
        data = await self._make_request("GET", f"/chats/{chat_id}/members/admins")
        return [User.from_dict(admin) for admin in data.get('admins', [])]

    async def promote_to_admin(self, chat_id: str, user_id: int) -> bool:
        """Promote user to chat administrator"""
        await self._make_request("POST", f"/chats/{chat_id}/members/admins", json={'user_id': user_id})
        return True

    async def demote_admin(self, chat_id: str, user_id: int) -> bool:
        """Demote chat administrator"""
        await self._make_request("DELETE", f"/chats/{chat_id}/members/admins/{user_id}")
        return True

    async def get_chat_members(self, chat_id: str) -> List[User]:
        """Get chat members"""
        data = await self._make_request("GET", f"/chats/{chat_id}/members")
        return [User.from_dict(member) for member in data.get('members', [])]

    async def add_chat_members(self, chat_id: str, user_ids: List[int]) -> bool:
        """Add members to a chat"""
        await self._make_request("POST", f"/chats/{chat_id}/members", json={'user_ids': user_ids})
        return True

    async def remove_chat_member(self, chat_id: str, user_id: int) -> bool:
        """Remove member from a chat"""
        await self._make_request("DELETE", f"/chats/{chat_id}/members/{user_id}")
        return True

    # Subscriptions methods
    async def get_subscriptions(self) -> Dict[str, Any]:
        """Get current subscriptions"""
        return await self._make_request("GET", "/subscriptions")

    async def subscribe(self, url: str, events: List[str]) -> Dict[str, Any]:
        """Subscribe to updates"""
        return await self._make_request("POST", "/subscriptions", json={
            'url': url,
            'events': events
        })

    async def unsubscribe(self, subscription_id: str) -> bool:
        """Unsubscribe from updates"""
        await self._make_request("DELETE", f"/subscriptions/{subscription_id}")
        return True

    async def get_updates(self, timeout: Optional[int] = None, limit: Optional[int] = None) -> List[Update]:
        """Get updates"""
        params = {}
        if timeout is not None:
            params['timeout'] = timeout
        if limit is not None:
            params['limit'] = limit

        data = await self._make_request("GET", "/updates", params=params)
        return [Update.from_dict(update) for update in data.get('updates', [])]

    # Uploads methods
    async def get_upload_url(self, file_name: str, file_size: int, mime_type: str) -> Dict[str, Any]:
        """Get URL for file upload"""
        return await self._make_request("POST", "/uploads", json={
            'file_name': file_name,
            'file_size': file_size,
            'mime_type': mime_type
        })

    # Messages methods
    async def get_messages(
            self,
            chat_id: Optional[str] = None,
            limit: Optional[int] = None,
            offset: Optional[int] = None
    ) -> List[Message]:
        """Get messages"""
        params = {}
        if chat_id is not None:
            params['chat_id'] = chat_id
        if limit is not None:
            params['limit'] = limit
        if offset is not None:
            params['offset'] = offset

        data = await self._make_request("GET", "/messages", params=params)
        return [Message.from_dict(message) for message in data.get('messages', [])]

    async def send_message(self, message: NewMessageBody) -> Message:
        """Send a message"""
        data = await self._make_request("POST", "/messages", json=message.to_dict())
        return Message.from_dict(data)

    async def edit_message(self, message_id: str, text: str) -> Message:
        """Edit a message"""
        data = await self._make_request("PUT", "/messages", json={
            'message_id': message_id,
            'text': text
        })
        return Message.from_dict(data)

    async def delete_message(self, message_id: str) -> bool:
        """Delete a message"""
        await self._make_request("DELETE", "/messages", json={'message_id': message_id})
        return True

    async def get_message(self, message_id: str) -> Message:
        """Get a message by ID"""
        data = await self._make_request("GET", f"/messages/{message_id}")
        return Message.from_dict(data)

    async def get_video_info(self, video_token: str) -> Dict[str, Any]:
        """Get information about a video"""
        return await self._make_request("GET", f"/videos/{video_token}")

    async def answer_callback(self, callback_query_id: str, text: Optional[str] = None) -> bool:
        """Answer a callback query"""
        payload = {'callback_query_id': callback_query_id}
        if text is not None:
            payload['text'] = text

        await self._make_request("POST", "/answers", json=payload)
        return True