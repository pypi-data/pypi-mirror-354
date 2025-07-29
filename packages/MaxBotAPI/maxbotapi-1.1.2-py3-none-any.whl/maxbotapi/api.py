import aiohttp
from typing import Optional, Dict, Any, List


class MaxAPIError(Exception):
    """Base exception for Max API errors"""
    pass


class User:
    """Represents a User object from Max API"""

    def __init__(self, data: Dict[str, Any]):
        self.id = data.get('id')
        self.username = data.get('username')
        self.first_name = data.get('firstName')
        self.last_name = data.get('lastName')
        self.phone = data.get('phone')
        self.avatar = data.get('avatar')
        self.is_bot = data.get('isBot')
        self.is_verified = data.get('isVerified')
        self.is_scam = data.get('isScam')
        self.is_support = data.get('isSupport')
        self.language_code = data.get('languageCode')


class Chat:
    """Represents a Chat object from Max API"""

    def __init__(self, data: Dict[str, Any]):
        self.id = data.get('id')
        self.type = data.get('type')
        self.title = data.get('title')
        self.photo = data.get('photo')
        self.link = data.get('link')
        self.description = data.get('description')
        self.members_count = data.get('membersCount')
        self.is_verified = data.get('isVerified')
        self.is_scam = data.get('isScam')
        self.is_support = data.get('isSupport')
        self.is_creator = data.get('isCreator')
        self.is_admin = data.get('isAdmin')
        self.can_edit = data.get('canEdit')
        self.can_pin = data.get('canPin')
        self.can_invite = data.get('canInvite')
        self.can_promote = data.get('canPromote')


class Message:
    """Represents a Message object from Max API"""

    def __init__(self, data: Dict[str, Any]):
        self.id = data.get('id')
        self.chat_id = data.get('chatId')
        self.user_id = data.get('userId')
        self.text = data.get('text')
        self.photo = data.get('photo')
        self.video = data.get('video')
        self.document = data.get('document')
        self.audio = data.get('audio')
        self.sticker = data.get('sticker')
        self.voice = data.get('voice')
        self.video_note = data.get('videoNote')
        self.contact = data.get('contact')
        self.location = data.get('location')
        self.venue = data.get('venue')
        self.poll = data.get('poll')
        self.dice = data.get('dice')
        self.game = data.get('game')
        self.invoice = data.get('invoice')
        self.animation = data.get('animation')
        self.entities = data.get('entities')
        self.date = data.get('date')
        self.edit_date = data.get('editDate')
        self.forward_from = data.get('forwardFrom')
        self.forward_from_chat = data.get('forwardFromChat')
        self.forward_from_message_id = data.get('forwardFromMessageId')
        self.reply_to_message = Message(data['replyToMessage']) if data.get('replyToMessage') else None
        self.via_bot = data.get('viaBot')
        self.views = data.get('views')
        self.is_pinned = data.get('isPinned')
        self.is_edited = data.get('isEdited')
        self.is_forwarded = data.get('isForwarded')
        self.has_media = data.get('hasMedia')
        self.has_photo = data.get('hasPhoto')
        self.has_video = data.get('hasVideo')
        self.has_document = data.get('hasDocument')
        self.has_audio = data.get('hasAudio')
        self.has_voice = data.get('hasVoice')
        self.has_video_note = data.get('hasVideoNote')
        self.has_contact = data.get('hasContact')
        self.has_location = data.get('hasLocation')
        self.has_venue = data.get('hasVenue')
        self.has_poll = data.get('hasPoll')
        self.has_dice = data.get('hasDice')
        self.has_game = data.get('hasGame')
        self.has_invoice = data.get('hasInvoice')
        self.has_animation = data.get('hasAnimation')


class NewMessageBody:
    """Represents a NewMessageBody object for sending messages"""

    def __init__(self, chat_id: str, text: str,
                 reply_markup: Optional[Dict[str, Any]] = None,
                 parse_mode: Optional[str] = None,
                 disable_web_page_preview: Optional[bool] = None,
                 disable_notification: Optional[bool] = None):
        self.chat_id = chat_id
        self.text = text
        self.reply_markup = reply_markup
        self.parse_mode = parse_mode
        self.disable_web_page_preview = disable_web_page_preview
        self.disable_notification = disable_notification

    def to_dict(self) -> Dict[str, Any]:
        return {
            'chatId': self.chat_id,
            'text': self.text,
            'replyMarkup': self.reply_markup,
            'parseMode': self.parse_mode,
            'disableWebPagePreview': self.disable_web_page_preview,
            'disableNotification': self.disable_notification
        }


