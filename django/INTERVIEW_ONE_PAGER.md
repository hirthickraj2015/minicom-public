# MINICOM INTERVIEW - ONE-PAGE CHEAT SHEET
## Print This & Keep It Beside You!

---

## ⏱️ TIME MANAGEMENT

| Phase | Time | MUST DO |
|-------|------|---------|
| **Setup** | 15m | ✅ Server running ✅ Both clients tested ✅ Asked clarifying questions |
| **Solo** | 45m | 0-25m: Requirement 1 DONE<br>25-40m: 2-3 features from Req 2<br>40-45m: TEST & CLEAN |
| **Pairing** | 45m | ✅ Demo (2m) ✅ Discuss next steps ✅ Narrate constantly ✅ Collaborate |
| **Wrap Up** | 15m | ✅ Demo (5m) ✅ Future improvements (7m) ✅ Reflection (3m) |

---

## 💬 COMMUNICATION TEMPLATES

### Starting Tasks
- "Let me start by..."
- "My approach would be..."
- "I'm thinking we could..."

### Asking for Input
- "What do you think about...?"
- "Does this make sense?"
- "Am I on the right track?"

### Receiving Feedback
- "Good point! Let me try that."
- "I hadn't thought of that. Let's do it."
- "Can you explain why that's better?"

### When Stuck
- "This is tricky. Mind if we look at this together?"
- "Let me check the docs quickly..."

---

## 🎯 SOLO SESSION PRIORITIES

**First 25 minutes - Requirement 1** (MUST COMPLETE):
1. WebSocket consumer (connect, disconnect, receive)
2. Frontend WebSocket connection
3. Send/receive messages
4. Show username + timestamp
5. **TEST IT WORKS!**

**Next 15 minutes - Pick 2-3 features**:
- ⭐ **Typing Indicator** (8 min, easy, impressive)
- ⭐ **Message History** (10 min, shows DB knowledge)
- ⭐ **User Presence** (7 min, good UX)

**Last 5 minutes**:
- Test everything again
- Remove console.logs
- Add comments to complex code

---

## 🤝 PAIRING SESSION DO's & DON'Ts

### ✅ DO
- Think out loud CONSTANTLY
- Ask "What do you think?" at decision points
- Say "Good catch!" when they spot issues
- Admit when you don't know something
- Test after each change
- Take their suggestions seriously

### ❌ DON'T
- Code silently for >1 minute
- Argue with suggestions
- Make excuses for bugs
- Say "I know" repeatedly
- Skip testing
- Over-engineer

---

## 🎤 DEMO SCRIPT (Use This!)

> "Let me show you what we built..."

**1. Core (30 sec)**:
"Two-way messaging works in real-time"
→ Send from Client1 → appears in both

**2. Feature 1 (30 sec)**:
"Typing indicators show when someone is typing"
→ Start typing → show indicator

**3. Feature 2 (30 sec)**:
"Messages persist and reload from database"
→ Refresh page → messages reappear

**4. Architecture (30 sec)**:
"Using Django Channels + WebSockets + SQLite"

**5. Collaboration (30 sec)**:
"During pairing, [Engineer] suggested [X] which improved [Y]"

---

## 🚀 FUTURE IMPROVEMENTS (Memorize These!)

### Short-term (Quick Wins):
- Error handling + auto-reconnect
- XSS protection (escape HTML)
- Input validation
- Better CSS styling

### Medium-term (Features):
- User authentication
- Multiple chat rooms
- Read receipts
- File/image sharing

### Long-term (Scale):
- Redis channel layer (multi-server)
- PostgreSQL (better concurrency)
- Load balancer + sticky sessions
- Caching (reduce DB load)
- Monitoring (Prometheus/Grafana)

---

## 🔍 KEY FILES (Know What Each Does)

| File | Purpose | Key Point |
|------|---------|-----------|
| `asgi.py` | WebSocket entry | Routes connections to consumers |
| `routing.py` | WS URL routing | Maps `/ws/chat/` → `ChatConsumer` |
| `consumers.py` | **MAIN FILE** | All WebSocket logic lives here |
| `models.py` | Database schema | Message table (username, content, timestamp) |
| `settings.py` | Config | Enables Channels, sets channel layer |

---

## 🐛 COMMON ERRORS & FIXES

**WebSocket won't connect**:
```javascript
// Check URL format
ws://localhost:3000/ws/chat/general/
```

