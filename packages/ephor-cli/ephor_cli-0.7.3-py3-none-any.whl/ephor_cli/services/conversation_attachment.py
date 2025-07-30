from typing import List
import os

from ephor_cli.clients.ddb.conversation_attachment import ConversationAttachmentDDBClient
from ephor_cli.types.conversation_attachment import ConversationAttachment
from ephor_cli.constant import DYNAMODB_TABLE_NAME


class ConversationAttachmentService:
    """Service for handling conversation attachment operations."""

    def __init__(self):
        self.ddb_client = ConversationAttachmentDDBClient(table_name=DYNAMODB_TABLE_NAME)

    def create_attachment(self, attachment: ConversationAttachment) -> ConversationAttachment:
        """Create a new conversation attachment.

        Args:
            attachment: The attachment to create

        Returns:
            The created attachment
        """
        success = self.ddb_client.store_attachment(attachment)
        if not success:
            raise Exception("Failed to store conversation attachment")
        return attachment

    def list_attachments(
        self, user_id: str, project_id: str, conversation_id: str
    ) -> List[ConversationAttachment]:
        """List all attachments for a conversation.

        Args:
            user_id: The ID of the user who owns the conversation
            project_id: The ID of the project the conversation belongs to
            conversation_id: The ID of the conversation

        Returns:
            List of conversation attachments
        """
        return self.ddb_client.list_attachments(user_id, project_id, conversation_id)

    def delete_attachment(
        self, user_id: str, project_id: str, conversation_id: str, attachment_id: str
    ) -> bool:
        """Delete a conversation attachment.

        Args:
            user_id: The ID of the user who owns the conversation
            project_id: The ID of the project the conversation belongs to
            conversation_id: The ID of the conversation
            attachment_id: The ID of the attachment to delete

        Returns:
            True if successful, False otherwise
        """
        return self.ddb_client.delete_attachment(user_id, project_id, conversation_id, attachment_id)

    def get_attachment_count(self, user_id: str, project_id: str, conversation_id: str) -> int:
        """Get the total count of attachments for a conversation.

        Args:
            user_id: The ID of the user who owns the conversation
            project_id: The ID of the project the conversation belongs to
            conversation_id: The ID of the conversation

        Returns:
            Total number of attachments
        """
        return self.ddb_client.get_attachment_count(user_id, project_id, conversation_id) 