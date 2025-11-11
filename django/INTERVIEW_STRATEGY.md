# Minicom Interview Strategy Guide
## Complete Playbook for Acing the 120-Minute Interview

---

## Interview Structure Overview

| Phase | Duration | What Happens | Your Goal |
|-------|----------|--------------|-----------|
| **Setup** | 15 mins | Environment setup, intro | Get everything working, ask clarifying questions |
| **Solo Task** | 45 mins | Code alone (Googling allowed) | Complete Requirement 1, start Requirement 2 |
| **Pairing** | 45 mins | Code with engineer | Show collaboration, finish features, discuss decisions |
| **Wrap Up** | 15 mins | Demo & discussion | Show what you built, discuss improvements |

**Total**: 120 minutes (2 hours)

---

## PRE-INTERVIEW PREPARATION (Do This Before!)

### Day Before Interview

#### 1. Practice the Setup Script
```bash
# Make sure you can run these without errors
cd /path/to/minicom-public
bash script/django/setup
bash script/django/start
```

**Test checklist**:
- ✅ Server starts without errors
- ✅ You can open http://localhost:3000/
- ✅ Client1 and Client2 load correctly
- ✅ Messages send between clients
- ✅ You know how to stop the server (Ctrl+C)

#### 2. Prepare Your Environment