**Messages not broadcasting**:
```python
# Check you called group_add in connect()
await self.channel_layer.group_add(
    self.room_group_name,
    self.channel_name
)
```

**Database error**:
```bash
# Reset database
rm django/db.sqlite3
python manage.py migrate
```

---

## 📊 MESSAGE FLOW (Memorize This!)

```
User types "Hello"
  ↓
JS: chatSocket.send()
  ↓
Daphne receives WebSocket frame
  ↓
ChatConsumer.receive() parses JSON
  ↓
Consumer saves to database (async)
  ↓
Consumer broadcasts via group_send()
  ↓
All consumers receive it
  ↓
Each consumer's chat_message() called
  ↓
consumer.send() → WebSocket → Browser
  ↓
JavaScript displays in UI
```

---

## 🎯 WRAP-UP QUESTIONS YOU'LL GET

**"How did you find the pairing session?"**
> "I really enjoyed it! I particularly liked when you suggested [X].
> I hadn't thought about [Y]. If I did it again, I'd [improvement].
> Overall a great experience."

**"What was most challenging?"**
> "Prioritizing which features to build in 45 minutes. I focused on
> typing indicators and message history because they showcase
> different aspects - real-time events and DB persistence."

**"How would you scale this?"**
> "For 1M users: Redis cluster, 100+ servers, PostgreSQL replicas,
> caching, load balancer, monitoring. Estimated $10k/month on AWS."

---

## 🚨 RED FLAGS TO AVOID

- ❌ Coding silently (talk constantly!)
- ❌ Not testing until the end
- ❌ Arguing with engineer
- ❌ Getting defensive about bugs
- ❌ Making excuses
- ❌ Never asking questions
- ❌ Trying to build everything
- ❌ Over-engineering

---

## ✅ GREEN FLAGS TO SHOW

- ✅ Think out loud
- ✅ Test frequently
- ✅ Ask thoughtful questions
- ✅ Listen to feedback
- ✅ Admit what you don't know
- ✅ Show curiosity
- ✅ Prioritize working code
- ✅ Keep it simple

---

## 🎓 QUICK TECHNICAL ANSWERS

**"Why WebSockets?"**
> "Bidirectional real-time communication. HTTP is request-response
> (high latency, polling wastes bandwidth). WebSockets maintain
> persistent connection - both sides can send anytime."

**"Why async?"**
> "Non-blocking. One thread handles 10,000 connections by switching
> between them while they wait (I/O). Sync blocks = need 10,000 threads."

**"What's the channel layer?"**
> "Message bus for pub/sub. When one consumer sends to a group,
> channel layer delivers to all consumers in that group. Like
> broadcasting. Using in-memory for dev, would use Redis for production."

**"Why database_sync_to_async?"**
> "Django ORM is sync (blocking). This decorator runs it in a thread
> pool, keeping the async event loop free for other connections."

---

## 🧠 MINDSET REMINDERS

### They Want You to Succeed
- Not trying to trick you
- Want to see if you can collaborate
- Interested in how you think, not just what you know

### It's Okay to Not Know
- "I haven't used X, but it's similar to Y"
- "Let me look that up quickly"
- "I'm not sure - what's your thinking?"

### Balance
- ⚖️ Confident but humble
- ⚖️ Independent but collaborative
- ⚖️ Fast but thorough
- ⚖️ Talking but also listening

---

## 📝 BEFORE YOU START

### Check These:
- [ ] Server runs: `bash script/django/start`
- [ ] Both clients load and can chat
- [ ] Browser DevTools work (F12)
- [ ] You have water nearby
- [ ] Notifications are OFF

### Mental Preparation:
- Take 3 deep breaths
- Remember: This is a conversation, not an interrogation
- They're a future colleague, not an adversary
- Show them the real you!

---

## 🎯 THE SECRET FORMULA

**1. Communicate** - Narrate your thinking
**2. Collaborate** - Ask for input, take feedback
**3. Code** - Simple, working > complex, broken
**4. Clean** - Test, refactor, comment
**5. Conclude** - Demo well, discuss improvements

---

## 💪 LAST WORDS

**You have**:
✅ A working app
✅ Deep technical understanding
✅ Communication templates
✅ Time management strategy
✅ This cheat sheet!

**Remember**:
- Think out loud
- Test constantly
- Ask questions
- Stay positive
- Be yourself

**YOU'VE GOT THIS!** 🚀
