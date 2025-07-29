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
