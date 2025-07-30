import base64
import logging
from typing import List

from ephor_cli.services.conversation_attachment import ConversationAttachmentService

def process_attachments(message, s3_service, user_id: str = None, project_id: str = None, conversation_id: str = None):
    """Process both message-level and conversation-level attachments."""
    attachments = message.additional_kwargs.get("attachments", [])
    if not attachments and not (user_id and project_id and conversation_id):
        return message

    # Handle both string and list content formats
    if isinstance(message.content, str):
        content = [{"type": "text", "text": message.content}]
    elif isinstance(message.content, list):
        content = message.content.copy()  
    else:
        content = [{"type": "text", "text": ""}]

    # Process message-level attachments
    for att in attachments:
        s3_key = att.get("s3_key")
        file_type = att.get("type", "")
        name = att.get("name", "")
        if not s3_key:
            continue
        try:
            file_content = s3_service.get_file_content(s3_key)
            if not file_content:
                continue

            if file_type.startswith("image/"):
                b64_data = base64.b64encode(file_content).decode("utf-8")
                content.append({
                    "type": "image",
                    "source_type": "base64",
                    "data": b64_data,
                    "mime_type": file_type,
                    "filename": name
                })
            elif file_type == "application/pdf":
                b64_data = base64.b64encode(file_content).decode("utf-8")
                content.append({
                    "type": "file",
                    "source_type": "base64",
                    "data": b64_data,
                    "mime_type": "application/pdf",
                    "filename": name
                })
            elif file_type == "text/plain":
                try:
                    text_content = file_content.decode("utf-8")
                    content.append({
                        "type": "text",
                        "text": f"<context>Content of {name}:\n\n{text_content}</context>"
                    })
                except UnicodeDecodeError:
                    pass
            else:
                content.append({
                    "type": "text",
                    "text": f"[File {name} attached, but type {file_type} is not supported for LLM input]"
                })
        except Exception as e:
            content.append({
                "type": "text",
                "text": f"[Could not load {name}: {e}]"
            })

    # Process conversation-level attachments if user_id, project_id, and conversation_id are provided
    if user_id and project_id and conversation_id:
        conversation_attachment_service = ConversationAttachmentService()
        conversation_attachments = conversation_attachment_service.list_attachments(
            user_id, project_id, conversation_id
        )

        for att in conversation_attachments:
            try:
                file_content = s3_service.get_file_content(att.s3_key)
                if not file_content:
                    continue

                if att.file_type.startswith("image/"):
                    b64_data = base64.b64encode(file_content).decode("utf-8")
                    content.append({
                        "type": "image",
                        "source_type": "base64",
                        "data": b64_data,
                        "mime_type": att.file_type,
                        "filename": att.file_name
                    })
                elif att.file_type == "application/pdf":
                    b64_data = base64.b64encode(file_content).decode("utf-8")
                    content.append({
                        "type": "file",
                        "source_type": "base64",
                        "data": b64_data,
                        "mime_type": "application/pdf",
                        "filename": att.file_name
                    })
                elif att.file_type == "text/plain":
                    try:
                        text_content = file_content.decode("utf-8")
                        content.append({
                            "type": "text",
                            "text": f"<context>Content of {att.file_name}:\n\n{text_content}</context>"
                        })
                    except UnicodeDecodeError:
                        pass                
                else:
                    content.append({
                        "type": "text",
                        "text": f"[File {att.file_name} attached, but type {att.file_type} is not supported for LLM input]"
                    })
            except Exception as e:
                content.append({
                    "type": "text",
                    "text": f"[Could not load {att.file_name}: {e}]"
                })

    message.content = content
    logging.debug("[attachments.py] Message content after attachment processing: %s", message.content)
    return message 

def cleanup_text_content_for_storage(message):
    """Clean up text file content from message before database storage.
    
    Removes content within <context></context> tags and replaces with metadata to prevent database bloat.
    """
    if not isinstance(message.content, list):
        return message

    cleaned_content = []

    for item in message.content:
        if item.get("type") == "text":
            text = item.get("text", "")

            # Check if this contains context tags with text file content
            if "<context>" in text and "</context>" in text:
                # Extract filename from the content within context tags
                start_tag = text.find("<context>")
                end_tag = text.find("</context>")

                if start_tag != -1 and end_tag != -1:
                    context_content = text[start_tag + 9:end_tag]  # +9 for len("<context>")

                    # Extract filename from "Content of filename:"
                    if context_content.startswith("Content of ") and ":\n\n" in context_content:
                        # Completely skip this item - don't add anything to cleaned_content
                        continue

        # Keep all other content as-is
        cleaned_content.append(item)

    # Update message content with cleaned version
    message.content = cleaned_content
    return message 