# Quick Start Guide

## Fixed Issues for Django 2.2.13 Compatibility

The application has been tested and verified to work with Django 2.2.13. The following compatibility fixes were made:

1. **ASGI Configuration**: Updated `asgi.py` to work with Django 2.2 (removed `get_asgi_application` which is only available in Django 3.0+)
2. **WebSocket Routing**: Fixed `routing.py` to use Channels 2.x syntax (removed `.as_asgi()` which is only in Channels 3.x)
3. **Import Order**: Fixed import order to call `django.setup()` before importing from Django/Channels modules

## Start the Application

### Step 1: Setup (First Time Only)

```bash
bash script/django/setup
```

This will:
- Create a Python 3.9 virtual environment
- Install all dependencies (Django, Channels, etc.)
- Run database migrations
- Create the SQLite database

### Step 2: Start the Server

```bash
bash script/django/start
```

The server will start at: **http://localhost:3000**

You should see output like:
```
Starting server at tcp:port=3000:interface=0.0.0.0
HTTP/2 support not enabled (install the http2 and tls Twisted extras)
Configuring endpoint tcp:port=3000:interface=0.0.0.0
Listening on TCP address 0.0.0.0:3000
```

### Step 3: Test the Application

Open these URLs in your browser:

1. **Landing Page**: http://localhost:3000/
2. **Client 1**: http://localhost:3000/client1/ (open in one tab/window)
3. **Client 2**: http://localhost:3000/client2/ (open in another tab/window)

### Step 4: Chat!

- Type a message in Client 1 and press Enter or click Send
- Watch it appear instantly in Client 2
- Try typing to see the typing indicator
- Watch the user presence badges update when clients connect
- Refresh the page to see message history persist

## Verified Features

✅ **Real-time bidirectional messaging** - Messages sync instantly between clients
✅ **Typing indicators** - See when the other person is typing (with animated dots)
✅ **Message history** - Last 50 messages load when you open the page
✅ **User presence** - See who's online with badges
✅ **Connection status** - Green/red indicator shows connection state
✅ **Auto-reconnection** - Automatically reconnects if connection drops
✅ **XSS protection** - All user input is properly escaped
✅ **Beautiful UI** - Modern gradient design with smooth animations

## Troubleshooting

### Port Already in Use

If you get "Address already in use" error:

```bash
# Find the process using port 3000
lsof -ti:3000 | xargs kill -9

# Then start the server again
bash script/django/start
```

### WebSocket Connection Fails

Make sure you're using Daphne (ASGI server), not Django's runserver. The start script handles this automatically.

### Browser Console Errors

Open browser DevTools (F12) → Console tab to see detailed WebSocket connection logs.

## Technical Details

- **Server**: Daphne ASGI server (required for WebSockets)
- **Backend**: Django 2.2.13 + Django Channels 2.4.0
- **Database**: SQLite (automatic, no setup required)
- **Channel Layer**: In-memory (no Redis required for this demo)
- **Frontend**: Vanilla JavaScript + WebSocket API

## Next Steps

See the main README.md for:
- Detailed architecture explanation
- Room for improvement
- API documentation
- Production deployment tips
