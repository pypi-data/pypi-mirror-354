r'''
# Wasend SDK

A powerful SDK for managing WhatsApp sessions across multiple programming languages. This SDK provides a simple and intuitive interface for creating, managing, and interacting with WhatsApp sessions.

## Features

* Create and manage WhatsApp sessions
* QR code authentication
* Session status management (create, start, stop, restart, delete, get QR code, get session info, get all sessions)
* Contact management (get contact, get all contacts, check if contact exists, get profile picture)
* Message sending (text, image, video, file, voice, link with custom preview, mark messages as seen)
* Group management (create, manage participants, settings, invites)
* Account protection features
* Message logging
* Webhook support
* Multi-language support (TypeScript/JavaScript, Python, Java, .NET, Go)

## Installation

### TypeScript/JavaScript (npm)

```bash
npm install @wasend/core
# or
yarn add @wasend/core
```

### Python (pip)

```bash
pip install wasend-dev
```

### Java (Maven)

```xml
<dependency>
    <groupId>com.wasend</groupId>
    <artifactId>wasend-core</artifactId>
    <version>1.0.0</version>
</dependency>
```

### .NET (NuGet)

```bash
dotnet add package Wasend.Core
```

### Go

```bash
go get github.com/wasenddev/wasend-sdk-go
```

## Quick Start

### TypeScript/JavaScript Example

```python
import { WasendClient, SessionCreateRequest } from '@wasend/core';

async function main() {
    // Initialize the client
    const client = new WasendClient({
        apiKey: 'your-api-key',
        baseUrl: 'https://api.wasend.dev'
    });

    // Create a new session
    const sessionParams: SessionCreateRequest = {
        sessionName: 'my-whatsapp-session',
        phoneNumber: '+919876543210', // Example phone number
        enableAccountProtection: true,
        enableMessageLogging: true,
        enableWebhook: false
    };
    const session = await client.createSession(sessionParams);

    // Get QR code for authentication
    const qrCode = await client.getQRCode(session.uniqueSessionId);
    console.log('Scan this QR code with WhatsApp:', qrCode.data);

    // Start the session
    await client.startSession(session.uniqueSessionId);

    // Get session information
    const sessionInfo = await client.getSessionInfo(session.uniqueSessionId);
    console.log('Session status:', sessionInfo.status);
}

main().catch(console.error);
```

### Python Example

```python
from wasend_dev import WasendClient

# Initialize the client
client = WasendClient(api_key='your-api-key', base_url='https://api.wasend.dev')

try:
    # Create a new session
    session = client.create_session(
        session_name='my-whatsapp-session-python',
        phone_number='+919876543210',  # Example phone number
        enable_account_protection=True,
        enable_message_logging=True,
        enable_webhook=False
    )
    # Assuming session object has unique_session_id or similar attribute/key
    # e.g., session.unique_session_id or session['uniqueSessionId']
    # For this example, let's assume it's session.unique_session_id based on TS example structure

    print(f"Session created with ID: {session.unique_session_id}")

    # Get QR code for authentication
    qr_code_response = client.get_qr_code(session_id=session.unique_session_id)
    print(f"Scan this QR code with WhatsApp: {qr_code_response.data}")

    # Start the session
    client.start_session(session_id=session.unique_session_id)
    print(f"Session {session.unique_session_id} starting...")

    # Get session information
    session_info = client.get_session_info(session_id=session.unique_session_id)
    print(f"Session status: {session_info.status}")

except Exception as e:
    print(f"An error occurred: {e}")
```

### Go Example

```go
package main

import (
	"fmt"
	"log"

	"github.com/wasenddev/wasend-sdk-go/wasend"
)

func main() {
	// Initialize the client
	// Ensure WasendClientOptions or similar struct is used if constructor expects it
	client, err := wasend.NewClient("your-api-key", "https://api.wasend.dev") // Or wasend.NewClient(&wasend.Config{...})
	if err != nil {
		log.Fatalf("Error creating client: %v", err)
	}

	// Create a new session
	sessionParams := wasend.SessionCreateRequest{
		SessionName:             "my-whatsapp-session-go",
		PhoneNumber:             "+919876543210", // Example phone number
		EnableAccountProtection: true,
		EnableMessageLogging:    true,
		EnableWebHook:           false,
	}
	session, err := client.CreateSession(sessionParams)
	if err != nil {
		log.Fatalf("Error creating session: %v", err)
	}
	fmt.Println("Session created with ID:", session.UniqueSessionId)

	// Get QR code for authentication
	qrCode, err := client.GetQRCode(session.UniqueSessionId)
	if err != nil {
		log.Fatalf("Error getting QR code: %v", err)
	}
	fmt.Println("Scan this QR code with WhatsApp:", qrCode.Data)

	// Start the session
	_, err = client.StartSession(session.UniqueSessionId)
	if err != nil {
		log.Fatalf("Error starting session: %v", err)
	}
	fmt.Println("Session starting...")

	// Get session information
	sessionInfo, err := client.GetSessionInfo(session.UniqueSessionId)
	if err != nil {
		log.Fatalf("Error getting session info: %v", err)
	}
	fmt.Println("Session status:", sessionInfo.Status)
}
```

### .NET Example

```csharp
using System;
using System.Threading.Tasks;
using Wasend.Core;

public class WasendExample
{
    public static async Task Main(string[] args)
    {
        // Initialize the client
        var client = new WasendClient(new WasendClientOptions
        {
            ApiKey = "your-api-key",
            BaseUrl = "https://api.wasend.dev"
        });

        try
        {
            // Create a new session
            var sessionParams = new SessionCreateRequest
            {
                SessionName = "my-whatsapp-session-dotnet",
                PhoneNumber = "+919876543210",
                EnableAccountProtection = true,
                EnableMessageLogging = true,
                EnableWebHook = false
            };
            var session = await client.CreateSessionAsync(sessionParams);
            Console.WriteLine($"Session created with ID: {session.UniqueSessionId}");

            // Get QR code for authentication
            var qrCode = await client.GetQRCodeAsync(session.UniqueSessionId);
            Console.WriteLine($"Scan this QR code with WhatsApp: {qrCode.Data}");

            // Start the session
            await client.StartSessionAsync(session.UniqueSessionId);
            Console.WriteLine($"Session {session.UniqueSessionId} starting...");

            // Get session information
            var sessionInfo = await client.GetSessionInfoAsync(session.UniqueSessionId);
            Console.WriteLine($"Session status: {sessionInfo.Status}");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"An error occurred: {ex.Message}");
        }
    }
}
```

## Session Management

### Creating a Session

```python
const session = await client.sessions.createSession({
    sessionName: 'my-whatsapp-session',
    phoneNumber: '+919876543210',
    enableAccountProtection: true,
    enableMessageLogging: true,
    enableWebhook: true,
    webhookUrl: 'https://your-webhook-url.com/callback'
});
```

### Session Configuration Options

* `sessionName`: A unique name for your session
* `phoneNumber`: The WhatsApp phone number to use (format: +[country code][number])
* `enableAccountProtection`: Enable additional security features
* `enableMessageLogging`: Enable message history logging
* `enableWebhook`: Enable webhook notifications
* `webhookUrl`: URL for receiving webhook notifications (required if enableWebhook is true)

### Managing Sessions

```python
// Get all sessions
const allSessions = await client.sessions.getAllSessions();

// Get specific session info
const sessionInfo = await client.sessions.getSessionInfo(sessionId);

// Start a session
await client.sessions.startSession(sessionId);

// Stop a session
await client.sessions.stopSession(sessionId);

// Restart a session
await client.sessions.restartSession(sessionId);

// Delete a session
await client.sessions.deleteSession(sessionId);
```

## Group Management

The SDK provides comprehensive group management features for WhatsApp groups.

### Creating a Group

```python
const group = await client.createGroup(sessionId, {
    name: "My Group",
    participants: [{ id: "+919876543210" }],
    description: "Group description"
});
```

### Group Configuration Options

* `name`: The name of the group
* `participants`: Array of participants with their phone numbers
* `description`: Optional group description
* `pictureUrl`: Optional URL for group picture
* `tags`: Optional array of tags for the group

### Managing Groups

```python
// Get all groups
const groups = await client.getGroups(sessionId);

// Get specific group info
const groupInfo = await client.getGroup(sessionId, groupId);

// Get group participants
const participants = await client.getGroupParticipants(sessionId, groupId);

// Add participants to group
await client.addGroupParticipants(sessionId, groupId, {
    participants: ["+919876543210"],
    notify: true
});

// Remove participants from group
await client.removeGroupParticipants(sessionId, groupId, {
    participants: ["+919876543210"],
    notify: true
});

// Promote participants to admin
await client.promoteGroupParticipants(sessionId, groupId, {
    participants: ["+919876543210"],
    notify: true
});

// Demote participants from admin
await client.demoteGroupParticipants(sessionId, groupId, {
    participants: ["+919876543210"],
    notify: true
});
```

### Group Settings

```python
// Set group description
await client.setGroupDescription(sessionId, groupId, {
    description: "New group description"
});

// Set group subject/name
await client.setGroupSubject(sessionId, groupId, {
    subject: "New group name"
});

// Set group picture
await client.setGroupPicture(sessionId, groupId, {
    url: "https://example.com/picture.jpg",
    format: "jpeg",
    cropToSquare: true
});

// Delete group picture
await client.deleteGroupPicture(sessionId, groupId);
```

### Group Security Settings

```python
// Set info admin only
await client.setGroupInfoAdminOnly(sessionId, groupId, {
    enabled: true
});

// Set messages admin only
await client.setGroupMessagesAdminOnly(sessionId, groupId, {
    enabled: true
});

// Get current security settings
const infoAdminOnly = await client.getGroupInfoAdminOnly(sessionId, groupId);
const messagesAdminOnly = await client.getGroupMessagesAdminOnly(sessionId, groupId);
```

### Group Invite Management

```python
// Get group invite code
const inviteCode = await client.getGroupInviteCode(sessionId, groupId);

// Revoke group invite code
const newInviteCode = await client.revokeGroupInviteCode(sessionId, groupId);

// Join a group using invite code
const joinInfo = await client.getGroupJoinInfo(sessionId, "https://chat.whatsapp.com/1234567890abcdef");
await client.joinGroup(sessionId, {
    code: "https://chat.whatsapp.com/1234567890abcdef"
});

// Leave a group
await client.leaveGroup(sessionId, groupId);
```

### Group Query Options

When retrieving groups, you can use various query parameters:

```python
const groups = await client.getGroups(sessionId, {
    sortBy: "creation",
    sortOrder: "desc",
    limit: 50,
    offset: 0,
    exclude: ["participants"],
    status: "ACTIVE",
    search: "group name",
    tags: ["tag1", "tag2"]
});
```

### Group Status

A group can have the following statuses:

* `ACTIVE`: Group is active and can be used
* `ARCHIVED`: Group has been archived
* `DELETED`: Group has been deleted

## Authentication

### QR Code Authentication

1. Create a session
2. Get the QR code
3. Scan the QR code with WhatsApp on your phone
4. The session will automatically connect once scanned

```python
const qrCode = await client.getQRCode(sessionId);
console.log('QR Code data:', qrCode.data);
```

## Session Status

A session can have the following statuses:

* `CREATED`: Session has been created but not started
* `STARTING`: Session is in the process of starting
* `CONNECTED`: Session is connected and ready to use
* `STOPPED`: Session has been stopped
* `ERROR`: Session encountered an error

## Webhook Integration

To receive notifications about session events:

1. Enable webhooks when creating a session
2. Provide a valid webhook URL
3. Handle incoming webhook notifications on your server

```python
const session = await client.sessions.createSession({
    sessionName: 'webhook-enabled-session',
    phoneNumber: '+919876543210',
    enableWebhook: true,
    webhookUrl: 'https://your-server.com/webhook'
});
```

## Error Handling

```python
try {
    const session = await client.sessions.createSession({
        sessionName: 'test-session',
        phoneNumber: '+919876543210'
    });
} catch (error) {
    console.error('Error creating session:', error);
}
```

## Contact Management

The SDK allows you to manage contacts associated with a session.

### Get Contact Details

```python
const contactId = "contact_jid@c.us";
const contact = await client.getContact(sessionId, contactId);
console.log('Contact details:', contact);
```

### Get All Contacts

```python
const params = { limit: 10, offset: 0, sortBy: "name", sortOrder: "asc" };
const contacts = await client.getContacts(sessionId, params);
console.log('Contacts list:', contacts);
```

### Check if Contact Exists

```python
const phoneNumber = "1234567890";
const exists = await client.checkContactExists(sessionId, { phone: phoneNumber });
console.log(`Contact with phone ${phoneNumber} exists:`, exists);
```

### Get Profile Picture URL

```python
const contactIdForPic = "contact_jid@c.us";
const picInfo = await client.getProfilePictureUrl(sessionId, { contactId: contactIdForPic, refresh: false });
console.log('Profile picture URL:', picInfo.url);
```

## Message Sending

The SDK provides methods to send various types of messages. All `send...` methods typically require the `sessionId` and a request object specific to the message type.

### Send Text Message

```python
const textMessage = {
    to: "recipient_jid@c.us",
    text: "Hello from Wasend SDK!"
};
const sentMessageInfo = await client.sendTextMessage(sessionId, textMessage);
console.log('Text message sent:', sentMessageInfo);
```

### Send Image Message

```python
const imageMessage = {
    to: "recipient_jid@c.us",
    url: "https://example.com/image.jpg",
    caption: "Check out this image!"
};
const sentImageInfo = await client.sendImageMessage(sessionId, imageMessage);
console.log('Image message sent:', sentImageInfo);
```

### Send Video Message

```python
const videoMessage = {
    to: "recipient_jid@c.us",
    url: "https://example.com/video.mp4",
    caption: "Watch this cool video!"
};
const sentVideoInfo = await client.sendVideoMessage(sessionId, videoMessage);
console.log('Video message sent:', sentVideoInfo);
```

### Send File/Document Message

```python
const fileMessage = {
    to: "recipient_jid@c.us",
    url: "https://example.com/document.pdf",
    fileName: "document.pdf",
    mimeType: "application/pdf"
};
const sentFileInfo = await client.sendFileMessage(sessionId, fileMessage);
console.log('File message sent:', sentFileInfo);
```

### Send Voice Message

```python
const voiceMessage = {
    to: "recipient_jid@c.us",
    url: "https://example.com/audio.ogg",
};
const sentVoiceInfo = await client.sendVoiceMessage(sessionId, voiceMessage);
console.log('Voice message sent:', sentVoiceInfo);
```

### Send Link with Custom Preview

```python
const linkPreview = {
    title: "Wasend SDK",
    description: "Powerful WhatsApp SDK",
    thumbnailUrl: "https://example.com/logo.png"
};

const linkMessage = {
    to: "recipient_jid@c.us",
    text: "Check out this SDK: https://wasend.dev",
    preview: linkPreview
};
const sentLinkInfo = await client.sendLinkWithCustomPreview(sessionId, linkMessage);
console.log('Link message with custom preview sent:', sentLinkInfo);
```

### Mark Message as Seen

```python
const seenRequest = {
    to: "sender_jid@c.us",
    messageId: "message_id_to_mark_seen"
};
await client.sendSeen(sessionId, seenRequest);
console.log('Message marked as seen.');
```

## Chat Management

The SDK provides methods to manage and retrieve chat information.

### Get All Chats

Retrieves all chats for a given session. You can paginate and sort the results.

**TypeScript**

```python
const chatsResponse = await client.getAllChats(sessionId, {
    limit: 10,
    sortBy: 'timestamp',
    sortOrder: 'desc'
});
if (chatsResponse.success && chatsResponse.data) {
    console.log('Chats:', chatsResponse.data);
} else {
    console.error('Failed to get chats:', chatsResponse.error);
}
```

**Python**

```python
# Ensure client is initialized: client = WasendClient(api_key='your-api-key')
# Assume sessionId is defined
try:
    chats_response = client.get_all_chats(
        session=sessionId,
        limit=10,
        sort_by='timestamp',
        sort_order='desc'
    )
    # Assuming the Python SDK client.get_all_chats returns an object
    # with success, data, and error attributes similar to the TypeScript SDK SdkResponse.
    if hasattr(chats_response, 'success') and chats_response.success and hasattr(chats_response, 'data'):
        print(f"Chats: {chats_response.data}")
    elif hasattr(chats_response, 'error'):
        print(f"Failed to get chats: {chats_response.error}")
    else:
        print(f"Chats: {chats_response}") # If it returns data directly on success
except Exception as e:
    print(f"An error occurred: {e}")
```

**Go**

```go
// Ensure client is initialized: client, err := wasend.NewClient(...)
// Assume sessionId is defined
// Assuming the Go SDK's GetAllChats returns (SdkResponseLikeObject, error)
// where SdkResponseLikeObject has Success, Data, Error fields.
options := &wasend.GetChatsOptions{
    Limit:     10,
    SortBy:    "timestamp",
    SortOrder: "desc",
}
sdkResponse, err := client.GetAllChats(sessionId, options) // Adjust method signature as per actual Go SDK
if err != nil {
    log.Fatalf("Error calling GetAllChats: %v", err)
}
if sdkResponse.Success {
    // Access sdkResponse.Data, which might need type assertion, e.g.:
    // chats, ok := sdkResponse.Data.([]wasend.Chat)
    // if !ok { log.Fatalf("Could not assert Data to []wasend.Chat") }
    fmt.Println("Chats:", sdkResponse.Data)
} else {
    log.Printf("Failed to get chats: %s", sdkResponse.Error)
}
```

**C# (.NET)**

```csharp
// Ensure client is initialized: var client = new WasendClient(new WasendClientOptions { ... });
// Assume sessionId is defined
var options = new GetChatsOptions
{
    Limit = 10,
    SortBy = "timestamp",
    SortOrder = "desc"
};
var chatsResponse = await client.GetAllChatsAsync(sessionId, options); // Adjust method signature as per actual .NET SDK
if (chatsResponse.Success && chatsResponse.Data != null)
{
    // Example: Assuming chatsResponse.Data is a list of Chat objects
    Console.WriteLine($"Chats count: {chatsResponse.Data.Count}");
    // foreach (var chat in chatsResponse.Data) { Console.WriteLine($"Chat ID: {chat.Id}"); }
}
else
{
    Console.WriteLine($"Failed to get chats: {chatsResponse.Error}");
}
```

### Get Chats Overview

Retrieves an overview of chats, allowing pagination and filtering by chat IDs.

**TypeScript**

```python
const overviewResponse = await client.getChatsOverview(sessionId, {
    limit: 10,
    ids: ['1234567890@c.us', 'another_chat_id@c.us']
});
if (overviewResponse.success && overviewResponse.data) {
    console.log('Chats Overview:', overviewResponse.data);
} else {
    console.error('Failed to get chats overview:', overviewResponse.error);
}
```

**Python**

```python
try:
    overview_response = client.get_chats_overview(
        session=sessionId,
        limit=10,
        ids=['1234567890@c.us', 'another_chat_id@c.us']
    )
    if hasattr(overview_response, 'success') and overview_response.success and hasattr(overview_response, 'data'):
        print(f"Chats Overview: {overview_response.data}")
    elif hasattr(overview_response, 'error'):
        print(f"Failed to get chats overview: {overview_response.error}")
    else:
        print(f"Chats Overview: {overview_response}")
except Exception as e:
    print(f"An error occurred: {e}")
```

**Go**

```go
options := &wasend.GetChatsOverviewOptions{
    Limit: 10,
    IDs:   []string{"1234567890@c.us", "another_chat_id@c.us"},
}
sdkResponse, err := client.GetChatsOverview(sessionId, options) // Adjust method signature as per actual Go SDK
if err != nil {
    log.Fatalf("Error calling GetChatsOverview: %v", err)
}
if sdkResponse.Success {
    fmt.Println("Chats Overview:", sdkResponse.Data)
} else {
    log.Printf("Failed to get chats overview: %s", sdkResponse.Error)
}
```

**C# (.NET)**

```csharp
var options = new GetChatsOverviewOptions
{
    Limit = 10,
    Ids = new List<string> { "1234567890@c.us", "another_chat_id@c.us" }
};
var overviewResponse = await client.GetChatsOverviewAsync(sessionId, options); // Adjust method signature as per actual .NET SDK
if (overviewResponse.Success && overviewResponse.Data != null)
{
    Console.WriteLine($"Chats Overview count: {overviewResponse.Data.Count}");
}
else
{
    Console.WriteLine($"Failed to get chats overview: {overviewResponse.Error}");
}
```

### Read Messages in a Chat

Marks messages in a specific chat as read. You can specify the number of latest messages or a number of days.

**TypeScript**

```python
const chatId = "recipient_or_group_jid@c.us"; // or "group_id@g.us"
const readResponse = await client.readMessages(sessionId, chatId, { messages: 5 }); // Mark last 5 messages as read
if (readResponse.success) {
    console.log(readResponse.message || 'Successfully marked messages as read.');
} else {
    console.error('Failed to mark messages as read:', readResponse.message);
}
```

**Python**

```python
chat_id = "recipient_or_group_jid@c.us"
try:
    read_response = client.read_messages(
        session=sessionId,
        chat_id=chat_id,
        messages=5  # Mark last 5 messages as read
        # or days=2 for messages from last 2 days
    )
    # read_messages is expected to return an object with 'success' and 'message' attributes
    if hasattr(read_response, 'success') and read_response.success:
        print(read_response.message or 'Successfully marked messages as read.')
    elif hasattr(read_response, 'message'):
        print(f"Failed to mark messages as read: {read_response.message}")
    else:
        print(f"Operation status unknown or failed: {read_response}")
except Exception as e:
    print(f"An error occurred: {e}")
```

**Go**

```go
chatId := "recipient_or_group_jid@c.us"
options := &wasend.ReadMessagesOptions{
    Messages: 5, // Mark last 5 messages as read
    // Days: 2, // Or mark messages from last 2 days
}
// readMessages returns a specific response type (ReadChatMessagesResponse in TS)
readResponse, err := client.ReadMessages(sessionId, chatId, options) // Adjust method signature
if err != nil {
    log.Fatalf("Error calling ReadMessages: %v", err)
}
if readResponse.Success {
    fmt.Println(readResponse.Message) // Message field from ReadChatMessagesResponse
} else {
    log.Printf("Failed to mark messages as read: %s", readResponse.Message)
}
```

**C# (.NET)**

```csharp
string chatId = "recipient_or_group_jid@c.us";
var options = new ReadMessagesOptions { Messages = 5 }; // Mark last 5 messages as read
// var options = new ReadMessagesOptions { Days = 2 }; // Or mark messages from last 2 days
var readResponse = await client.ReadMessagesAsync(sessionId, chatId, options); // Adjust method signature
if (readResponse.Success)
{
    Console.WriteLine(readResponse.Message ?? "Successfully marked messages as read.");
}
else
{
    Console.WriteLine($"Failed to mark messages as read: {read_response.Message}");
}
```

### Get Messages from a Chat

Retrieves messages from a chat, with options for pagination, media download, and filtering.

**TypeScript**

```python
const chatId = "recipient_or_group_jid@c.us";
const messagesResponse = await client.getMessages(sessionId, chatId, {
    limit: 10, // Required: number of messages to retrieve
    downloadMedia: true,
    filter: {
        timestampGte: Math.floor((Date.now() - 24 * 60 * 60 * 1000) / 1000), // Messages from last 24 hours
        fromMe: true, // Only messages sent by you
    },
});
if (messagesResponse.success && messagesResponse.data) {
    console.log('Messages:', messagesResponse.data);
} else {
    console.error('Failed to get messages:', messagesResponse.error);
}
```

**Python**

```python
import time
chat_id = "recipient_or_group_jid@c.us"
try:
    messages_response = client.get_messages(
        session=sessionId,
        chat_id=chat_id,
        limit=10,  # Required
        download_media=True,
        filter={
            'timestamp_gte': int(time.time()) - (24 * 60 * 60), # Last 24 hours
            'from_me': True
        }
    )
    if hasattr(messages_response, 'success') and messages_response.success and hasattr(messages_response, 'data'):
        print(f"Messages: {messages_response.data}")
    elif hasattr(messages_response, 'error'):
        print(f"Failed to get messages: {messages_response.error}")
    else:
        print(f"Messages: {messages_response}")
except Exception as e:
    print(f"An error occurred: {e}")
```

**Go**

```go
import "time"
chatId := "recipient_or_group_jid@c.us"
options := &wasend.GetMessagesOptions{
    Limit:         10, // Required
    DownloadMedia: true,
    Filter: &wasend.GetMessagesFilterOptions{
        TimestampGte: time.Now().Add(-24 * time.Hour).Unix(), // Last 24 hours
        FromMe:       true,
    },
}
sdkResponse, err := client.GetMessages(sessionId, chatId, options) // Adjust method signature
if err != nil {
    log.Fatalf("Error calling GetMessages: %v", err)
}
if sdkResponse.Success {
    fmt.Println("Messages:", sdkResponse.Data)
} else {
    log.Printf("Failed to get messages: %s", sdkResponse.Error)
}
```

**C# (.NET)**

```csharp
string chatId = "recipient_or_group_jid@c.us";
var options = new GetMessagesOptions
{
    Limit = 10, // Required
    DownloadMedia = true,
    Filter = new GetMessagesFilterOptions
    {
        TimestampGte = DateTimeOffset.UtcNow.AddHours(-24).ToUnixTimeSeconds(), // Last 24 hours
        FromMe = true
    }
};
var messagesResponse = await client.GetMessagesAsync(sessionId, chatId, options); // Adjust method signature
if (messagesResponse.Success && messagesResponse.Data != null)
{
    Console.WriteLine($"Messages count: {messagesResponse.Data.Count}");
}
else
{
    Console.WriteLine($"Failed to get messages: {messagesResponse.Error}");
}
```

### Get Chat Picture

Retrieves the profile picture of a chat (user or group).

**TypeScript**

```python
const chatId = "recipient_or_group_jid@c.us";
const chatPictureResponse = await client.getChatPicture(sessionId, chatId, { refresh: true });
if (chatPictureResponse.success && chatPictureResponse.data) {
    console.log('Chat Picture URL:', chatPictureResponse.data.url);
} else {
    console.error('Failed to get chat picture:', chatPictureResponse.error);
}
```

**Python**

```python
chat_id = "recipient_or_group_jid@c.us"
try:
    chat_picture_response = client.get_chat_picture(
        session=sessionId,
        chat_id=chat_id,
        refresh=True
    )
    # Assuming data is an object/dict with a 'url' attribute/key
    if hasattr(chat_picture_response, 'success') and chat_picture_response.success and hasattr(chat_picture_response, 'data'):
        picture_data = chat_picture_response.data
        url = getattr(picture_data, 'url', None) if hasattr(picture_data, 'url') else picture_data.get('url') if isinstance(picture_data, dict) else None
        print(f"Chat Picture URL: {url}")
    elif hasattr(chat_picture_response, 'error'):
        print(f"Failed to get chat picture: {chat_picture_response.error}")
    else:
        print(f"Chat picture response: {chat_picture_response}")
except Exception as e:
    print(f"An error occurred: {e}")
```

**Go**

```go
chatId := "recipient_or_group_jid@c.us"
options := &wasend.GetChatPictureOptions{
    Refresh: true,
}
// getChatPicture returns SdkResponse where Data is ChatPictureResponse (with URL)
sdkResponse, err := client.GetChatPicture(sessionId, chatId, options) // Adjust method signature
if err != nil {
    log.Fatalf("Error calling GetChatPicture: %v", err)
}
if sdkResponse.Success {
    // Assuming sdkResponse.Data can be asserted to a struct with a Url field
    // chatPicData, ok := sdkResponse.Data.(wasend.ChatPictureResponse)
    // if ok { fmt.Println("Chat Picture URL:", chatPicData.Url) }
    fmt.Println("Chat Picture data:", sdkResponse.Data) // Print the raw data for inspection
} else {
    log.Printf("Failed to get chat picture: %s", sdkResponse.Error)
}
```

**C# (.NET)**

```csharp
string chatId = "recipient_or_group_jid@c.us";
var options = new GetChatPictureOptions { Refresh = true };
var chatPictureResponse = await client.GetChatPictureAsync(sessionId, chatId, options); // Adjust method signature
if (chatPictureResponse.Success && chatPictureResponse.Data != null)
{
    Console.WriteLine($"Chat Picture URL: {chatPictureResponse.Data.Url}");
}
else
{
    Console.WriteLine($"Failed to get chat picture: {chatPictureResponse.Error}");
}
```

### Get Message By ID

Retrieves a specific message by its ID from a given chat.

**TypeScript**

```python
const chatId = "recipient_or_group_jid@c.us";
const messageId = "specific_message_id";
const messageResponse = await client.getMessageById(sessionId, chatId, messageId, { downloadMedia: true });
if (messageResponse.success && messageResponse.data) {
    console.log('Message:', messageResponse.data);
} else {
    console.error('Failed to get message by ID:', messageResponse.error);
}
```

**Python**

```python
chat_id = "recipient_or_group_jid@c.us"
message_id = "specific_message_id"
try:
    message_response = client.get_message_by_id(
        session=sessionId,
        chat_id=chat_id,
        message_id=message_id,
        download_media=True
    )
    if hasattr(message_response, 'success') and message_response.success and hasattr(message_response, 'data'):
        print(f"Message: {message_response.data}")
    elif hasattr(message_response, 'error'):
        print(f"Failed to get message by ID: {message_response.error}")
    else:
        print(f"Message response: {message_response}")
except Exception as e:
    print(f"An error occurred: {e}")
```

**Go**

```go
chatId := "recipient_or_group_jid@c.us"
messageId := "specific_message_id"
options := &wasend.GetMessageByIdOptions{
    DownloadMedia: true,
}
// getMessageById returns SdkResponse where Data is WAMessage
sdkResponse, err := client.GetMessageById(sessionId, chatId, messageId, options) // Adjust method signature
if err != nil {
    log.Fatalf("Error calling GetMessageById: %v", err)
}
if sdkResponse.Success {
    fmt.Println("Message:", sdkResponse.Data)
} else {
    log.Printf("Failed to get message by ID: %s", sdkResponse.Error)
}
```

**C# (.NET)**

```csharp
string chatId = "recipient_or_group_jid@c.us";
string messageId = "specific_message_id";
var options = new GetMessageByIdOptions { DownloadMedia = true };
var messageResponse = await client.GetMessageByIdAsync(sessionId, chatId, messageId, options); // Adjust method signature
if (messageResponse.Success && messageResponse.Data != null)
{
    Console.WriteLine($"Message ID: {messageResponse.Data.Id}, Text: {messageResponse.Data.Text}"); // Example properties
}
else
{
    Console.WriteLine($"Failed to get message by ID: {messageResponse.Error}");
}
```

## Best Practices

1. Always store the `sessionId` securely after creating a session.
2. Implement robust error handling for all API calls. Always check the `success` field in the response and handle the `error` field appropriately.
3. Use environment variables or a secure configuration management system for your API key and other sensitive credentials. Do not hardcode them in your application.
4. Enable account protection features when creating sessions, especially for production environments, to enhance security.
5. If your application requires real-time updates (e.g., for incoming messages, session status changes), implement webhook handling. Ensure your webhook endpoint is secure and can process notifications efficiently.
6. Regularly monitor the status of your WhatsApp sessions using `retrieveSessionInfo` (or `getSessionInfo`) and implement logic to handle disconnections or errors (e.g., by attempting to restart the session or notifying an administrator).
7. Periodically clean up unused or old sessions using `deleteSession` to manage resources effectively and avoid hitting account limits.
8. Utilize pagination parameters (e.g., `limit`, `offset`) when retrieving lists of chats (`getAllChats`, `getChatsOverview`) or messages (`getMessages`). This helps manage data flow, improves performance, and prevents timeouts when dealing with large datasets.
9. Be mindful of the `downloadMedia` option when fetching messages (`getMessages`, `getMessageById`). Enabling it can significantly increase response size and processing time. Use it selectively only when the media content is immediately required by your application.
10. When polling for new messages or updates, use appropriate filters (e.g., `timestampGte` in `getMessages` options) to fetch only new or relevant data. This reduces redundant data transfer and processing on your end.
11. Consider implementing a caching layer in your application for frequently accessed but less volatile data, such as chat overviews or profile pictures. Use cache invalidation strategies (e.g., time-based expiry or using the `refresh` option where available, like in `getChatPicture`) to ensure data freshness.
12. For marking messages as read using `readMessages`, choose the most suitable option (`messages` count or `days`) based on your application's specific requirements for managing unread states.
13. When using utility methods like `processMessage` that introduce deliberate delays (for simulating human-like typing), ensure your application handles these asynchronous operations gracefully, without blocking critical execution paths or user interface responsiveness.
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from ._jsii import *


@jsii.data_type(
    jsii_type="@wasend/core.AccountInfo",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "name": "name", "plan": "plan"},
)
class AccountInfo:
    def __init__(
        self,
        *,
        id: builtins.str,
        name: builtins.str,
        plan: builtins.str,
    ) -> None:
        '''Account information structure.

        :param id: Account ID.
        :param name: Account name.
        :param plan: Account plan.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8d187f8daf4945ee8cc7af4c965fbd16ceba9a4a4f1a826ace5438a45da1cd0)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument plan", value=plan, expected_type=type_hints["plan"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "name": name,
            "plan": plan,
        }

    @builtins.property
    def id(self) -> builtins.str:
        '''Account ID.'''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Account name.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def plan(self) -> builtins.str:
        '''Account plan.'''
        result = self._values.get("plan")
        assert result is not None, "Required property 'plan' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccountInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.Chat",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "archived": "archived",
        "is_group": "isGroup",
        "name": "name",
        "pinned": "pinned",
        "timestamp": "timestamp",
        "unread_count": "unreadCount",
    },
)
class Chat:
    def __init__(
        self,
        *,
        id: builtins.str,
        archived: typing.Optional[builtins.bool] = None,
        is_group: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
        pinned: typing.Optional[builtins.bool] = None,
        timestamp: typing.Optional[jsii.Number] = None,
        unread_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param id: 
        :param archived: 
        :param is_group: 
        :param name: 
        :param pinned: 
        :param timestamp: 
        :param unread_count: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfa06278962f83f68df8d947f16f2877395e96a371674392b0ae5e7f31e29a49)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument archived", value=archived, expected_type=type_hints["archived"])
            check_type(argname="argument is_group", value=is_group, expected_type=type_hints["is_group"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument pinned", value=pinned, expected_type=type_hints["pinned"])
            check_type(argname="argument timestamp", value=timestamp, expected_type=type_hints["timestamp"])
            check_type(argname="argument unread_count", value=unread_count, expected_type=type_hints["unread_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
        }
        if archived is not None:
            self._values["archived"] = archived
        if is_group is not None:
            self._values["is_group"] = is_group
        if name is not None:
            self._values["name"] = name
        if pinned is not None:
            self._values["pinned"] = pinned
        if timestamp is not None:
            self._values["timestamp"] = timestamp
        if unread_count is not None:
            self._values["unread_count"] = unread_count

    @builtins.property
    def id(self) -> builtins.str:
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def archived(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("archived")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def is_group(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("is_group")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pinned(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("pinned")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def timestamp(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("timestamp")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def unread_count(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("unread_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Chat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.ChatOverview",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "is_group": "isGroup",
        "name": "name",
        "timestamp": "timestamp",
        "unread_count": "unreadCount",
    },
)
class ChatOverview:
    def __init__(
        self,
        *,
        id: builtins.str,
        is_group: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
        timestamp: typing.Optional[jsii.Number] = None,
        unread_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param id: 
        :param is_group: 
        :param name: 
        :param timestamp: 
        :param unread_count: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9eb6c31d0ff337b91d63c70aabfbeb18483eeab3cc8c50d725e19b624c3b7f6)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument is_group", value=is_group, expected_type=type_hints["is_group"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument timestamp", value=timestamp, expected_type=type_hints["timestamp"])
            check_type(argname="argument unread_count", value=unread_count, expected_type=type_hints["unread_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
        }
        if is_group is not None:
            self._values["is_group"] = is_group
        if name is not None:
            self._values["name"] = name
        if timestamp is not None:
            self._values["timestamp"] = timestamp
        if unread_count is not None:
            self._values["unread_count"] = unread_count

    @builtins.property
    def id(self) -> builtins.str:
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def is_group(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("is_group")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestamp(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("timestamp")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def unread_count(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("unread_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChatOverview(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.ChatPictureResponse",
    jsii_struct_bases=[],
    name_mapping={"file": "file", "mimetype": "mimetype", "url": "url"},
)
class ChatPictureResponse:
    def __init__(
        self,
        *,
        file: typing.Optional[builtins.str] = None,
        mimetype: typing.Optional[builtins.str] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param file: 
        :param mimetype: 
        :param url: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09da9e3c62cc36091ae66a18e93d6e95bbfaa6b1a7892888208297e973448b1a)
            check_type(argname="argument file", value=file, expected_type=type_hints["file"])
            check_type(argname="argument mimetype", value=mimetype, expected_type=type_hints["mimetype"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if file is not None:
            self._values["file"] = file
        if mimetype is not None:
            self._values["mimetype"] = mimetype
        if url is not None:
            self._values["url"] = url

    @builtins.property
    def file(self) -> typing.Optional[builtins.str]:
        result = self._values.get("file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mimetype(self) -> typing.Optional[builtins.str]:
        result = self._values.get("mimetype")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChatPictureResponse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.ChatRequest",
    jsii_struct_bases=[],
    name_mapping={"session": "session", "to": "to"},
)
class ChatRequest:
    def __init__(self, *, session: builtins.str, to: builtins.str) -> None:
        '''Base chat request interface.

        :param session: The session ID.
        :param to: The recipient's phone number or group JID.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90e9bd02629e7e5613e4e5f308462c781bb094fe3968ab3ec2f24d3e0c9b7143)
            check_type(argname="argument session", value=session, expected_type=type_hints["session"])
            check_type(argname="argument to", value=to, expected_type=type_hints["to"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "session": session,
            "to": to,
        }

    @builtins.property
    def session(self) -> builtins.str:
        '''The session ID.'''
        result = self._values.get("session")
        assert result is not None, "Required property 'session' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def to(self) -> builtins.str:
        '''The recipient's phone number or group JID.

        Example::

            "+1234567890" or "1234567890-12345678@g.us"
        '''
        result = self._values.get("to")
        assert result is not None, "Required property 'to' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChatRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.ChatWAMessage",
    jsii_struct_bases=[],
    name_mapping={
        "chat_id": "chatId",
        "from_": "from",
        "from_me": "fromMe",
        "id": "id",
        "timestamp": "timestamp",
        "to": "to",
        "type": "type",
        "ack": "ack",
        "body": "body",
        "caption": "caption",
        "filename": "filename",
        "has_media": "hasMedia",
        "media_url": "mediaUrl",
        "mimetype": "mimetype",
        "quoted_msg_id": "quotedMsgId",
    },
)
class ChatWAMessage:
    def __init__(
        self,
        *,
        chat_id: builtins.str,
        from_: builtins.str,
        from_me: builtins.bool,
        id: builtins.str,
        timestamp: jsii.Number,
        to: builtins.str,
        type: builtins.str,
        ack: typing.Optional[jsii.Number] = None,
        body: typing.Any = None,
        caption: typing.Optional[builtins.str] = None,
        filename: typing.Optional[builtins.str] = None,
        has_media: typing.Optional[builtins.bool] = None,
        media_url: typing.Optional[builtins.str] = None,
        mimetype: typing.Optional[builtins.str] = None,
        quoted_msg_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param chat_id: 
        :param from_: 
        :param from_me: 
        :param id: 
        :param timestamp: 
        :param to: 
        :param type: 
        :param ack: 
        :param body: 
        :param caption: 
        :param filename: 
        :param has_media: 
        :param media_url: 
        :param mimetype: 
        :param quoted_msg_id: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__425bb91f9998c0944d4eee1a8c13654ecc9ec498632c36161567320fe07138e3)
            check_type(argname="argument chat_id", value=chat_id, expected_type=type_hints["chat_id"])
            check_type(argname="argument from_", value=from_, expected_type=type_hints["from_"])
            check_type(argname="argument from_me", value=from_me, expected_type=type_hints["from_me"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timestamp", value=timestamp, expected_type=type_hints["timestamp"])
            check_type(argname="argument to", value=to, expected_type=type_hints["to"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument ack", value=ack, expected_type=type_hints["ack"])
            check_type(argname="argument body", value=body, expected_type=type_hints["body"])
            check_type(argname="argument caption", value=caption, expected_type=type_hints["caption"])
            check_type(argname="argument filename", value=filename, expected_type=type_hints["filename"])
            check_type(argname="argument has_media", value=has_media, expected_type=type_hints["has_media"])
            check_type(argname="argument media_url", value=media_url, expected_type=type_hints["media_url"])
            check_type(argname="argument mimetype", value=mimetype, expected_type=type_hints["mimetype"])
            check_type(argname="argument quoted_msg_id", value=quoted_msg_id, expected_type=type_hints["quoted_msg_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "chat_id": chat_id,
            "from_": from_,
            "from_me": from_me,
            "id": id,
            "timestamp": timestamp,
            "to": to,
            "type": type,
        }
        if ack is not None:
            self._values["ack"] = ack
        if body is not None:
            self._values["body"] = body
        if caption is not None:
            self._values["caption"] = caption
        if filename is not None:
            self._values["filename"] = filename
        if has_media is not None:
            self._values["has_media"] = has_media
        if media_url is not None:
            self._values["media_url"] = media_url
        if mimetype is not None:
            self._values["mimetype"] = mimetype
        if quoted_msg_id is not None:
            self._values["quoted_msg_id"] = quoted_msg_id

    @builtins.property
    def chat_id(self) -> builtins.str:
        result = self._values.get("chat_id")
        assert result is not None, "Required property 'chat_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def from_(self) -> builtins.str:
        result = self._values.get("from_")
        assert result is not None, "Required property 'from_' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def from_me(self) -> builtins.bool:
        result = self._values.get("from_me")
        assert result is not None, "Required property 'from_me' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def id(self) -> builtins.str:
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def timestamp(self) -> jsii.Number:
        result = self._values.get("timestamp")
        assert result is not None, "Required property 'timestamp' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def to(self) -> builtins.str:
        result = self._values.get("to")
        assert result is not None, "Required property 'to' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ack(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("ack")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def body(self) -> typing.Any:
        result = self._values.get("body")
        return typing.cast(typing.Any, result)

    @builtins.property
    def caption(self) -> typing.Optional[builtins.str]:
        result = self._values.get("caption")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filename(self) -> typing.Optional[builtins.str]:
        result = self._values.get("filename")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def has_media(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("has_media")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def media_url(self) -> typing.Optional[builtins.str]:
        result = self._values.get("media_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mimetype(self) -> typing.Optional[builtins.str]:
        result = self._values.get("mimetype")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def quoted_msg_id(self) -> typing.Optional[builtins.str]:
        result = self._values.get("quoted_msg_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChatWAMessage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.CheckContactExistsQueryParams",
    jsii_struct_bases=[],
    name_mapping={"phone": "phone"},
)
class CheckContactExistsQueryParams:
    def __init__(self, *, phone: builtins.str) -> None:
        '''Check contact exists query parameters.

        :param phone: The phone number to check.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ce7e73e4a188e6c18688efc76051366d41bfd5ce1e53874bcbc6b5410105e14)
            check_type(argname="argument phone", value=phone, expected_type=type_hints["phone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "phone": phone,
        }

    @builtins.property
    def phone(self) -> builtins.str:
        '''The phone number to check.

        Example::

            "1213213213"
        '''
        result = self._values.get("phone")
        assert result is not None, "Required property 'phone' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CheckContactExistsQueryParams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.Contact",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "phone_number": "phoneNumber",
        "business_profile": "businessProfile",
        "name": "name",
        "profile_picture_url": "profilePictureUrl",
        "push_name": "pushName",
        "status": "status",
    },
)
class Contact:
    def __init__(
        self,
        *,
        id: builtins.str,
        phone_number: builtins.str,
        business_profile: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        profile_picture_url: typing.Optional[builtins.str] = None,
        push_name: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Contact information.

        :param id: Contact ID (phone number with.
        :param phone_number: Contact phone number.
        :param business_profile: Contact business profile.
        :param name: Contact name.
        :param profile_picture_url: Contact profile picture URL.
        :param push_name: Contact push name.
        :param status: Contact status.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f01784379d90bd6517ad09f6e9c44b252cc798ffb866437f0a769f0c2ea8aba0)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument phone_number", value=phone_number, expected_type=type_hints["phone_number"])
            check_type(argname="argument business_profile", value=business_profile, expected_type=type_hints["business_profile"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument profile_picture_url", value=profile_picture_url, expected_type=type_hints["profile_picture_url"])
            check_type(argname="argument push_name", value=push_name, expected_type=type_hints["push_name"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "phone_number": phone_number,
        }
        if business_profile is not None:
            self._values["business_profile"] = business_profile
        if name is not None:
            self._values["name"] = name
        if profile_picture_url is not None:
            self._values["profile_picture_url"] = profile_picture_url
        if push_name is not None:
            self._values["push_name"] = push_name
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def id(self) -> builtins.str:
        '''Contact ID (phone number with.

        :c: .us suffix)

        Example::

            "11111111111@c.us"
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def phone_number(self) -> builtins.str:
        '''Contact phone number.'''
        result = self._values.get("phone_number")
        assert result is not None, "Required property 'phone_number' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def business_profile(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Contact business profile.'''
        result = self._values.get("business_profile")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Contact name.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def profile_picture_url(self) -> typing.Optional[builtins.str]:
        '''Contact profile picture URL.'''
        result = self._values.get("profile_picture_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def push_name(self) -> typing.Optional[builtins.str]:
        '''Contact push name.'''
        result = self._values.get("push_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Contact status.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Contact(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.CountResponse",
    jsii_struct_bases=[],
    name_mapping={"total": "total", "by_status": "byStatus"},
)
class CountResponse:
    def __init__(
        self,
        *,
        total: jsii.Number,
        by_status: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Response for count operations.

        :param total: The total count.
        :param by_status: Count breakdown by status.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db0f9d976503c59b6d78d15007dad94a45caac923d28a1c60227137ef9450dc1)
            check_type(argname="argument total", value=total, expected_type=type_hints["total"])
            check_type(argname="argument by_status", value=by_status, expected_type=type_hints["by_status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "total": total,
        }
        if by_status is not None:
            self._values["by_status"] = by_status

    @builtins.property
    def total(self) -> jsii.Number:
        '''The total count.'''
        result = self._values.get("total")
        assert result is not None, "Required property 'total' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def by_status(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Count breakdown by status.

        Example::

            {
              "ACTIVE": "10",
              "ARCHIVED": "5",
              "DELETED": "2"
            }
        '''
        result = self._values.get("by_status")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CountResponse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.CreateGroupParticipant",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "is_admin": "isAdmin"},
)
class CreateGroupParticipant:
    def __init__(
        self,
        *,
        id: builtins.str,
        is_admin: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Create group request participant.

        :param id: Participant ID (phone number with country code).
        :param is_admin: Whether to make the participant an admin. Default: false
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11dbb0617142989f518d5efdf030f4e40b95426ea99cefe74225710d84e9e707)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument is_admin", value=is_admin, expected_type=type_hints["is_admin"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
        }
        if is_admin is not None:
            self._values["is_admin"] = is_admin

    @builtins.property
    def id(self) -> builtins.str:
        '''Participant ID (phone number with country code).

        Example::

            "+919545251359"
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def is_admin(self) -> typing.Optional[builtins.bool]:
        '''Whether to make the participant an admin.

        :default: false
        '''
        result = self._values.get("is_admin")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CreateGroupParticipant(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.CreateGroupRequest",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "participants": "participants",
        "description": "description",
        "picture_url": "pictureUrl",
        "tags": "tags",
    },
)
class CreateGroupRequest:
    def __init__(
        self,
        *,
        name: builtins.str,
        participants: typing.Sequence[typing.Union[CreateGroupParticipant, typing.Dict[builtins.str, typing.Any]]],
        description: typing.Optional[builtins.str] = None,
        picture_url: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Create group request.

        :param name: Group name.
        :param participants: Group participants.
        :param description: Group description (optional).
        :param picture_url: Group picture URL (optional).
        :param tags: Group tags (optional).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b801fefb4c7f7aae3c00a9656c8348c463f4a5ca8695facef63b7c41043cc8b0)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument participants", value=participants, expected_type=type_hints["participants"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument picture_url", value=picture_url, expected_type=type_hints["picture_url"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "participants": participants,
        }
        if description is not None:
            self._values["description"] = description
        if picture_url is not None:
            self._values["picture_url"] = picture_url
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''Group name.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def participants(self) -> typing.List[CreateGroupParticipant]:
        '''Group participants.'''
        result = self._values.get("participants")
        assert result is not None, "Required property 'participants' is missing"
        return typing.cast(typing.List[CreateGroupParticipant], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Group description (optional).'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def picture_url(self) -> typing.Optional[builtins.str]:
        '''Group picture URL (optional).'''
        result = self._values.get("picture_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Group tags (optional).'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CreateGroupRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.DescriptionRequest",
    jsii_struct_bases=[],
    name_mapping={"description": "description"},
)
class DescriptionRequest:
    def __init__(self, *, description: builtins.str) -> None:
        '''Description request.

        :param description: Group description.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf438daec090025706f7968ab6b280029fe549899179470b1a48211f2cbf6694)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''Group description.'''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DescriptionRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.DownstreamInfo",
    jsii_struct_bases=[],
    name_mapping={
        "config": "config",
        "engine": "engine",
        "name": "name",
        "status": "status",
    },
)
class DownstreamInfo:
    def __init__(
        self,
        *,
        config: typing.Union["SessionConfig", typing.Dict[builtins.str, typing.Any]],
        engine: typing.Union["EngineStatus", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        status: builtins.str,
    ) -> None:
        '''Downstream connection information.

        :param config: Configuration for the downstream connection.
        :param engine: Engine status information.
        :param name: Name of the downstream connection.
        :param status: Status of the downstream connection.
        '''
        if isinstance(config, dict):
            config = SessionConfig(**config)
        if isinstance(engine, dict):
            engine = EngineStatus(**engine)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e85038298b8fa1b5985855072c2560ca953a48eea4a7ee8b9f750e8bc6f62348)
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument engine", value=engine, expected_type=type_hints["engine"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "config": config,
            "engine": engine,
            "name": name,
            "status": status,
        }

    @builtins.property
    def config(self) -> "SessionConfig":
        '''Configuration for the downstream connection.'''
        result = self._values.get("config")
        assert result is not None, "Required property 'config' is missing"
        return typing.cast("SessionConfig", result)

    @builtins.property
    def engine(self) -> "EngineStatus":
        '''Engine status information.'''
        result = self._values.get("engine")
        assert result is not None, "Required property 'engine' is missing"
        return typing.cast("EngineStatus", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the downstream connection.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def status(self) -> builtins.str:
        '''Status of the downstream connection.'''
        result = self._values.get("status")
        assert result is not None, "Required property 'status' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DownstreamInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.EngineStatus",
    jsii_struct_bases=[],
    name_mapping={"gows": "gows", "grpc": "grpc"},
)
class EngineStatus:
    def __init__(
        self,
        *,
        gows: typing.Union["GowsStatus", typing.Dict[builtins.str, typing.Any]],
        grpc: typing.Union["GrpcStatus", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''Engine status information.

        :param gows: GoWS status.
        :param grpc: gRPC status.
        '''
        if isinstance(gows, dict):
            gows = GowsStatus(**gows)
        if isinstance(grpc, dict):
            grpc = GrpcStatus(**grpc)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62f98c4efad3df7d9dcd0fbf647c894254a448f6718f0c1fad58962182024475)
            check_type(argname="argument gows", value=gows, expected_type=type_hints["gows"])
            check_type(argname="argument grpc", value=grpc, expected_type=type_hints["grpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "gows": gows,
            "grpc": grpc,
        }

    @builtins.property
    def gows(self) -> "GowsStatus":
        '''GoWS status.'''
        result = self._values.get("gows")
        assert result is not None, "Required property 'gows' is missing"
        return typing.cast("GowsStatus", result)

    @builtins.property
    def grpc(self) -> "GrpcStatus":
        '''gRPC status.'''
        result = self._values.get("grpc")
        assert result is not None, "Required property 'grpc' is missing"
        return typing.cast("GrpcStatus", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EngineStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.GetAllSessionsResponse",
    jsii_struct_bases=[],
    name_mapping={"sessions": "sessions"},
)
class GetAllSessionsResponse:
    def __init__(
        self,
        *,
        sessions: typing.Sequence[typing.Union["SessionListItem", typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''Response wrapper for getAllSessions.

        :param sessions: Array of sessions.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09647a94e3d8e4aee98f4628c3fa572a7d308b6f12281833bf5a01c156dec696)
            check_type(argname="argument sessions", value=sessions, expected_type=type_hints["sessions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "sessions": sessions,
        }

    @builtins.property
    def sessions(self) -> typing.List["SessionListItem"]:
        '''Array of sessions.'''
        result = self._values.get("sessions")
        assert result is not None, "Required property 'sessions' is missing"
        return typing.cast(typing.List["SessionListItem"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GetAllSessionsResponse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.GetChatPictureOptions",
    jsii_struct_bases=[],
    name_mapping={"refresh": "refresh"},
)
class GetChatPictureOptions:
    def __init__(self, *, refresh: typing.Optional[builtins.bool] = None) -> None:
        '''
        :param refresh: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98b4ef55b5f7c0f54f8142583fb4be24180dbe24212e4b0868579c431ad52b26)
            check_type(argname="argument refresh", value=refresh, expected_type=type_hints["refresh"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if refresh is not None:
            self._values["refresh"] = refresh

    @builtins.property
    def refresh(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("refresh")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GetChatPictureOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.GetChatsOptions",
    jsii_struct_bases=[],
    name_mapping={
        "limit": "limit",
        "offset": "offset",
        "sort_by": "sortBy",
        "sort_order": "sortOrder",
    },
)
class GetChatsOptions:
    def __init__(
        self,
        *,
        limit: typing.Optional[jsii.Number] = None,
        offset: typing.Optional[jsii.Number] = None,
        sort_by: typing.Optional[builtins.str] = None,
        sort_order: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param limit: 
        :param offset: 
        :param sort_by: 
        :param sort_order: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1a3d89e80e38a81cfd275a69cc98fb292e237c976e6a9c7ecacd631851661dc)
            check_type(argname="argument limit", value=limit, expected_type=type_hints["limit"])
            check_type(argname="argument offset", value=offset, expected_type=type_hints["offset"])
            check_type(argname="argument sort_by", value=sort_by, expected_type=type_hints["sort_by"])
            check_type(argname="argument sort_order", value=sort_order, expected_type=type_hints["sort_order"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if limit is not None:
            self._values["limit"] = limit
        if offset is not None:
            self._values["offset"] = offset
        if sort_by is not None:
            self._values["sort_by"] = sort_by
        if sort_order is not None:
            self._values["sort_order"] = sort_order

    @builtins.property
    def limit(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def offset(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("offset")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def sort_by(self) -> typing.Optional[builtins.str]:
        result = self._values.get("sort_by")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sort_order(self) -> typing.Optional[builtins.str]:
        result = self._values.get("sort_order")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GetChatsOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.GetChatsOverviewOptions",
    jsii_struct_bases=[],
    name_mapping={"ids": "ids", "limit": "limit", "offset": "offset"},
)
class GetChatsOverviewOptions:
    def __init__(
        self,
        *,
        ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        limit: typing.Optional[jsii.Number] = None,
        offset: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param ids: 
        :param limit: 
        :param offset: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f131e3eb5d9a18d6a467f0cf0a4840b91cbc75d743963badbf4ceb227d9f2da5)
            check_type(argname="argument ids", value=ids, expected_type=type_hints["ids"])
            check_type(argname="argument limit", value=limit, expected_type=type_hints["limit"])
            check_type(argname="argument offset", value=offset, expected_type=type_hints["offset"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ids is not None:
            self._values["ids"] = ids
        if limit is not None:
            self._values["limit"] = limit
        if offset is not None:
            self._values["offset"] = offset

    @builtins.property
    def ids(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def limit(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def offset(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("offset")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GetChatsOverviewOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.GetContactQueryParams",
    jsii_struct_bases=[],
    name_mapping={"contact_id": "contactId"},
)
class GetContactQueryParams:
    def __init__(self, *, contact_id: builtins.str) -> None:
        '''Get contact query parameters.

        :param contact_id: Contact ID (phone number with.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ab74c0b993c79a49ecd8b57b84b899caac6adf3a35c750484a98167b95d949b)
            check_type(argname="argument contact_id", value=contact_id, expected_type=type_hints["contact_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "contact_id": contact_id,
        }

    @builtins.property
    def contact_id(self) -> builtins.str:
        '''Contact ID (phone number with.

        :c: .us suffix)

        Example::

            "11111111111@c.us"
        '''
        result = self._values.get("contact_id")
        assert result is not None, "Required property 'contact_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GetContactQueryParams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.GetContactsQueryParams",
    jsii_struct_bases=[],
    name_mapping={
        "limit": "limit",
        "offset": "offset",
        "sort_by": "sortBy",
        "sort_order": "sortOrder",
    },
)
class GetContactsQueryParams:
    def __init__(
        self,
        *,
        limit: typing.Optional[jsii.Number] = None,
        offset: typing.Optional[jsii.Number] = None,
        sort_by: typing.Optional[builtins.str] = None,
        sort_order: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Get contacts query parameters.

        :param limit: Maximum number of results. Default: 10
        :param offset: Number of results to skip. Default: 0
        :param sort_by: Sort by field.
        :param sort_order: Sort order.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3680033b53e752044b09d690a76a7f9763f7c4e9b1c4aeb2b997110eeaa93948)
            check_type(argname="argument limit", value=limit, expected_type=type_hints["limit"])
            check_type(argname="argument offset", value=offset, expected_type=type_hints["offset"])
            check_type(argname="argument sort_by", value=sort_by, expected_type=type_hints["sort_by"])
            check_type(argname="argument sort_order", value=sort_order, expected_type=type_hints["sort_order"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if limit is not None:
            self._values["limit"] = limit
        if offset is not None:
            self._values["offset"] = offset
        if sort_by is not None:
            self._values["sort_by"] = sort_by
        if sort_order is not None:
            self._values["sort_order"] = sort_order

    @builtins.property
    def limit(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of results.

        :default: 10
        '''
        result = self._values.get("limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def offset(self) -> typing.Optional[jsii.Number]:
        '''Number of results to skip.

        :default: 0
        '''
        result = self._values.get("offset")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def sort_by(self) -> typing.Optional[builtins.str]:
        '''Sort by field.'''
        result = self._values.get("sort_by")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sort_order(self) -> typing.Optional[builtins.str]:
        '''Sort order.'''
        result = self._values.get("sort_order")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GetContactsQueryParams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.GetGroupsQueryParams",
    jsii_struct_bases=[],
    name_mapping={
        "exclude": "exclude",
        "limit": "limit",
        "offset": "offset",
        "search": "search",
        "sort_by": "sortBy",
        "sort_order": "sortOrder",
        "status": "status",
        "tags": "tags",
    },
)
class GetGroupsQueryParams:
    def __init__(
        self,
        *,
        exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        limit: typing.Optional[jsii.Number] = None,
        offset: typing.Optional[jsii.Number] = None,
        search: typing.Optional[builtins.str] = None,
        sort_by: typing.Optional[builtins.str] = None,
        sort_order: typing.Optional[builtins.str] = None,
        status: typing.Optional["GroupStatus"] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Get groups query parameters.

        :param exclude: Fields to exclude from response.
        :param limit: Maximum number of results. Default: 50
        :param offset: Number of results to skip. Default: 0
        :param search: Search by name or description.
        :param sort_by: Sort by field.
        :param sort_order: Sort order.
        :param status: Filter by status.
        :param tags: Filter by tags.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60bb8c0fe3cf07942ae17d6192dd6e29a24bb3837ce9c87fa0fd46c8c649fc24)
            check_type(argname="argument exclude", value=exclude, expected_type=type_hints["exclude"])
            check_type(argname="argument limit", value=limit, expected_type=type_hints["limit"])
            check_type(argname="argument offset", value=offset, expected_type=type_hints["offset"])
            check_type(argname="argument search", value=search, expected_type=type_hints["search"])
            check_type(argname="argument sort_by", value=sort_by, expected_type=type_hints["sort_by"])
            check_type(argname="argument sort_order", value=sort_order, expected_type=type_hints["sort_order"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exclude is not None:
            self._values["exclude"] = exclude
        if limit is not None:
            self._values["limit"] = limit
        if offset is not None:
            self._values["offset"] = offset
        if search is not None:
            self._values["search"] = search
        if sort_by is not None:
            self._values["sort_by"] = sort_by
        if sort_order is not None:
            self._values["sort_order"] = sort_order
        if status is not None:
            self._values["status"] = status
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def exclude(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Fields to exclude from response.'''
        result = self._values.get("exclude")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def limit(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of results.

        :default: 50
        '''
        result = self._values.get("limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def offset(self) -> typing.Optional[jsii.Number]:
        '''Number of results to skip.

        :default: 0
        '''
        result = self._values.get("offset")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def search(self) -> typing.Optional[builtins.str]:
        '''Search by name or description.'''
        result = self._values.get("search")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sort_by(self) -> typing.Optional[builtins.str]:
        '''Sort by field.'''
        result = self._values.get("sort_by")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sort_order(self) -> typing.Optional[builtins.str]:
        '''Sort order.'''
        result = self._values.get("sort_order")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional["GroupStatus"]:
        '''Filter by status.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional["GroupStatus"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Filter by tags.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GetGroupsQueryParams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.GetMessageByIdOptions",
    jsii_struct_bases=[],
    name_mapping={"download_media": "downloadMedia"},
)
class GetMessageByIdOptions:
    def __init__(
        self,
        *,
        download_media: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param download_media: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a93a910aaab3132f5c5033203d954c5a1ba65b2d786f0447d6c997f2c2491344)
            check_type(argname="argument download_media", value=download_media, expected_type=type_hints["download_media"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if download_media is not None:
            self._values["download_media"] = download_media

    @builtins.property
    def download_media(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("download_media")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GetMessageByIdOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.GetMessagesFilterOptions",
    jsii_struct_bases=[],
    name_mapping={
        "ack": "ack",
        "from_me": "fromMe",
        "timestamp_gte": "timestampGte",
        "timestamp_lte": "timestampLte",
    },
)
class GetMessagesFilterOptions:
    def __init__(
        self,
        *,
        ack: typing.Optional[typing.Union[jsii.Number, typing.Sequence[jsii.Number]]] = None,
        from_me: typing.Optional[builtins.bool] = None,
        timestamp_gte: typing.Optional[jsii.Number] = None,
        timestamp_lte: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param ack: 
        :param from_me: 
        :param timestamp_gte: 
        :param timestamp_lte: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__918a0fe200c9476b7e2c780fff5f5509042a9c3513e86defd74f6f221516d045)
            check_type(argname="argument ack", value=ack, expected_type=type_hints["ack"])
            check_type(argname="argument from_me", value=from_me, expected_type=type_hints["from_me"])
            check_type(argname="argument timestamp_gte", value=timestamp_gte, expected_type=type_hints["timestamp_gte"])
            check_type(argname="argument timestamp_lte", value=timestamp_lte, expected_type=type_hints["timestamp_lte"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ack is not None:
            self._values["ack"] = ack
        if from_me is not None:
            self._values["from_me"] = from_me
        if timestamp_gte is not None:
            self._values["timestamp_gte"] = timestamp_gte
        if timestamp_lte is not None:
            self._values["timestamp_lte"] = timestamp_lte

    @builtins.property
    def ack(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, typing.List[jsii.Number]]]:
        result = self._values.get("ack")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, typing.List[jsii.Number]]], result)

    @builtins.property
    def from_me(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("from_me")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def timestamp_gte(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("timestamp_gte")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timestamp_lte(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("timestamp_lte")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GetMessagesFilterOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.GetMessagesOptions",
    jsii_struct_bases=[],
    name_mapping={
        "limit": "limit",
        "download_media": "downloadMedia",
        "filter": "filter",
        "offset": "offset",
    },
)
class GetMessagesOptions:
    def __init__(
        self,
        *,
        limit: jsii.Number,
        download_media: typing.Optional[builtins.bool] = None,
        filter: typing.Optional[typing.Union[GetMessagesFilterOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        offset: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param limit: 
        :param download_media: 
        :param filter: 
        :param offset: 
        '''
        if isinstance(filter, dict):
            filter = GetMessagesFilterOptions(**filter)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ca33f45329ebae61ec00f7584ddd35bd417aee164fe2854c27c20810611576a)
            check_type(argname="argument limit", value=limit, expected_type=type_hints["limit"])
            check_type(argname="argument download_media", value=download_media, expected_type=type_hints["download_media"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument offset", value=offset, expected_type=type_hints["offset"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "limit": limit,
        }
        if download_media is not None:
            self._values["download_media"] = download_media
        if filter is not None:
            self._values["filter"] = filter
        if offset is not None:
            self._values["offset"] = offset

    @builtins.property
    def limit(self) -> jsii.Number:
        result = self._values.get("limit")
        assert result is not None, "Required property 'limit' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def download_media(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("download_media")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def filter(self) -> typing.Optional[GetMessagesFilterOptions]:
        result = self._values.get("filter")
        return typing.cast(typing.Optional[GetMessagesFilterOptions], result)

    @builtins.property
    def offset(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("offset")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GetMessagesOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.GetProfilePictureQueryParams",
    jsii_struct_bases=[],
    name_mapping={"contact_id": "contactId", "refresh": "refresh"},
)
class GetProfilePictureQueryParams:
    def __init__(
        self,
        *,
        contact_id: builtins.str,
        refresh: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Get profile picture query parameters.

        :param contact_id: Contact ID (phone number with.
        :param refresh: Refresh the picture from the server (24h cache by default). Default: false
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__490e028bd1817925bde1eab0649d7f86084e21aeb689ac6594663b7f4efb0e31)
            check_type(argname="argument contact_id", value=contact_id, expected_type=type_hints["contact_id"])
            check_type(argname="argument refresh", value=refresh, expected_type=type_hints["refresh"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "contact_id": contact_id,
        }
        if refresh is not None:
            self._values["refresh"] = refresh

    @builtins.property
    def contact_id(self) -> builtins.str:
        '''Contact ID (phone number with.

        :c: .us suffix)

        Example::

            "11111111111@c.us"
        '''
        result = self._values.get("contact_id")
        assert result is not None, "Required property 'contact_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def refresh(self) -> typing.Optional[builtins.bool]:
        '''Refresh the picture from the server (24h cache by default).

        :default: false
        '''
        result = self._values.get("refresh")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GetProfilePictureQueryParams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.GowsStatus",
    jsii_struct_bases=[],
    name_mapping={"connected": "connected", "found": "found"},
)
class GowsStatus:
    def __init__(self, *, connected: builtins.bool, found: builtins.bool) -> None:
        '''
        :param connected: 
        :param found: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9c788395f63b322df62cfa06c64f225e1401e968d5af857d8143e86d9b74616)
            check_type(argname="argument connected", value=connected, expected_type=type_hints["connected"])
            check_type(argname="argument found", value=found, expected_type=type_hints["found"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "connected": connected,
            "found": found,
        }

    @builtins.property
    def connected(self) -> builtins.bool:
        result = self._values.get("connected")
        assert result is not None, "Required property 'connected' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def found(self) -> builtins.bool:
        result = self._values.get("found")
        assert result is not None, "Required property 'found' is missing"
        return typing.cast(builtins.bool, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GowsStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.Group",
    jsii_struct_bases=[],
    name_mapping={
        "addressing_mode": "addressingMode",
        "announce_version_id": "announceVersionId",
        "creator_country_code": "creatorCountryCode",
        "default_membership_approval_mode": "defaultMembershipApprovalMode",
        "disappearing_timer": "disappearingTimer",
        "group_created": "groupCreated",
        "is_announce": "isAnnounce",
        "is_default_sub_group": "isDefaultSubGroup",
        "is_ephemeral": "isEphemeral",
        "is_incognito": "isIncognito",
        "is_join_approval_required": "isJoinApprovalRequired",
        "is_locked": "isLocked",
        "is_parent": "isParent",
        "jid": "jid",
        "linked_parent_jid": "linkedParentJid",
        "member_add_mode": "memberAddMode",
        "name": "name",
        "name_set_at": "nameSetAt",
        "name_set_by": "nameSetBy",
        "name_set_by_pn": "nameSetByPn",
        "owner_jid": "ownerJid",
        "owner_pn": "ownerPn",
        "participants": "participants",
        "participant_version_id": "participantVersionId",
        "topic": "topic",
        "topic_deleted": "topicDeleted",
        "topic_id": "topicId",
        "topic_set_at": "topicSetAt",
        "topic_set_by": "topicSetBy",
        "topic_set_by_pn": "topicSetByPn",
    },
)
class Group:
    def __init__(
        self,
        *,
        addressing_mode: builtins.str,
        announce_version_id: builtins.str,
        creator_country_code: builtins.str,
        default_membership_approval_mode: builtins.str,
        disappearing_timer: jsii.Number,
        group_created: builtins.str,
        is_announce: builtins.bool,
        is_default_sub_group: builtins.bool,
        is_ephemeral: builtins.bool,
        is_incognito: builtins.bool,
        is_join_approval_required: builtins.bool,
        is_locked: builtins.bool,
        is_parent: builtins.bool,
        jid: builtins.str,
        linked_parent_jid: builtins.str,
        member_add_mode: builtins.str,
        name: builtins.str,
        name_set_at: builtins.str,
        name_set_by: builtins.str,
        name_set_by_pn: builtins.str,
        owner_jid: builtins.str,
        owner_pn: builtins.str,
        participants: typing.Sequence[typing.Union["GroupParticipant", typing.Dict[builtins.str, typing.Any]]],
        participant_version_id: builtins.str,
        topic: builtins.str,
        topic_deleted: builtins.bool,
        topic_id: builtins.str,
        topic_set_at: builtins.str,
        topic_set_by: builtins.str,
        topic_set_by_pn: builtins.str,
    ) -> None:
        '''Group information.

        :param addressing_mode: Addressing mode.
        :param announce_version_id: Announcement version ID.
        :param creator_country_code: Creator's country code.
        :param default_membership_approval_mode: Default membership approval mode.
        :param disappearing_timer: Disappearing messages timer in seconds.
        :param group_created: When the group was created.
        :param is_announce: Whether the group is an announcement group.
        :param is_default_sub_group: Whether the group is a default subgroup.
        :param is_ephemeral: Whether the group is ephemeral.
        :param is_incognito: Whether the group is incognito.
        :param is_join_approval_required: Whether join approval is required.
        :param is_locked: Whether the group is locked.
        :param is_parent: Whether the group is a parent group.
        :param jid: Group JID.
        :param linked_parent_jid: Linked parent group JID.
        :param member_add_mode: Member add mode.
        :param name: Group name.
        :param name_set_at: When the name was set.
        :param name_set_by: Who set the name.
        :param name_set_by_pn: Phone number of who set the name.
        :param owner_jid: Owner JID.
        :param owner_pn: Owner phone number.
        :param participants: Group participants.
        :param participant_version_id: Participant version ID.
        :param topic: Group topic/description.
        :param topic_deleted: Whether the topic was deleted.
        :param topic_id: Topic ID.
        :param topic_set_at: When the topic was set.
        :param topic_set_by: Who set the topic.
        :param topic_set_by_pn: Phone number of who set the topic.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7f6588b08fde062fbfd9593c1e1c125af02ecac9c40b142f1f404ffc7068352)
            check_type(argname="argument addressing_mode", value=addressing_mode, expected_type=type_hints["addressing_mode"])
            check_type(argname="argument announce_version_id", value=announce_version_id, expected_type=type_hints["announce_version_id"])
            check_type(argname="argument creator_country_code", value=creator_country_code, expected_type=type_hints["creator_country_code"])
            check_type(argname="argument default_membership_approval_mode", value=default_membership_approval_mode, expected_type=type_hints["default_membership_approval_mode"])
            check_type(argname="argument disappearing_timer", value=disappearing_timer, expected_type=type_hints["disappearing_timer"])
            check_type(argname="argument group_created", value=group_created, expected_type=type_hints["group_created"])
            check_type(argname="argument is_announce", value=is_announce, expected_type=type_hints["is_announce"])
            check_type(argname="argument is_default_sub_group", value=is_default_sub_group, expected_type=type_hints["is_default_sub_group"])
            check_type(argname="argument is_ephemeral", value=is_ephemeral, expected_type=type_hints["is_ephemeral"])
            check_type(argname="argument is_incognito", value=is_incognito, expected_type=type_hints["is_incognito"])
            check_type(argname="argument is_join_approval_required", value=is_join_approval_required, expected_type=type_hints["is_join_approval_required"])
            check_type(argname="argument is_locked", value=is_locked, expected_type=type_hints["is_locked"])
            check_type(argname="argument is_parent", value=is_parent, expected_type=type_hints["is_parent"])
            check_type(argname="argument jid", value=jid, expected_type=type_hints["jid"])
            check_type(argname="argument linked_parent_jid", value=linked_parent_jid, expected_type=type_hints["linked_parent_jid"])
            check_type(argname="argument member_add_mode", value=member_add_mode, expected_type=type_hints["member_add_mode"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument name_set_at", value=name_set_at, expected_type=type_hints["name_set_at"])
            check_type(argname="argument name_set_by", value=name_set_by, expected_type=type_hints["name_set_by"])
            check_type(argname="argument name_set_by_pn", value=name_set_by_pn, expected_type=type_hints["name_set_by_pn"])
            check_type(argname="argument owner_jid", value=owner_jid, expected_type=type_hints["owner_jid"])
            check_type(argname="argument owner_pn", value=owner_pn, expected_type=type_hints["owner_pn"])
            check_type(argname="argument participants", value=participants, expected_type=type_hints["participants"])
            check_type(argname="argument participant_version_id", value=participant_version_id, expected_type=type_hints["participant_version_id"])
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
            check_type(argname="argument topic_deleted", value=topic_deleted, expected_type=type_hints["topic_deleted"])
            check_type(argname="argument topic_id", value=topic_id, expected_type=type_hints["topic_id"])
            check_type(argname="argument topic_set_at", value=topic_set_at, expected_type=type_hints["topic_set_at"])
            check_type(argname="argument topic_set_by", value=topic_set_by, expected_type=type_hints["topic_set_by"])
            check_type(argname="argument topic_set_by_pn", value=topic_set_by_pn, expected_type=type_hints["topic_set_by_pn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "addressing_mode": addressing_mode,
            "announce_version_id": announce_version_id,
            "creator_country_code": creator_country_code,
            "default_membership_approval_mode": default_membership_approval_mode,
            "disappearing_timer": disappearing_timer,
            "group_created": group_created,
            "is_announce": is_announce,
            "is_default_sub_group": is_default_sub_group,
            "is_ephemeral": is_ephemeral,
            "is_incognito": is_incognito,
            "is_join_approval_required": is_join_approval_required,
            "is_locked": is_locked,
            "is_parent": is_parent,
            "jid": jid,
            "linked_parent_jid": linked_parent_jid,
            "member_add_mode": member_add_mode,
            "name": name,
            "name_set_at": name_set_at,
            "name_set_by": name_set_by,
            "name_set_by_pn": name_set_by_pn,
            "owner_jid": owner_jid,
            "owner_pn": owner_pn,
            "participants": participants,
            "participant_version_id": participant_version_id,
            "topic": topic,
            "topic_deleted": topic_deleted,
            "topic_id": topic_id,
            "topic_set_at": topic_set_at,
            "topic_set_by": topic_set_by,
            "topic_set_by_pn": topic_set_by_pn,
        }

    @builtins.property
    def addressing_mode(self) -> builtins.str:
        '''Addressing mode.'''
        result = self._values.get("addressing_mode")
        assert result is not None, "Required property 'addressing_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def announce_version_id(self) -> builtins.str:
        '''Announcement version ID.'''
        result = self._values.get("announce_version_id")
        assert result is not None, "Required property 'announce_version_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def creator_country_code(self) -> builtins.str:
        '''Creator's country code.'''
        result = self._values.get("creator_country_code")
        assert result is not None, "Required property 'creator_country_code' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_membership_approval_mode(self) -> builtins.str:
        '''Default membership approval mode.'''
        result = self._values.get("default_membership_approval_mode")
        assert result is not None, "Required property 'default_membership_approval_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def disappearing_timer(self) -> jsii.Number:
        '''Disappearing messages timer in seconds.'''
        result = self._values.get("disappearing_timer")
        assert result is not None, "Required property 'disappearing_timer' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def group_created(self) -> builtins.str:
        '''When the group was created.'''
        result = self._values.get("group_created")
        assert result is not None, "Required property 'group_created' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def is_announce(self) -> builtins.bool:
        '''Whether the group is an announcement group.'''
        result = self._values.get("is_announce")
        assert result is not None, "Required property 'is_announce' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def is_default_sub_group(self) -> builtins.bool:
        '''Whether the group is a default subgroup.'''
        result = self._values.get("is_default_sub_group")
        assert result is not None, "Required property 'is_default_sub_group' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def is_ephemeral(self) -> builtins.bool:
        '''Whether the group is ephemeral.'''
        result = self._values.get("is_ephemeral")
        assert result is not None, "Required property 'is_ephemeral' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def is_incognito(self) -> builtins.bool:
        '''Whether the group is incognito.'''
        result = self._values.get("is_incognito")
        assert result is not None, "Required property 'is_incognito' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def is_join_approval_required(self) -> builtins.bool:
        '''Whether join approval is required.'''
        result = self._values.get("is_join_approval_required")
        assert result is not None, "Required property 'is_join_approval_required' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def is_locked(self) -> builtins.bool:
        '''Whether the group is locked.'''
        result = self._values.get("is_locked")
        assert result is not None, "Required property 'is_locked' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def is_parent(self) -> builtins.bool:
        '''Whether the group is a parent group.'''
        result = self._values.get("is_parent")
        assert result is not None, "Required property 'is_parent' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def jid(self) -> builtins.str:
        '''Group JID.'''
        result = self._values.get("jid")
        assert result is not None, "Required property 'jid' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def linked_parent_jid(self) -> builtins.str:
        '''Linked parent group JID.'''
        result = self._values.get("linked_parent_jid")
        assert result is not None, "Required property 'linked_parent_jid' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def member_add_mode(self) -> builtins.str:
        '''Member add mode.'''
        result = self._values.get("member_add_mode")
        assert result is not None, "Required property 'member_add_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Group name.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name_set_at(self) -> builtins.str:
        '''When the name was set.'''
        result = self._values.get("name_set_at")
        assert result is not None, "Required property 'name_set_at' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name_set_by(self) -> builtins.str:
        '''Who set the name.'''
        result = self._values.get("name_set_by")
        assert result is not None, "Required property 'name_set_by' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name_set_by_pn(self) -> builtins.str:
        '''Phone number of who set the name.'''
        result = self._values.get("name_set_by_pn")
        assert result is not None, "Required property 'name_set_by_pn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def owner_jid(self) -> builtins.str:
        '''Owner JID.'''
        result = self._values.get("owner_jid")
        assert result is not None, "Required property 'owner_jid' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def owner_pn(self) -> builtins.str:
        '''Owner phone number.'''
        result = self._values.get("owner_pn")
        assert result is not None, "Required property 'owner_pn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def participants(self) -> typing.List["GroupParticipant"]:
        '''Group participants.'''
        result = self._values.get("participants")
        assert result is not None, "Required property 'participants' is missing"
        return typing.cast(typing.List["GroupParticipant"], result)

    @builtins.property
    def participant_version_id(self) -> builtins.str:
        '''Participant version ID.'''
        result = self._values.get("participant_version_id")
        assert result is not None, "Required property 'participant_version_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def topic(self) -> builtins.str:
        '''Group topic/description.'''
        result = self._values.get("topic")
        assert result is not None, "Required property 'topic' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def topic_deleted(self) -> builtins.bool:
        '''Whether the topic was deleted.'''
        result = self._values.get("topic_deleted")
        assert result is not None, "Required property 'topic_deleted' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def topic_id(self) -> builtins.str:
        '''Topic ID.'''
        result = self._values.get("topic_id")
        assert result is not None, "Required property 'topic_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def topic_set_at(self) -> builtins.str:
        '''When the topic was set.'''
        result = self._values.get("topic_set_at")
        assert result is not None, "Required property 'topic_set_at' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def topic_set_by(self) -> builtins.str:
        '''Who set the topic.'''
        result = self._values.get("topic_set_by")
        assert result is not None, "Required property 'topic_set_by' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def topic_set_by_pn(self) -> builtins.str:
        '''Phone number of who set the topic.'''
        result = self._values.get("topic_set_by_pn")
        assert result is not None, "Required property 'topic_set_by_pn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Group(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.GroupParticipant",
    jsii_struct_bases=[],
    name_mapping={
        "is_admin": "isAdmin",
        "is_super_admin": "isSuperAdmin",
        "jid": "jid",
        "phone_number": "phoneNumber",
        "add_request": "addRequest",
        "display_name": "displayName",
        "error": "error",
        "lid": "lid",
    },
)
class GroupParticipant:
    def __init__(
        self,
        *,
        is_admin: builtins.bool,
        is_super_admin: builtins.bool,
        jid: builtins.str,
        phone_number: builtins.str,
        add_request: typing.Any = None,
        display_name: typing.Optional[builtins.str] = None,
        error: typing.Optional[jsii.Number] = None,
        lid: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Group participant information.

        :param is_admin: Whether the participant is an admin.
        :param is_super_admin: Whether the participant is a super admin.
        :param jid: Participant JID.
        :param phone_number: Participant phone number.
        :param add_request: Add request information (if any).
        :param display_name: Participant display name.
        :param error: Error code (if any).
        :param lid: Participant LID (if available).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78b419bf2b928f7f297941e05587ce28c1ed0d03a36769f37143c8e58b5b4aa6)
            check_type(argname="argument is_admin", value=is_admin, expected_type=type_hints["is_admin"])
            check_type(argname="argument is_super_admin", value=is_super_admin, expected_type=type_hints["is_super_admin"])
            check_type(argname="argument jid", value=jid, expected_type=type_hints["jid"])
            check_type(argname="argument phone_number", value=phone_number, expected_type=type_hints["phone_number"])
            check_type(argname="argument add_request", value=add_request, expected_type=type_hints["add_request"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument error", value=error, expected_type=type_hints["error"])
            check_type(argname="argument lid", value=lid, expected_type=type_hints["lid"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "is_admin": is_admin,
            "is_super_admin": is_super_admin,
            "jid": jid,
            "phone_number": phone_number,
        }
        if add_request is not None:
            self._values["add_request"] = add_request
        if display_name is not None:
            self._values["display_name"] = display_name
        if error is not None:
            self._values["error"] = error
        if lid is not None:
            self._values["lid"] = lid

    @builtins.property
    def is_admin(self) -> builtins.bool:
        '''Whether the participant is an admin.'''
        result = self._values.get("is_admin")
        assert result is not None, "Required property 'is_admin' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def is_super_admin(self) -> builtins.bool:
        '''Whether the participant is a super admin.'''
        result = self._values.get("is_super_admin")
        assert result is not None, "Required property 'is_super_admin' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def jid(self) -> builtins.str:
        '''Participant JID.'''
        result = self._values.get("jid")
        assert result is not None, "Required property 'jid' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def phone_number(self) -> builtins.str:
        '''Participant phone number.'''
        result = self._values.get("phone_number")
        assert result is not None, "Required property 'phone_number' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def add_request(self) -> typing.Any:
        '''Add request information (if any).'''
        result = self._values.get("add_request")
        return typing.cast(typing.Any, result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Participant display name.'''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def error(self) -> typing.Optional[jsii.Number]:
        '''Error code (if any).'''
        result = self._values.get("error")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def lid(self) -> typing.Optional[builtins.str]:
        '''Participant LID (if available).'''
        result = self._values.get("lid")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupParticipant(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@wasend/core.GroupParticipantRole")
class GroupParticipantRole(enum.Enum):
    '''Group participant role.'''

    PARTICIPANT = "PARTICIPANT"
    '''Regular participant.'''
    ADMIN = "ADMIN"
    '''Group admin.'''
    OWNER = "OWNER"
    '''Group owner.'''


@jsii.data_type(
    jsii_type="@wasend/core.GroupPictureResponse",
    jsii_struct_bases=[],
    name_mapping={
        "url": "url",
        "dimensions": "dimensions",
        "format": "format",
        "size": "size",
    },
)
class GroupPictureResponse:
    def __init__(
        self,
        *,
        url: builtins.str,
        dimensions: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        format: typing.Optional[builtins.str] = None,
        size: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Response for group picture operations.

        :param url: The URL of the group picture.
        :param dimensions: The dimensions of the picture.
        :param format: The format of the picture (e.g., 'jpeg', 'png').
        :param size: The size of the picture in bytes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab62018fb9da12e666c73d8ed7ee31553cf14dec0bbff4e812c637cacc6169d6)
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "url": url,
        }
        if dimensions is not None:
            self._values["dimensions"] = dimensions
        if format is not None:
            self._values["format"] = format
        if size is not None:
            self._values["size"] = size

    @builtins.property
    def url(self) -> builtins.str:
        '''The URL of the group picture.'''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dimensions(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The dimensions of the picture.

        Example::

            {
              "width": "800",
              "height": "600"
            }
        '''
        result = self._values.get("dimensions")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def format(self) -> typing.Optional[builtins.str]:
        '''The format of the picture (e.g., 'jpeg', 'png').'''
        result = self._values.get("format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def size(self) -> typing.Optional[jsii.Number]:
        '''The size of the picture in bytes.'''
        result = self._values.get("size")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupPictureResponse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.GroupSettings",
    jsii_struct_bases=[],
    name_mapping={
        "info_admin_only": "infoAdminOnly",
        "messages_admin_only": "messagesAdminOnly",
        "archived": "archived",
        "muted": "muted",
        "pinned": "pinned",
    },
)
class GroupSettings:
    def __init__(
        self,
        *,
        info_admin_only: builtins.bool,
        messages_admin_only: builtins.bool,
        archived: typing.Optional[builtins.bool] = None,
        muted: typing.Optional[builtins.bool] = None,
        pinned: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Group settings.

        :param info_admin_only: Whether only admins can edit group info.
        :param messages_admin_only: Whether only admins can send messages.
        :param archived: Whether group is archived.
        :param muted: Whether group is muted.
        :param pinned: Whether group is pinned.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__253ec022b4ad3544d7ac905bcc30c46e6f0b23024623a1bc65986f4c9b209794)
            check_type(argname="argument info_admin_only", value=info_admin_only, expected_type=type_hints["info_admin_only"])
            check_type(argname="argument messages_admin_only", value=messages_admin_only, expected_type=type_hints["messages_admin_only"])
            check_type(argname="argument archived", value=archived, expected_type=type_hints["archived"])
            check_type(argname="argument muted", value=muted, expected_type=type_hints["muted"])
            check_type(argname="argument pinned", value=pinned, expected_type=type_hints["pinned"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "info_admin_only": info_admin_only,
            "messages_admin_only": messages_admin_only,
        }
        if archived is not None:
            self._values["archived"] = archived
        if muted is not None:
            self._values["muted"] = muted
        if pinned is not None:
            self._values["pinned"] = pinned

    @builtins.property
    def info_admin_only(self) -> builtins.bool:
        '''Whether only admins can edit group info.'''
        result = self._values.get("info_admin_only")
        assert result is not None, "Required property 'info_admin_only' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def messages_admin_only(self) -> builtins.bool:
        '''Whether only admins can send messages.'''
        result = self._values.get("messages_admin_only")
        assert result is not None, "Required property 'messages_admin_only' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def archived(self) -> typing.Optional[builtins.bool]:
        '''Whether group is archived.'''
        result = self._values.get("archived")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def muted(self) -> typing.Optional[builtins.bool]:
        '''Whether group is muted.'''
        result = self._values.get("muted")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def pinned(self) -> typing.Optional[builtins.bool]:
        '''Whether group is pinned.'''
        result = self._values.get("pinned")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@wasend/core.GroupStatus")
class GroupStatus(enum.Enum):
    '''Group status.'''

    ACTIVE = "ACTIVE"
    '''Group is active.'''
    ARCHIVED = "ARCHIVED"
    '''Group is archived.'''
    DELETED = "DELETED"
    '''Group is deleted.'''


@jsii.data_type(
    jsii_type="@wasend/core.GrpcStatus",
    jsii_struct_bases=[],
    name_mapping={"client": "client", "stream": "stream"},
)
class GrpcStatus:
    def __init__(self, *, client: builtins.str, stream: builtins.str) -> None:
        '''
        :param client: 
        :param stream: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a90498c82c9829383ee4faed719fa2d55e4aaaa0a02c2c7519ed1097813a50e6)
            check_type(argname="argument client", value=client, expected_type=type_hints["client"])
            check_type(argname="argument stream", value=stream, expected_type=type_hints["stream"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client": client,
            "stream": stream,
        }

    @builtins.property
    def client(self) -> builtins.str:
        result = self._values.get("client")
        assert result is not None, "Required property 'client' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stream(self) -> builtins.str:
        result = self._values.get("stream")
        assert result is not None, "Required property 'stream' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GrpcStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.JoinGroupRequest",
    jsii_struct_bases=[],
    name_mapping={"code": "code"},
)
class JoinGroupRequest:
    def __init__(self, *, code: builtins.str) -> None:
        '''Join group request.

        :param code: Group code or invite URL.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18eb877dbca925b12bfad5ab99b6f84f785d923f2f4d49670915d0ffcc97132b)
            check_type(argname="argument code", value=code, expected_type=type_hints["code"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "code": code,
        }

    @builtins.property
    def code(self) -> builtins.str:
        '''Group code or invite URL.

        Example::

            "https://chat.whatsapp.com/1234567890abcdef"
        '''
        result = self._values.get("code")
        assert result is not None, "Required property 'code' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JoinGroupRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.JoinGroupResponse",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "name": "name",
        "participants_count": "participantsCount",
        "description": "description",
        "picture_url": "pictureUrl",
    },
)
class JoinGroupResponse:
    def __init__(
        self,
        *,
        id: builtins.str,
        name: builtins.str,
        participants_count: jsii.Number,
        description: typing.Optional[builtins.str] = None,
        picture_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Join group response.

        :param id: Group ID.
        :param name: Group name.
        :param participants_count: Group participants count.
        :param description: Group description.
        :param picture_url: Group picture URL.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f99c27e22fb714eb748dcd645448e3ff75f9496926bcd39064f0a77c5c34232)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument participants_count", value=participants_count, expected_type=type_hints["participants_count"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument picture_url", value=picture_url, expected_type=type_hints["picture_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "name": name,
            "participants_count": participants_count,
        }
        if description is not None:
            self._values["description"] = description
        if picture_url is not None:
            self._values["picture_url"] = picture_url

    @builtins.property
    def id(self) -> builtins.str:
        '''Group ID.'''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Group name.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def participants_count(self) -> jsii.Number:
        '''Group participants count.'''
        result = self._values.get("participants_count")
        assert result is not None, "Required property 'participants_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Group description.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def picture_url(self) -> typing.Optional[builtins.str]:
        '''Group picture URL.'''
        result = self._values.get("picture_url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JoinGroupResponse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.LinkPreviewRequest",
    jsii_struct_bases=[],
    name_mapping={
        "title": "title",
        "description": "description",
        "thumbnail_url": "thumbnailUrl",
    },
)
class LinkPreviewRequest:
    def __init__(
        self,
        *,
        title: builtins.str,
        description: typing.Optional[builtins.str] = None,
        thumbnail_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Link preview request.

        :param title: The link title.
        :param description: The link description.
        :param thumbnail_url: The link thumbnail URL.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15e7e6bc1f84a49e376d8c03802f7374297acc7ac1beacdf62c6bb438927dc67)
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument thumbnail_url", value=thumbnail_url, expected_type=type_hints["thumbnail_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "title": title,
        }
        if description is not None:
            self._values["description"] = description
        if thumbnail_url is not None:
            self._values["thumbnail_url"] = thumbnail_url

    @builtins.property
    def title(self) -> builtins.str:
        '''The link title.'''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The link description.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def thumbnail_url(self) -> typing.Optional[builtins.str]:
        '''The link thumbnail URL.'''
        result = self._values.get("thumbnail_url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LinkPreviewRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.Message",
    jsii_struct_bases=[],
    name_mapping={
        "content": "content",
        "id": "id",
        "sent_at": "sentAt",
        "status": "status",
        "to": "to",
    },
)
class Message:
    def __init__(
        self,
        *,
        content: builtins.str,
        id: builtins.str,
        sent_at: builtins.str,
        status: builtins.str,
        to: builtins.str,
    ) -> None:
        '''Message data structure.

        :param content: The content of the message.
        :param id: Unique identifier for the message.
        :param sent_at: Timestamp when the message was sent (ISO string).
        :param status: Message status.
        :param to: The recipient of the message.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e6ddabade18cb6b127a9542093b14870224ca085a4fedc56304aeee1c2f06ce)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument sent_at", value=sent_at, expected_type=type_hints["sent_at"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument to", value=to, expected_type=type_hints["to"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content": content,
            "id": id,
            "sent_at": sent_at,
            "status": status,
            "to": to,
        }

    @builtins.property
    def content(self) -> builtins.str:
        '''The content of the message.'''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> builtins.str:
        '''Unique identifier for the message.'''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sent_at(self) -> builtins.str:
        '''Timestamp when the message was sent (ISO string).'''
        result = self._values.get("sent_at")
        assert result is not None, "Required property 'sent_at' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def status(self) -> builtins.str:
        '''Message status.'''
        result = self._values.get("status")
        assert result is not None, "Required property 'status' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def to(self) -> builtins.str:
        '''The recipient of the message.'''
        result = self._values.get("to")
        assert result is not None, "Required property 'to' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Message(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.MessageRequest",
    jsii_struct_bases=[],
    name_mapping={"content": "content", "to": "to"},
)
class MessageRequest:
    def __init__(self, *, content: builtins.str, to: builtins.str) -> None:
        '''Message request structure.

        :param content: The content of the message.
        :param to: The recipient of the message.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa2d4015027c18549dff3d305605433dfdca504013c7fd0895520c8d64d08e82)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument to", value=to, expected_type=type_hints["to"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content": content,
            "to": to,
        }

    @builtins.property
    def content(self) -> builtins.str:
        '''The content of the message.'''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def to(self) -> builtins.str:
        '''The recipient of the message.'''
        result = self._values.get("to")
        assert result is not None, "Required property 'to' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MessageRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.MessageTextRequest",
    jsii_struct_bases=[MessageRequest],
    name_mapping={"content": "content", "to": "to", "text": "text"},
)
class MessageTextRequest(MessageRequest):
    def __init__(
        self,
        *,
        content: builtins.str,
        to: builtins.str,
        text: builtins.str,
    ) -> None:
        '''Text message request.

        :param content: The content of the message.
        :param to: The recipient of the message.
        :param text: The text content of the message.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae2238e853b97085efa0eeb50f1ae5743eb32aef4c893315febce3916b070e41)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument to", value=to, expected_type=type_hints["to"])
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content": content,
            "to": to,
            "text": text,
        }

    @builtins.property
    def content(self) -> builtins.str:
        '''The content of the message.'''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def to(self) -> builtins.str:
        '''The recipient of the message.'''
        result = self._values.get("to")
        assert result is not None, "Required property 'to' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def text(self) -> builtins.str:
        '''The text content of the message.'''
        result = self._values.get("text")
        assert result is not None, "Required property 'text' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MessageTextRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.MessageVideoRequest",
    jsii_struct_bases=[MessageRequest],
    name_mapping={
        "content": "content",
        "to": "to",
        "caption": "caption",
        "data": "data",
        "url": "url",
    },
)
class MessageVideoRequest(MessageRequest):
    def __init__(
        self,
        *,
        content: builtins.str,
        to: builtins.str,
        caption: typing.Optional[builtins.str] = None,
        data: typing.Optional[builtins.str] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Video message request.

        :param content: The content of the message.
        :param to: The recipient of the message.
        :param caption: The video caption.
        :param data: The video data in base64 format.
        :param url: The video URL.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c864831bd2e2b101ffe29610161aa4af0bbf977f549ad7d06aa0ebf52393f333)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument to", value=to, expected_type=type_hints["to"])
            check_type(argname="argument caption", value=caption, expected_type=type_hints["caption"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content": content,
            "to": to,
        }
        if caption is not None:
            self._values["caption"] = caption
        if data is not None:
            self._values["data"] = data
        if url is not None:
            self._values["url"] = url

    @builtins.property
    def content(self) -> builtins.str:
        '''The content of the message.'''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def to(self) -> builtins.str:
        '''The recipient of the message.'''
        result = self._values.get("to")
        assert result is not None, "Required property 'to' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def caption(self) -> typing.Optional[builtins.str]:
        '''The video caption.'''
        result = self._values.get("caption")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data(self) -> typing.Optional[builtins.str]:
        '''The video data in base64 format.'''
        result = self._values.get("data")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''The video URL.'''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MessageVideoRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.MessageVoiceRequest",
    jsii_struct_bases=[MessageRequest],
    name_mapping={
        "content": "content",
        "to": "to",
        "data": "data",
        "duration": "duration",
        "url": "url",
    },
)
class MessageVoiceRequest(MessageRequest):
    def __init__(
        self,
        *,
        content: builtins.str,
        to: builtins.str,
        data: typing.Optional[builtins.str] = None,
        duration: typing.Optional[jsii.Number] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Voice message request.

        :param content: The content of the message.
        :param to: The recipient of the message.
        :param data: The voice message data in base64 format.
        :param duration: The voice message duration in seconds.
        :param url: The voice message URL.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ac045910aedce36eae36948cbdf9a304bd003e99462584d3b7756d264f15223)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument to", value=to, expected_type=type_hints["to"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content": content,
            "to": to,
        }
        if data is not None:
            self._values["data"] = data
        if duration is not None:
            self._values["duration"] = duration
        if url is not None:
            self._values["url"] = url

    @builtins.property
    def content(self) -> builtins.str:
        '''The content of the message.'''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def to(self) -> builtins.str:
        '''The recipient of the message.'''
        result = self._values.get("to")
        assert result is not None, "Required property 'to' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data(self) -> typing.Optional[builtins.str]:
        '''The voice message data in base64 format.'''
        result = self._values.get("data")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def duration(self) -> typing.Optional[jsii.Number]:
        '''The voice message duration in seconds.'''
        result = self._values.get("duration")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''The voice message URL.'''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MessageVoiceRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.NowebConfig",
    jsii_struct_bases=[],
    name_mapping={"mark_online": "markOnline", "store": "store"},
)
class NowebConfig:
    def __init__(
        self,
        *,
        mark_online: builtins.bool,
        store: typing.Union["NowebStoreConfig", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param mark_online: 
        :param store: 
        '''
        if isinstance(store, dict):
            store = NowebStoreConfig(**store)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1d9acc660dd7af1a46bcbe0beab4ac7f79e0cb52e2e591c905cb18a2e402a31)
            check_type(argname="argument mark_online", value=mark_online, expected_type=type_hints["mark_online"])
            check_type(argname="argument store", value=store, expected_type=type_hints["store"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mark_online": mark_online,
            "store": store,
        }

    @builtins.property
    def mark_online(self) -> builtins.bool:
        result = self._values.get("mark_online")
        assert result is not None, "Required property 'mark_online' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def store(self) -> "NowebStoreConfig":
        result = self._values.get("store")
        assert result is not None, "Required property 'store' is missing"
        return typing.cast("NowebStoreConfig", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NowebConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.NowebStoreConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "full_sync": "fullSync"},
)
class NowebStoreConfig:
    def __init__(self, *, enabled: builtins.bool, full_sync: builtins.bool) -> None:
        '''
        :param enabled: 
        :param full_sync: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3504aad6bb01adf6b4e052cec8a4b4630e3f6d4463e67757a39a236969ffb0c8)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument full_sync", value=full_sync, expected_type=type_hints["full_sync"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
            "full_sync": full_sync,
        }

    @builtins.property
    def enabled(self) -> builtins.bool:
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def full_sync(self) -> builtins.bool:
        result = self._values.get("full_sync")
        assert result is not None, "Required property 'full_sync' is missing"
        return typing.cast(builtins.bool, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NowebStoreConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.PaginationOptions",
    jsii_struct_bases=[],
    name_mapping={"limit": "limit", "offset": "offset"},
)
class PaginationOptions:
    def __init__(
        self,
        *,
        limit: typing.Optional[jsii.Number] = None,
        offset: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param limit: 
        :param offset: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22a12ee180062e139189a9c2a4e37e712259928182668c5e31b5fb121268d73c)
            check_type(argname="argument limit", value=limit, expected_type=type_hints["limit"])
            check_type(argname="argument offset", value=offset, expected_type=type_hints["offset"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if limit is not None:
            self._values["limit"] = limit
        if offset is not None:
            self._values["offset"] = offset

    @builtins.property
    def limit(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def offset(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("offset")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PaginationOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.ParticipantsRequest",
    jsii_struct_bases=[],
    name_mapping={"participants": "participants", "notify": "notify"},
)
class ParticipantsRequest:
    def __init__(
        self,
        *,
        participants: typing.Sequence[builtins.str],
        notify: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Participants request.

        :param participants: List of participant IDs.
        :param notify: Whether to notify participants. Default: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdcd7bfcdef1239ec09bf635d6cb80127869a5b47b64abce0e0077d71e52fc18)
            check_type(argname="argument participants", value=participants, expected_type=type_hints["participants"])
            check_type(argname="argument notify", value=notify, expected_type=type_hints["notify"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "participants": participants,
        }
        if notify is not None:
            self._values["notify"] = notify

    @builtins.property
    def participants(self) -> typing.List[builtins.str]:
        '''List of participant IDs.

        Example::

            ["+919545251359", "+919545251360"]
        '''
        result = self._values.get("participants")
        assert result is not None, "Required property 'participants' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def notify(self) -> typing.Optional[builtins.bool]:
        '''Whether to notify participants.

        :default: true
        '''
        result = self._values.get("notify")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ParticipantsRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.ProfilePictureRequest",
    jsii_struct_bases=[],
    name_mapping={"url": "url", "crop_to_square": "cropToSquare", "format": "format"},
)
class ProfilePictureRequest:
    def __init__(
        self,
        *,
        url: builtins.str,
        crop_to_square: typing.Optional[builtins.bool] = None,
        format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Profile picture request.

        :param url: Picture URL.
        :param crop_to_square: Whether to crop the picture to a square. Default: true
        :param format: Picture format (optional). Default: "jpeg"
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a964f3f73efc5e8488da0bac80a171d233f4796182c0f6f6747cfb98e285554)
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument crop_to_square", value=crop_to_square, expected_type=type_hints["crop_to_square"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "url": url,
        }
        if crop_to_square is not None:
            self._values["crop_to_square"] = crop_to_square
        if format is not None:
            self._values["format"] = format

    @builtins.property
    def url(self) -> builtins.str:
        '''Picture URL.'''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def crop_to_square(self) -> typing.Optional[builtins.bool]:
        '''Whether to crop the picture to a square.

        :default: true
        '''
        result = self._values.get("crop_to_square")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def format(self) -> typing.Optional[builtins.str]:
        '''Picture format (optional).

        :default: "jpeg"
        '''
        result = self._values.get("format")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProfilePictureRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.ProfilePictureResponse",
    jsii_struct_bases=[],
    name_mapping={
        "url": "url",
        "dimensions": "dimensions",
        "format": "format",
        "size": "size",
    },
)
class ProfilePictureResponse:
    def __init__(
        self,
        *,
        url: builtins.str,
        dimensions: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        format: typing.Optional[builtins.str] = None,
        size: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Profile picture response.

        :param url: The URL of the profile picture.
        :param dimensions: The dimensions of the picture.
        :param format: The format of the picture (e.g., 'jpeg', 'png').
        :param size: The size of the picture in bytes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__459a32ee7266a8c5463906dab80b39d592816aaf349c8bb0974bab94794ae2a6)
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "url": url,
        }
        if dimensions is not None:
            self._values["dimensions"] = dimensions
        if format is not None:
            self._values["format"] = format
        if size is not None:
            self._values["size"] = size

    @builtins.property
    def url(self) -> builtins.str:
        '''The URL of the profile picture.'''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dimensions(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The dimensions of the picture.

        Example::

            {
              "width": "800",
              "height": "600"
            }
        '''
        result = self._values.get("dimensions")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def format(self) -> typing.Optional[builtins.str]:
        '''The format of the picture (e.g., 'jpeg', 'png').'''
        result = self._values.get("format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def size(self) -> typing.Optional[jsii.Number]:
        '''The size of the picture in bytes.'''
        result = self._values.get("size")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProfilePictureResponse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.QRCodeResponse",
    jsii_struct_bases=[],
    name_mapping={"data": "data"},
)
class QRCodeResponse:
    def __init__(self, *, data: builtins.str) -> None:
        '''QR code response.

        :param data: QR code data.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96354063aeb190a9953a739f8ddd730b166f0b989d0a398486425665f25137a3)
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data": data,
        }

    @builtins.property
    def data(self) -> builtins.str:
        '''QR code data.'''
        result = self._values.get("data")
        assert result is not None, "Required property 'data' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QRCodeResponse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.ReadChatMessagesResponse",
    jsii_struct_bases=[],
    name_mapping={"success": "success", "message": "message"},
)
class ReadChatMessagesResponse:
    def __init__(
        self,
        *,
        success: builtins.bool,
        message: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param success: 
        :param message: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c51f8bb25ad6378d464bb3616f09efc647e7e0e3ea4b317af603825757af3deb)
            check_type(argname="argument success", value=success, expected_type=type_hints["success"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "success": success,
        }
        if message is not None:
            self._values["message"] = message

    @builtins.property
    def success(self) -> builtins.bool:
        result = self._values.get("success")
        assert result is not None, "Required property 'success' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def message(self) -> typing.Optional[builtins.str]:
        result = self._values.get("message")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReadChatMessagesResponse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.ReadMessagesOptions",
    jsii_struct_bases=[],
    name_mapping={"days": "days", "messages": "messages"},
)
class ReadMessagesOptions:
    def __init__(
        self,
        *,
        days: typing.Optional[jsii.Number] = None,
        messages: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param days: 
        :param messages: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__857cddd5fe1274f4c8c1d5739156643ea6050e034b8e2931a6e7c4d8c7078993)
            check_type(argname="argument days", value=days, expected_type=type_hints["days"])
            check_type(argname="argument messages", value=messages, expected_type=type_hints["messages"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if days is not None:
            self._values["days"] = days
        if messages is not None:
            self._values["messages"] = messages

    @builtins.property
    def days(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def messages(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("messages")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReadMessagesOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.SdkResponse",
    jsii_struct_bases=[],
    name_mapping={"success": "success", "data": "data", "error": "error"},
)
class SdkResponse:
    def __init__(
        self,
        *,
        success: builtins.bool,
        data: typing.Any = None,
        error: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Response from API calls.

        :param success: Whether the request was successful.
        :param data: The response data (if successful).
        :param error: Error message if the request failed.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98004618b306ee3b99405ad13a11ba93b9108620a864642dce62c6eddd07efbb)
            check_type(argname="argument success", value=success, expected_type=type_hints["success"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument error", value=error, expected_type=type_hints["error"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "success": success,
        }
        if data is not None:
            self._values["data"] = data
        if error is not None:
            self._values["error"] = error

    @builtins.property
    def success(self) -> builtins.bool:
        '''Whether the request was successful.'''
        result = self._values.get("success")
        assert result is not None, "Required property 'success' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def data(self) -> typing.Any:
        '''The response data (if successful).'''
        result = self._values.get("data")
        return typing.cast(typing.Any, result)

    @builtins.property
    def error(self) -> typing.Optional[builtins.str]:
        '''Error message if the request failed.'''
        result = self._values.get("error")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SdkResponse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.SendRequest",
    jsii_struct_bases=[],
    name_mapping={
        "session": "session",
        "to": "to",
        "audio_url": "audioUrl",
        "document_url": "documentUrl",
        "filename": "filename",
        "image_url": "imageUrl",
        "mimetype": "mimetype",
        "preview": "preview",
        "text": "text",
        "video_url": "videoUrl",
    },
)
class SendRequest:
    def __init__(
        self,
        *,
        session: builtins.str,
        to: builtins.str,
        audio_url: typing.Optional[builtins.str] = None,
        document_url: typing.Optional[builtins.str] = None,
        filename: typing.Optional[builtins.str] = None,
        image_url: typing.Optional[builtins.str] = None,
        mimetype: typing.Optional[builtins.str] = None,
        preview: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        text: typing.Optional[builtins.str] = None,
        video_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Send message request interface.

        :param session: The session ID.
        :param to: The recipient's phone number or group JID.
        :param audio_url: The audio URL.
        :param document_url: The document URL.
        :param filename: The filename for the media.
        :param image_url: The image URL.
        :param mimetype: The MIME type of the media.
        :param preview: The link preview information.
        :param text: The message text or caption.
        :param video_url: The video URL.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d5c286a82ad51ebf302b12e832392238be9b9400c357ea5359a201d69ba37f5)
            check_type(argname="argument session", value=session, expected_type=type_hints["session"])
            check_type(argname="argument to", value=to, expected_type=type_hints["to"])
            check_type(argname="argument audio_url", value=audio_url, expected_type=type_hints["audio_url"])
            check_type(argname="argument document_url", value=document_url, expected_type=type_hints["document_url"])
            check_type(argname="argument filename", value=filename, expected_type=type_hints["filename"])
            check_type(argname="argument image_url", value=image_url, expected_type=type_hints["image_url"])
            check_type(argname="argument mimetype", value=mimetype, expected_type=type_hints["mimetype"])
            check_type(argname="argument preview", value=preview, expected_type=type_hints["preview"])
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
            check_type(argname="argument video_url", value=video_url, expected_type=type_hints["video_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "session": session,
            "to": to,
        }
        if audio_url is not None:
            self._values["audio_url"] = audio_url
        if document_url is not None:
            self._values["document_url"] = document_url
        if filename is not None:
            self._values["filename"] = filename
        if image_url is not None:
            self._values["image_url"] = image_url
        if mimetype is not None:
            self._values["mimetype"] = mimetype
        if preview is not None:
            self._values["preview"] = preview
        if text is not None:
            self._values["text"] = text
        if video_url is not None:
            self._values["video_url"] = video_url

    @builtins.property
    def session(self) -> builtins.str:
        '''The session ID.'''
        result = self._values.get("session")
        assert result is not None, "Required property 'session' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def to(self) -> builtins.str:
        '''The recipient's phone number or group JID.

        Example::

            "+1234567890" or "1234567890-12345678@g.us"
        '''
        result = self._values.get("to")
        assert result is not None, "Required property 'to' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def audio_url(self) -> typing.Optional[builtins.str]:
        '''The audio URL.

        Example::

            "https://example.com/audio.mp3"
        '''
        result = self._values.get("audio_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def document_url(self) -> typing.Optional[builtins.str]:
        '''The document URL.

        Example::

            "https://example.com/document.pdf"
        '''
        result = self._values.get("document_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filename(self) -> typing.Optional[builtins.str]:
        '''The filename for the media.

        Example::

            "custom_image.jpg"
        '''
        result = self._values.get("filename")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_url(self) -> typing.Optional[builtins.str]:
        '''The image URL.

        Example::

            "https://example.com/image.jpg"
        '''
        result = self._values.get("image_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mimetype(self) -> typing.Optional[builtins.str]:
        '''The MIME type of the media.

        Example::

            "image/jpeg"
        '''
        result = self._values.get("mimetype")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preview(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The link preview information.'''
        result = self._values.get("preview")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def text(self) -> typing.Optional[builtins.str]:
        '''The message text or caption.

        Example::

            "Hello from WASend!"
        '''
        result = self._values.get("text")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def video_url(self) -> typing.Optional[builtins.str]:
        '''The video URL.

        Example::

            "https://example.com/video.mp4"
        '''
        result = self._values.get("video_url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SendRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.SendSeenRequest",
    jsii_struct_bases=[ChatRequest],
    name_mapping={"session": "session", "to": "to", "message_id": "messageId"},
)
class SendSeenRequest(ChatRequest):
    def __init__(
        self,
        *,
        session: builtins.str,
        to: builtins.str,
        message_id: builtins.str,
    ) -> None:
        '''Send seen request.

        :param session: The session ID.
        :param to: The recipient's phone number or group JID.
        :param message_id: The message ID to mark as seen.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3bc536760d406c093d044345b6224c45408f03e06e559ccc19ccdc89f98d4d0)
            check_type(argname="argument session", value=session, expected_type=type_hints["session"])
            check_type(argname="argument to", value=to, expected_type=type_hints["to"])
            check_type(argname="argument message_id", value=message_id, expected_type=type_hints["message_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "session": session,
            "to": to,
            "message_id": message_id,
        }

    @builtins.property
    def session(self) -> builtins.str:
        '''The session ID.'''
        result = self._values.get("session")
        assert result is not None, "Required property 'session' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def to(self) -> builtins.str:
        '''The recipient's phone number or group JID.

        Example::

            "+1234567890" or "1234567890-12345678@g.us"
        '''
        result = self._values.get("to")
        assert result is not None, "Required property 'to' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def message_id(self) -> builtins.str:
        '''The message ID to mark as seen.'''
        result = self._values.get("message_id")
        assert result is not None, "Required property 'message_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SendSeenRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.SessionConfig",
    jsii_struct_bases=[],
    name_mapping={
        "debug": "debug",
        "metadata": "metadata",
        "noweb": "noweb",
        "proxy": "proxy",
        "webhooks": "webhooks",
    },
)
class SessionConfig:
    def __init__(
        self,
        *,
        debug: builtins.bool,
        metadata: typing.Union["SessionMetadata", typing.Dict[builtins.str, typing.Any]],
        noweb: typing.Union[NowebConfig, typing.Dict[builtins.str, typing.Any]],
        proxy: typing.Any,
        webhooks: typing.Sequence[typing.Any],
    ) -> None:
        '''Session configuration.

        :param debug: Debug mode.
        :param metadata: User metadata.
        :param noweb: Noweb configuration.
        :param proxy: Proxy configuration.
        :param webhooks: Webhook configurations.
        '''
        if isinstance(metadata, dict):
            metadata = SessionMetadata(**metadata)
        if isinstance(noweb, dict):
            noweb = NowebConfig(**noweb)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4bda00ff00f4da8f5d020b9ae62f84aef28dfe5100c707bc597e0d613a8ca00)
            check_type(argname="argument debug", value=debug, expected_type=type_hints["debug"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument noweb", value=noweb, expected_type=type_hints["noweb"])
            check_type(argname="argument proxy", value=proxy, expected_type=type_hints["proxy"])
            check_type(argname="argument webhooks", value=webhooks, expected_type=type_hints["webhooks"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "debug": debug,
            "metadata": metadata,
            "noweb": noweb,
            "proxy": proxy,
            "webhooks": webhooks,
        }

    @builtins.property
    def debug(self) -> builtins.bool:
        '''Debug mode.'''
        result = self._values.get("debug")
        assert result is not None, "Required property 'debug' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def metadata(self) -> "SessionMetadata":
        '''User metadata.'''
        result = self._values.get("metadata")
        assert result is not None, "Required property 'metadata' is missing"
        return typing.cast("SessionMetadata", result)

    @builtins.property
    def noweb(self) -> NowebConfig:
        '''Noweb configuration.'''
        result = self._values.get("noweb")
        assert result is not None, "Required property 'noweb' is missing"
        return typing.cast(NowebConfig, result)

    @builtins.property
    def proxy(self) -> typing.Any:
        '''Proxy configuration.'''
        result = self._values.get("proxy")
        assert result is not None, "Required property 'proxy' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def webhooks(self) -> typing.List[typing.Any]:
        '''Webhook configurations.'''
        result = self._values.get("webhooks")
        assert result is not None, "Required property 'webhooks' is missing"
        return typing.cast(typing.List[typing.Any], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SessionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.SessionCreateRequest",
    jsii_struct_bases=[],
    name_mapping={
        "phone_number": "phoneNumber",
        "session_name": "sessionName",
        "enable_account_protection": "enableAccountProtection",
        "enable_message_logging": "enableMessageLogging",
        "enable_webhook": "enableWebhook",
        "webhook_url": "webhookUrl",
    },
)
class SessionCreateRequest:
    def __init__(
        self,
        *,
        phone_number: builtins.str,
        session_name: builtins.str,
        enable_account_protection: typing.Optional[builtins.bool] = None,
        enable_message_logging: typing.Optional[builtins.bool] = None,
        enable_webhook: typing.Optional[builtins.bool] = None,
        webhook_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Session creation request body.

        :param phone_number: Phone number for the WhatsApp session.
        :param session_name: Name of the session.
        :param enable_account_protection: Enable account protection features. Default: false
        :param enable_message_logging: Enable message logging. Default: false
        :param enable_webhook: Enable webhook notifications. Default: false
        :param webhook_url: Webhook URL for notifications Required if enableWebhook is true.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e3cdcf8dd89941a7ff518341872e1a93509aae9d708132cd86835fcac559df4)
            check_type(argname="argument phone_number", value=phone_number, expected_type=type_hints["phone_number"])
            check_type(argname="argument session_name", value=session_name, expected_type=type_hints["session_name"])
            check_type(argname="argument enable_account_protection", value=enable_account_protection, expected_type=type_hints["enable_account_protection"])
            check_type(argname="argument enable_message_logging", value=enable_message_logging, expected_type=type_hints["enable_message_logging"])
            check_type(argname="argument enable_webhook", value=enable_webhook, expected_type=type_hints["enable_webhook"])
            check_type(argname="argument webhook_url", value=webhook_url, expected_type=type_hints["webhook_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "phone_number": phone_number,
            "session_name": session_name,
        }
        if enable_account_protection is not None:
            self._values["enable_account_protection"] = enable_account_protection
        if enable_message_logging is not None:
            self._values["enable_message_logging"] = enable_message_logging
        if enable_webhook is not None:
            self._values["enable_webhook"] = enable_webhook
        if webhook_url is not None:
            self._values["webhook_url"] = webhook_url

    @builtins.property
    def phone_number(self) -> builtins.str:
        '''Phone number for the WhatsApp session.'''
        result = self._values.get("phone_number")
        assert result is not None, "Required property 'phone_number' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def session_name(self) -> builtins.str:
        '''Name of the session.'''
        result = self._values.get("session_name")
        assert result is not None, "Required property 'session_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enable_account_protection(self) -> typing.Optional[builtins.bool]:
        '''Enable account protection features.

        :default: false
        '''
        result = self._values.get("enable_account_protection")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_message_logging(self) -> typing.Optional[builtins.bool]:
        '''Enable message logging.

        :default: false
        '''
        result = self._values.get("enable_message_logging")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_webhook(self) -> typing.Optional[builtins.bool]:
        '''Enable webhook notifications.

        :default: false
        '''
        result = self._values.get("enable_webhook")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def webhook_url(self) -> typing.Optional[builtins.str]:
        '''Webhook URL for notifications Required if enableWebhook is true.'''
        result = self._values.get("webhook_url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SessionCreateRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.SessionDetails",
    jsii_struct_bases=[],
    name_mapping={
        "created_at": "createdAt",
        "enable_account_protection": "enableAccountProtection",
        "enable_message_logging": "enableMessageLogging",
        "enable_webhook": "enableWebhook",
        "id": "id",
        "phone_number": "phoneNumber",
        "session_name": "sessionName",
        "unique_session_id": "uniqueSessionId",
        "updated_at": "updatedAt",
        "user_id": "userId",
        "webhook_url": "webhookUrl",
    },
)
class SessionDetails:
    def __init__(
        self,
        *,
        created_at: builtins.str,
        enable_account_protection: builtins.bool,
        enable_message_logging: builtins.bool,
        enable_webhook: builtins.bool,
        id: builtins.str,
        phone_number: builtins.str,
        session_name: builtins.str,
        unique_session_id: builtins.str,
        updated_at: builtins.str,
        user_id: builtins.str,
        webhook_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Session details.

        :param created_at: Creation timestamp.
        :param enable_account_protection: Session configuration flags.
        :param enable_message_logging: 
        :param enable_webhook: 
        :param id: MongoDB ID of the session.
        :param phone_number: Phone number associated with the session.
        :param session_name: Name of the session.
        :param unique_session_id: Unique session identifier.
        :param updated_at: Last update timestamp.
        :param user_id: User ID who owns the session.
        :param webhook_url: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__596f395204ab95febe6f3697a1d4c0d5942a1dfe1e6f52a0af2b14e28390e61b)
            check_type(argname="argument created_at", value=created_at, expected_type=type_hints["created_at"])
            check_type(argname="argument enable_account_protection", value=enable_account_protection, expected_type=type_hints["enable_account_protection"])
            check_type(argname="argument enable_message_logging", value=enable_message_logging, expected_type=type_hints["enable_message_logging"])
            check_type(argname="argument enable_webhook", value=enable_webhook, expected_type=type_hints["enable_webhook"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument phone_number", value=phone_number, expected_type=type_hints["phone_number"])
            check_type(argname="argument session_name", value=session_name, expected_type=type_hints["session_name"])
            check_type(argname="argument unique_session_id", value=unique_session_id, expected_type=type_hints["unique_session_id"])
            check_type(argname="argument updated_at", value=updated_at, expected_type=type_hints["updated_at"])
            check_type(argname="argument user_id", value=user_id, expected_type=type_hints["user_id"])
            check_type(argname="argument webhook_url", value=webhook_url, expected_type=type_hints["webhook_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "created_at": created_at,
            "enable_account_protection": enable_account_protection,
            "enable_message_logging": enable_message_logging,
            "enable_webhook": enable_webhook,
            "id": id,
            "phone_number": phone_number,
            "session_name": session_name,
            "unique_session_id": unique_session_id,
            "updated_at": updated_at,
            "user_id": user_id,
        }
        if webhook_url is not None:
            self._values["webhook_url"] = webhook_url

    @builtins.property
    def created_at(self) -> builtins.str:
        '''Creation timestamp.'''
        result = self._values.get("created_at")
        assert result is not None, "Required property 'created_at' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enable_account_protection(self) -> builtins.bool:
        '''Session configuration flags.'''
        result = self._values.get("enable_account_protection")
        assert result is not None, "Required property 'enable_account_protection' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def enable_message_logging(self) -> builtins.bool:
        result = self._values.get("enable_message_logging")
        assert result is not None, "Required property 'enable_message_logging' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def enable_webhook(self) -> builtins.bool:
        result = self._values.get("enable_webhook")
        assert result is not None, "Required property 'enable_webhook' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def id(self) -> builtins.str:
        '''MongoDB ID of the session.'''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def phone_number(self) -> builtins.str:
        '''Phone number associated with the session.'''
        result = self._values.get("phone_number")
        assert result is not None, "Required property 'phone_number' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def session_name(self) -> builtins.str:
        '''Name of the session.'''
        result = self._values.get("session_name")
        assert result is not None, "Required property 'session_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def unique_session_id(self) -> builtins.str:
        '''Unique session identifier.'''
        result = self._values.get("unique_session_id")
        assert result is not None, "Required property 'unique_session_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def updated_at(self) -> builtins.str:
        '''Last update timestamp.'''
        result = self._values.get("updated_at")
        assert result is not None, "Required property 'updated_at' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_id(self) -> builtins.str:
        '''User ID who owns the session.'''
        result = self._values.get("user_id")
        assert result is not None, "Required property 'user_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def webhook_url(self) -> typing.Optional[builtins.str]:
        result = self._values.get("webhook_url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SessionDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.SessionListItem",
    jsii_struct_bases=[],
    name_mapping={"downstream": "downstream", "session": "session"},
)
class SessionListItem:
    def __init__(
        self,
        *,
        downstream: typing.Union[DownstreamInfo, typing.Dict[builtins.str, typing.Any]],
        session: typing.Union[SessionDetails, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''Session information from getAllSessions.

        :param downstream: Downstream connection information.
        :param session: Session details.
        '''
        if isinstance(downstream, dict):
            downstream = DownstreamInfo(**downstream)
        if isinstance(session, dict):
            session = SessionDetails(**session)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__253a32a9275ecf9e72bcf1f2b75cf11a6a77a921015a702c79b2bfc420b72ef5)
            check_type(argname="argument downstream", value=downstream, expected_type=type_hints["downstream"])
            check_type(argname="argument session", value=session, expected_type=type_hints["session"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "downstream": downstream,
            "session": session,
        }

    @builtins.property
    def downstream(self) -> DownstreamInfo:
        '''Downstream connection information.'''
        result = self._values.get("downstream")
        assert result is not None, "Required property 'downstream' is missing"
        return typing.cast(DownstreamInfo, result)

    @builtins.property
    def session(self) -> SessionDetails:
        '''Session details.'''
        result = self._values.get("session")
        assert result is not None, "Required property 'session' is missing"
        return typing.cast(SessionDetails, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SessionListItem(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.SessionMetadata",
    jsii_struct_bases=[],
    name_mapping={"user_email": "userEmail", "user_id": "userId"},
)
class SessionMetadata:
    def __init__(self, *, user_email: builtins.str, user_id: builtins.str) -> None:
        '''
        :param user_email: 
        :param user_id: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07c4740974554c0849a34dbedfa991994373e666f12451f52bdcd86b56796bfb)
            check_type(argname="argument user_email", value=user_email, expected_type=type_hints["user_email"])
            check_type(argname="argument user_id", value=user_id, expected_type=type_hints["user_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_email": user_email,
            "user_id": user_id,
        }

    @builtins.property
    def user_email(self) -> builtins.str:
        result = self._values.get("user_email")
        assert result is not None, "Required property 'user_email' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_id(self) -> builtins.str:
        result = self._values.get("user_id")
        assert result is not None, "Required property 'user_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SessionMetadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.SettingsSecurityChangeInfo",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "changed_at": "changedAt",
        "changed_by": "changedBy",
    },
)
class SettingsSecurityChangeInfo:
    def __init__(
        self,
        *,
        enabled: builtins.bool,
        changed_at: typing.Optional[builtins.str] = None,
        changed_by: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Settings security change info.

        :param enabled: Whether the setting is enabled.
        :param changed_at: When the setting was last changed.
        :param changed_by: Who changed the setting.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00214282c14641108c81a775130df264580c07d52d42f8115a838ca3596d1bfa)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument changed_at", value=changed_at, expected_type=type_hints["changed_at"])
            check_type(argname="argument changed_by", value=changed_by, expected_type=type_hints["changed_by"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }
        if changed_at is not None:
            self._values["changed_at"] = changed_at
        if changed_by is not None:
            self._values["changed_by"] = changed_by

    @builtins.property
    def enabled(self) -> builtins.bool:
        '''Whether the setting is enabled.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def changed_at(self) -> typing.Optional[builtins.str]:
        '''When the setting was last changed.'''
        result = self._values.get("changed_at")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def changed_by(self) -> typing.Optional[builtins.str]:
        '''Who changed the setting.'''
        result = self._values.get("changed_by")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SettingsSecurityChangeInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.SubjectRequest",
    jsii_struct_bases=[],
    name_mapping={"subject": "subject"},
)
class SubjectRequest:
    def __init__(self, *, subject: builtins.str) -> None:
        '''Subject request.

        :param subject: Group subject/name.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a531353acb198b346ac710373ae9842a1a785cd44825751b6b68e6ae1312b900)
            check_type(argname="argument subject", value=subject, expected_type=type_hints["subject"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subject": subject,
        }

    @builtins.property
    def subject(self) -> builtins.str:
        '''Group subject/name.'''
        result = self._values.get("subject")
        assert result is not None, "Required property 'subject' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SubjectRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.WAMessage",
    jsii_struct_bases=[],
    name_mapping={
        "content": "content",
        "from_me": "fromMe",
        "id": "id",
        "recipient": "recipient",
        "sender": "sender",
        "status": "status",
        "timestamp": "timestamp",
        "to": "to",
        "type": "type",
    },
)
class WAMessage:
    def __init__(
        self,
        *,
        content: builtins.str,
        from_me: builtins.bool,
        id: builtins.str,
        recipient: builtins.str,
        sender: builtins.str,
        status: builtins.str,
        timestamp: builtins.str,
        to: builtins.str,
        type: builtins.str,
    ) -> None:
        '''WhatsApp message response.

        :param content: The message content.
        :param from_me: Whether the message is from me.
        :param id: The message ID.
        :param recipient: The message recipient.
        :param sender: The message sender.
        :param status: The message status.
        :param timestamp: The message timestamp.
        :param to: The recipient's phone number or group JID.
        :param type: The message type.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb18d81c4798685e0c7d24fb90be1d9433e8a027998cb1588ca65befb16e2d53)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument from_me", value=from_me, expected_type=type_hints["from_me"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument recipient", value=recipient, expected_type=type_hints["recipient"])
            check_type(argname="argument sender", value=sender, expected_type=type_hints["sender"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument timestamp", value=timestamp, expected_type=type_hints["timestamp"])
            check_type(argname="argument to", value=to, expected_type=type_hints["to"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content": content,
            "from_me": from_me,
            "id": id,
            "recipient": recipient,
            "sender": sender,
            "status": status,
            "timestamp": timestamp,
            "to": to,
            "type": type,
        }

    @builtins.property
    def content(self) -> builtins.str:
        '''The message content.'''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def from_me(self) -> builtins.bool:
        '''Whether the message is from me.'''
        result = self._values.get("from_me")
        assert result is not None, "Required property 'from_me' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def id(self) -> builtins.str:
        '''The message ID.'''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def recipient(self) -> builtins.str:
        '''The message recipient.'''
        result = self._values.get("recipient")
        assert result is not None, "Required property 'recipient' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sender(self) -> builtins.str:
        '''The message sender.'''
        result = self._values.get("sender")
        assert result is not None, "Required property 'sender' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def status(self) -> builtins.str:
        '''The message status.'''
        result = self._values.get("status")
        assert result is not None, "Required property 'status' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def timestamp(self) -> builtins.str:
        '''The message timestamp.'''
        result = self._values.get("timestamp")
        assert result is not None, "Required property 'timestamp' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def to(self) -> builtins.str:
        '''The recipient's phone number or group JID.'''
        result = self._values.get("to")
        assert result is not None, "Required property 'to' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The message type.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WAMessage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.WANumberExistResult",
    jsii_struct_bases=[],
    name_mapping={"exists": "exists", "phone": "phone", "jid": "jid"},
)
class WANumberExistResult:
    def __init__(
        self,
        *,
        exists: builtins.bool,
        phone: builtins.str,
        jid: typing.Optional[builtins.str] = None,
    ) -> None:
        '''WhatsApp number existence check result.

        :param exists: Whether the number exists on WhatsApp.
        :param phone: The phone number that was checked.
        :param jid: The JID of the contact if it exists.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1322fd26c65f22aed45b65186990bfd4e62fedc82adb7666f244dda382b4486)
            check_type(argname="argument exists", value=exists, expected_type=type_hints["exists"])
            check_type(argname="argument phone", value=phone, expected_type=type_hints["phone"])
            check_type(argname="argument jid", value=jid, expected_type=type_hints["jid"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "exists": exists,
            "phone": phone,
        }
        if jid is not None:
            self._values["jid"] = jid

    @builtins.property
    def exists(self) -> builtins.bool:
        '''Whether the number exists on WhatsApp.'''
        result = self._values.get("exists")
        assert result is not None, "Required property 'exists' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def phone(self) -> builtins.str:
        '''The phone number that was checked.'''
        result = self._values.get("phone")
        assert result is not None, "Required property 'phone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def jid(self) -> typing.Optional[builtins.str]:
        '''The JID of the contact if it exists.'''
        result = self._values.get("jid")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WANumberExistResult(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WasendClient(metaclass=jsii.JSIIMeta, jsii_type="@wasend/core.WasendClient"):
    '''Main Wasend SDK Client.

    This class provides access to the Wasend API for sending messages,
    managing contacts, and other messaging operations.

    Example::

        const client = new WasendClient({
          apiKey: 'your-api-key'
        });
        
        const result = await client.sendMessage({
          to: '+1234567890',
          content: 'Hello, World!'
        });
    '''

    def __init__(
        self,
        *,
        api_key: builtins.str,
        base_url: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Creates a new Wasend client instance.

        :param api_key: The API key for authentication.
        :param base_url: The base URL for the API (optional). Default: https://api.wasend.dev
        :param timeout: Request timeout in milliseconds. Default: 30000
        '''
        config = WasendConfig(api_key=api_key, base_url=base_url, timeout=timeout)

        jsii.create(self.__class__, self, [config])

    @jsii.member(jsii_name="addGroupParticipants")
    def add_group_participants(
        self,
        session_id: builtins.str,
        group_id: builtins.str,
        *,
        participants: typing.Sequence[builtins.str],
        notify: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Add participants to group.

        :param session_id: - The session ID.
        :param group_id: - The group ID (full JID, e.g., 1234567890-12345678@g.us).
        :param participants: List of participant IDs.
        :param notify: Whether to notify participants. Default: true

        Example::

            curl -X POST 'http://localhost:3001/{sessionId}/groups/{groupId}/participants/add' \
              -H 'Authorization: Bearer {apiKey}' \
              -H 'Content-Type: application/json' \
              -d '{
                "participants": ["+1234567890", "+0987654321"],
                "notify": true
              }'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d04492a423af28b395df4631b1e8504bfe332d323a4d844b1f74ffa6d0bc1bed)
            check_type(argname="argument session_id", value=session_id, expected_type=type_hints["session_id"])
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
        request = ParticipantsRequest(participants=participants, notify=notify)

        return typing.cast(None, jsii.ainvoke(self, "addGroupParticipants", [session_id, group_id, request]))

    @jsii.member(jsii_name="checkContactExists")
    def check_contact_exists(
        self,
        session_id: builtins.str,
        *,
        phone: builtins.str,
    ) -> WANumberExistResult:
        '''Check if a phone number is registered in WhatsApp.

        :param session_id: - The session ID.
        :param phone: The phone number to check.

        :return: Promise resolving to the check result

        Example::

            curl -X GET 'http://localhost:3001/contacts/check-exists?session={sessionId}&phone=1213213213' \
              -H 'Authorization: Bearer {apiKey}'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99a95a59c1a3b4445f873f11ef6baffe53f6dd829735d4e9cbd963f5f4d03750)
            check_type(argname="argument session_id", value=session_id, expected_type=type_hints["session_id"])
        params = CheckContactExistsQueryParams(phone=phone)

        return typing.cast(WANumberExistResult, jsii.ainvoke(self, "checkContactExists", [session_id, params]))

    @jsii.member(jsii_name="createGroup")
    def create_group(
        self,
        session_id: builtins.str,
        *,
        name: builtins.str,
        participants: typing.Sequence[typing.Union[CreateGroupParticipant, typing.Dict[builtins.str, typing.Any]]],
        description: typing.Optional[builtins.str] = None,
        picture_url: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> Group:
        '''Create a new group.

        :param session_id: - The session ID.
        :param name: Group name.
        :param participants: Group participants.
        :param description: Group description (optional).
        :param picture_url: Group picture URL (optional).
        :param tags: Group tags (optional).

        :return: Promise resolving to the created group

        Example::

            curl -X POST 'http://localhost:3001/{sessionId}/groups' \
              -H 'Authorization: Bearer {apiKey}' \
              -H 'Content-Type: application/json' \
              -d '{
                "name": "My Group",
                "participants": [{"id": "+1234567890"}],
                "description": "Group description"
              }'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7729a3030ecbc268f6363fbf99c6f1e1bc24e714f8db5d7d265301b563adc021)
            check_type(argname="argument session_id", value=session_id, expected_type=type_hints["session_id"])
        request = CreateGroupRequest(
            name=name,
            participants=participants,
            description=description,
            picture_url=picture_url,
            tags=tags,
        )

        return typing.cast(Group, jsii.ainvoke(self, "createGroup", [session_id, request]))

    @jsii.member(jsii_name="createSession")
    def create_session(
        self,
        *,
        phone_number: builtins.str,
        session_name: builtins.str,
        enable_account_protection: typing.Optional[builtins.bool] = None,
        enable_message_logging: typing.Optional[builtins.bool] = None,
        enable_webhook: typing.Optional[builtins.bool] = None,
        webhook_url: typing.Optional[builtins.str] = None,
    ) -> "Session":
        '''
        :param phone_number: Phone number for the WhatsApp session.
        :param session_name: Name of the session.
        :param enable_account_protection: Enable account protection features. Default: false
        :param enable_message_logging: Enable message logging. Default: false
        :param enable_webhook: Enable webhook notifications. Default: false
        :param webhook_url: Webhook URL for notifications Required if enableWebhook is true.
        '''
        request = SessionCreateRequest(
            phone_number=phone_number,
            session_name=session_name,
            enable_account_protection=enable_account_protection,
            enable_message_logging=enable_message_logging,
            enable_webhook=enable_webhook,
            webhook_url=webhook_url,
        )

        return typing.cast("Session", jsii.ainvoke(self, "createSession", [request]))

    @jsii.member(jsii_name="deleteGroupPicture")
    def delete_group_picture(
        self,
        session_id: builtins.str,
        group_id: builtins.str,
    ) -> None:
        '''Delete group picture.

        :param session_id: - The session ID.
        :param group_id: - The group ID.

        Example::

            curl -X DELETE 'http://localhost:3001/{sessionId}/groups/{groupId}/picture' \
              -H 'Authorization: Bearer {apiKey}'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acd94bad66a6e473e68654c72f4f17951aaaf98b516f2fc2ae23525f4d19142d)
            check_type(argname="argument session_id", value=session_id, expected_type=type_hints["session_id"])
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
        return typing.cast(None, jsii.ainvoke(self, "deleteGroupPicture", [session_id, group_id]))

    @jsii.member(jsii_name="deleteSession")
    def delete_session(self, session_id: builtins.str) -> None:
        '''
        :param session_id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b81b617d22cf593cff9ddd2976e6f0737bcab6b6cbfd35d40b731b45e7f5210)
            check_type(argname="argument session_id", value=session_id, expected_type=type_hints["session_id"])
        return typing.cast(None, jsii.ainvoke(self, "deleteSession", [session_id]))

    @jsii.member(jsii_name="demoteGroupParticipants")
    def demote_group_participants(
        self,
        session_id: builtins.str,
        group_id: builtins.str,
        *,
        participants: typing.Sequence[builtins.str],
        notify: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Demote participants from admin.

        :param session_id: - The session ID.
        :param group_id: - The group ID (full JID, e.g., 1234567890-12345678@g.us).
        :param participants: List of participant IDs.
        :param notify: Whether to notify participants. Default: true

        Example::

            curl -X POST 'http://localhost:3001/{sessionId}/groups/{groupId}/admin/demote' \
              -H 'Authorization: Bearer {apiKey}' \
              -H 'Content-Type: application/json' \
              -d '{
                "participants": ["+1234567890", "+0987654321"],
                "notify": true
              }'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__139540a56d71cd0ce28d760b8121524e566176105230d2d10368e8c868a0b1bf)
            check_type(argname="argument session_id", value=session_id, expected_type=type_hints["session_id"])
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
        request = ParticipantsRequest(participants=participants, notify=notify)

        return typing.cast(None, jsii.ainvoke(self, "demoteGroupParticipants", [session_id, group_id, request]))

    @jsii.member(jsii_name="getAllChats")
    def get_all_chats(
        self,
        session: builtins.str,
        *,
        limit: typing.Optional[jsii.Number] = None,
        offset: typing.Optional[jsii.Number] = None,
        sort_by: typing.Optional[builtins.str] = None,
        sort_order: typing.Optional[builtins.str] = None,
    ) -> SdkResponse:
        '''Retrieves all chats for a given session.

        :param session: - The session identifier.
        :param limit: 
        :param offset: 
        :param sort_by: 
        :param sort_order: 

        :return: A promise that resolves to an SdkResponse object. If successful, ``data`` contains an array of Chat objects. If failed, ``error`` contains the error message.

        Example::

            const client = new WasendClient({ apiKey: 'your-api-key' });
            const result = await client.getAllChats('my-session', { limit: 10, sortBy: 'timestamp', sortOrder: 'desc' });
            if (result.success && result.data) {
              console.log('Chats:', result.data);
            } else {
              console.error('Failed to get chats:', result.error);
            }
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e70a7c80e4d2ba1ecb16738c3c23397463440182d1920123fdecb98f03ea831f)
            check_type(argname="argument session", value=session, expected_type=type_hints["session"])
        options = GetChatsOptions(
            limit=limit, offset=offset, sort_by=sort_by, sort_order=sort_order
        )

        return typing.cast(SdkResponse, jsii.ainvoke(self, "getAllChats", [session, options]))

    @jsii.member(jsii_name="getChatPicture")
    def get_chat_picture(
        self,
        session: builtins.str,
        chat_id: builtins.str,
        *,
        refresh: typing.Optional[builtins.bool] = None,
    ) -> SdkResponse:
        '''Retrieves the profile picture of a chat (user or group).

        :param session: - The session identifier.
        :param chat_id: - The ID of the chat (e.g., '1234567890@c.us' for a user or '1234567890-1234567890@g.us' for a group).
        :param refresh: 

        :return: A promise that resolves to an SdkResponse object. If successful, ``data`` contains a ``ChatPictureResponse`` object. If failed, ``error`` contains the error message.

        Example::

            const client = new WasendClient({ apiKey: 'your-api-key' });
            const session = 'my-session';
            const chatId = '1234567890@c.us';
            
            const result = await client.getChatPicture(session, chatId);
            if (result.success && result.data) {
              if (result.data.url) {
                console.log('Chat picture URL:', result.data.url);
              } else {
                console.log('Chat does not have a picture or it could not be retrieved.');
              }
            
              // Force refresh
              const refreshedResult = await client.getChatPicture(session, chatId, { refresh: true });
              if (refreshedResult.success && refreshedResult.data) {
                 console.log('Refreshed picture URL:', refreshedResult.data.url);
              } else {
                 console.error('Failed to refresh chat picture:', refreshedResult.error);
              }
            } else {
              console.error('Failed to get chat picture:', result.error);
            }
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee7da13a77009acdddeff305e10a5db368f4c9cb074406c192bedc4057d9e8a6)
            check_type(argname="argument session", value=session, expected_type=type_hints["session"])
            check_type(argname="argument chat_id", value=chat_id, expected_type=type_hints["chat_id"])
        options = GetChatPictureOptions(refresh=refresh)

        return typing.cast(SdkResponse, jsii.ainvoke(self, "getChatPicture", [session, chat_id, options]))

    @jsii.member(jsii_name="getChatsOverview")
    def get_chats_overview(
        self,
        session: builtins.str,
        *,
        ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        limit: typing.Optional[jsii.Number] = None,
        offset: typing.Optional[jsii.Number] = None,
    ) -> SdkResponse:
        '''Retrieves an overview of chats for a given session, allowing pagination and filtering by chat IDs.

        :param session: - The session identifier.
        :param ids: 
        :param limit: 
        :param offset: 

        :return: A promise that resolves to an SdkResponse object. If successful, ``data`` contains an array of ChatOverview objects. If failed, ``error`` contains the error message.

        Example::

            const client = new WasendClient({ apiKey: 'your-api-key' });
            const result = await client.getChatsOverview('my-session', { limit: 10, ids: ['1234567890@c.us'] });
            if (result.success && result.data) {
              console.log(result.data);
            } else {
              console.error('Failed to get chats overview:', result.error);
            }
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__492c79af76a7bd8dac211d2193193c8d3e039fbf87cacce721f0b2ddc937ab8f)
            check_type(argname="argument session", value=session, expected_type=type_hints["session"])
        options = GetChatsOverviewOptions(ids=ids, limit=limit, offset=offset)

        return typing.cast(SdkResponse, jsii.ainvoke(self, "getChatsOverview", [session, options]))

    @jsii.member(jsii_name="getContact")
    def get_contact(
        self,
        session_id: builtins.str,
        *,
        contact_id: builtins.str,
    ) -> Contact:
        '''Get contact basic info.

        :param session_id: - The session ID.
        :param contact_id: Contact ID (phone number with.

        :return: Promise resolving to the contact information

        Example::

            curl -X GET 'http://localhost:3001/contacts?session={sessionId}&contactId=+11111111111' \
              -H 'Authorization: Bearer {apiKey}'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d77ef7352da27ed2ec09684fca511169a5faff56a447a1ccf86cf980f7e1a460)
            check_type(argname="argument session_id", value=session_id, expected_type=type_hints["session_id"])
        params = GetContactQueryParams(contact_id=contact_id)

        return typing.cast(Contact, jsii.ainvoke(self, "getContact", [session_id, params]))

    @jsii.member(jsii_name="getContactProfilePicture")
    def get_contact_profile_picture(
        self,
        session_id: builtins.str,
        *,
        contact_id: builtins.str,
        refresh: typing.Optional[builtins.bool] = None,
    ) -> ProfilePictureResponse:
        '''Get contact's profile picture URL.

        :param session_id: - The session ID.
        :param contact_id: Contact ID (phone number with.
        :param refresh: Refresh the picture from the server (24h cache by default). Default: false

        :return: Promise resolving to the profile picture response

        Example::

            curl -X GET 'http://localhost:3001/contacts/profile-picture?session={sessionId}&contactId=+11111111111&refresh=false' \
              -H 'Authorization: Bearer {apiKey}'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f22d74965b45389836d7b39cb4b56ecdba92406c4bea6e9cdc5bec11546658a)
            check_type(argname="argument session_id", value=session_id, expected_type=type_hints["session_id"])
        params = GetProfilePictureQueryParams(contact_id=contact_id, refresh=refresh)

        return typing.cast(ProfilePictureResponse, jsii.ainvoke(self, "getContactProfilePicture", [session_id, params]))

    @jsii.member(jsii_name="getContacts")
    def get_contacts(
        self,
        session_id: builtins.str,
        *,
        limit: typing.Optional[jsii.Number] = None,
        offset: typing.Optional[jsii.Number] = None,
        sort_by: typing.Optional[builtins.str] = None,
        sort_order: typing.Optional[builtins.str] = None,
    ) -> typing.List[Contact]:
        '''Get all contacts.

        :param session_id: - The session ID.
        :param limit: Maximum number of results. Default: 10
        :param offset: Number of results to skip. Default: 0
        :param sort_by: Sort by field.
        :param sort_order: Sort order.

        :return: Promise resolving to the list of contacts

        Example::

            curl -X GET 'http://localhost:3001/contacts/all?session={sessionId}&sortBy=name&sortOrder=asc&limit=10&offset=0' \
              -H 'Authorization: Bearer {apiKey}'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12f47d2c48c79766fb1f65cf404cb9f5860981e8e13a359f33e05b426d780b7b)
            check_type(argname="argument session_id", value=session_id, expected_type=type_hints["session_id"])
        params = GetContactsQueryParams(
            limit=limit, offset=offset, sort_by=sort_by, sort_order=sort_order
        )

        return typing.cast(typing.List[Contact], jsii.ainvoke(self, "getContacts", [session_id, params]))

    @jsii.member(jsii_name="getGroup")
    def get_group(self, session_id: builtins.str, group_id: builtins.str) -> Group:
        '''Get a specific group.

        :param session_id: - The session ID.
        :param group_id: - The group ID.

        :return: Promise resolving to the group

        Example::

            curl -X GET 'http://localhost:3001/{sessionId}/groups/{groupId}' \
              -H 'Authorization: Bearer {apiKey}'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8030276c85cb8c16e95e727aa18f585dca4407ab282e54c3fc14d5dca85b6ec8)
            check_type(argname="argument session_id", value=session_id, expected_type=type_hints["session_id"])
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
        return typing.cast(Group, jsii.ainvoke(self, "getGroup", [session_id, group_id]))

    @jsii.member(jsii_name="getGroupInfoAdminOnly")
    def get_group_info_admin_only(
        self,
        session_id: builtins.str,
        group_id: builtins.str,
    ) -> SettingsSecurityChangeInfo:
        '''Get group info admin only setting.

        :param session_id: - The session ID.
        :param group_id: - The group ID.

        :return: Promise resolving to the settings security change info

        Example::

            curl -X GET 'http://localhost:3001/{sessionId}/groups/{groupId}/settings/security/info-admin-only' \
              -H 'Authorization: Bearer {apiKey}'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7e034eb5f212f98a6ac3e0971b4320d19293a250557ded9fdbdc62d2f093d52)
            check_type(argname="argument session_id", value=session_id, expected_type=type_hints["session_id"])
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
        return typing.cast(SettingsSecurityChangeInfo, jsii.ainvoke(self, "getGroupInfoAdminOnly", [session_id, group_id]))

    @jsii.member(jsii_name="getGroupInviteCode")
    def get_group_invite_code(
        self,
        session_id: builtins.str,
        group_id: builtins.str,
    ) -> builtins.str:
        '''Get group invite code.

        :param session_id: - The session ID.
        :param group_id: - The group ID.

        :return: Promise resolving to the invite code

        Example::

            curl -X GET 'http://localhost:3001/{sessionId}/groups/{groupId}/invite-code' \
              -H 'Authorization: Bearer {apiKey}'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2e46ec9091dbb97e1a93d52648d33e2341ce3c91e90c3a2add13403799eaa27)
            check_type(argname="argument session_id", value=session_id, expected_type=type_hints["session_id"])
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
        return typing.cast(builtins.str, jsii.ainvoke(self, "getGroupInviteCode", [session_id, group_id]))

    @jsii.member(jsii_name="getGroupJoinInfo")
    def get_group_join_info(
        self,
        session_id: builtins.str,
        code: builtins.str,
    ) -> Group:
        '''Get group join info.

        :param session_id: - The session ID.
        :param code: - Group code or invite URL.

        :return: Promise resolving to the group info

        Example::

            curl -X GET 'http://localhost:3001/{sessionId}/groups/join-info?code=https://chat.whatsapp.com/1234567890abcdef' \
              -H 'Authorization: Bearer {apiKey}'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c931f18445ef721ad90f49d0e44558dca33ffaa85d023870f59d3d56755e94cc)
            check_type(argname="argument session_id", value=session_id, expected_type=type_hints["session_id"])
            check_type(argname="argument code", value=code, expected_type=type_hints["code"])
        return typing.cast(Group, jsii.ainvoke(self, "getGroupJoinInfo", [session_id, code]))

    @jsii.member(jsii_name="getGroupMessagesAdminOnly")
    def get_group_messages_admin_only(
        self,
        session_id: builtins.str,
        group_id: builtins.str,
    ) -> SettingsSecurityChangeInfo:
        '''Get group messages admin only setting.

        :param session_id: - The session ID.
        :param group_id: - The group ID.

        :return: Promise resolving to the settings security change info

        Example::

            curl -X GET 'http://localhost:3001/{sessionId}/groups/{groupId}/settings/security/messages-admin-only' \
              -H 'Authorization: Bearer {apiKey}'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81f7b2f48b68ce43a72907022490663f7a361147617503ccb0f1a31b9f28e0a7)
            check_type(argname="argument session_id", value=session_id, expected_type=type_hints["session_id"])
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
        return typing.cast(SettingsSecurityChangeInfo, jsii.ainvoke(self, "getGroupMessagesAdminOnly", [session_id, group_id]))

    @jsii.member(jsii_name="getGroupParticipants")
    def get_group_participants(
        self,
        session_id: builtins.str,
        group_id: builtins.str,
    ) -> typing.List[GroupParticipant]:
        '''Get group participants.

        :param session_id: - The session ID.
        :param group_id: - The group ID.

        :return: Promise resolving to the list of participants

        Example::

            curl -X GET 'http://localhost:3001/{sessionId}/groups/{groupId}/participants' \
              -H 'Authorization: Bearer {apiKey}'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fdbed9bcbb62155a20fb7bbaa0dfde2143ac26d926c271859d4c28c5d34ff46)
            check_type(argname="argument session_id", value=session_id, expected_type=type_hints["session_id"])
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
        return typing.cast(typing.List[GroupParticipant], jsii.ainvoke(self, "getGroupParticipants", [session_id, group_id]))

    @jsii.member(jsii_name="getGroupPicture")
    def get_group_picture(
        self,
        session_id: builtins.str,
        group_id: builtins.str,
        refresh: typing.Optional[builtins.bool] = None,
    ) -> GroupPictureResponse:
        '''Get group picture.

        :param session_id: - The session ID.
        :param group_id: - The group ID.
        :param refresh: - Whether to refresh the picture from server.

        :return: Promise resolving to the group picture response

        Example::

            curl -X GET 'http://localhost:3001/{sessionId}/groups/{groupId}/picture?refresh=true' \
              -H 'Authorization: Bearer {apiKey}'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e87990fa3a3febaa8547346458de3d6a592f085fb6619b4eb52c8d898718e96)
            check_type(argname="argument session_id", value=session_id, expected_type=type_hints["session_id"])
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
            check_type(argname="argument refresh", value=refresh, expected_type=type_hints["refresh"])
        return typing.cast(GroupPictureResponse, jsii.ainvoke(self, "getGroupPicture", [session_id, group_id, refresh]))

    @jsii.member(jsii_name="getGroups")
    def get_groups(
        self,
        session_id: builtins.str,
        *,
        exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        limit: typing.Optional[jsii.Number] = None,
        offset: typing.Optional[jsii.Number] = None,
        search: typing.Optional[builtins.str] = None,
        sort_by: typing.Optional[builtins.str] = None,
        sort_order: typing.Optional[builtins.str] = None,
        status: typing.Optional[GroupStatus] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> typing.List[Group]:
        '''Get all groups.

        :param session_id: - The session ID.
        :param exclude: Fields to exclude from response.
        :param limit: Maximum number of results. Default: 50
        :param offset: Number of results to skip. Default: 0
        :param search: Search by name or description.
        :param sort_by: Sort by field.
        :param sort_order: Sort order.
        :param status: Filter by status.
        :param tags: Filter by tags.

        :return: Promise resolving to the list of groups

        Example::

            curl -X GET 'http://localhost:3001/{sessionId}/groups?sortBy=creation&sortOrder=desc&limit=50&offset=0' \
              -H 'Authorization: Bearer {apiKey}'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79e446fdce747cc36adaedf856e4febf5056e6bc7178859337a491a0110da4b7)
            check_type(argname="argument session_id", value=session_id, expected_type=type_hints["session_id"])
        params = GetGroupsQueryParams(
            exclude=exclude,
            limit=limit,
            offset=offset,
            search=search,
            sort_by=sort_by,
            sort_order=sort_order,
            status=status,
            tags=tags,
        )

        return typing.cast(typing.List[Group], jsii.ainvoke(self, "getGroups", [session_id, params]))

    @jsii.member(jsii_name="getGroupsCount")
    def get_groups_count(self, session_id: builtins.str) -> CountResponse:
        '''Get groups count.

        :param session_id: - The session ID.

        :return: Promise resolving to the count response

        Example::

            curl -X GET 'http://localhost:3001/{sessionId}/groups/count' \
              -H 'Authorization: Bearer {apiKey}'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b67c9b6e5d06ffdbdb23ed7573a858300956858942ea8657bf86b82f9caa4602)
            check_type(argname="argument session_id", value=session_id, expected_type=type_hints["session_id"])
        return typing.cast(CountResponse, jsii.ainvoke(self, "getGroupsCount", [session_id]))

    @jsii.member(jsii_name="getMessage")
    def get_message(self, message_id: builtins.str) -> SdkResponse:
        '''Get message by ID.

        :param message_id: - The ID of the message to retrieve.

        :return: Promise resolving to the API response
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cb1dc5792b15a5416b556e58d46fc39554d89dbc043723fca120ccd8c6d7a24)
            check_type(argname="argument message_id", value=message_id, expected_type=type_hints["message_id"])
        return typing.cast(SdkResponse, jsii.ainvoke(self, "getMessage", [message_id]))

    @jsii.member(jsii_name="getMessageById")
    def get_message_by_id(
        self,
        session: builtins.str,
        chat_id: builtins.str,
        message_id: builtins.str,
        *,
        download_media: typing.Optional[builtins.bool] = None,
    ) -> SdkResponse:
        '''Retrieves a specific message by its ID from a given chat.

        :param session: - The session identifier.
        :param chat_id: - The ID of the chat from which to retrieve the message.
        :param message_id: - The ID of the message to retrieve.
        :param download_media: 

        :return: A promise that resolves to an SdkResponse object. If successful, ``data`` contains the ``WAMessage`` object. If failed, ``error`` contains the error message.

        Example::

            const client = new WasendClient({ apiKey: 'your-api-key' });
            const session = 'my-session';
            const chatId = '1234567890@c.us';
            const messageId = 'messageId123';
            
            const result = await client.getMessageById(session, chatId, messageId);
            if (result.success && result.data) {
              console.log('Retrieved message:', result.data);
            
              // Retrieve message and attempt to include media
              const mediaResult = await client.getMessageById(session, chatId, messageId, { downloadMedia: true });
              if (mediaResult.success && mediaResult.data) {
                 console.log('Message with media (if any):', mediaResult.data);
              } else {
                 console.error('Failed to get message with media:', mediaResult.error);
              }
            } else {
              console.error('Failed to get message by ID:', result.error);
            }
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dab9c1728004f37a8f1acdb766ca2064a65defb623b014815c34b01b45f8c11a)
            check_type(argname="argument session", value=session, expected_type=type_hints["session"])
            check_type(argname="argument chat_id", value=chat_id, expected_type=type_hints["chat_id"])
            check_type(argname="argument message_id", value=message_id, expected_type=type_hints["message_id"])
        options = GetMessageByIdOptions(download_media=download_media)

        return typing.cast(SdkResponse, jsii.ainvoke(self, "getMessageById", [session, chat_id, message_id, options]))

    @jsii.member(jsii_name="getMessages")
    def get_messages(
        self,
        session: builtins.str,
        chat_id: builtins.str,
        *,
        limit: jsii.Number,
        download_media: typing.Optional[builtins.bool] = None,
        filter: typing.Optional[typing.Union[GetMessagesFilterOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        offset: typing.Optional[jsii.Number] = None,
    ) -> SdkResponse:
        '''Get messages from a chat.

        This method retrieves a list of messages from a specified chat, allowing for pagination,
        media download preferences, and filtering based on various criteria.

        :param session: - The session identifier.
        :param chat_id: - The ID of the chat (e.g., '1234567890@c.us' for a user or '1234567890-1234567890@g.us' for a group).
        :param limit: 
        :param download_media: 
        :param filter: 
        :param offset: 

        :return: A promise that resolves to an SdkResponse object. If successful, ``data`` contains an array of WAMessage objects. If failed, ``error`` contains the error message.

        Example::

            const client = new WasendClient({ apiKey: 'your-api-key' });
            const session = 'my-session';
            const chatId = '1234567890@c.us';
            
            // Get the last 10 messages
            const result = await client.getMessages(session, chatId, { limit: 10 });
            if (result.success && result.data) {
              console.log('Last 10 messages:', result.data);
            
              // Get messages from the last 24 hours, with media, sent by me
              const twentyFourHoursAgo = Math.floor((Date.now() - 24 * 60 * 60 * 1000) / 1000);
              const myMessagesResult = await client.getMessages(session, chatId, {
                limit: 50, // Max 50
                downloadMedia: true,
                filter: {
                  timestampGte: twentyFourHoursAgo,
                  fromMe: true,
                },
              });
              if (myMessagesResult.success && myMessagesResult.data) {
                 console.log('My messages from last 24h with media:', myMessagesResult.data);
              } else {
                 console.error('Failed to get my messages:', myMessagesResult.error);
              }
            } else {
             console.error('Failed to get messages:', result.error);
            }
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0bc5589803a84f85c893d759095ed8bdc83708c0e3255e8fde94e29f184ed03)
            check_type(argname="argument session", value=session, expected_type=type_hints["session"])
            check_type(argname="argument chat_id", value=chat_id, expected_type=type_hints["chat_id"])
        options = GetMessagesOptions(
            limit=limit, download_media=download_media, filter=filter, offset=offset
        )

        return typing.cast(SdkResponse, jsii.ainvoke(self, "getMessages", [session, chat_id, options]))

    @jsii.member(jsii_name="joinGroup")
    def join_group(
        self,
        session_id: builtins.str,
        *,
        code: builtins.str,
    ) -> JoinGroupResponse:
        '''Join a group.

        :param session_id: - The session ID.
        :param code: Group code or invite URL.

        :return: Promise resolving to the join group response

        Example::

            curl -X POST 'http://localhost:3001/{sessionId}/groups/join' \
              -H 'Authorization: Bearer {apiKey}' \
              -H 'Content-Type: application/json' \
              -d '{
                "code": "https://chat.whatsapp.com/1234567890abcdef"
              }'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1ce14e57c07700725ac03b1625ae7b1dd49be5322a3f62315ddb9b5d8b073e0)
            check_type(argname="argument session_id", value=session_id, expected_type=type_hints["session_id"])
        request = JoinGroupRequest(code=code)

        return typing.cast(JoinGroupResponse, jsii.ainvoke(self, "joinGroup", [session_id, request]))

    @jsii.member(jsii_name="leaveGroup")
    def leave_group(self, session_id: builtins.str, group_id: builtins.str) -> None:
        '''Leave a group.

        :param session_id: - The session ID.
        :param group_id: - The group ID.

        Example::

            curl -X POST 'http://localhost:3001/{sessionId}/groups/{groupId}/leave' \
              -H 'Authorization: Bearer {apiKey}'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad558ece6289316cb6c96cbcd2874d636299d55acf6b5001971b29a88534d99a)
            check_type(argname="argument session_id", value=session_id, expected_type=type_hints["session_id"])
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
        return typing.cast(None, jsii.ainvoke(self, "leaveGroup", [session_id, group_id]))

    @jsii.member(jsii_name="processMessage")
    def process_message(
        self,
        request: typing.Union[SendRequest, typing.Dict[builtins.str, typing.Any]],
        options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> WAMessage:
        '''Utility method to process a message with proper timing and typing indicators This follows WhatsApp's guidelines to avoid being flagged as spam.

        :param request: - The send request to process. For 'to', use recipient's phone number (e.g., +1234567890) or a full group JID.
        :param options: - Optional configuration for the message processing.

        :return: Promise resolving to the sent message

        Example::

            // Send a text message with proper processing
            const message = await client.processMessage({
              session: "sessionId",
              to: "+1234567890",
              text: "Hello, World!"
            });
            
            // Send an image with caption and proper processing
            const imageMessage = await client.processMessage({
              session: "sessionId",
              to: "+1234567890",
              imageUrl: "https://example.com/image.jpg",
              text: "Check out this image!"
            });
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c363ed8cf42447ba6ef57176faadd0997865f1533903ed8de24df601d5990f0)
            check_type(argname="argument request", value=request, expected_type=type_hints["request"])
            check_type(argname="argument options", value=options, expected_type=type_hints["options"])
        return typing.cast(WAMessage, jsii.ainvoke(self, "processMessage", [request, options]))

    @jsii.member(jsii_name="promoteGroupParticipants")
    def promote_group_participants(
        self,
        session_id: builtins.str,
        group_id: builtins.str,
        *,
        participants: typing.Sequence[builtins.str],
        notify: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Promote participants to admin.

        :param session_id: - The session ID.
        :param group_id: - The group ID (full JID, e.g., 1234567890-12345678@g.us).
        :param participants: List of participant IDs.
        :param notify: Whether to notify participants. Default: true

        Example::

            curl -X POST 'http://localhost:3001/{sessionId}/groups/{groupId}/admin/promote' \
              -H 'Authorization: Bearer {apiKey}' \
              -H 'Content-Type: application/json' \
              -d '{
                "participants": ["+1234567890", "+0987654321"],
                "notify": true
              }'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf8386881c4864c8999a84821ec8b8c63f8c21174180d155609c8fe66a7634cc)
            check_type(argname="argument session_id", value=session_id, expected_type=type_hints["session_id"])
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
        request = ParticipantsRequest(participants=participants, notify=notify)

        return typing.cast(None, jsii.ainvoke(self, "promoteGroupParticipants", [session_id, group_id, request]))

    @jsii.member(jsii_name="readMessages")
    def read_messages(
        self,
        session: builtins.str,
        chat_id: builtins.str,
        *,
        days: typing.Optional[jsii.Number] = None,
        messages: typing.Optional[jsii.Number] = None,
    ) -> ReadChatMessagesResponse:
        '''Marks messages in a specific chat as read.

        This can be done by specifying the number of
        latest messages to mark as read, or by specifying a number of days to mark messages from.

        If the API request fails due to network issues or server-side errors, this method will
        return a ``ReadChatMessagesResponse`` object with ``success: false`` and an error message.

        :param session: - The session identifier.
        :param chat_id: - The ID of the chat (e.g., '1234567890@c.us' or '1234567890-1234567890@g.us').
        :param days: 
        :param messages: 

        :return:

        A promise that resolves to a ``ReadChatMessagesResponse`` object indicating the success or failure
        of the operation, along with an optional descriptive message.

        Example::

            const client = new WasendClient({ apiKey: 'your-api-key' });
            const session = 'my-session';
            const chatId = '1234567890@c.us';
            
            // Mark the last 5 messages as read
            const response1 = await client.readMessages(session, chatId, { messages: 5 });
            if (response1.success) {
              console.log(response1.message || 'Successfully marked 5 messages as read.');
            } else {
              console.error('Failed to mark messages as read:', response1.message);
            }
            
            // Mark messages from the last 2 days as read
            const response2 = await client.readMessages(session, chatId, { days: 2 });
            if (response2.success) {
              console.log(response2.message || 'Successfully marked messages from last 2 days as read.');
            } else {
              console.error('Failed to mark messages as read:', response2.message);
            }
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40124cbc6cbf96cfa9e9d1ad29d0370d746bcf4314f15f715c91af9923b664d6)
            check_type(argname="argument session", value=session, expected_type=type_hints["session"])
            check_type(argname="argument chat_id", value=chat_id, expected_type=type_hints["chat_id"])
        options = ReadMessagesOptions(days=days, messages=messages)

        return typing.cast(ReadChatMessagesResponse, jsii.ainvoke(self, "readMessages", [session, chat_id, options]))

    @jsii.member(jsii_name="removeGroupParticipants")
    def remove_group_participants(
        self,
        session_id: builtins.str,
        group_id: builtins.str,
        *,
        participants: typing.Sequence[builtins.str],
        notify: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Remove participants from group.

        :param session_id: - The session ID.
        :param group_id: - The group ID (full JID, e.g., 1234567890-12345678@g.us).
        :param participants: List of participant IDs.
        :param notify: Whether to notify participants. Default: true

        Example::

            curl -X POST 'http://localhost:3001/{sessionId}/groups/{groupId}/participants/remove' \
              -H 'Authorization: Bearer {apiKey}' \
              -H 'Content-Type: application/json' \
              -d '{
                "participants": ["+1234567890", "+0987654321"],
                "notify": true
              }'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf96f551c9495cee95efea4f156c3cd3a914cde297e48549cd3589aac13a77c7)
            check_type(argname="argument session_id", value=session_id, expected_type=type_hints["session_id"])
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
        request = ParticipantsRequest(participants=participants, notify=notify)

        return typing.cast(None, jsii.ainvoke(self, "removeGroupParticipants", [session_id, group_id, request]))

    @jsii.member(jsii_name="restartSession")
    def restart_session(self, session_id: builtins.str) -> "Session":
        '''
        :param session_id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__434c60505ee2fb2a5457c0dbf03cd3dfeaefd14bed60b513aaefc899f45188c2)
            check_type(argname="argument session_id", value=session_id, expected_type=type_hints["session_id"])
        return typing.cast("Session", jsii.ainvoke(self, "restartSession", [session_id]))

    @jsii.member(jsii_name="retrieveAccount")
    def retrieve_account(self) -> SdkResponse:
        '''Get account information.

        :return: Promise resolving to the API response
        '''
        return typing.cast(SdkResponse, jsii.ainvoke(self, "retrieveAccount", []))

    @jsii.member(jsii_name="retrieveAllSessions")
    def retrieve_all_sessions(self) -> GetAllSessionsResponse:
        return typing.cast(GetAllSessionsResponse, jsii.ainvoke(self, "retrieveAllSessions", []))

    @jsii.member(jsii_name="retrieveConfig")
    def retrieve_config(self) -> "WasendConfigInfo":
        '''Get the current configuration.

        :return: The configuration object (without sensitive data)
        '''
        return typing.cast("WasendConfigInfo", jsii.invoke(self, "retrieveConfig", []))

    @jsii.member(jsii_name="retrieveQRCode")
    def retrieve_qr_code(self, session_id: builtins.str) -> QRCodeResponse:
        '''
        :param session_id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28c5d954ff13b65e026a7d45c6cb568a11d7bcc2d8c09e6c7e2b6d6364b1104c)
            check_type(argname="argument session_id", value=session_id, expected_type=type_hints["session_id"])
        return typing.cast(QRCodeResponse, jsii.ainvoke(self, "retrieveQRCode", [session_id]))

    @jsii.member(jsii_name="retrieveSessionInfo")
    def retrieve_session_info(self, session_id: builtins.str) -> "Session":
        '''
        :param session_id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0df4545c26c4a54c2feea4d8159760885691ec730352cae801811b0e3276ec21)
            check_type(argname="argument session_id", value=session_id, expected_type=type_hints["session_id"])
        return typing.cast("Session", jsii.ainvoke(self, "retrieveSessionInfo", [session_id]))

    @jsii.member(jsii_name="revokeGroupInviteCode")
    def revoke_group_invite_code(
        self,
        session_id: builtins.str,
        group_id: builtins.str,
    ) -> builtins.str:
        '''Revoke group invite code.

        :param session_id: - The session ID.
        :param group_id: - The group ID.

        :return: Promise resolving to the new invite code

        Example::

            curl -X POST 'http://localhost:3001/{sessionId}/groups/{groupId}/invite-code/revoke' \
              -H 'Authorization: Bearer {apiKey}'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57a4ef47ff269e952b181227322868fa3ed5b2390aab0831ded042080bbdbbe3)
            check_type(argname="argument session_id", value=session_id, expected_type=type_hints["session_id"])
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
        return typing.cast(builtins.str, jsii.ainvoke(self, "revokeGroupInviteCode", [session_id, group_id]))

    @jsii.member(jsii_name="send")
    def send(
        self,
        *,
        session: builtins.str,
        to: builtins.str,
        audio_url: typing.Optional[builtins.str] = None,
        document_url: typing.Optional[builtins.str] = None,
        filename: typing.Optional[builtins.str] = None,
        image_url: typing.Optional[builtins.str] = None,
        mimetype: typing.Optional[builtins.str] = None,
        preview: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        text: typing.Optional[builtins.str] = None,
        video_url: typing.Optional[builtins.str] = None,
    ) -> WAMessage:
        '''Send a message using the unified send endpoint.

        :param session: The session ID.
        :param to: The recipient's phone number or group JID.
        :param audio_url: The audio URL.
        :param document_url: The document URL.
        :param filename: The filename for the media.
        :param image_url: The image URL.
        :param mimetype: The MIME type of the media.
        :param preview: The link preview information.
        :param text: The message text or caption.
        :param video_url: The video URL.

        :return: Promise resolving to the sent message

        Example::

            // Send a text message
            const textMessage = await client.send({
              session: "sessionId",
              to: "+1234567890",
              text: "Hello from WASend!"
            });
            
            // Send an image
            const imageMessage = await client.send({
              session: "sessionId",
              to: "+1234567890",
              imageUrl: "https://example.com/image.jpg",
              text: "Check out this image!",
              mimetype: "image/jpeg"
            });
            
            // Send a video
            const videoMessage = await client.send({
              session: "sessionId",
              to: "+1234567890",
              videoUrl: "https://example.com/video.mp4",
              text: "Check out this video!",
              mimetype: "video/mp4"
            });
            
            // Send a document
            const documentMessage = await client.send({
              session: "sessionId",
              to: "+1234567890",
              documentUrl: "https://example.com/document.pdf",
              filename: "document.pdf",
              mimetype: "application/pdf"
            });
            
            // Send an audio message
            const audioMessage = await client.send({
              session: "sessionId",
              to: "+1234567890",
              audioUrl: "https://example.com/audio.mp3",
              mimetype: "audio/mpeg"
            });
        '''
        request = SendRequest(
            session=session,
            to=to,
            audio_url=audio_url,
            document_url=document_url,
            filename=filename,
            image_url=image_url,
            mimetype=mimetype,
            preview=preview,
            text=text,
            video_url=video_url,
        )

        return typing.cast(WAMessage, jsii.ainvoke(self, "send", [request]))

    @jsii.member(jsii_name="sendFile")
    def send_file(
        self,
        *,
        file_name: builtins.str,
        mime_type: builtins.str,
        data: typing.Optional[builtins.str] = None,
        url: typing.Optional[builtins.str] = None,
        content: builtins.str,
        to: builtins.str,
    ) -> WAMessage:
        '''Send a file message.

        :param file_name: The file name.
        :param mime_type: The file mime type.
        :param data: The file data in base64 format.
        :param url: The file URL.
        :param content: The content of the message.
        :param to: The recipient of the message.

        :return: Promise resolving to the sent message

        Example::

            curl -X POST 'http://localhost:3001/sendFile' \
              -H 'Authorization: Bearer {apiKey}' \
              -H 'Content-Type: application/json' \
              -d '{
                "session": "sessionId",
                "to": "+11111111111",
                "url": "https://example.com/file.pdf",
                "fileName": "document.pdf",
                "mimeType": "application/pdf"
              }'
        '''
        request = MessageFileRequest(
            file_name=file_name,
            mime_type=mime_type,
            data=data,
            url=url,
            content=content,
            to=to,
        )

        return typing.cast(WAMessage, jsii.ainvoke(self, "sendFile", [request]))

    @jsii.member(jsii_name="sendImage")
    def send_image(
        self,
        *,
        caption: typing.Optional[builtins.str] = None,
        data: typing.Optional[builtins.str] = None,
        url: typing.Optional[builtins.str] = None,
        content: builtins.str,
        to: builtins.str,
    ) -> WAMessage:
        '''Send an image message.

        :param caption: The image caption.
        :param data: The image data in base64 format.
        :param url: The image URL.
        :param content: The content of the message.
        :param to: The recipient of the message.

        :return: Promise resolving to the sent message

        Example::

            curl -X POST 'http://localhost:3001/sendImage' \
              -H 'Authorization: Bearer {apiKey}' \
              -H 'Content-Type: application/json' \
              -d '{
                "session": "sessionId",
                "to": "+11111111111",
                "url": "https://example.com/image.jpg",
                "caption": "Check out this image!"
              }'
        '''
        request = MessageImageRequest(
            caption=caption, data=data, url=url, content=content, to=to
        )

        return typing.cast(WAMessage, jsii.ainvoke(self, "sendImage", [request]))

    @jsii.member(jsii_name="sendLinkCustomPreview")
    def send_link_custom_preview(
        self,
        *,
        preview: typing.Union[LinkPreviewRequest, typing.Dict[builtins.str, typing.Any]],
        text: builtins.str,
        content: builtins.str,
        to: builtins.str,
    ) -> WAMessage:
        '''Send a text message with custom link preview.

        :param preview: The link preview information.
        :param text: The text content of the message.
        :param content: The content of the message.
        :param to: The recipient of the message.

        :return: Promise resolving to the sent message

        Example::

            curl -X POST 'http://localhost:3001/send/link-custom-preview' \
              -H 'Authorization: Bearer {apiKey}' \
              -H 'Content-Type: application/json' \
              -d '{
                "session": "sessionId",
                "to": "+11111111111",
                "text": "Check out this link!",
                "preview": {
                  "title": "Example Website",
                  "description": "A great website",
                  "thumbnailUrl": "https://example.com/thumbnail.jpg"
                }
              }'
        '''
        request = MessageLinkCustomPreviewRequest(
            preview=preview, text=text, content=content, to=to
        )

        return typing.cast(WAMessage, jsii.ainvoke(self, "sendLinkCustomPreview", [request]))

    @jsii.member(jsii_name="sendMessage")
    def send_message(self, *, content: builtins.str, to: builtins.str) -> SdkResponse:
        '''Send a message to a recipient.

        :param content: The content of the message.
        :param to: The recipient of the message.

        :return: Promise resolving to the API response
        '''
        request = MessageRequest(content=content, to=to)

        return typing.cast(SdkResponse, jsii.ainvoke(self, "sendMessage", [request]))

    @jsii.member(jsii_name="sendSeen")
    def send_seen(
        self,
        *,
        message_id: builtins.str,
        session: builtins.str,
        to: builtins.str,
    ) -> None:
        '''Mark a message as seen.

        :param message_id: The message ID to mark as seen.
        :param session: The session ID.
        :param to: The recipient's phone number or group JID.

        Example::

            curl -X POST 'http://localhost:3001/sendSeen' \
              -H 'Authorization: Bearer {apiKey}' \
              -H 'Content-Type: application/json' \
              -d '{
                "session": "sessionId",
                "to": "+11111111111",
                "messageId": "messageId"
              }'
        '''
        request = SendSeenRequest(message_id=message_id, session=session, to=to)

        return typing.cast(None, jsii.ainvoke(self, "sendSeen", [request]))

    @jsii.member(jsii_name="sendText")
    def send_text(
        self,
        *,
        text: builtins.str,
        content: builtins.str,
        to: builtins.str,
    ) -> WAMessage:
        '''Send a text message.

        :param text: The text content of the message.
        :param content: The content of the message.
        :param to: The recipient of the message.

        :return: Promise resolving to the sent message

        Example::

            curl -X POST 'http://localhost:3001/sendText' \
              -H 'Authorization: Bearer {apiKey}' \
              -H 'Content-Type: application/json' \
              -d '{
                "session": "sessionId",
                "to": "+11111111111",
                "text": "Hello, World!"
              }'
        '''
        request = MessageTextRequest(text=text, content=content, to=to)

        return typing.cast(WAMessage, jsii.ainvoke(self, "sendText", [request]))

    @jsii.member(jsii_name="sendVideo")
    def send_video(
        self,
        *,
        caption: typing.Optional[builtins.str] = None,
        data: typing.Optional[builtins.str] = None,
        url: typing.Optional[builtins.str] = None,
        content: builtins.str,
        to: builtins.str,
    ) -> WAMessage:
        '''Send a video message.

        :param caption: The video caption.
        :param data: The video data in base64 format.
        :param url: The video URL.
        :param content: The content of the message.
        :param to: The recipient of the message.

        :return: Promise resolving to the sent message

        Example::

            curl -X POST 'http://localhost:3001/sendVideo' \
              -H 'Authorization: Bearer {apiKey}' \
              -H 'Content-Type: application/json' \
              -d '{
                "session": "sessionId",
                "to": "+11111111111",
                "url": "https://example.com/video.mp4",
                "caption": "Check out this video!"
              }'
        '''
        request = MessageVideoRequest(
            caption=caption, data=data, url=url, content=content, to=to
        )

        return typing.cast(WAMessage, jsii.ainvoke(self, "sendVideo", [request]))

    @jsii.member(jsii_name="sendVoice")
    def send_voice(
        self,
        *,
        data: typing.Optional[builtins.str] = None,
        duration: typing.Optional[jsii.Number] = None,
        url: typing.Optional[builtins.str] = None,
        content: builtins.str,
        to: builtins.str,
    ) -> WAMessage:
        '''Send a voice message.

        :param data: The voice message data in base64 format.
        :param duration: The voice message duration in seconds.
        :param url: The voice message URL.
        :param content: The content of the message.
        :param to: The recipient of the message.

        :return: Promise resolving to the sent message

        Example::

            curl -X POST 'http://localhost:3001/sendVoice' \
              -H 'Authorization: Bearer {apiKey}' \
              -H 'Content-Type: application/json' \
              -d '{
                "session": "sessionId",
                "to": "+11111111111",
                "url": "https://example.com/voice.mp3",
                "duration": 30
              }'
        '''
        request = MessageVoiceRequest(
            data=data, duration=duration, url=url, content=content, to=to
        )

        return typing.cast(WAMessage, jsii.ainvoke(self, "sendVoice", [request]))

    @jsii.member(jsii_name="setGroupDescription")
    def set_group_description(
        self,
        session_id: builtins.str,
        group_id: builtins.str,
        *,
        description: builtins.str,
    ) -> None:
        '''Set group description.

        :param session_id: - The session ID.
        :param group_id: - The group ID.
        :param description: Group description.

        Example::

            curl -X PUT 'http://localhost:3001/{sessionId}/groups/{groupId}/description' \
              -H 'Authorization: Bearer {apiKey}' \
              -H 'Content-Type: application/json' \
              -d '{
                "description": "New group description"
              }'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d996da125e7066eec8c63ab6217f55bcfdb9750a7dfac528a8dfdb665cdcb06)
            check_type(argname="argument session_id", value=session_id, expected_type=type_hints["session_id"])
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
        request = DescriptionRequest(description=description)

        return typing.cast(None, jsii.ainvoke(self, "setGroupDescription", [session_id, group_id, request]))

    @jsii.member(jsii_name="setGroupInfoAdminOnly")
    def set_group_info_admin_only(
        self,
        session_id: builtins.str,
        group_id: builtins.str,
        *,
        enabled: builtins.bool,
        changed_at: typing.Optional[builtins.str] = None,
        changed_by: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Set group info admin only setting.

        :param session_id: - The session ID.
        :param group_id: - The group ID.
        :param enabled: Whether the setting is enabled.
        :param changed_at: When the setting was last changed.
        :param changed_by: Who changed the setting.

        Example::

            curl -X PUT 'http://localhost:3001/{sessionId}/groups/{groupId}/settings/security/info-admin-only' \
              -H 'Authorization: Bearer {apiKey}' \
              -H 'Content-Type: application/json' \
              -d '{
                "enabled": true
              }'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01f992487d1068e66a04e21b3f6a815a82a56176d0da3ef12c2d9afe82c7d339)
            check_type(argname="argument session_id", value=session_id, expected_type=type_hints["session_id"])
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
        request = SettingsSecurityChangeInfo(
            enabled=enabled, changed_at=changed_at, changed_by=changed_by
        )

        return typing.cast(None, jsii.ainvoke(self, "setGroupInfoAdminOnly", [session_id, group_id, request]))

    @jsii.member(jsii_name="setGroupMessagesAdminOnly")
    def set_group_messages_admin_only(
        self,
        session_id: builtins.str,
        group_id: builtins.str,
        *,
        enabled: builtins.bool,
        changed_at: typing.Optional[builtins.str] = None,
        changed_by: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Set group messages admin only setting.

        :param session_id: - The session ID.
        :param group_id: - The group ID.
        :param enabled: Whether the setting is enabled.
        :param changed_at: When the setting was last changed.
        :param changed_by: Who changed the setting.

        Example::

            curl -X PUT 'http://localhost:3001/{sessionId}/groups/{groupId}/settings/security/messages-admin-only' \
              -H 'Authorization: Bearer {apiKey}' \
              -H 'Content-Type: application/json' \
              -d '{
                "enabled": true
              }'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d04e5287c8d30def6a53429e00e5612221a56fd49e7e2946d77a68bd1309b70a)
            check_type(argname="argument session_id", value=session_id, expected_type=type_hints["session_id"])
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
        request = SettingsSecurityChangeInfo(
            enabled=enabled, changed_at=changed_at, changed_by=changed_by
        )

        return typing.cast(None, jsii.ainvoke(self, "setGroupMessagesAdminOnly", [session_id, group_id, request]))

    @jsii.member(jsii_name="setGroupPicture")
    def set_group_picture(
        self,
        session_id: builtins.str,
        group_id: builtins.str,
        *,
        url: builtins.str,
        crop_to_square: typing.Optional[builtins.bool] = None,
        format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Set group picture.

        :param session_id: - The session ID.
        :param group_id: - The group ID.
        :param url: Picture URL.
        :param crop_to_square: Whether to crop the picture to a square. Default: true
        :param format: Picture format (optional). Default: "jpeg"

        Example::

            curl -X PUT 'http://localhost:3001/{sessionId}/groups/{groupId}/picture' \
              -H 'Authorization: Bearer {apiKey}' \
              -H 'Content-Type: application/json' \
              -d '{
                "url": "https://example.com/picture.jpg",
                "format": "jpeg",
                "cropToSquare": true
              }'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97881afa91799d88ce91f801dd54ffd039ecfdf3c4cffaabcd56350b0208268b)
            check_type(argname="argument session_id", value=session_id, expected_type=type_hints["session_id"])
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
        request = ProfilePictureRequest(
            url=url, crop_to_square=crop_to_square, format=format
        )

        return typing.cast(None, jsii.ainvoke(self, "setGroupPicture", [session_id, group_id, request]))

    @jsii.member(jsii_name="setGroupSubject")
    def set_group_subject(
        self,
        session_id: builtins.str,
        group_id: builtins.str,
        *,
        subject: builtins.str,
    ) -> None:
        '''Set group subject.

        :param session_id: - The session ID.
        :param group_id: - The group ID.
        :param subject: Group subject/name.

        Example::

            curl -X PUT 'http://localhost:3001/{sessionId}/groups/{groupId}/subject' \
              -H 'Authorization: Bearer {apiKey}' \
              -H 'Content-Type: application/json' \
              -d '{
                "subject": "New group name"
              }'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13d698cfe11326ad055a7380a45198a7063790bb0d9f383ddcb6e310349857fa)
            check_type(argname="argument session_id", value=session_id, expected_type=type_hints["session_id"])
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
        request = SubjectRequest(subject=subject)

        return typing.cast(None, jsii.ainvoke(self, "setGroupSubject", [session_id, group_id, request]))

    @jsii.member(jsii_name="startSession")
    def start_session(self, session_id: builtins.str) -> "Session":
        '''
        :param session_id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa7a8584f39c683cf7a8b0b493cff8b738a07457858bf3cd19b6c31a06e322f5)
            check_type(argname="argument session_id", value=session_id, expected_type=type_hints["session_id"])
        return typing.cast("Session", jsii.ainvoke(self, "startSession", [session_id]))

    @jsii.member(jsii_name="startTyping")
    def start_typing(self, *, session: builtins.str, to: builtins.str) -> None:
        '''Start typing indicator.

        :param session: The session ID.
        :param to: The recipient's phone number or group JID.

        Example::

            curl -X POST 'http://localhost:3001/startTyping' \
              -H 'Authorization: Bearer {apiKey}' \
              -H 'Content-Type: application/json' \
              -d '{
                "session": "sessionId",
                "to": "+11111111111"
              }'
        '''
        request = ChatRequest(session=session, to=to)

        return typing.cast(None, jsii.ainvoke(self, "startTyping", [request]))

    @jsii.member(jsii_name="stopSession")
    def stop_session(self, session_id: builtins.str) -> "Session":
        '''
        :param session_id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90776ed81605470091e6ac1e31d09ac72b2c7b36b5504d37ae9ba1995f67c193)
            check_type(argname="argument session_id", value=session_id, expected_type=type_hints["session_id"])
        return typing.cast("Session", jsii.ainvoke(self, "stopSession", [session_id]))

    @jsii.member(jsii_name="stopTyping")
    def stop_typing(self, *, session: builtins.str, to: builtins.str) -> None:
        '''Stop typing indicator.

        :param session: The session ID.
        :param to: The recipient's phone number or group JID.

        Example::

            curl -X POST 'http://localhost:3001/stopTyping' \
              -H 'Authorization: Bearer {apiKey}' \
              -H 'Content-Type: application/json' \
              -d '{
                "session": "sessionId",
                "to": "+11111111111"
              }'
        '''
        request = ChatRequest(session=session, to=to)

        return typing.cast(None, jsii.ainvoke(self, "stopTyping", [request]))


@jsii.data_type(
    jsii_type="@wasend/core.WasendConfig",
    jsii_struct_bases=[],
    name_mapping={"api_key": "apiKey", "base_url": "baseUrl", "timeout": "timeout"},
)
class WasendConfig:
    def __init__(
        self,
        *,
        api_key: builtins.str,
        base_url: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Configuration options for the Wasend SDK.

        :param api_key: The API key for authentication.
        :param base_url: The base URL for the API (optional). Default: https://api.wasend.dev
        :param timeout: Request timeout in milliseconds. Default: 30000
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c206f9f03c1e9230f7c6c5569fcc5de78f0c947a9e73ad39ca3b1ff4c771d2c)
            check_type(argname="argument api_key", value=api_key, expected_type=type_hints["api_key"])
            check_type(argname="argument base_url", value=base_url, expected_type=type_hints["base_url"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_key": api_key,
        }
        if base_url is not None:
            self._values["base_url"] = base_url
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def api_key(self) -> builtins.str:
        '''The API key for authentication.'''
        result = self._values.get("api_key")
        assert result is not None, "Required property 'api_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def base_url(self) -> typing.Optional[builtins.str]:
        '''The base URL for the API (optional).

        :default: https://api.wasend.dev
        '''
        result = self._values.get("base_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''Request timeout in milliseconds.

        :default: 30000
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WasendConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.WasendConfigInfo",
    jsii_struct_bases=[],
    name_mapping={"base_url": "baseUrl", "timeout": "timeout"},
)
class WasendConfigInfo:
    def __init__(
        self,
        *,
        base_url: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Configuration information (without sensitive data).

        :param base_url: The base URL for the API.
        :param timeout: Request timeout in milliseconds.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6abbc9d87deb2b837793c948e1cf709fe5599235bd5573df1224f4163f2401ad)
            check_type(argname="argument base_url", value=base_url, expected_type=type_hints["base_url"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if base_url is not None:
            self._values["base_url"] = base_url
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def base_url(self) -> typing.Optional[builtins.str]:
        '''The base URL for the API.'''
        result = self._values.get("base_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''Request timeout in milliseconds.'''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WasendConfigInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WasendUtils(metaclass=jsii.JSIIMeta, jsii_type="@wasend/core.WasendUtils"):
    '''Utility functions for the Wasend SDK.'''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="formatPhoneNumber")
    @builtins.classmethod
    def format_phone_number(
        cls,
        phone_number: builtins.str,
        country_code: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        '''Format a phone number to international format.

        :param phone_number: - The phone number to format.
        :param country_code: - Optional country code to use.

        :return: Formatted phone number
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eec89eaaa50e420d927618815b182bd6b5ce4b4a016f10a5e4b0ccc37fc905be)
            check_type(argname="argument phone_number", value=phone_number, expected_type=type_hints["phone_number"])
            check_type(argname="argument country_code", value=country_code, expected_type=type_hints["country_code"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "formatPhoneNumber", [phone_number, country_code]))

    @jsii.member(jsii_name="isValidPhoneNumber")
    @builtins.classmethod
    def is_valid_phone_number(cls, phone_number: builtins.str) -> builtins.bool:
        '''Check if a phone number is valid.

        :param phone_number: - The phone number to validate.

        :return: Whether the phone number is valid
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f3e44e026e6ad10ba5cef7676e8b8f792085bec1680d62137a198b09822712a)
            check_type(argname="argument phone_number", value=phone_number, expected_type=type_hints["phone_number"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isValidPhoneNumber", [phone_number]))


@jsii.data_type(
    jsii_type="@wasend/core.MessageFileRequest",
    jsii_struct_bases=[MessageRequest],
    name_mapping={
        "content": "content",
        "to": "to",
        "file_name": "fileName",
        "mime_type": "mimeType",
        "data": "data",
        "url": "url",
    },
)
class MessageFileRequest(MessageRequest):
    def __init__(
        self,
        *,
        content: builtins.str,
        to: builtins.str,
        file_name: builtins.str,
        mime_type: builtins.str,
        data: typing.Optional[builtins.str] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''File message request.

        :param content: The content of the message.
        :param to: The recipient of the message.
        :param file_name: The file name.
        :param mime_type: The file mime type.
        :param data: The file data in base64 format.
        :param url: The file URL.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8373abf07139df0e10a00cd6fa9e4241e31eeb1c4b95d5c6cbacef4eb6760e68)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument to", value=to, expected_type=type_hints["to"])
            check_type(argname="argument file_name", value=file_name, expected_type=type_hints["file_name"])
            check_type(argname="argument mime_type", value=mime_type, expected_type=type_hints["mime_type"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content": content,
            "to": to,
            "file_name": file_name,
            "mime_type": mime_type,
        }
        if data is not None:
            self._values["data"] = data
        if url is not None:
            self._values["url"] = url

    @builtins.property
    def content(self) -> builtins.str:
        '''The content of the message.'''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def to(self) -> builtins.str:
        '''The recipient of the message.'''
        result = self._values.get("to")
        assert result is not None, "Required property 'to' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def file_name(self) -> builtins.str:
        '''The file name.'''
        result = self._values.get("file_name")
        assert result is not None, "Required property 'file_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mime_type(self) -> builtins.str:
        '''The file mime type.'''
        result = self._values.get("mime_type")
        assert result is not None, "Required property 'mime_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data(self) -> typing.Optional[builtins.str]:
        '''The file data in base64 format.'''
        result = self._values.get("data")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''The file URL.'''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MessageFileRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.MessageImageRequest",
    jsii_struct_bases=[MessageRequest],
    name_mapping={
        "content": "content",
        "to": "to",
        "caption": "caption",
        "data": "data",
        "url": "url",
    },
)
class MessageImageRequest(MessageRequest):
    def __init__(
        self,
        *,
        content: builtins.str,
        to: builtins.str,
        caption: typing.Optional[builtins.str] = None,
        data: typing.Optional[builtins.str] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Image message request.

        :param content: The content of the message.
        :param to: The recipient of the message.
        :param caption: The image caption.
        :param data: The image data in base64 format.
        :param url: The image URL.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f4feac6a3f3e2263ff153c7a829e0045b7fcfb529a99b0e512e54b7f5974c0e)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument to", value=to, expected_type=type_hints["to"])
            check_type(argname="argument caption", value=caption, expected_type=type_hints["caption"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content": content,
            "to": to,
        }
        if caption is not None:
            self._values["caption"] = caption
        if data is not None:
            self._values["data"] = data
        if url is not None:
            self._values["url"] = url

    @builtins.property
    def content(self) -> builtins.str:
        '''The content of the message.'''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def to(self) -> builtins.str:
        '''The recipient of the message.'''
        result = self._values.get("to")
        assert result is not None, "Required property 'to' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def caption(self) -> typing.Optional[builtins.str]:
        '''The image caption.'''
        result = self._values.get("caption")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data(self) -> typing.Optional[builtins.str]:
        '''The image data in base64 format.'''
        result = self._values.get("data")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''The image URL.'''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MessageImageRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.MessageLinkCustomPreviewRequest",
    jsii_struct_bases=[MessageTextRequest],
    name_mapping={
        "content": "content",
        "to": "to",
        "text": "text",
        "preview": "preview",
    },
)
class MessageLinkCustomPreviewRequest(MessageTextRequest):
    def __init__(
        self,
        *,
        content: builtins.str,
        to: builtins.str,
        text: builtins.str,
        preview: typing.Union[LinkPreviewRequest, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''Message with custom link preview request.

        :param content: The content of the message.
        :param to: The recipient of the message.
        :param text: The text content of the message.
        :param preview: The link preview information.
        '''
        if isinstance(preview, dict):
            preview = LinkPreviewRequest(**preview)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ebbbe9d645bc5355f122d8a16cc77dc5abbf89d380f119db914ef148786df20)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument to", value=to, expected_type=type_hints["to"])
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
            check_type(argname="argument preview", value=preview, expected_type=type_hints["preview"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content": content,
            "to": to,
            "text": text,
            "preview": preview,
        }

    @builtins.property
    def content(self) -> builtins.str:
        '''The content of the message.'''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def to(self) -> builtins.str:
        '''The recipient of the message.'''
        result = self._values.get("to")
        assert result is not None, "Required property 'to' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def text(self) -> builtins.str:
        '''The text content of the message.'''
        result = self._values.get("text")
        assert result is not None, "Required property 'text' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def preview(self) -> LinkPreviewRequest:
        '''The link preview information.'''
        result = self._values.get("preview")
        assert result is not None, "Required property 'preview' is missing"
        return typing.cast(LinkPreviewRequest, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MessageLinkCustomPreviewRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@wasend/core.Session",
    jsii_struct_bases=[SessionDetails],
    name_mapping={
        "created_at": "createdAt",
        "enable_account_protection": "enableAccountProtection",
        "enable_message_logging": "enableMessageLogging",
        "enable_webhook": "enableWebhook",
        "id": "id",
        "phone_number": "phoneNumber",
        "session_name": "sessionName",
        "unique_session_id": "uniqueSessionId",
        "updated_at": "updatedAt",
        "user_id": "userId",
        "webhook_url": "webhookUrl",
        "config": "config",
        "engine": "engine",
        "name": "name",
        "status": "status",
    },
)
class Session(SessionDetails):
    def __init__(
        self,
        *,
        created_at: builtins.str,
        enable_account_protection: builtins.bool,
        enable_message_logging: builtins.bool,
        enable_webhook: builtins.bool,
        id: builtins.str,
        phone_number: builtins.str,
        session_name: builtins.str,
        unique_session_id: builtins.str,
        updated_at: builtins.str,
        user_id: builtins.str,
        webhook_url: typing.Optional[builtins.str] = None,
        config: typing.Union[SessionConfig, typing.Dict[builtins.str, typing.Any]],
        engine: typing.Union[EngineStatus, typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        status: builtins.str,
    ) -> None:
        '''Session information from createSession and other operations.

        :param created_at: Creation timestamp.
        :param enable_account_protection: Session configuration flags.
        :param enable_message_logging: 
        :param enable_webhook: 
        :param id: MongoDB ID of the session.
        :param phone_number: Phone number associated with the session.
        :param session_name: Name of the session.
        :param unique_session_id: Unique session identifier.
        :param updated_at: Last update timestamp.
        :param user_id: User ID who owns the session.
        :param webhook_url: 
        :param config: Session configuration.
        :param engine: Engine status information.
        :param name: Name of the session.
        :param status: Current status of the session.
        '''
        if isinstance(config, dict):
            config = SessionConfig(**config)
        if isinstance(engine, dict):
            engine = EngineStatus(**engine)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3d85e74d62c2d977dab7cc527e9efb8b60c3e669b984e32b30b46f61ca261fa)
            check_type(argname="argument created_at", value=created_at, expected_type=type_hints["created_at"])
            check_type(argname="argument enable_account_protection", value=enable_account_protection, expected_type=type_hints["enable_account_protection"])
            check_type(argname="argument enable_message_logging", value=enable_message_logging, expected_type=type_hints["enable_message_logging"])
            check_type(argname="argument enable_webhook", value=enable_webhook, expected_type=type_hints["enable_webhook"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument phone_number", value=phone_number, expected_type=type_hints["phone_number"])
            check_type(argname="argument session_name", value=session_name, expected_type=type_hints["session_name"])
            check_type(argname="argument unique_session_id", value=unique_session_id, expected_type=type_hints["unique_session_id"])
            check_type(argname="argument updated_at", value=updated_at, expected_type=type_hints["updated_at"])
            check_type(argname="argument user_id", value=user_id, expected_type=type_hints["user_id"])
            check_type(argname="argument webhook_url", value=webhook_url, expected_type=type_hints["webhook_url"])
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument engine", value=engine, expected_type=type_hints["engine"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "created_at": created_at,
            "enable_account_protection": enable_account_protection,
            "enable_message_logging": enable_message_logging,
            "enable_webhook": enable_webhook,
            "id": id,
            "phone_number": phone_number,
            "session_name": session_name,
            "unique_session_id": unique_session_id,
            "updated_at": updated_at,
            "user_id": user_id,
            "config": config,
            "engine": engine,
            "name": name,
            "status": status,
        }
        if webhook_url is not None:
            self._values["webhook_url"] = webhook_url

    @builtins.property
    def created_at(self) -> builtins.str:
        '''Creation timestamp.'''
        result = self._values.get("created_at")
        assert result is not None, "Required property 'created_at' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enable_account_protection(self) -> builtins.bool:
        '''Session configuration flags.'''
        result = self._values.get("enable_account_protection")
        assert result is not None, "Required property 'enable_account_protection' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def enable_message_logging(self) -> builtins.bool:
        result = self._values.get("enable_message_logging")
        assert result is not None, "Required property 'enable_message_logging' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def enable_webhook(self) -> builtins.bool:
        result = self._values.get("enable_webhook")
        assert result is not None, "Required property 'enable_webhook' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def id(self) -> builtins.str:
        '''MongoDB ID of the session.'''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def phone_number(self) -> builtins.str:
        '''Phone number associated with the session.'''
        result = self._values.get("phone_number")
        assert result is not None, "Required property 'phone_number' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def session_name(self) -> builtins.str:
        '''Name of the session.'''
        result = self._values.get("session_name")
        assert result is not None, "Required property 'session_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def unique_session_id(self) -> builtins.str:
        '''Unique session identifier.'''
        result = self._values.get("unique_session_id")
        assert result is not None, "Required property 'unique_session_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def updated_at(self) -> builtins.str:
        '''Last update timestamp.'''
        result = self._values.get("updated_at")
        assert result is not None, "Required property 'updated_at' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_id(self) -> builtins.str:
        '''User ID who owns the session.'''
        result = self._values.get("user_id")
        assert result is not None, "Required property 'user_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def webhook_url(self) -> typing.Optional[builtins.str]:
        result = self._values.get("webhook_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def config(self) -> SessionConfig:
        '''Session configuration.'''
        result = self._values.get("config")
        assert result is not None, "Required property 'config' is missing"
        return typing.cast(SessionConfig, result)

    @builtins.property
    def engine(self) -> EngineStatus:
        '''Engine status information.'''
        result = self._values.get("engine")
        assert result is not None, "Required property 'engine' is missing"
        return typing.cast(EngineStatus, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the session.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def status(self) -> builtins.str:
        '''Current status of the session.'''
        result = self._values.get("status")
        assert result is not None, "Required property 'status' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Session(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AccountInfo",
    "Chat",
    "ChatOverview",
    "ChatPictureResponse",
    "ChatRequest",
    "ChatWAMessage",
    "CheckContactExistsQueryParams",
    "Contact",
    "CountResponse",
    "CreateGroupParticipant",
    "CreateGroupRequest",
    "DescriptionRequest",
    "DownstreamInfo",
    "EngineStatus",
    "GetAllSessionsResponse",
    "GetChatPictureOptions",
    "GetChatsOptions",
    "GetChatsOverviewOptions",
    "GetContactQueryParams",
    "GetContactsQueryParams",
    "GetGroupsQueryParams",
    "GetMessageByIdOptions",
    "GetMessagesFilterOptions",
    "GetMessagesOptions",
    "GetProfilePictureQueryParams",
    "GowsStatus",
    "Group",
    "GroupParticipant",
    "GroupParticipantRole",
    "GroupPictureResponse",
    "GroupSettings",
    "GroupStatus",
    "GrpcStatus",
    "JoinGroupRequest",
    "JoinGroupResponse",
    "LinkPreviewRequest",
    "Message",
    "MessageFileRequest",
    "MessageImageRequest",
    "MessageLinkCustomPreviewRequest",
    "MessageRequest",
    "MessageTextRequest",
    "MessageVideoRequest",
    "MessageVoiceRequest",
    "NowebConfig",
    "NowebStoreConfig",
    "PaginationOptions",
    "ParticipantsRequest",
    "ProfilePictureRequest",
    "ProfilePictureResponse",
    "QRCodeResponse",
    "ReadChatMessagesResponse",
    "ReadMessagesOptions",
    "SdkResponse",
    "SendRequest",
    "SendSeenRequest",
    "Session",
    "SessionConfig",
    "SessionCreateRequest",
    "SessionDetails",
    "SessionListItem",
    "SessionMetadata",
    "SettingsSecurityChangeInfo",
    "SubjectRequest",
    "WAMessage",
    "WANumberExistResult",
    "WasendClient",
    "WasendConfig",
    "WasendConfigInfo",
    "WasendUtils",
]

publication.publish()

def _typecheckingstub__b8d187f8daf4945ee8cc7af4c965fbd16ceba9a4a4f1a826ace5438a45da1cd0(
    *,
    id: builtins.str,
    name: builtins.str,
    plan: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfa06278962f83f68df8d947f16f2877395e96a371674392b0ae5e7f31e29a49(
    *,
    id: builtins.str,
    archived: typing.Optional[builtins.bool] = None,
    is_group: typing.Optional[builtins.bool] = None,
    name: typing.Optional[builtins.str] = None,
    pinned: typing.Optional[builtins.bool] = None,
    timestamp: typing.Optional[jsii.Number] = None,
    unread_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9eb6c31d0ff337b91d63c70aabfbeb18483eeab3cc8c50d725e19b624c3b7f6(
    *,
    id: builtins.str,
    is_group: typing.Optional[builtins.bool] = None,
    name: typing.Optional[builtins.str] = None,
    timestamp: typing.Optional[jsii.Number] = None,
    unread_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09da9e3c62cc36091ae66a18e93d6e95bbfaa6b1a7892888208297e973448b1a(
    *,
    file: typing.Optional[builtins.str] = None,
    mimetype: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90e9bd02629e7e5613e4e5f308462c781bb094fe3968ab3ec2f24d3e0c9b7143(
    *,
    session: builtins.str,
    to: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__425bb91f9998c0944d4eee1a8c13654ecc9ec498632c36161567320fe07138e3(
    *,
    chat_id: builtins.str,
    from_: builtins.str,
    from_me: builtins.bool,
    id: builtins.str,
    timestamp: jsii.Number,
    to: builtins.str,
    type: builtins.str,
    ack: typing.Optional[jsii.Number] = None,
    body: typing.Any = None,
    caption: typing.Optional[builtins.str] = None,
    filename: typing.Optional[builtins.str] = None,
    has_media: typing.Optional[builtins.bool] = None,
    media_url: typing.Optional[builtins.str] = None,
    mimetype: typing.Optional[builtins.str] = None,
    quoted_msg_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ce7e73e4a188e6c18688efc76051366d41bfd5ce1e53874bcbc6b5410105e14(
    *,
    phone: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f01784379d90bd6517ad09f6e9c44b252cc798ffb866437f0a769f0c2ea8aba0(
    *,
    id: builtins.str,
    phone_number: builtins.str,
    business_profile: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    profile_picture_url: typing.Optional[builtins.str] = None,
    push_name: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db0f9d976503c59b6d78d15007dad94a45caac923d28a1c60227137ef9450dc1(
    *,
    total: jsii.Number,
    by_status: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11dbb0617142989f518d5efdf030f4e40b95426ea99cefe74225710d84e9e707(
    *,
    id: builtins.str,
    is_admin: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b801fefb4c7f7aae3c00a9656c8348c463f4a5ca8695facef63b7c41043cc8b0(
    *,
    name: builtins.str,
    participants: typing.Sequence[typing.Union[CreateGroupParticipant, typing.Dict[builtins.str, typing.Any]]],
    description: typing.Optional[builtins.str] = None,
    picture_url: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf438daec090025706f7968ab6b280029fe549899179470b1a48211f2cbf6694(
    *,
    description: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e85038298b8fa1b5985855072c2560ca953a48eea4a7ee8b9f750e8bc6f62348(
    *,
    config: typing.Union[SessionConfig, typing.Dict[builtins.str, typing.Any]],
    engine: typing.Union[EngineStatus, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    status: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62f98c4efad3df7d9dcd0fbf647c894254a448f6718f0c1fad58962182024475(
    *,
    gows: typing.Union[GowsStatus, typing.Dict[builtins.str, typing.Any]],
    grpc: typing.Union[GrpcStatus, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09647a94e3d8e4aee98f4628c3fa572a7d308b6f12281833bf5a01c156dec696(
    *,
    sessions: typing.Sequence[typing.Union[SessionListItem, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98b4ef55b5f7c0f54f8142583fb4be24180dbe24212e4b0868579c431ad52b26(
    *,
    refresh: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1a3d89e80e38a81cfd275a69cc98fb292e237c976e6a9c7ecacd631851661dc(
    *,
    limit: typing.Optional[jsii.Number] = None,
    offset: typing.Optional[jsii.Number] = None,
    sort_by: typing.Optional[builtins.str] = None,
    sort_order: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f131e3eb5d9a18d6a467f0cf0a4840b91cbc75d743963badbf4ceb227d9f2da5(
    *,
    ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    limit: typing.Optional[jsii.Number] = None,
    offset: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ab74c0b993c79a49ecd8b57b84b899caac6adf3a35c750484a98167b95d949b(
    *,
    contact_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3680033b53e752044b09d690a76a7f9763f7c4e9b1c4aeb2b997110eeaa93948(
    *,
    limit: typing.Optional[jsii.Number] = None,
    offset: typing.Optional[jsii.Number] = None,
    sort_by: typing.Optional[builtins.str] = None,
    sort_order: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60bb8c0fe3cf07942ae17d6192dd6e29a24bb3837ce9c87fa0fd46c8c649fc24(
    *,
    exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    limit: typing.Optional[jsii.Number] = None,
    offset: typing.Optional[jsii.Number] = None,
    search: typing.Optional[builtins.str] = None,
    sort_by: typing.Optional[builtins.str] = None,
    sort_order: typing.Optional[builtins.str] = None,
    status: typing.Optional[GroupStatus] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a93a910aaab3132f5c5033203d954c5a1ba65b2d786f0447d6c997f2c2491344(
    *,
    download_media: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__918a0fe200c9476b7e2c780fff5f5509042a9c3513e86defd74f6f221516d045(
    *,
    ack: typing.Optional[typing.Union[jsii.Number, typing.Sequence[jsii.Number]]] = None,
    from_me: typing.Optional[builtins.bool] = None,
    timestamp_gte: typing.Optional[jsii.Number] = None,
    timestamp_lte: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ca33f45329ebae61ec00f7584ddd35bd417aee164fe2854c27c20810611576a(
    *,
    limit: jsii.Number,
    download_media: typing.Optional[builtins.bool] = None,
    filter: typing.Optional[typing.Union[GetMessagesFilterOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    offset: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__490e028bd1817925bde1eab0649d7f86084e21aeb689ac6594663b7f4efb0e31(
    *,
    contact_id: builtins.str,
    refresh: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9c788395f63b322df62cfa06c64f225e1401e968d5af857d8143e86d9b74616(
    *,
    connected: builtins.bool,
    found: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7f6588b08fde062fbfd9593c1e1c125af02ecac9c40b142f1f404ffc7068352(
    *,
    addressing_mode: builtins.str,
    announce_version_id: builtins.str,
    creator_country_code: builtins.str,
    default_membership_approval_mode: builtins.str,
    disappearing_timer: jsii.Number,
    group_created: builtins.str,
    is_announce: builtins.bool,
    is_default_sub_group: builtins.bool,
    is_ephemeral: builtins.bool,
    is_incognito: builtins.bool,
    is_join_approval_required: builtins.bool,
    is_locked: builtins.bool,
    is_parent: builtins.bool,
    jid: builtins.str,
    linked_parent_jid: builtins.str,
    member_add_mode: builtins.str,
    name: builtins.str,
    name_set_at: builtins.str,
    name_set_by: builtins.str,
    name_set_by_pn: builtins.str,
    owner_jid: builtins.str,
    owner_pn: builtins.str,
    participants: typing.Sequence[typing.Union[GroupParticipant, typing.Dict[builtins.str, typing.Any]]],
    participant_version_id: builtins.str,
    topic: builtins.str,
    topic_deleted: builtins.bool,
    topic_id: builtins.str,
    topic_set_at: builtins.str,
    topic_set_by: builtins.str,
    topic_set_by_pn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78b419bf2b928f7f297941e05587ce28c1ed0d03a36769f37143c8e58b5b4aa6(
    *,
    is_admin: builtins.bool,
    is_super_admin: builtins.bool,
    jid: builtins.str,
    phone_number: builtins.str,
    add_request: typing.Any = None,
    display_name: typing.Optional[builtins.str] = None,
    error: typing.Optional[jsii.Number] = None,
    lid: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab62018fb9da12e666c73d8ed7ee31553cf14dec0bbff4e812c637cacc6169d6(
    *,
    url: builtins.str,
    dimensions: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    format: typing.Optional[builtins.str] = None,
    size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__253ec022b4ad3544d7ac905bcc30c46e6f0b23024623a1bc65986f4c9b209794(
    *,
    info_admin_only: builtins.bool,
    messages_admin_only: builtins.bool,
    archived: typing.Optional[builtins.bool] = None,
    muted: typing.Optional[builtins.bool] = None,
    pinned: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a90498c82c9829383ee4faed719fa2d55e4aaaa0a02c2c7519ed1097813a50e6(
    *,
    client: builtins.str,
    stream: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18eb877dbca925b12bfad5ab99b6f84f785d923f2f4d49670915d0ffcc97132b(
    *,
    code: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f99c27e22fb714eb748dcd645448e3ff75f9496926bcd39064f0a77c5c34232(
    *,
    id: builtins.str,
    name: builtins.str,
    participants_count: jsii.Number,
    description: typing.Optional[builtins.str] = None,
    picture_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15e7e6bc1f84a49e376d8c03802f7374297acc7ac1beacdf62c6bb438927dc67(
    *,
    title: builtins.str,
    description: typing.Optional[builtins.str] = None,
    thumbnail_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e6ddabade18cb6b127a9542093b14870224ca085a4fedc56304aeee1c2f06ce(
    *,
    content: builtins.str,
    id: builtins.str,
    sent_at: builtins.str,
    status: builtins.str,
    to: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa2d4015027c18549dff3d305605433dfdca504013c7fd0895520c8d64d08e82(
    *,
    content: builtins.str,
    to: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae2238e853b97085efa0eeb50f1ae5743eb32aef4c893315febce3916b070e41(
    *,
    content: builtins.str,
    to: builtins.str,
    text: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c864831bd2e2b101ffe29610161aa4af0bbf977f549ad7d06aa0ebf52393f333(
    *,
    content: builtins.str,
    to: builtins.str,
    caption: typing.Optional[builtins.str] = None,
    data: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ac045910aedce36eae36948cbdf9a304bd003e99462584d3b7756d264f15223(
    *,
    content: builtins.str,
    to: builtins.str,
    data: typing.Optional[builtins.str] = None,
    duration: typing.Optional[jsii.Number] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1d9acc660dd7af1a46bcbe0beab4ac7f79e0cb52e2e591c905cb18a2e402a31(
    *,
    mark_online: builtins.bool,
    store: typing.Union[NowebStoreConfig, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3504aad6bb01adf6b4e052cec8a4b4630e3f6d4463e67757a39a236969ffb0c8(
    *,
    enabled: builtins.bool,
    full_sync: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22a12ee180062e139189a9c2a4e37e712259928182668c5e31b5fb121268d73c(
    *,
    limit: typing.Optional[jsii.Number] = None,
    offset: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdcd7bfcdef1239ec09bf635d6cb80127869a5b47b64abce0e0077d71e52fc18(
    *,
    participants: typing.Sequence[builtins.str],
    notify: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a964f3f73efc5e8488da0bac80a171d233f4796182c0f6f6747cfb98e285554(
    *,
    url: builtins.str,
    crop_to_square: typing.Optional[builtins.bool] = None,
    format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__459a32ee7266a8c5463906dab80b39d592816aaf349c8bb0974bab94794ae2a6(
    *,
    url: builtins.str,
    dimensions: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    format: typing.Optional[builtins.str] = None,
    size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96354063aeb190a9953a739f8ddd730b166f0b989d0a398486425665f25137a3(
    *,
    data: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c51f8bb25ad6378d464bb3616f09efc647e7e0e3ea4b317af603825757af3deb(
    *,
    success: builtins.bool,
    message: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__857cddd5fe1274f4c8c1d5739156643ea6050e034b8e2931a6e7c4d8c7078993(
    *,
    days: typing.Optional[jsii.Number] = None,
    messages: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98004618b306ee3b99405ad13a11ba93b9108620a864642dce62c6eddd07efbb(
    *,
    success: builtins.bool,
    data: typing.Any = None,
    error: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d5c286a82ad51ebf302b12e832392238be9b9400c357ea5359a201d69ba37f5(
    *,
    session: builtins.str,
    to: builtins.str,
    audio_url: typing.Optional[builtins.str] = None,
    document_url: typing.Optional[builtins.str] = None,
    filename: typing.Optional[builtins.str] = None,
    image_url: typing.Optional[builtins.str] = None,
    mimetype: typing.Optional[builtins.str] = None,
    preview: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    text: typing.Optional[builtins.str] = None,
    video_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3bc536760d406c093d044345b6224c45408f03e06e559ccc19ccdc89f98d4d0(
    *,
    session: builtins.str,
    to: builtins.str,
    message_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4bda00ff00f4da8f5d020b9ae62f84aef28dfe5100c707bc597e0d613a8ca00(
    *,
    debug: builtins.bool,
    metadata: typing.Union[SessionMetadata, typing.Dict[builtins.str, typing.Any]],
    noweb: typing.Union[NowebConfig, typing.Dict[builtins.str, typing.Any]],
    proxy: typing.Any,
    webhooks: typing.Sequence[typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e3cdcf8dd89941a7ff518341872e1a93509aae9d708132cd86835fcac559df4(
    *,
    phone_number: builtins.str,
    session_name: builtins.str,
    enable_account_protection: typing.Optional[builtins.bool] = None,
    enable_message_logging: typing.Optional[builtins.bool] = None,
    enable_webhook: typing.Optional[builtins.bool] = None,
    webhook_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__596f395204ab95febe6f3697a1d4c0d5942a1dfe1e6f52a0af2b14e28390e61b(
    *,
    created_at: builtins.str,
    enable_account_protection: builtins.bool,
    enable_message_logging: builtins.bool,
    enable_webhook: builtins.bool,
    id: builtins.str,
    phone_number: builtins.str,
    session_name: builtins.str,
    unique_session_id: builtins.str,
    updated_at: builtins.str,
    user_id: builtins.str,
    webhook_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__253a32a9275ecf9e72bcf1f2b75cf11a6a77a921015a702c79b2bfc420b72ef5(
    *,
    downstream: typing.Union[DownstreamInfo, typing.Dict[builtins.str, typing.Any]],
    session: typing.Union[SessionDetails, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07c4740974554c0849a34dbedfa991994373e666f12451f52bdcd86b56796bfb(
    *,
    user_email: builtins.str,
    user_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00214282c14641108c81a775130df264580c07d52d42f8115a838ca3596d1bfa(
    *,
    enabled: builtins.bool,
    changed_at: typing.Optional[builtins.str] = None,
    changed_by: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a531353acb198b346ac710373ae9842a1a785cd44825751b6b68e6ae1312b900(
    *,
    subject: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb18d81c4798685e0c7d24fb90be1d9433e8a027998cb1588ca65befb16e2d53(
    *,
    content: builtins.str,
    from_me: builtins.bool,
    id: builtins.str,
    recipient: builtins.str,
    sender: builtins.str,
    status: builtins.str,
    timestamp: builtins.str,
    to: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1322fd26c65f22aed45b65186990bfd4e62fedc82adb7666f244dda382b4486(
    *,
    exists: builtins.bool,
    phone: builtins.str,
    jid: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d04492a423af28b395df4631b1e8504bfe332d323a4d844b1f74ffa6d0bc1bed(
    session_id: builtins.str,
    group_id: builtins.str,
    *,
    participants: typing.Sequence[builtins.str],
    notify: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99a95a59c1a3b4445f873f11ef6baffe53f6dd829735d4e9cbd963f5f4d03750(
    session_id: builtins.str,
    *,
    phone: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7729a3030ecbc268f6363fbf99c6f1e1bc24e714f8db5d7d265301b563adc021(
    session_id: builtins.str,
    *,
    name: builtins.str,
    participants: typing.Sequence[typing.Union[CreateGroupParticipant, typing.Dict[builtins.str, typing.Any]]],
    description: typing.Optional[builtins.str] = None,
    picture_url: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acd94bad66a6e473e68654c72f4f17951aaaf98b516f2fc2ae23525f4d19142d(
    session_id: builtins.str,
    group_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b81b617d22cf593cff9ddd2976e6f0737bcab6b6cbfd35d40b731b45e7f5210(
    session_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__139540a56d71cd0ce28d760b8121524e566176105230d2d10368e8c868a0b1bf(
    session_id: builtins.str,
    group_id: builtins.str,
    *,
    participants: typing.Sequence[builtins.str],
    notify: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e70a7c80e4d2ba1ecb16738c3c23397463440182d1920123fdecb98f03ea831f(
    session: builtins.str,
    *,
    limit: typing.Optional[jsii.Number] = None,
    offset: typing.Optional[jsii.Number] = None,
    sort_by: typing.Optional[builtins.str] = None,
    sort_order: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee7da13a77009acdddeff305e10a5db368f4c9cb074406c192bedc4057d9e8a6(
    session: builtins.str,
    chat_id: builtins.str,
    *,
    refresh: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__492c79af76a7bd8dac211d2193193c8d3e039fbf87cacce721f0b2ddc937ab8f(
    session: builtins.str,
    *,
    ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    limit: typing.Optional[jsii.Number] = None,
    offset: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d77ef7352da27ed2ec09684fca511169a5faff56a447a1ccf86cf980f7e1a460(
    session_id: builtins.str,
    *,
    contact_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f22d74965b45389836d7b39cb4b56ecdba92406c4bea6e9cdc5bec11546658a(
    session_id: builtins.str,
    *,
    contact_id: builtins.str,
    refresh: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12f47d2c48c79766fb1f65cf404cb9f5860981e8e13a359f33e05b426d780b7b(
    session_id: builtins.str,
    *,
    limit: typing.Optional[jsii.Number] = None,
    offset: typing.Optional[jsii.Number] = None,
    sort_by: typing.Optional[builtins.str] = None,
    sort_order: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8030276c85cb8c16e95e727aa18f585dca4407ab282e54c3fc14d5dca85b6ec8(
    session_id: builtins.str,
    group_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7e034eb5f212f98a6ac3e0971b4320d19293a250557ded9fdbdc62d2f093d52(
    session_id: builtins.str,
    group_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2e46ec9091dbb97e1a93d52648d33e2341ce3c91e90c3a2add13403799eaa27(
    session_id: builtins.str,
    group_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c931f18445ef721ad90f49d0e44558dca33ffaa85d023870f59d3d56755e94cc(
    session_id: builtins.str,
    code: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81f7b2f48b68ce43a72907022490663f7a361147617503ccb0f1a31b9f28e0a7(
    session_id: builtins.str,
    group_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fdbed9bcbb62155a20fb7bbaa0dfde2143ac26d926c271859d4c28c5d34ff46(
    session_id: builtins.str,
    group_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e87990fa3a3febaa8547346458de3d6a592f085fb6619b4eb52c8d898718e96(
    session_id: builtins.str,
    group_id: builtins.str,
    refresh: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79e446fdce747cc36adaedf856e4febf5056e6bc7178859337a491a0110da4b7(
    session_id: builtins.str,
    *,
    exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    limit: typing.Optional[jsii.Number] = None,
    offset: typing.Optional[jsii.Number] = None,
    search: typing.Optional[builtins.str] = None,
    sort_by: typing.Optional[builtins.str] = None,
    sort_order: typing.Optional[builtins.str] = None,
    status: typing.Optional[GroupStatus] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b67c9b6e5d06ffdbdb23ed7573a858300956858942ea8657bf86b82f9caa4602(
    session_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cb1dc5792b15a5416b556e58d46fc39554d89dbc043723fca120ccd8c6d7a24(
    message_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dab9c1728004f37a8f1acdb766ca2064a65defb623b014815c34b01b45f8c11a(
    session: builtins.str,
    chat_id: builtins.str,
    message_id: builtins.str,
    *,
    download_media: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0bc5589803a84f85c893d759095ed8bdc83708c0e3255e8fde94e29f184ed03(
    session: builtins.str,
    chat_id: builtins.str,
    *,
    limit: jsii.Number,
    download_media: typing.Optional[builtins.bool] = None,
    filter: typing.Optional[typing.Union[GetMessagesFilterOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    offset: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1ce14e57c07700725ac03b1625ae7b1dd49be5322a3f62315ddb9b5d8b073e0(
    session_id: builtins.str,
    *,
    code: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad558ece6289316cb6c96cbcd2874d636299d55acf6b5001971b29a88534d99a(
    session_id: builtins.str,
    group_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c363ed8cf42447ba6ef57176faadd0997865f1533903ed8de24df601d5990f0(
    request: typing.Union[SendRequest, typing.Dict[builtins.str, typing.Any]],
    options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf8386881c4864c8999a84821ec8b8c63f8c21174180d155609c8fe66a7634cc(
    session_id: builtins.str,
    group_id: builtins.str,
    *,
    participants: typing.Sequence[builtins.str],
    notify: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40124cbc6cbf96cfa9e9d1ad29d0370d746bcf4314f15f715c91af9923b664d6(
    session: builtins.str,
    chat_id: builtins.str,
    *,
    days: typing.Optional[jsii.Number] = None,
    messages: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf96f551c9495cee95efea4f156c3cd3a914cde297e48549cd3589aac13a77c7(
    session_id: builtins.str,
    group_id: builtins.str,
    *,
    participants: typing.Sequence[builtins.str],
    notify: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__434c60505ee2fb2a5457c0dbf03cd3dfeaefd14bed60b513aaefc899f45188c2(
    session_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28c5d954ff13b65e026a7d45c6cb568a11d7bcc2d8c09e6c7e2b6d6364b1104c(
    session_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0df4545c26c4a54c2feea4d8159760885691ec730352cae801811b0e3276ec21(
    session_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57a4ef47ff269e952b181227322868fa3ed5b2390aab0831ded042080bbdbbe3(
    session_id: builtins.str,
    group_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d996da125e7066eec8c63ab6217f55bcfdb9750a7dfac528a8dfdb665cdcb06(
    session_id: builtins.str,
    group_id: builtins.str,
    *,
    description: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01f992487d1068e66a04e21b3f6a815a82a56176d0da3ef12c2d9afe82c7d339(
    session_id: builtins.str,
    group_id: builtins.str,
    *,
    enabled: builtins.bool,
    changed_at: typing.Optional[builtins.str] = None,
    changed_by: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d04e5287c8d30def6a53429e00e5612221a56fd49e7e2946d77a68bd1309b70a(
    session_id: builtins.str,
    group_id: builtins.str,
    *,
    enabled: builtins.bool,
    changed_at: typing.Optional[builtins.str] = None,
    changed_by: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97881afa91799d88ce91f801dd54ffd039ecfdf3c4cffaabcd56350b0208268b(
    session_id: builtins.str,
    group_id: builtins.str,
    *,
    url: builtins.str,
    crop_to_square: typing.Optional[builtins.bool] = None,
    format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13d698cfe11326ad055a7380a45198a7063790bb0d9f383ddcb6e310349857fa(
    session_id: builtins.str,
    group_id: builtins.str,
    *,
    subject: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa7a8584f39c683cf7a8b0b493cff8b738a07457858bf3cd19b6c31a06e322f5(
    session_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90776ed81605470091e6ac1e31d09ac72b2c7b36b5504d37ae9ba1995f67c193(
    session_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c206f9f03c1e9230f7c6c5569fcc5de78f0c947a9e73ad39ca3b1ff4c771d2c(
    *,
    api_key: builtins.str,
    base_url: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6abbc9d87deb2b837793c948e1cf709fe5599235bd5573df1224f4163f2401ad(
    *,
    base_url: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eec89eaaa50e420d927618815b182bd6b5ce4b4a016f10a5e4b0ccc37fc905be(
    phone_number: builtins.str,
    country_code: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f3e44e026e6ad10ba5cef7676e8b8f792085bec1680d62137a198b09822712a(
    phone_number: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8373abf07139df0e10a00cd6fa9e4241e31eeb1c4b95d5c6cbacef4eb6760e68(
    *,
    content: builtins.str,
    to: builtins.str,
    file_name: builtins.str,
    mime_type: builtins.str,
    data: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f4feac6a3f3e2263ff153c7a829e0045b7fcfb529a99b0e512e54b7f5974c0e(
    *,
    content: builtins.str,
    to: builtins.str,
    caption: typing.Optional[builtins.str] = None,
    data: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ebbbe9d645bc5355f122d8a16cc77dc5abbf89d380f119db914ef148786df20(
    *,
    content: builtins.str,
    to: builtins.str,
    text: builtins.str,
    preview: typing.Union[LinkPreviewRequest, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3d85e74d62c2d977dab7cc527e9efb8b60c3e669b984e32b30b46f61ca261fa(
    *,
    created_at: builtins.str,
    enable_account_protection: builtins.bool,
    enable_message_logging: builtins.bool,
    enable_webhook: builtins.bool,
    id: builtins.str,
    phone_number: builtins.str,
    session_name: builtins.str,
    unique_session_id: builtins.str,
    updated_at: builtins.str,
    user_id: builtins.str,
    webhook_url: typing.Optional[builtins.str] = None,
    config: typing.Union[SessionConfig, typing.Dict[builtins.str, typing.Any]],
    engine: typing.Union[EngineStatus, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    status: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
