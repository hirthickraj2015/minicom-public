# Interview Cheat Sheet - Quick Reference

## 30-Second System Overview

**What we built**: Real-time bidirectional chat using Django Channels + WebSockets

**Tech stack**: Django 2.2 + Channels 2.4 + SQLite + Vanilla JS + Daphne (ASGI server)

**Key features**: Real-time messaging, typing indicators, message history, user presence

---

## Critical Files (What Each Does)

| File | Purpose | Key Point to Remember |
|------|---------|----------------------|
| `asgi.py` | WebSocket entry point | Routes WebSocket connections to consumers |
| `routing.py` | WebSocket URL routing | Maps `/ws/chat/room/` → `ChatConsumer` |
| `consumers.py` | WebSocket handler | **MOST IMPORTANT** - all chat logic here |
| `models.py` | Database schema | Stores messages with username, content, timestamp |
| `settings.py` | Configuration | Enables Channels, sets channel layer (in-memory) |
| `views.py` | HTTP endpoints | Serves HTML pages (client1.html, client2.html) |
| `urls.py` | HTTP URL routing | Maps `/client1/` → `views.client1` |

---

## Message Flow (Memorize This!)

```
1. User types "Hello" in browser
   ↓
2. JavaScript: chatSocket.send({type: 'chat_message', message: 'Hello'})
   ↓
3. WebSocket → Daphne (ASGI server)
   ↓
4. Daphne → ChatConsumer.receive()
   ↓
5. Consumer saves to database (async)
   ↓
6. Consumer broadcasts via channel_layer.group_send()
   ↓
7. All consumers in group receive it
   ↓
8. Each consumer's chat_message() method called
   ↓
9. consumer.send() → WebSocket → Browser
   ↓
10. JavaScript displays message in UI
```

**Total time**: 10-50ms

---

## Key Concepts to Explain

### 1. Why WebSockets?

**Wrong answer**: "Because they're real-time"

**Right answer**:
"HTTP is request-response (client must ask for updates). For chat, we need the server to push updates instantly. WebSockets provide a persistent bidirectional connection, allowing both client and server to send messages anytime. The alternative would be polling (client asking every second 'any updates?') which is inefficient - wastes bandwidth and has high latency."

---

### 2. What's a Channel Layer?

**Wrong answer**: "It's for messaging"

**Right answer**:
"The channel layer is a message broker (like pub/sub) that allows different parts of the application to communicate. When a user sends a message, their consumer broadcasts it to a 'group' (all users in that room). The channel layer delivers it to every consumer in that group. Think of it as a message bus.

We use **in-memory** for development (simple, no setup) but would use **Redis** in production for multi-server scaling."

---

### 3. Async vs Sync?

**Wrong answer**: "Async is faster"

**Right answer**:
"Async is non-blocking. When you `await` a database query, Python can switch to handling other requests while waiting. This allows one thread to handle thousands of concurrent WebSocket connections.

Sync blocks the thread - if you have 1000 connections and each waits 100ms for database, you need 1000 threads. Async lets one thread handle all 1000 by switching between them when they're waiting."

**Real-world analogy**:
- Sync = You call a restaurant and wait on hold
- Async = You call, they say "we'll call back", you do other things

---

### 4. Why database_sync_to_async?

**Wrong answer**: "To make database async"

**Right answer**:
"Django ORM is synchronous (blocking). If we call it directly in an async function, it blocks the entire event loop. The `@database_sync_to_async` decorator runs the blocking ORM code in a thread pool, keeping the event loop free to handle other connections."

---

## Code Snippets to Know

### 1. How to Join a Group

```python
async def connect(self):
    self.room_group_name = 'chat_general'

    # Add this connection to the group
    await self.channel_layer.group_add(
        self.room_group_name,
        self.channel_name  # Unique ID for this connection
    )

    await self.accept()  # Accept WebSocket connection
```

---

### 2. How to Broadcast a Message

```python
# Send to all in group
await self.channel_layer.group_send(
    self.room_group_name,
    {
        'type': 'chat_message',  # Calls self.chat_message() on each consumer
        'message': {
            'username': 'Alice',
            'content': 'Hello!'
        }
    }
)
```

---

### 3. How to Handle Broadcast

```python
async def chat_message(self, event):
    """Called by channel layer when group_send happens"""
    # Send to this client's WebSocket
    await self.send(text_data=json.dumps({
        'type': 'chat_message',
        'message': event['message']
    }))
```