class Update:
    """Represents an Update object from Max API"""

    def __init__(self, data: Dict[str, Any]):
        self.update_id = data.get('updateId')
        self.message = Message(data['message']) if data.get('message') else None
        self.edited_message = Message(data['editedMessage']) if data.get('editedMessage') else None
        self.channel_post = Message(data['channelPost']) if data.get('channelPost') else None
        self.edited_channel_post = Message(data['editedChannelPost']) if data.get('editedChannelPost') else None
        self.callback_query = data.get('callbackQuery')
        self.poll = data.get('poll')
        self.poll_answer = data.get('pollAnswer')
        self.my_chat_member = data.get('myChatMember')
        self.chat_member = data.get('chatMember')
        self.chat_join_request = data.get('chatJoinRequest')


class MaxAPI:
    """Asynchronous Python client for the Max Messenger API"""

    def __init__(self, token: str, base_url: str = "botapi.max.ru"):
        self.token = token
        self.base_url = base_url
        self.session = None

    async def _ensure_session(self):
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()

    async def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        await self._ensure_session()

        url = f"{self.base_url}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        async with self.session.request(method, url, headers=headers, **kwargs) as response:
            if response.status != 200:
                error_text = await response.text()
                raise MaxAPIError(f"API request failed with status {response.status}: {error_text}")

            return await response.json()

    async def close(self):
        """Close the aiohttp session"""
        if self.session and not self.session.closed:
            await self.session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    # Bot methods
    async def get_bot_info(self) -> User:
        """Get information about the current bot"""
        response = await self._request("GET", "/me")
        return User(response)

    async def update_bot_info(self, **kwargs) -> User:
        """Update information about the current bot

        Args:
            kwargs: Fields to update (username, firstName, lastName, description, etc.)
        """
        response = await self._request("PATCH", "/me", json=kwargs)
        return User(response)

    # Chats methods
    async def get_chats(self, limit: int = 100, offset: int = 0) -> List[Chat]:
        """Get list of all chats"""
        params = {"limit": limit, "offset": offset}
        response = await self._request("GET", "/chats", params=params)
        return [Chat(chat_data) for chat_data in response.get('chats', [])]

    async def get_chat_by_link(self, chat_link: str) -> Chat:
        """Get chat by its link"""
        response = await self._request("GET", f"/chats/{chat_link}")
        return Chat(response)

    async def get_chat_info(self, chat_id: str) -> Chat:
        """Get information about a chat"""
        response = await self._request("GET", f"/chats/{chat_id}")
        return Chat(response)

    async def update_chat_info(self, chat_id: str, **kwargs) -> Chat:
        """Update information about a chat

        Args:
            chat_id: ID of the chat to update
            kwargs: Fields to update (title, description, photo, etc.)
        """
        response = await self._request("PATCH", f"/chats/{chat_id}", json=kwargs)
        return Chat(response)

    async def delete_chat(self, chat_id: str) -> bool:
        """Delete a chat"""
        await self._request("DELETE", f"/chats/{chat_id}")
        return True

    async def send_chat_action(self, chat_id: str, action: str) -> bool:
        """Send an action to a chat (typing, uploading photo, etc.)"""
        await self._request("POST", f"/chats/{chat_id}/actions", json={"action": action})
        return True

    async def get_pinned_message(self, chat_id: str) -> Optional[Message]:
        """Get the pinned message in a chat"""
        response = await self._request("GET", f"/chats/{chat_id}/pin")
        return Message(response) if response else None

    async def pin_message(self, chat_id: str, message_id: str) -> bool:
        """Pin a message in a chat"""
        await self._request("PUT", f"/chats/{chat_id}/pin", json={"messageId": message_id})
        return True

    async def unpin_message(self, chat_id: str) -> bool:
        """Unpin the pinned message in a chat"""
        await self._request("DELETE", f"/chats/{chat_id}/pin")
        return True

    async def get_chat_membership(self, chat_id: str) -> Dict[str, Any]:
        """Get information about the bot's membership in a chat"""
        return await self._request("GET", f"/chats/{chat_id}/members/me")

    async def leave_chat(self, chat_id: str) -> bool:
        """Remove the bot from a chat"""
        await self._request("DELETE", f"/chats/{chat_id}/members/me")
        return True

    async def get_chat_admins(self, chat_id: str) -> List[User]:
        """Get list of chat administrators"""
        response = await self._request("GET", f"/chats/{chat_id}/members/admins")
        return [User(admin_data) for admin_data in response.get('admins', [])]

    async def promote_chat_admin(self, chat_id: str, user_id: str) -> bool:
        """Promote a user to chat administrator"""
        await self._request("POST", f"/chats/{chat_id}/members/admins", json={"userId": user_id})
        return True

    async def demote_chat_admin(self, chat_id: str, user_id: str) -> bool:
        """Demote a chat administrator"""
        await self._request("DELETE", f"/chats/{chat_id}/members/admins/{user_id}")
        return True

    async def get_chat_members(self, chat_id: str) -> List[User]:
        """Get list of chat members"""
        response = await self._request("GET", f"/chats/{chat_id}/members")
        return [User(member_data) for member_data in response.get('members', [])]

    async def add_chat_members(self, chat_id: str, user_ids: List[str]) -> bool:
        """Add members to a chat"""
        await self._request("POST", f"/chats/{chat_id}/members", json={"userIds": user_ids})
        return True

    async def remove_chat_member(self, chat_id: str, user_id: str) -> bool:
        """Remove a member from a chat"""
        await self._request("DELETE", f"/chats/{chat_id}/members/{user_id}")
        return True

    # Subscriptions methods
    async def get_subscriptions(self) -> List[Dict[str, Any]]:
        """Get list of current subscriptions"""
        response = await self._request("GET", "/subscriptions")
        return response.get('subscriptions', [])

    async def subscribe(self, url: str, events: List[str]) -> Dict[str, Any]:
        """Subscribe to updates"""
        payload = {"url": url, "events": events}
        return await self._request("POST", "/subscriptions", json=payload)

    async def unsubscribe(self, subscription_id: str) -> bool:
        """Unsubscribe from updates"""
        await self._request("DELETE", f"/subscriptions/{subscription_id}")
        return True

    async def get_updates(self, limit: int = 100, offset: int = 0) -> List[Update]:
        """Get updates"""
        params = {"limit": limit, "offset": offset}
        response = await self._request("GET", "/updates", params=params)
        return [Update(update_data) for update_data in response.get('updates', [])]

    # Uploads methods
    async def get_upload_url(self, file_name: str, file_size: int, mime_type: str) -> Dict[str, Any]:
        """Get URL for file upload"""
        payload = {
            "fileName": file_name,
            "fileSize": file_size,
            "mimeType": mime_type
        }
        return await self._request("POST", "/uploads", json=payload)

    # Messages methods
    async def get_messages(self, chat_id: str, limit: int = 100, offset: int = 0) -> List[Message]:
        """Get messages from a chat"""
        params = {"chatId": chat_id, "limit": limit, "offset": offset}
        response = await self._request("GET", "/messages", params=params)
        return [Message(msg_data) for msg_data in response.get('messages', [])]

    async def send_message(self, message: NewMessageBody) -> Message:
        """Send a message"""
        response = await self._request("POST", "/messages", json=message.to_dict())
        return Message(response)

    async def edit_message(self, message_id: str, text: str,
                           reply_markup: Optional[Dict[str, Any]] = None) -> Message:
        """Edit a message"""
        payload = {
            "messageId": message_id,
            "text": text,
            "replyMarkup": reply_markup
        }
        response = await self._request("PUT", "/messages", json=payload)
        return Message(response)

    async def delete_message(self, message_id: str) -> bool:
        """Delete a message"""
        await self._request("DELETE", f"/messages/{message_id}")
        return True

    async def get_message(self, message_id: str) -> Message:
        """Get a specific message"""
        response = await self._request("GET", f"/messages/{message_id}")
        return Message(response)

    async def get_video_info(self, video_token: str) -> Dict[str, Any]:
        """Get information about a video"""
        return await self._request("GET", f"/videos/{video_token}")

    async def answer_callback(self, callback_query_id: str, text: Optional[str] = None,
                              show_alert: bool = False, url: Optional[str] = None) -> bool:
        """Answer a callback query"""
        payload = {
            "callbackQueryId": callback_query_id,
            "text": text,
            "showAlert": show_alert,
            "url": url
        }
        await self._request("POST", "/answers", json=payload)
        return True