**Have these ready**:
- ✅ IDE/editor with Django/Python syntax highlighting
- ✅ Browser with DevTools bookmarked (F12)
- ✅ Terminal with good font size (will be screen shared)
- ✅ Notepad/sticky notes for quick notes
- ✅ Water nearby (you'll be talking a lot!)

**Browser tabs to have open**:
1. Django Channels documentation: https://channels.readthedocs.io/
2. Django Models reference: https://docs.djangoproject.com/en/2.2/ref/models/
3. WebSocket JavaScript API: https://developer.mozilla.org/en-US/docs/Web/API/WebSocket
4. StackOverflow (will be searching here)

#### 3. Memorize the File Structure

```
django/minicom/
├── asgi.py         - WebSocket entry point
├── routing.py      - WebSocket URL routing
├── consumers.py    - WebSocket handlers (MAIN FILE)
├── models.py       - Database models
├── views.py        - HTTP views
├── urls.py         - HTTP URL routing
├── settings.py     - Configuration
└── templates/
    ├── index.html
    ├── client1.html
    └── client2.html
```

**Quick mental map**: "ASGI routes to consumers, consumers use models, templates are the frontend."

#### 4. Practice Talking Through Code

**Bad**: *Silently types for 5 minutes*

**Good**: "I'm going to add a typing indicator. First, I'll update the consumer to handle a new message type called 'typing'. Then I'll broadcast it to other clients, and finally update the frontend to display it."

**Practice saying out loud**:
- "Let me start by..."
- "The next step is..."
- "I'm thinking about..."
- "I want to test if..."

---

## PHASE 1: SETUP (15 Minutes)

### What Happens

- Engineer joins the call
- Introduces themselves and the interview structure
- Helps you get the environment running
- Explains the task requirements
- Answers setup questions

### Your Strategy

#### Step 1: Make a Great First Impression (First 2 minutes)

**Say this**:
> "Hi! I'm [Name], great to meet you. I'm excited about this exercise. I've prepared my development environment and I'm ready to go. Should I share my screen now?"

**Energy level**: Enthusiastic but not over-the-top. Show you're excited and prepared.

**Webcam**: Keep it on (builds rapport). Smile, make eye contact, nod when they talk.

#### Step 2: Listen Carefully to Requirements (5 minutes)

**Take notes on**:
- Must-have features (Requirement 1)
- Nice-to-have features (Requirement 2)
- Time allocations
- How to ask for help during solo time
- How the pairing session will work

**Good questions to ask**:
- ✅ "Just to confirm, Requirement 1 is the baseline, and I should implement at least 2 features from Requirement 2, correct?"
- ✅ "During the solo session, can I send you questions via chat, or should I save them for the pairing session?"
- ✅ "For the database, should I use migrations or is it okay to recreate the database?"
- ✅ "Are there any specific constraints on which libraries I can use?"

**Don't ask**:
- ❌ "What's the best approach?" (shows you can't make decisions)
- ❌ "Can you give me hints?" (wait for solo time to start)
- ❌ Super specific technical questions (save these for when you encounter them)

#### Step 3: Verify Environment (8 minutes)

**Checklist (say these out loud)**:

```bash
# 1. Clone/navigate to repository
cd minicom-public

# 2. Run setup
bash script/django/setup

# Say: "Running the setup script now..."
```

**While it's running**:
- ✅ Check if any errors appear
- ✅ Watch for successful migration messages
- ✅ Confirm virtual environment created

```bash
# 3. Start server
bash script/django/start

# Say: "Starting the server, should be available at localhost:3000..."
```

**Verify in browser**:
- ✅ Visit http://localhost:3000/ - "Landing page loads correctly"
- ✅ Open http://localhost:3000/client1/ - "Client 1 looks good"
- ✅ Open http://localhost:3000/client2/ in new tab - "Client 2 is up"
- ✅ Send a test message - "Messages are working between clients"

**Say to interviewer**:
> "Everything looks good! I can see both clients, messages are sending, and the server is running without errors. I'm ready to start."

#### Common Setup Issues (Be Ready!)

**Issue**: Port 3000 already in use
```bash
# Find and kill the process
lsof -ti:3000 | xargs kill -9
bash script/django/start
```
**Say**: "Port was in use from a previous session, I've cleared it and restarted."

**Issue**: Module not found
```bash
# Reinstall dependencies
source django/.venv/bin/activate
pip install -r django/requirements.txt
```
**Say**: "Dependencies weren't installed correctly, reinstalling now."

**Issue**: Database locked
```bash
# Reset database
rm django/db.sqlite3
cd django && python manage.py migrate
```
**Say**: "Database was locked, I've reset it and rerun migrations."

---

## PHASE 2: SOLO TASK (45 Minutes) - THE CRITICAL PHASE

### Time Management Strategy

| Time | Task | Status Check |
|------|------|--------------|
| 0-5 min | Plan & read requirements | "What exactly do I need to build?" |
| 5-20 min | Implement Requirement 1 (basic messaging) | "Is two-way messaging working?" |
| 20-25 min | Test Requirement 1 thoroughly | "Did I test all acceptance criteria?" |
| 25-40 min | Implement 2-3 features from Requirement 2 | "Which features add most value?" |
| 40-45 min | Clean up code, test, prepare talking points | "What will I show the engineer?" |

### Minutes 0-5: Planning Phase

#### Step 1: Re-read Requirements Carefully

Open the requirements doc. **Highlight or write down**:

**Requirement 1 (MUST COMPLETE)**:
- [ ] User in Client 1 can type and send
- [ ] Message appears in Client 2
- [ ] User in Client 2 can reply
- [ ] Reply appears in Client 1
- [ ] Messages show sender identification
- [ ] Messages show timestamp

**Requirement 2 (Choose 2-3)**:
- [ ] Which features will I build?
- [ ] Why these features? (be ready to explain)

#### Step 2: Quick Codebase Scan (2 minutes)

**Don't read every line**. Just identify:
- Where is the WebSocket consumer? → `consumers.py`
- Where is the database model? → `models.py`
- Where is the frontend? → `templates/`
- Is there existing code or starting from scratch?

#### Step 3: Create a Task List (1 minute)

**Write on paper or comment in code**:
```python
# TODO: Phase 2 - Solo Task
# [x] 1. Set up WebSocket consumer
# [x] 2. Create Message model
# [x] 3. Implement send/receive in consumer
# [x] 4. Update frontend to connect WebSocket
# [x] 5. Test two-way messaging
# [ ] 6. Add typing indicator
# [ ] 7. Add message history
# [ ] 8. Test everything
```

**Say out loud** (if you're in the habit):
> "Okay, my plan is to first ensure basic messaging works, then add typing indicators and message history. Let me start with the consumer."

### Minutes 5-20: Implement Requirement 1

#### Strategy: Go Deep, Not Wide

**❌ Don't**: Try to make it perfect, add fancy features, over-engineer

**✅ Do**: Get basic messaging working end-to-end, then iterate

#### Step-by-Step Implementation

**1. Create/Update Consumer (5 minutes)**

**Think out loud** (even to yourself):
> "I need a WebSocket consumer that can receive messages and broadcast them to all clients. Let me check if there's already a consumer..."

```python
# minicom/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join room group
        self.room_name = 'general'
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Receive message from WebSocket
        data = json.loads(text_data)
        message = data['message']
        username = data['username']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username']
        }))
```

**As you code, think**:
- "Am I following the existing code style?"
- "Are my variable names clear?"
- "Should I add a comment here?"

**2. Update Frontend (5 minutes)**

```javascript
// In client1.html and client2.html
const chatSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/chat/general/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    document.querySelector('#messages').innerHTML +=
        '<div><strong>' + data.username + ':</strong> ' +
        data.message + '</div>';
};

document.querySelector('#send-button').onclick = function(e) {
    const messageInput = document.querySelector('#message-input');
    const message = messageInput.value;
    chatSocket.send(JSON.stringify({
        'message': message,
        'username': 'Client1'  // or 'Client2'
    }));
    messageInput.value = '';
};
```

**3. Test Immediately (3 minutes)**

**Don't wait until everything is done!**

Open two browser tabs:
- Tab 1: http://localhost:3000/client1/
- Tab 2: http://localhost:3000/client2/

**Test checklist**:
- ✅ Type "Hello from Client1" → appears in both tabs?
- ✅ Type "Reply from Client2" → appears in both tabs?
- ✅ Refresh Client1 → messages disappear (expected, no persistence yet)
- ✅ Check browser console for errors

**If it doesn't work**:
1. Check browser console (F12) for JavaScript errors
2. Check terminal for Python errors
3. Check if WebSocket connected (console should show connection message)

**Debugging mindset**:
> "Hmm, messages aren't appearing. Let me check the console... ah, WebSocket URL is wrong. Let me fix that."

### Minutes 20-25: Add Timestamps and Sender ID

**Now make it meet ALL Requirement 1 criteria**

```python
# In consumer
from django.utils import timezone

async def receive(self, text_data):
    data = json.loads(text_data)

    await self.channel_layer.group_send(
        self.room_group_name,
        {
            'type': 'chat_message',
            'message': data['message'],
            'username': data['username'],
            'timestamp': timezone.now().isoformat()  # Add timestamp
        }
    )

async def chat_message(self, event):
    await self.send(text_data=json.dumps({
        'message': event['message'],
        'username': event['username'],
        'timestamp': event['timestamp']
    }))
```

```javascript
// In frontend
chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const time = new Date(data.timestamp).toLocaleTimeString();

    document.querySelector('#messages').innerHTML +=
        '<div>' +
        '<strong>' + data.username + '</strong> ' +
        '<span class="time">(' + time + ')</span>: ' +
        data.message +
        '</div>';
};
```

**Test again**: Messages should now show username and timestamp!

### Minutes 25-40: Add Features from Requirement 2

**CRITICAL DECISION**: Which features to build?

#### Recommended Priority (Choose 2-3):

**High Value, Low Complexity** (Do These First):

1. **Typing Indicator (Option B)** - Easy, impressive
   - Time: ~8 minutes
   - Impact: Shows real-time capability
   - Code: ~30 lines

2. **Message History (Option C)** - Valuable, moderate
   - Time: ~10 minutes
   - Impact: Shows database knowledge
   - Code: ~40 lines

3. **User Presence (Option G)** - Good for collaboration
   - Time: ~7 minutes
   - Impact: Shows system thinking
   - Code: ~25 lines

**Medium Value** (If Time Permits):

4. **Read Receipts (Option D)** - Complex but impressive
5. **Emoji Reactions (Option A)** - Fun but time-consuming

#### Quick Implementation: Typing Indicator (8 minutes)

**Backend (2 minutes)**:
```python
async def receive(self, text_data):
    data = json.loads(text_data)

    if data['type'] == 'typing':
        # Broadcast typing status
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_typing',
                'username': data['username'],
                'is_typing': data['is_typing']
            }
        )
    elif data['type'] == 'message':
        # ... existing message handling
        pass

async def user_typing(self, event):
    await self.send(text_data=json.dumps({
        'type': 'typing',
        'username': event['username'],
        'is_typing': event['is_typing']
    }))
```

**Frontend (6 minutes)**:
```javascript
let typingTimeout;

document.querySelector('#message-input').oninput = function() {
    // Send typing=true
    chatSocket.send(JSON.stringify({
        'type': 'typing',
        'username': 'Client1',
        'is_typing': true
    }));

    // Reset timeout
    clearTimeout(typingTimeout);
    typingTimeout = setTimeout(() => {
        chatSocket.send(JSON.stringify({
            'type': 'typing',
            'username': 'Client1',
            'is_typing': false
        }));
    }, 3000);
};

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);

    if (data.type === 'typing') {
        const indicator = document.querySelector('#typing-indicator');
        if (data.is_typing && data.username !== 'Client1') {
            indicator.textContent = data.username + ' is typing...';
        } else {
            indicator.textContent = '';
        }
    }
    // ... handle other message types
};
```

**Add HTML**:
```html
<div id="typing-indicator"></div>
```

**Test**: Type in one client → see "Client1 is typing..." in other client

#### Quick Implementation: Message History (10 minutes)

**Create Model (3 minutes)**:
```python
# models.py
from django.db import models

class Message(models.Model):
    username = models.CharField(max_length=100)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
```

**Run Migration**:
```bash
cd django
python manage.py makemigrations
python manage.py migrate
```

**Update Consumer (5 minutes)**:
```python
from channels.db import database_sync_to_async
from .models import Message

@database_sync_to_async
def save_message(username, content):
    return Message.objects.create(username=username, content=content)

@database_sync_to_async
def get_recent_messages():
    messages = Message.objects.all()[:50]
    return [{'username': m.username, 'content': m.content,
             'timestamp': m.timestamp.isoformat()} for m in messages]

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # ... existing code ...
        await self.accept()

        # Send message history
        messages = await get_recent_messages()
        await self.send(text_data=json.dumps({
            'type': 'history',
            'messages': messages
        }))

    async def receive(self, text_data):
        data = json.loads(text_data)

        if data['type'] == 'message':
            # Save to database
            await save_message(data['username'], data['message'])

            # ... existing broadcast code ...
```

**Update Frontend (2 minutes)**:
```javascript
chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);

    if (data.type === 'history') {
        data.messages.forEach(msg => {
            displayMessage(msg.username, msg.content, msg.timestamp);
        });
    } else {
        displayMessage(data.username, data.message, data.timestamp);
    }
};

function displayMessage(username, content, timestamp) {
    const time = new Date(timestamp).toLocaleTimeString();
    document.querySelector('#messages').innerHTML +=
        '<div><strong>' + username + '</strong> (' + time + '): ' +
        content + '</div>';
}
```

**Test**:
1. Send messages
2. Refresh page
3. Messages should reappear!

### Minutes 40-45: Clean Up & Prepare

**Don't skip this! It's crucial for the pairing session.**

#### Code Cleanup (2 minutes)

**Checklist**:
- ✅ Remove `console.log()` statements (or leave helpful ones)
- ✅ Remove commented-out code
- ✅ Fix indentation
- ✅ Add brief comments for complex logic

**Example**:
```python
# Before
async def receive(self, text_data):
    data = json.loads(text_data)
    # print(data)  # debug
    # old_implementation()
    # TODO: make this better
    ...

# After
async def receive(self, text_data):
    """Handle incoming WebSocket messages"""
    data = json.loads(text_data)

    # Route based on message type
    if data['type'] == 'message':
        await self.handle_chat_message(data)
    elif data['type'] == 'typing':
        await self.handle_typing_indicator(data)
```

#### Testing Checklist (2 minutes)

**Test each feature methodically**:

1. **Basic Messaging**:
   - [ ] Send from Client1 → appears in both
   - [ ] Send from Client2 → appears in both
   - [ ] Messages show correct username
   - [ ] Messages show timestamp

2. **Typing Indicator** (if implemented):
   - [ ] Type in Client1 → "Client1 is typing" in Client2
   - [ ] Stop typing → indicator disappears after 3s
   - [ ] Doesn't show own typing indicator

3. **Message History** (if implemented):
   - [ ] Send 5 messages
   - [ ] Refresh page
   - [ ] All 5 messages reappear

**If you find bugs**: Fix the critical ones, note the minor ones (you'll mention them in pairing).

#### Prepare Talking Points (1 minute)

**Write down (on paper or in comments)**:

```
WHAT I BUILT:
- ✅ Two-way messaging with WebSocket
- ✅ Typing indicator (3-second timeout)
- ✅ Message history (last 50 messages)

WHAT I'D IMPROVE:
- Add error handling for WebSocket disconnect
- Better UI styling
- User authentication

QUESTIONS FOR ENGINEER:
- Is in-memory channel layer okay, or should I use Redis?
- Should I add tests?
```

**Take a deep breath. You're ready for pairing!**

---

## PHASE 3: PAIRING SESSION (45 Minutes) - SHOW COLLABORATION

### Mindset Shift

**Solo session**: You vs. the problem
**Pairing session**: You + Engineer vs. the problem

**This is NOT a test of coding speed. It's a test of**:
- Communication
- Collaboration
- Receptiveness to feedback
- Technical discussion
- Problem-solving approach

### First 5 Minutes: Transition & Context Sharing

#### When Engineer Joins

**Greet warmly**:
> "Hey! Good to see you. I've made good progress on the basic requirements. Would you like me to do a quick demo first, or jump straight into the code?"

**Most likely they'll say**: "Let's see what you've built!"

#### Give a 2-Minute Demo

**Use this script**:

> "Sure! Let me show you what's working. I have two clients open here..."

**Demo checklist** (actually do these actions):
1. Type "Hello from Client1" → show it in both windows
2. Type "Reply from Client2" → show it in both windows
3. Start typing → show typing indicator
4. Refresh one client → show message history loads

> "So the core two-way messaging is working. I also added typing indicators - you can see it shows 'Client1 is typing' when I type here - and message history, which persists in SQLite and loads when you refresh."

**Mention what's NOT done** (honesty builds trust):
> "I haven't added [X feature] yet, and the UI is pretty basic. I was thinking we could work on [Y] during this session if that makes sense?"

#### Discuss What to Build Next

**Engineer might say**: "What do you think we should work on next?"

**Your response** (shows initiative):
> "I'm thinking we could add [feature X] because [reason]. But I'm also curious what you think would add the most value? Or is there something specific you'd like to explore?"

**Good features to suggest**:
- User authentication (shows security thinking)
- Error handling and reconnection (shows reliability thinking)
- Multiple rooms (shows scalability thinking)
- Better UI/UX (shows product thinking)

**Listen to their suggestion and agree enthusiastically**:
> "Oh, that's a great idea! I hadn't thought about [X]. Let's do that."

### During Pairing: Communication Patterns

#### Pattern 1: Think Out Loud (Constantly!)

**Bad** (silent coding):
```
*types for 3 minutes in silence*
*engineer sits there awkwardly*
```

**Good** (narrating):
```
You: "Okay, so to add user authentication, I'm thinking we need to..."
     *pause to let them interject*

You: "First, I'll create a User model. Let me open models.py..."
     *navigate to file*

You: "I'm going to import Django's AbstractUser because it has most
      of what we need..."
     *start typing*

Engineer: "Actually, what if we use the built-in User model?"

You: "Oh good point! That's simpler. Let me do that instead."
```

**Key phrases to use constantly**:
- "I'm thinking..."
- "My approach would be..."
- "Let me try..."
- "What do you think about...?"
- "Does that make sense?"
- "Am I on the right track?"

#### Pattern 2: Ask for Input (But Not Too Much)

**Balance**:
- ❌ Too independent: Never asking for input (seems arrogant)
- ❌ Too dependent: Asking for every line of code (seems incompetent)
- ✅ Just right: Ask at decision points, implement on your own

**When to ask**:
- Architecture decisions: "Should I create a new file or add to existing?"
- Approach choices: "Should we use JWT tokens or session auth?"
- Stuck for >2 minutes: "I'm not sure why this isn't working. Could you take a look?"
- Uncertainty: "I haven't used feature X before. Is it okay if I look it up quickly?"

**When NOT to ask**:
- Syntax questions: "How do I write a for loop?" (Google it)
- Obvious next steps: "Should I save the file?" (just do it)
- Implementation details you can figure out

#### Pattern 3: Receive Feedback Gracefully

**Engineer suggests something different**:

**Bad response**:
- ❌ "No, my way is better because..."
- ❌ "I already tried that, it doesn't work"
- ❌ *Silently ignores suggestion*

**Good response**:
- ✅ "Interesting! I was thinking [X], but I like your idea because [Y]. Let's try that."
- ✅ "Oh, I hadn't considered that approach. What's the advantage over [my approach]?"
- ✅ "That makes sense. Let me refactor to do it that way."

**If you disagree** (it's okay!):
- ✅ "I see the benefit of [their approach], but I'm a bit concerned about [X]. What do you think?"
- ✅ "Could you explain why that's better? I want to understand the trade-off."
- ✅ "Interesting! I've used [alternative] before and it worked well. Have you found issues with that?"

**Key**: Be curious, not combative. Frame as learning, not arguing.

#### Pattern 4: Handle Getting Stuck

**You will get stuck. It's expected! Here's how to handle it:**

**Stuck for 30 seconds**: Keep thinking out loud
> "Hmm, this isn't working as expected. Let me check..."

**Stuck for 1 minute**: Verbalize what you've tried
> "I've tried X and Y, but I'm getting this error. Let me look at the docs..."

**Stuck for 2 minutes**: Ask for help
> "I'm stuck on this error. Mind if we debug together?"

**Debugging together**:
1. **Read the error out loud**: "It says 'ConnectionRefusedError on line 42'"
2. **State your hypothesis**: "I think it's because the WebSocket URL is wrong"
3. **Propose a test**: "Let me print the URL and see what it is"
4. **Execute**: Add print statement, refresh, check
5. **Iterate**: "That wasn't it. Maybe it's..."

**If engineer finds the bug**:
> "Ah! I see it now. Thanks for catching that. I was looking at the wrong place."

**Never**:
- ❌ Get defensive: "Well that's a weird error message"
- ❌ Give up: "I don't know how to fix this"
- ❌ Blame: "This framework is confusing"

#### Pattern 5: Navigate Disagreements

**Scenario**: Engineer suggests approach X, but you think Y is better

**Example**:
```
Engineer: "Why don't we use polling instead of WebSockets?"

You (internal): *This is wrong! Polling is inefficient!*

You (external - BAD): "No, WebSockets are way better. Polling is outdated."

You (external - GOOD): "Interesting! I went with WebSockets because of the
lower latency and bidirectional capability. Are you thinking polling might
be simpler for this use case? I'm curious about the trade-offs you're seeing."

Engineer: "Oh, I was just testing if you understood the choice. WebSockets
          are definitely right here."
```

**They might be**:
1. Testing your understanding (explain your reasoning)
2. Playing devil's advocate (defend your choice politely)
3. Actually correct (listen and learn!)

**Framework for respectful disagreement**:
1. Acknowledge their point: "I see where you're coming from..."
2. State your reasoning: "I chose X because..."
3. Ask for their perspective: "What's your thinking on this?"
4. Find common ground: "I think we both agree that [goal]. Maybe we could..."

### Pairing Scenarios & How to Handle

#### Scenario 1: Engineer Types (Driver-Navigator)

**What might happen**: "Mind if I drive for a bit? I want to show you something."

**Your response**:
> "Of course! Go ahead."

**Your role as navigator**:
- Watch what they're typing
- Ask questions: "Oh, why did you use that approach?"
- Offer suggestions: "Should we also handle the error case?"
- Take notes mentally (or on paper)
- Don't just sit silently!

**When they finish**:
> "That makes sense! I like how you [X]. I wouldn't have thought of that."

#### Scenario 2: Live Debugging Session

**What might happen**: "This error is tricky. Let's debug together."

**Your approach**:
1. **Read error carefully**: "Okay, it's a KeyError on line 45..."
2. **Add print statements**: "Let me print what's in the dictionary..."
3. **Explain findings**: "Interesting, the key 'username' doesn't exist. I think it's because..."
4. **Propose fix**: "If I add a default value here..."
5. **Test fix**: "Let me try this again..."
6. **Confirm**: "Great, that fixed it!"

**Stay positive**:
- ✅ "Good catch!"
- ✅ "Let's figure this out"
- ✅ "Ah, I see the issue now"
- ❌ "This is frustrating"
- ❌ "I don't understand this error"

#### Scenario 3: Design Discussion

**Engineer asks**: "How would you handle 1000 concurrent users?"

**Bad answer**: "Um... I guess we'd need more servers?"

**Good answer** (use structure):
> "Great question. Let me think through this...
>
> Currently we're using an in-memory channel layer, which won't work across multiple servers. For 1000 concurrent users, I'd:
>
> 1. Replace the in-memory layer with Redis so multiple servers can communicate
> 2. Put servers behind a load balancer with sticky sessions for WebSocket
> 3. Use PostgreSQL instead of SQLite for better concurrent write handling
> 4. Add connection pooling to manage database connections efficiently
>
> Is that the kind of scaling you're thinking about, or were you asking about something else?"

**Framework**:
1. Acknowledge the question
2. State your current limitation
3. Propose concrete solutions (3-5 specific things)
4. Invite feedback

#### Scenario 4: Code Review / Refactoring

**Engineer**: "This function is getting pretty long. How could we refactor it?"

**Your approach**:
> "You're right, it's doing too much. Let me see..."
>
> *Look at the code*
>
> "I think we could extract the message validation into a separate function, and the database save into another. That would make this easier to test too. Want me to try that?"

**Then**:
1. Create new function
2. Move code
3. Update caller
4. Test that it still works

**Name refactored functions clearly**:
- ✅ `validate_message_data()`
- ✅ `save_message_to_database()`
- ❌ `helper1()`
- ❌ `do_stuff()`

#### Scenario 5: Time Running Out

**Engineer**: "We have 10 minutes left. What should we prioritize?"

**Your response** (shows prioritization skills):
> "Good point. Let me think about what's most important...
>
> I think we should:
> 1. Finish the feature we're working on (5 minutes)
> 2. Test it thoroughly (3 minutes)
> 3. Clean up any console errors (2 minutes)
>
> The [other feature] is nice to have, but I'd rather have what we built working solidly. Does that sound good?"

**They're testing**:
- Can you prioritize?
- Do you focus on quality over quantity?
- Do you think about the user?

### Communication Red Flags to Avoid

#### ❌ Red Flag 1: Being a "Know-It-All"

**Bad**:
```
Engineer: "Have you considered using Redis?"
You: "Yeah, I know all about Redis. I've used it tons of times."
```

**Good**:
```
Engineer: "Have you considered using Redis?"
You: "I've used Redis for caching before. Are you thinking we should use
     it for the channel layer? That would help with multi-server
     deployment, right?"
```

#### ❌ Red Flag 2: Not Listening

**Bad**:
```
Engineer: "What if we tried—"
You: *interrupts* "Yeah I know, I was just about to do that"
```

**Good**:
```
Engineer: "What if we tried—"
You: *wait for them to finish*
You: "Oh interesting! I was thinking along similar lines. Let's try that."
```

#### ❌ Red Flag 3: Making Excuses

**Bad**:
```
Engineer: "This function has a bug"
You: "Well, I was rushed and didn't have time to test properly"
```

**Good**:
```
Engineer: "This function has a bug"
You: "Good catch! Let me fix that. I should have added a test case for this."
```

#### ❌ Red Flag 4: Being Passive

**Bad**:
```
Engineer: "What should we do next?"
You: "I don't know, what do you think?"

Engineer: "Should we use approach A or B?"
You: "Either is fine with me"
```

**Good**:
```
Engineer: "What should we do next?"
You: "I'm thinking we should add error handling because [reason].
     But I'm also curious what you think is most important?"

Engineer: "Should we use approach A or B?"
You: "I'd lean toward A because [reason], but I can see B being
     better if we're prioritizing [other thing]. What's your take?"
```

#### ❌ Red Flag 5: Getting Flustered

**Bad**:
```
*Something breaks*
You: "Oh no! Why isn't this working? This is so frustrating. I don't
     understand what's happening."
```

**Good**:
```
*Something breaks*
You: "Interesting, that's not what I expected. Let me check the console...
     Ah, I see the error. Looks like [X]. Let me try [fix]."
```

---

## PHASE 4: WRAP UP (15 Minutes) - SEAL THE DEAL

### What Happens

- Demo what you built
- Discuss future improvements
- Talk about collaboration during pairing
- Engineer may ask reflection questions

### Your Goal

- Show what you accomplished
- Demonstrate system thinking (future improvements)
- Show you're pleasant to work with
- End on a high note

### Minutes 1-5: Demo What You Built

#### Structure Your Demo

**Opening**:
> "Thanks for the session! That was really fun working together. Let me show you what we built."

**Demo Script** (actually perform these actions):

**1. Core Features** (2 minutes):
> "Starting with the basics, we have real-time bidirectional messaging.
> Let me send a message from Client 1..."
> *Type and send*
> "...and it appears instantly in both clients with the username and timestamp."
>
> "Client 2 can reply..."
> *Type from Client 2*
> "...and that also appears in real time."

**2. Additional Features** (2 minutes):
> "We also implemented [features you built]:
>
> **Typing Indicator**: When I start typing here...
> *Start typing*
> ...you can see 'Client1 is typing' appears in the other window.
>
> **Message History**: If I refresh the page...
> *Refresh*
> ...all the messages persist and reload from the database."

**3. Architecture Highlight** (1 minute):
> "Under the hood, we're using Django Channels with WebSockets for
> real-time communication, SQLite for message persistence, and an
> in-memory channel layer for broadcasting. The async consumer
> handles all the WebSocket logic."

**Don't forget to mention engineer's contributions**:
> "During pairing, [Engineer Name] suggested we refactor the consumer
> to handle different message types, which made the code much cleaner."

### Minutes 5-12: Discuss Future Improvements

**This is critical! They're testing your system thinking.**

#### Framework: Present 3 Categories of Improvements

**1. Short-term (Quick Wins)**:
> "If I had another hour, I'd add:
> - Error handling for WebSocket disconnections with auto-reconnect
> - Input validation to prevent empty messages
> - Better UI styling with CSS
> - XSS protection by escaping HTML in messages"

**Why this is good**: Shows you think about quality, security, UX

**2. Medium-term (Feature Expansion)**:
> "For the next sprint, I'd prioritize:
> - User authentication so people have persistent identities
> - Multiple chat rooms instead of just one
> - Read receipts to show when messages are seen
> - File and image sharing
> - Better mobile responsiveness"

**Why this is good**: Shows you think about product evolution

**3. Long-term (Scale & Architecture)**:
> "For production scale, we'd need:
> - Replace in-memory channel layer with Redis for multi-server support
> - Switch to PostgreSQL for better concurrent writes
> - Add load balancer with sticky sessions for WebSockets
> - Implement caching for message history (reduce DB queries)
> - Add monitoring with Prometheus/Grafana
> - Deploy across multiple regions for low latency globally"

**Why this is good**: Shows you think about scale, reliability, performance

#### Invite Discussion

**Don't just list things! Make it a conversation:**

> "Those are some ideas I had. I'm curious - if this were a real product,
> what would you prioritize? And are there any scaling challenges you've
> seen with similar systems?"

**Possible responses from engineer**:

**They might ask**: "How would you handle message ordering across multiple servers?"

**Your answer**:
> "Great question! With multiple servers, clock skew could cause issues.
> I'd use database-generated timestamps since all servers connect to the
> same database, ensuring consistent ordering. For distributed systems,
> I might also look into Lamport timestamps or vector clocks for causality."

**They might ask**: "What about security concerns?"

**Your answer**:
> "Good point! I'd focus on:
> 1. XSS prevention - escaping all user input
> 2. Authentication - JWT tokens for WebSocket connections
> 3. Authorization - checking if users can access specific rooms
> 4. Rate limiting - preventing spam/DoS attacks
> 5. WSS - using secure WebSocket in production
>
> Are there other security aspects you'd prioritize?"

### Minutes 12-15: Reflect on Collaboration

**Engineer might ask**: "How did you find the pairing session?"

**Framework for response**:

**1. Positive opening**:
> "I really enjoyed it! It felt like real collaboration."

**2. Specific thing you learned**:
> "I particularly liked when you suggested [X]. I hadn't thought about
> [Y], and it made the solution much better."

**3. What you brought**:
> "I think we worked well together on [specific thing]. I appreciated
> how we could discuss trade-offs openly."

**4. Growth mindset**:
> "If I were to do it again, I'd probably [one thing you'd improve].
> But overall it was a great experience."

**Example**:
> "I really enjoyed the pairing session! It felt like authentic collaboration
> rather than just being tested.
>
> I particularly liked when you suggested refactoring the receive() method
> to use a routing dictionary. I was going with if/elif statements, but your
> approach is much more extensible.
>
> I think we worked well together on the debugging when the WebSocket
> wouldn't connect. I appreciated how we methodically checked each layer.
>
> If I were to do it again, I'd probably communicate my thought process
> even more clearly. But overall it was a really great experience."

**Engineer might ask**: "What was the most challenging part?"

**Bad answer**: "The time pressure was really hard"

**Good answer**:
> "I'd say the most challenging part was deciding which features to
> prioritize in the 45 minutes. I wanted to build everything, but had
> to make trade-offs. I ended up focusing on typing indicators and
> message history because they showcased different aspects - real-time
> events and database persistence. But it meant leaving out some other
> cool features like emoji reactions."

**Why this is good**: Shows prioritization skills, decision-making, understanding of trade-offs

### Final Moments: Ask a Question

**This shows engagement and interest!**

**Good questions**:
- "I'm curious - what patterns have you seen work well for WebSocket architecture at Intercom's scale?"
- "What would a production version of this look like in Intercom's stack?"
- "What's the most interesting technical challenge you've worked on recently?"
- "How does the team approach balancing new features vs. technical debt?"

**Avoid**:
- "Did I pass?" (puts them on the spot)
- "What were you looking for?" (sounds insecure)
- Generic questions you could Google

**Closing**:
> "Thanks so much for the session! This was really fun, and I learned a lot.
> I appreciated your feedback on [specific thing]. Looking forward to hearing
> from you!"

---

## BONUS: COMMON PITFALLS & HOW TO AVOID

### Pitfall 1: Trying to Build Too Much

**Scenario**: You try to implement 5 features and all are half-done

**Solution**: Build 2-3 features that WORK COMPLETELY
- ✅ Working typing indicator + message history
- ❌ Half-working typing indicator + half-working history + broken reactions

**Remember**: Working > Impressive

### Pitfall 2: Not Testing

**Scenario**: You code for 40 minutes straight, then test and everything is broken

**Solution**: Test after every small change
- Write function → Test it → Move to next function
- Don't wait until the end!

### Pitfall 3: Silent Coding During Pairing

**Scenario**: You code silently for 5 minutes while engineer watches

**Solution**: Narrate constantly
- "I'm going to..."
- "Let me try..."
- "What do you think if..."

**Set a mental timer**: If you haven't spoken in 30 seconds, you're too quiet!

### Pitfall 4: Arguing with the Engineer

**Scenario**: Engineer suggests X, you insist on Y, tension rises

**Solution**: Be curious, not combative
- ✅ "Interesting! Why do you prefer that approach?"
- ❌ "No, my way is better"

**Remember**: They're not testing if you're right. They're testing if you collaborate well.

### Pitfall 5: Getting Defensive About Bugs

**Scenario**: Engineer finds a bug in your code

**Bad response**: "Well I didn't have time to test that part"
**Good response**: "Good catch! Let me fix that right away"

**Remember**: Everyone writes bugs. It's how you respond that matters.

### Pitfall 6: Not Asking for Help When Stuck

**Scenario**: You're stuck for 5 minutes, too embarrassed to ask

**Solution**: Ask for help after 2 minutes
- It's better to collaborate than struggle silently
- Shows you know when to seek input

### Pitfall 7: Over-Engineering

**Scenario**: You build an elaborate class hierarchy for a simple feature

**Solution**: Keep it simple (KISS)
- Simple working code > Complex elegant code
- You can always refactor later

### Pitfall 8: Poor Time Management

**Scenario**: You spend 30 minutes on CSS styling, 5 minutes on core features

**Solution**: Prioritize ruthlessly
1. Core functionality FIRST
2. Additional features SECOND
3. Polish LAST (if time permits)

---

## PRE-INTERVIEW CHECKLIST

### Night Before

- [ ] Run the setup script successfully
- [ ] Test that both clients can chat
- [ ] Read through the code files once
- [ ] Review WebSocket basics
- [ ] Get good sleep (seriously!)

### 1 Hour Before

- [ ] Test your mic and camera
- [ ] Close all unnecessary applications
- [ ] Have water nearby
- [ ] Open browser with docs tabs
- [ ] Set up your IDE
- [ ] Go to bathroom (you'll be on camera for 2 hours!)

### 15 Minutes Before

- [ ] Test screen sharing works
- [ ] Close Slack, email, phone notifications
- [ ] Set terminal to readable font size
- [ ] Have notepad ready for notes
- [ ] Take 3 deep breaths

---

## FINAL MINDSET TIPS

### Remember: They Want You to Succeed

The engineer is NOT trying to trick you or catch you out. They want to:
- See if you can code
- See if you can collaborate
- See if they'd enjoy working with you

### It's Okay to Not Know Everything

You will NOT know everything. That's expected! What matters:
- How you approach unknowns (research, ask questions)
- How you communicate uncertainty
- How you learn in real-time

### Think Like a Product Engineer

**They're looking for**:
- Someone who thinks about users ("This feature would make users happy because...")
- Someone who thinks about trade-offs ("We could do X which is fast, or Y which is better long-term")
- Someone who thinks about the team ("This code is readable, so others can maintain it")

### Show Your Personality

**Be yourself!** They're hiring a human, not a coding robot.
- It's okay to laugh
- It's okay to say "that's a great question!"
- It's okay to show enthusiasm
- It's okay to admit when something is tricky

### The Secret Sauce

**The best candidates**:
1. Communicate clearly and constantly
2. Listen actively and respond thoughtfully
3. Show curiosity and ask good questions
4. Handle feedback gracefully
5. Think out loud through problems
6. Balance confidence with humility
7. Focus on collaboration over competition

**You've got this!** 🚀

---

## QUICK REFERENCE CARDS

### Card 1: Time Management

| Phase | Time | Key Goals |
|-------|------|-----------|
| Setup | 15m | Environment working, understand requirements |
| Solo | 45m | Req 1 done (25m), 2-3 features from Req 2 (15m), test & clean (5m) |
| Pairing | 45m | Collaborate, extend features, discuss architecture |
| Wrap Up | 15m | Demo (5m), future ideas (7m), reflection (3m) |

### Card 2: Communication Phrases

**Starting tasks**:
- "Let me start by..."
- "My approach would be..."
- "I'm thinking we could..."

**Asking for input**:
- "What do you think about...?"
- "Does this make sense?"
- "I'm not sure about X. What's your take?"

**Receiving suggestions**:
- "Good point! Let me try that."
- "I hadn't thought of that. Let's do it."
- "Interesting! Can you explain why that's better?"

**When stuck**:
- "I'm hitting an error. Let me debug..."
- "This is tricky. Mind if we look at this together?"
- "Let me check the docs quickly..."

### Card 3: Demo Script

```
1. "Let me show you what we built..."

2. Core feature: "We have two-way messaging working in real-time"
   *Demo: send from Client1, appears in both*

3. Feature 1: "We added typing indicators"
   *Demo: start typing, show indicator*

4. Feature 2: "Messages persist in the database"
   *Demo: refresh, messages reload*

5. Architecture: "Under the hood, we're using WebSockets with Django Channels"

6. Future: "If I had more time, I'd add [3 specific things]"
```

### Card 4: Red Flags to Avoid

❌ Coding silently for >1 minute
❌ Not testing until the end
❌ Arguing with suggestions
❌ Getting defensive about bugs
❌ Making excuses for issues
❌ Not asking questions
❌ Trying to build everything
❌ Over-engineering simple things

### Card 5: Green Flags to Show

✅ Think out loud constantly
✅ Test frequently (after each feature)
✅ Ask thoughtful questions
✅ Listen and respond to feedback
✅ Admit when you don't know
✅ Show curiosity
✅ Prioritize working code
✅ Keep it simple

---

## YOU'RE READY!

You have:
- ✅ A working application
- ✅ Deep understanding of the code
- ✅ Strategy for each interview phase
- ✅ Communication templates
- ✅ Collaboration techniques
- ✅ Time management plan

**Now go show them what you can do!** 🎯

Remember: The interviewer is a future colleague, not an adversary. Treat it like you're already on the team, solving a problem together.

**Good luck! You've got this!** 💪