---

### 4. Database Query (Async Safe)

```python
@database_sync_to_async
def save_message(self, username, content, room):
    msg = Message.objects.create(
        username=username,
        content=content,
        room=room
    )
    return msg.to_dict()

# Usage:
saved_msg = await self.save_message('Alice', 'Hello', 'general')
```

---

## Interview Questions You'll Get

### Q: "What if one server crashes?"

**Answer**:
"Currently, we're single-server, so it's a single point of failure. For production:

1. **Load balancer** (nginx) distributes traffic across multiple servers
2. **Redis channel layer** so servers can communicate
3. **Database with replicas** for high availability
4. **Health checks** - load balancer only sends traffic to healthy servers
5. **Graceful shutdown** - drain connections before restart

Result: No downtime even if one server crashes."

---

### Q: "How do you scale to 1 million users?"

**Answer**:
"Current architecture supports ~10,000 concurrent users (single server). For 1 million:

**Horizontal scaling**:
- 100 application servers (10k connections each)
- Redis Cluster for channel layer
- PostgreSQL with read replicas
- CDN for static assets

**Cost**: ~$10k/month on AWS

**Optimizations**:
- Cache message history in Redis (reduce DB load)
- Compress WebSocket messages (reduce bandwidth)
- Geographic distribution (lower latency)
- Message queue for async tasks"

---

### Q: "How do you prevent XSS attacks?"

**Answer**:
"Cross-Site Scripting is when malicious JavaScript gets executed. For example:

**Attack**: User sends `<script>alert('HACKED')</script>`

**Without protection**: Browser executes the script ❌

**With protection**: We escape HTML before rendering ✅
```javascript
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;  // Auto-escapes
    return div.innerHTML;
}
```

**Result**: `<script>` becomes `&lt;script&gt;` (harmless text)"

---

### Q: "What if the database is slow?"

**Answer**:
"Database performance is critical. Solutions:

**1. Indexing**
```python
class Meta:
    indexes = [
        models.Index(fields=['room', '-timestamp'])
    ]
```
Speeds up queries by 100-1000x

**2. Caching**
- Cache last 50 messages in Redis
- 60-second TTL (time to live)
- First request: 50ms (database)
- Cached requests: 0.5ms (Redis)

**3. Connection pooling**
- Reuse database connections
- Avoid overhead of creating new connections

**4. Read replicas**
- Write to primary database
- Read from replicas (distribute load)

**5. Query optimization**
- Use `select_related()` to avoid N+1 queries
- Use `only()` to fetch only needed fields"

---

## Design Decisions (Know Why!)

| Decision | Why This Choice | Alternative | Trade-off |
|----------|-----------------|-------------|-----------|
| **WebSockets** | Bidirectional real-time | Polling | More complex but much better UX |
| **Django Channels** | Extends Django to WebSockets | Node.js | Steeper learning curve but consistent stack |
| **In-memory channel layer** | No external dependencies | Redis | Can't scale horizontally, but simpler |
| **SQLite** | Zero configuration | PostgreSQL | Not for production, but great for dev |
| **Vanilla JS** | No build step, simple | React | Less features but faster load time |
| **AsyncWebsocketConsumer** | High concurrency | Sync consumer | More complex but 100x better performance |

---

## Numbers to Know (Impress Interviewers!)

| Metric | Value | Context |
|--------|-------|---------|
| WebSocket message latency | 10-50ms | Local network |
| HTTP request latency | 100-200ms | Includes connection overhead |
| Max connections (async) | ~10,000 | Per server, single thread |
| Max connections (sync) | ~100 | Per server, one thread per connection |
| Database query (indexed) | 1-10ms | Fast |
| Database query (no index) | 100-1000ms | 100x slower! |
| Redis cache hit | 0.5ms | Very fast |
| WebSocket frame overhead | ~2 bytes | Very efficient |
| HTTP request overhead | ~500 bytes | Headers add weight |

---

## Common Mistakes to Avoid

### ❌ Mistake 1: Blocking in Async
```python
async def receive(self):
    msg = Message.objects.create(...)  # BLOCKS event loop!
```

### ✅ Fix:
```python
async def receive(self):
    msg = await self.save_message(...)  # Non-blocking
```

---

### ❌ Mistake 2: No Error Handling
```python
await self.channel_layer.group_send(...)  # What if it fails?
```

### ✅ Fix:
```python
try:
    await self.channel_layer.group_send(...)
except Exception as e:
    logger.error(f"Failed to broadcast: {e}")
    # Fallback logic
```

