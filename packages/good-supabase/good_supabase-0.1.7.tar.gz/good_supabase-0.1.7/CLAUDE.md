# Good Supabase Library

Supabase client wrapper with dependency injection support, providing easy integration with FastAPI and other frameworks.

## Package Overview

good-supabase wraps the official Supabase Python client with fast_depends providers for dependency injection. It includes support for authentication, database operations, storage, and realtime subscriptions.

## Key Components

### Clients (`_client.py`)
- `Supabase`: Synchronous client wrapper
- `SupabaseAsync`: Asynchronous client wrapper
- `SupabaseProvider`/`SupabaseAsyncProvider`: Dependency injection providers
- Automatic retry logic with tenacity
- Configurable timeouts and error handling

### Authentication (`_auth.py`)
- Google OAuth callback handler
- Token management
- User session handling

### Realtime (`_realtime.py`)
- WebSocket connection management
- Channel subscriptions
- Presence and broadcast support

## Usage Examples

### Basic Setup
```python
from good_supabase import SupabaseAsyncProvider
from fast_depends import inject

@inject
async def get_users(
    supabase: SupabaseAsync = SupabaseAsyncProvider(
        url="https://project.supabase.co",
        key="your-anon-key"
    )
):
    response = await supabase.table("users").select("*").execute()
    return response.data
```

### Database Operations
```python
# Insert data
user = {
    "email": "user@example.com",
    "name": "John Doe",
    "created_at": datetime.now().isoformat()
}
await supabase.table("users").insert(user).execute()

# Query with filters
active_users = await (
    supabase.table("users")
    .select("id, name, email")
    .eq("active", True)
    .order("created_at", desc=True)
    .limit(10)
    .execute()
)

# Update data
await (
    supabase.table("users")
    .update({"last_login": datetime.now().isoformat()})
    .eq("id", user_id)
    .execute()
)

# Delete data
await supabase.table("users").delete().eq("id", user_id).execute()
```

### Storage Operations
```python
# Upload file
with open("image.jpg", "rb") as f:
    await supabase.storage.from_("avatars").upload(
        path=f"users/{user_id}/avatar.jpg",
        file=f,
        file_options={"content-type": "image/jpeg"}
    )

# Get public URL
url = supabase.storage.from_("avatars").get_public_url(
    f"users/{user_id}/avatar.jpg"
)

# Download file
data = await supabase.storage.from_("avatars").download(
    f"users/{user_id}/avatar.jpg"
)

# List files
files = await supabase.storage.from_("avatars").list(
    path=f"users/{user_id}"
)
```

### Authentication
```python
# Sign up
auth_response = await supabase.auth.sign_up({
    "email": "user@example.com",
    "password": "secure-password"
})

# Sign in
auth_response = await supabase.auth.sign_in_with_password({
    "email": "user@example.com", 
    "password": "secure-password"
})

# Get current user
user = supabase.auth.get_user()

# Sign out
await supabase.auth.sign_out()
```

### Google OAuth
```python
from good_supabase.auth import handle_google_callback

# In your OAuth callback route
async def google_callback(code: str):
    tokens = await handle_google_callback(
        supabase_client=supabase,
        google_client_id=GOOGLE_CLIENT_ID,
        google_client_secret=GOOGLE_CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        code=code
    )
    return tokens
```

### Realtime Subscriptions
```python
# Subscribe to changes
channel = supabase.channel("room:123")

# Listen for all changes
channel.on(
    event="*",
    schema="public", 
    table="messages",
    callback=lambda payload: print(f"Change: {payload}")
)

# Listen for inserts only
channel.on(
    event="INSERT",
    schema="public",
    table="messages", 
    callback=lambda payload: print(f"New message: {payload}")
)

# Subscribe to channel
await channel.subscribe()

# Broadcast to channel
await channel.send({
    "type": "broadcast",
    "event": "message",
    "payload": {"text": "Hello!"}
})

# Unsubscribe
await supabase.remove_channel(channel)
```

### Pydantic Models
```python
from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    id: int
    email: str
    name: str
    created_at: datetime
    active: bool = True

# Use with type safety
response = await supabase.table("users").select("*").execute()
users = [User(**row) for row in response.data]
```

### Advanced Queries
```python
# Complex filters
results = await (
    supabase.table("posts")
    .select("*, author:users(name, email)")
    .eq("published", True)
    .in_("category", ["tech", "science"])
    .gte("created_at", "2024-01-01")
    .order("views", desc=True)
    .range(0, 9)  # Pagination
    .execute()
)

# RPC calls
result = await supabase.rpc(
    "calculate_total",
    {"user_id": 123, "date_from": "2024-01-01"}
).execute()

# Upsert
await supabase.table("users").upsert({
    "email": "user@example.com",
    "name": "Updated Name"
}, on_conflict="email").execute()
```

## Configuration

### Environment Variables
```python
import os

supabase = SupabaseAsyncProvider(
    url=os.getenv("SUPABASE_URL"),
    key=os.getenv("SUPABASE_ANON_KEY"),
    options={
        "schema": "custom_schema",  # Default: "public"
        "headers": {
            "x-custom-header": "value"
        },
        "auto_refresh_token": True,
        "persist_session": True
    }
)
```

### Custom Timeout
```python
# Configure PostgREST timeout
supabase = SupabaseAsyncProvider(
    url=url,
    key=key,
    timeout=30  # seconds
)
```

### Retry Configuration
The client automatically retries failed requests using tenacity:
- Exponential backoff
- Retry on network errors
- Configurable retry attempts

## Error Handling

```python
from postgrest.exceptions import APIError

try:
    response = await supabase.table("users").select("*").execute()
except APIError as e:
    print(f"API Error: {e.message}")
    print(f"Details: {e.details}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Best Practices

1. Use async client for better performance
2. Implement proper error handling
3. Use Pydantic models for type safety
4. Configure appropriate timeouts
5. Use RLS (Row Level Security) policies
6. Cache Supabase client instances
7. Handle auth token refresh

## Testing

When testing, mock the Supabase client:
```python
from unittest.mock import AsyncMock

mock_supabase = AsyncMock()
mock_supabase.table.return_value.select.return_value.execute.return_value = {
    "data": [{"id": 1, "name": "Test"}]
}
```

## Dependencies

- `supabase`: Official Supabase client
- `postgrest`: PostgREST client
- `tenacity`: Retry logic
- `good-common`: Shared utilities
- `fast-depends`: Dependency injection