---

### ❌ Mistake 3: Not Escaping HTML
```javascript
messageDiv.innerHTML = message.content;  // XSS vulnerability!
```

### ✅ Fix:
```javascript
messageDiv.innerHTML = escapeHtml(message.content);  // Safe
```

---

## Key Phrases to Use

### Show System Thinking:
- "I considered three approaches: A, B, and C. I chose B because..."
- "The trade-off is X, but I think it's worth it because Y"
- "For this prototype, I used X. For production, I'd use Y because..."

### Show You Understand Scale:
- "This handles ~10,000 concurrent users. To scale to 1 million, we'd need..."
- "Current latency is 50ms. We could reduce it to 10ms by..."
- "I'd add monitoring with Prometheus to track connections/sec, message latency, and error rates"

### Show You Understand Security:
- "I escaped all user input to prevent XSS attacks"
- "For production, I'd add authentication using JWT tokens"
- "We'd need rate limiting to prevent DoS attacks - max 10 connections per IP"

---

## The "Secret Sauce" Answer Template

When asked "Why did you choose X?", use this structure:

1. **Context**: "For a real-time chat application, we need..."
2. **Options**: "I evaluated three approaches: A, B, C"
3. **Analysis**:
   - "A was simple but has latency issues"
   - "B was powerful but overkill for our needs"
   - "C was the sweet spot - real-time with reasonable complexity"
4. **Decision**: "I chose C because..."
5. **Trade-offs**: "The downside is X, but I accept that because Y"
6. **Future**: "If requirements change to Z, I'd reconsider A"

**Example**:
"For real-time chat, we need instant message delivery. I evaluated three approaches:

1. **Polling**: Client asks server every second for updates
   - ✅ Simple to implement
   - ❌ High latency (up to 1 second)
   - ❌ Wastes bandwidth

2. **Server-Sent Events**: Server pushes to client
   - ✅ Real-time
   - ❌ One-way only (client still needs HTTP POST)

3. **WebSockets**: Bidirectional persistent connection
   - ✅ Real-time, both directions
   - ✅ Efficient (one connection)
   - ❌ More complex to implement

I chose WebSockets because bidirectional communication is essential for chat. The trade-off is increased complexity (need ASGI server, channel layer), but the performance benefits justify it. If we only needed server→client updates (like a stock ticker), I'd reconsider SSE for simplicity."

---

## Last-Minute Review (5 minutes before interview)

1. **Architecture**: Browser → WebSocket → Daphne → ChatConsumer → Channel Layer → Database
2. **Message flow**: User types → JS send → Consumer receive → Database save → Broadcast → All clients
3. **Key files**: asgi.py (entry), consumers.py (logic), models.py (schema)
4. **Why WebSockets**: Bidirectional real-time (vs polling's high latency)
5. **Why async**: Non-blocking = high concurrency (10k connections vs 100)
6. **Scaling**: Add Redis channel layer + load balancer + multiple servers
7. **Security**: Escape HTML (XSS), add auth (CSRF), rate limit (DoS)

---

## Interview Success Formula

1. ✅ **Explain your thinking** - Don't just say what, say WHY
2. ✅ **Show trade-offs** - Every decision has pros/cons
3. ✅ **Think about scale** - What works for 10 users vs 1 million?
4. ✅ **Mention security** - XSS, CSRF, DoS, authentication
5. ✅ **Draw diagrams** - Visual learners (and interviewers) love this
6. ✅ **Ask clarifying questions** - "Are we optimizing for latency or simplicity?"
7. ✅ **Be honest** - "I don't know, but here's how I'd find out..."

---

## Red Flags to Avoid

- ❌ "I used it because it's popular"
- ❌ "I don't know" (without showing how you'd learn)
- ❌ Only talking about what you built (not why or alternatives)
- ❌ No mention of security
- ❌ No mention of error handling
- ❌ Saying "it's perfect" (everything has trade-offs!)

---

## Final Tip

**The interviewer wants to see**:
1. Can you make good technical decisions? (Why WebSockets?)
2. Can you explain trade-offs? (In-memory vs Redis)
3. Can you think about scale? (10 users → 1 million)
4. Can you write clean code? (Async, error handling)
5. Can you learn? ("I don't know X, but I know Y which is similar...")

You don't need to know everything. You need to show you can **think systematically** and **learn quickly**.

**Good luck! You've got this! 🚀**
