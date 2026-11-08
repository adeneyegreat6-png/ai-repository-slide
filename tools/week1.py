#!/usr/bin/env python3
import sys, os, io, json
sys.path.insert(0, "/home/claude/thirty")
from core import cover_slide, body_slide, tool_slide, cta_slide, build_background
import cairosvg
from PIL import Image

W, H = 1080, 1350
ROOT = "/home/claude/week1"
PILLS = ["Save this post", "Comment the number (01–04)", "Send it to a friend"]
PL = "TRY THIS PROMPT"

def B(n, head, sub, prompt, label=PL, kick=None):
    return ("body", n, head, sub, label, prompt, kick)

def T(n, name, letter, accent, best, bullets):
    return ("tool", n, name, letter, accent, best, bullets)

def build(c):
    s = [("01_cover", cover_slide(0, c["kicker"], c["head"], c["sub"]))]
    for i, sp in enumerate(c["slides"], start=1):
        n = f"{i:02d}"
        if sp[0] == "body":
            _, _, head, sub, label, prompt, kick = sp
            k = kick or f"{c['unit']} {n}"
            s.append((f"{i+1:02d}_{c['unit'].lower()}{n}", body_slide(i, k, n, head, sub, label, prompt)))
        else:
            _, _, name, letter, accent, best, bullets = sp
            s.append((f"{i+1:02d}_tool{n}", tool_slide(i, f"{c['unit']} {n}", n, name, letter, accent, best, bullets)))
    s.append(("06_cta", cta_slide(5, "YOUR MOVE", c["cta_head"], c["cta_sub"], PILLS)))
    return s

C = []

# ---------- D1 A: practical — notes to plans ----------
C.append(dict(id="d1a", date="2026-11-09", time="08:00", unit="TASK", kicker="PRACTICAL AI",
 head=["Turn Messy Notes", "Into A Clear Plan"],
 sub=["4 prompts that turn a chaotic brain", "dump into something you can act on", "today."],
 slides=[
  B("01", ["Brain Dump", "To Priorities"], ["Type everything on your mind, then", "let AI rank what actually matters."],
    ["\"Here is everything on my mind: [dump].", "Sort it into Do Today, This Week,", "and Drop. Explain each choice in", "one line.\""]),
  B("02", ["Meetings To", "Action Items"], ["Skip rereading the notes. Pull out", "what has an owner and a date."],
    ["\"From these notes: [paste]. List every", "action item with an owner and a", "deadline. Flag anything missing", "either.\""]),
  B("03", ["Long Email To", "Three Lines"], ["Get the point of a wall of text", "before you decide to reply."],
    ["\"Summarize this email in 3 lines: what", "they want, by when, and what I need", "to decide. Then draft a 2-sentence", "reply.\""]),
  B("04", ["Goals To A", "Weekly Plan"], ["A big goal is just a calendar problem", "once it is broken down."],
    ["\"My goal is [goal] by [date]. I have", "[X] hours a week. Build a week-by-week", "plan with one clear deliverable", "each week.\""]),
 ],
 cta_head=["Which Prompt Are", "You Using First?"], cta_sub=["Save this for your next messy Monday", "— then send it to someone whose", "to-do list is out of control."],
 hook="Your notes are not the problem. The missing structure is.",
 items=["Brain dump to priorities", "Meetings to action items", "Long email to three lines", "Goals to a weekly plan"],
 ask="Which one will you try first? Comment the number 👇",
 tags="#LearnAIWithDoyin #PracticalAI #Productivity #AITools #AIForBeginners"))

# ---------- D1 B: concept — tokens ----------
C.append(dict(id="d1b", date="2026-11-09", time="18:00", unit="CONCEPT", kicker="AI CONCEPTS",
 head=["What Is A Token?", "AI Explained", "Simply"],
 sub=["The word behind AI limits, pricing,", "and why long chats get forgetful.", "Four ideas, no jargon."],
 slides=[
  B("01", ["AI Reads In", "Chunks, Not Words"], ["A token is a piece of text: a word,", "part of a word, or punctuation."],
    ["\"Explain tokens like I am 12, using", "the sentence 'Unbelievable weather", "today' as an example, split into", "tokens.\""], label="TRY IT YOURSELF"),
  B("02", ["Why Limits", "Exist"], ["Every model can only handle so many", "tokens at once, your words and its", "reply combined."],
    ["\"What happens when a conversation goes", "past a model's token limit? Explain", "with a bookshelf analogy.\""], label="TRY IT YOURSELF"),
  B("03", ["Why Pricing Uses", "Tokens"], ["More text in, more text out means", "more computing. That is what you", "are really paying for."],
    ["\"Estimate how many tokens a 1,000-word", "article is, and why a short, clear", "prompt costs less than a rambling", "one.\""], label="TRY IT YOURSELF"),
  B("04", ["Shorter Prompts,", "Better Results"], ["Clear and concise beats long and", "vague. Trim before you send."],
    ["\"Rewrite this prompt to use fewer words", "without losing meaning: [paste your", "prompt]. Show the before and after.\""], label="TRY IT YOURSELF"),
 ],
 cta_head=["Which Idea Was", "New To You?"], cta_sub=["Save this for the next time AI cuts", "you off mid-answer — then send it to", "the friend who asks how it works."],
 hook="You use AI every day. Do you know what it is actually counting?",
 items=["AI reads in chunks, not words", "Why every model has limits", "Why pricing uses tokens", "Why shorter prompts win"],
 ask="Which idea was new to you? Comment the number 👇",
 tags="#LearnAIWithDoyin #AIConcepts #AIExplained #AIForBeginners #LLM"))

# ---------- D2 A: tools — research ----------
C.append(dict(id="d2a", date="2026-11-10", time="08:00", unit="TOOL", kicker="AI TOOLS",
 head=["4 AI Tools That", "Do Your Research", "For You"],
 sub=["Stop opening twenty tabs. These four", "find, read, and summarize while you", "think."],
 slides=[
  T("01", "NotebookLM", "N", "#4a90e2", ["Asking questions about your", "own documents"],
    ["Upload a report, ask what matters", "Turn notes into a study guide", "Get answers tied to your sources"]),
  T("02", "Perplexity", "P", "#3bbfad", ["Quick answers with", "sources attached"],
    ["Ask a question, get cited links", "Compare products or options fast", "Follow up without starting over"]),
  T("03", "Consensus", "C", "#8e7cf0", ["Finding what research", "actually says"],
    ["Ask a yes or no health question", "See what published studies conclude", "Skip the opinion blogs"]),
  T("04", "Claude", "C", "#f0a04b", ["Reading long documents", "and explaining them"],
    ["Paste a 40-page PDF, ask for a brief", "Ask it to find the weak arguments", "Request a plain-English rewrite"]),
 ],
 cta_head=["Which One Will", "You Test First?"], cta_sub=["Save this before your next research", "rabbit hole — then send it to a", "student or a very busy colleague."],
 hook="Research used to take an afternoon. These four cut it to minutes.",
 items=["NotebookLM: questions about your own documents", "Perplexity: fast answers with sources", "Consensus: what research actually says", "Claude: long documents explained"],
 ask="Which one are you testing first? Comment the number 👇",
 tags="#LearnAIWithDoyin #AITools #AIResearch #Productivity #AIForBeginners"))

# ---------- D2 B: practical — interviews ----------
C.append(dict(id="d2b", date="2026-11-10", time="18:00", unit="TASK", kicker="PRACTICAL AI",
 head=["Use AI To Walk", "Into Any Interview", "Prepared"],
 sub=["Four prompts that replace hours of", "guessing what they will ask and how", "to answer."],
 slides=[
  B("01", ["Decode The", "Job Post"], ["Find out what they really want hidden", "behind the buzzwords."],
    ["\"Here is a job post: [paste]. List the", "5 skills that matter most, and the", "3 things they are quietly worried", "about in a hire.\""]),
  B("02", ["Practice The", "Hard Questions"], ["Get asked one at a time, with honest", "feedback on each answer."],
    ["\"Act as an interviewer for [role]. Ask me", "one question at a time. After each", "answer, score it out of 10 and say", "how to improve it.\""]),
  B("03", ["Turn Experience", "Into Stories"], ["Your past work is the answer. It just", "needs a shape."],
    ["\"Turn this experience into a 90-second", "story: situation, action, result. Make", "the result measurable: [paste your", "experience].\""]),
  B("04", ["Ask Smart", "Questions Back"], ["The last question you ask is the one", "they remember."],
    ["\"I am interviewing for [role] at [company].", "Give me 5 thoughtful questions to ask", "that show I understand their", "challenges.\""]),
 ],
 cta_head=["Interview Coming", "Up?"], cta_sub=["Save this for the night before —", "then send it to someone job hunting", "right now."],
 hook="Most people prepare answers. Few prepare for the questions behind the questions.",
 items=["Decode the job post", "Practice the hard questions", "Turn experience into stories", "Ask smart questions back"],
 ask="Got an interview coming up? Comment the number you will try 👇",
 tags="#LearnAIWithDoyin #PracticalAI #JobSearch #InterviewTips #CareerGrowth"))

# ---------- D3 A: concept — hallucination ----------
C.append(dict(id="d3a", date="2026-11-11", time="08:00", unit="CONCEPT", kicker="AI CONCEPTS",
 head=["Why AI Makes", "Things Up", "(And What To Do)"],
 sub=["It is called a hallucination. Here is", "why it happens and how to protect", "yourself."],
 slides=[
  B("01", ["It Predicts,", "It Does Not Know"], ["AI guesses the most likely next words.", "Sounding right and being right are", "different things."],
    ["\"Explain why a language model can state", "something false with total confidence.", "Use a simple analogy.\""], label="TRY IT YOURSELF"),
  B("02", ["Gaps Get", "Filled In"], ["Ask about something obscure or recent", "and it may invent a plausible answer."],
    ["\"What do you not know well? List the", "topics where you are most likely to", "give me a wrong answer.\""], label="TRY IT YOURSELF"),
  B("03", ["Make It Show", "Its Work"], ["Asking for sources and reasoning", "exposes weak answers fast."],
    ["\"Answer this, then list the claims you", "are least sure about and what I should", "verify elsewhere: [question].\""], label="TRY IT YOURSELF"),
  B("04", ["Verify What", "Matters"], ["Names, numbers, quotes, and laws deserve", "a second source every time."],
    ["\"List every statistic, name, and date in", "your last answer so I can check each", "one against a trusted source.\""], label="TRY IT YOURSELF"),
 ],
 cta_head=["Trust, But", "Verify"], cta_sub=["Save this before you paste an AI", "answer into something important —", "then send it to a colleague."],
 hook="AI can be wrong and sound completely sure. Here is the fix.",
 items=["It predicts, it does not know", "Gaps get filled in", "Make it show its work", "Verify what matters"],
 ask="Has AI ever confidently told you something wrong? Tell me below 👇",
 tags="#LearnAIWithDoyin #AIConcepts #AIHallucination #AIForBeginners #CriticalThinking"))

# ---------- D3 B: practical — spreadsheets ----------
C.append(dict(id="d3b", date="2026-11-11", time="18:00", unit="TASK", kicker="PRACTICAL AI",
 head=["Make Spreadsheets", "Easy With AI"],
 sub=["No formulas to memorize. Describe what", "you want and let AI build it."],
 slides=[
  B("01", ["Describe It,", "Get The Formula"], ["Plain English in, working Excel or", "Google Sheets formula out."],
    ["\"Write a Google Sheets formula that sums", "column C only when column A says", "'Paid' and column B is this month.", "Explain how it works.\""]),
  B("02", ["Clean Messy", "Data Fast"], ["Duplicates, odd spacing, mixed date", "formats. Fixed in one pass."],
    ["\"Here is a sample of my data: [paste].", "Give me steps to remove duplicates,", "trim spaces, and standardize dates in", "Excel.\""]),
  B("03", ["Build A Budget", "Template"], ["Start from a working layout instead", "of a blank sheet."],
    ["\"Design a monthly budget sheet with", "income, fixed costs, variable costs,", "and a savings tracker. List the", "columns and formulas.\""]),
  B("04", ["Explain A", "Formula You Inherited"], ["Understand someone else's sheet before", "you break it."],
    ["\"Explain this formula step by step in", "plain English: [paste formula]. Then", "suggest a simpler way to write it.\""]),
 ],
 cta_head=["Which Sheet Are", "You Fixing First?"], cta_sub=["Save this for your next spreadsheet", "headache — then send it to the", "person who owns the budget file."],
 hook="You do not need to memorize formulas anymore. You need to describe the result.",
 items=["Describe it, get the formula", "Clean messy data fast", "Build a budget template", "Explain an inherited formula"],
 ask="Which spreadsheet problem is yours? Comment the number 👇",
 tags="#LearnAIWithDoyin #PracticalAI #Excel #GoogleSheets #Productivity"))

# ---------- D4 A: tools — visuals ----------
C.append(dict(id="d4a", date="2026-11-12", time="08:00", unit="TOOL", kicker="AI TOOLS",
 head=["4 AI Tools For", "Visuals Without", "A Designer"],
 sub=["Posters, product shots, social graphics.", "Pick the right one for the job."],
 slides=[
  T("01", "Canva", "C", "#4a90e2", ["Fast, clean graphics and", "social posts"],
    ["Turn a text prompt into a design", "Resize one post for every platform", "Keep your brand colors consistent"]),
  T("02", "Midjourney", "M", "#c86dd7", ["Striking, artistic images", "from a short prompt"],
    ["Create concept art for a project", "Explore moods and styles quickly", "Make a hero image for a page"]),
  T("03", "Adobe Firefly", "F", "#f0a04b", ["Editing and extending", "existing photos"],
    ["Remove an object from a photo", "Extend a background to fit a new size", "Generate variations of one image"]),
  T("04", "Ideogram", "I", "#3bbfad", ["Images that include", "readable text"],
    ["Design a poster with a real headline", "Create a logo concept with lettering", "Make a quote graphic in seconds"]),
 ],
 cta_head=["Which One Fits", "Your Work?"], cta_sub=["Save this before you pay a designer", "for a first draft — then send it to", "a small business owner."],
 hook="You do not need a designer for a first draft anymore. You need the right tool.",
 items=["Canva: fast, clean graphics", "Midjourney: striking artistic images", "Adobe Firefly: edit and extend photos", "Ideogram: images with readable text"],
 ask="Which one do you want to try? Comment the number 👇",
 tags="#LearnAIWithDoyin #AITools #AIDesign #Canva #ContentCreation"))

# ---------- D4 B: concept — context window ----------
C.append(dict(id="d4b", date="2026-11-12", time="18:00", unit="CONCEPT", kicker="AI CONCEPTS",
 head=["The Context Window", "Explained"],
 sub=["Why AI forgets what you said earlier", "and how to work around it."],
 slides=[
  B("01", ["AI Has Short-Term", "Memory Only"], ["The context window is everything the", "model can see in one conversation."],
    ["\"Explain a context window using the", "analogy of a desk: what fits on it,", "and what falls off the edge.\""], label="TRY IT YOURSELF"),
  B("02", ["Why It Forgets", "Your Instructions"], ["Long chats push early messages out of", "view. Your first rule quietly vanishes."],
    ["\"Here are my rules for this chat: [rules].", "Repeat them back to me every 10", "messages so we do not drift.\""], label="TRY IT YOURSELF"),
  B("03", ["Summarize To", "Reset"], ["Compress a long chat into a short", "brief and start fresh with it."],
    ["\"Summarize our conversation in 10 bullets:", "decisions made, open questions, and", "my preferences. I will paste it into", "a new chat.\""], label="TRY IT YOURSELF"),
  B("04", ["Bigger Is Not", "Always Better"], ["A huge window can still miss details", "buried in the middle. Be specific."],
    ["\"From the document above, find the exact", "paragraph about [topic] and quote it,", "then answer using only that.\""], label="TRY IT YOURSELF"),
 ],
 cta_head=["Which Idea Changes", "How You Chat?"], cta_sub=["Save this for your next long AI", "session — then send it to someone", "who says AI keeps forgetting."],
 hook="If AI keeps forgetting what you told it, this is why.",
 items=["AI has short-term memory only", "Why it forgets your instructions", "Summarize to reset", "Bigger is not always better"],
 ask="Which one changes how you use AI chats? Comment the number 👇",
 tags="#LearnAIWithDoyin #AIConcepts #ContextWindow #AIForBeginners #LLM"))

# ---------- D5 A: practical — posts that sound like you ----------
C.append(dict(id="d5a", date="2026-11-13", time="08:00", unit="TASK", kicker="PRACTICAL AI",
 head=["Write Posts That", "Sound Like You,", "Not Like A Robot"],
 sub=["Four prompts to keep your voice while", "AI does the heavy lifting."],
 slides=[
  B("01", ["Teach It", "Your Voice"], ["Show it real examples first so it", "copies how you actually write."],
    ["\"Here are 3 posts I wrote: [paste].", "Describe my tone, sentence length,", "and favorite phrases in 5 bullets.\""]),
  B("02", ["Turn One Idea", "Into Five Posts"], ["One thought, many angles. Never face", "a blank page again."],
    ["\"Using my voice, turn this idea into 5", "different posts: a story, a tip, a", "question, a myth, a lesson: [idea].\""]),
  B("03", ["Cut The", "AI Fluff"], ["Delete the filler phrases that give", "machine writing away."],
    ["\"Edit this draft: remove clichés, buzzwords,", "and 'in today's world'. Keep my meaning", "and make it sound spoken: [draft].\""]),
  B("04", ["Write A Hook That", "Stops The Scroll"], ["The first line decides if anyone reads", "the second."],
    ["\"Give me 10 opening lines for a post about", "[topic]. Mix a bold claim, a question,", "and a surprising number.\""]),
 ],
 cta_head=["Which Prompt Fits", "Your Voice?"], cta_sub=["Save this before your next post —", "then send it to a creator who sounds", "a bit too much like AI."],
 hook="AI should sound like you, not like everyone else using AI.",
 items=["Teach it your voice", "Turn one idea into five posts", "Cut the AI fluff", "Write a hook that stops the scroll"],
 ask="Which one will you try first? Comment the number 👇",
 tags="#LearnAIWithDoyin #PracticalAI #ContentCreation #PersonalBrand #AIWriting"))

# ---------- D5 B: tools — video and audio ----------
C.append(dict(id="d5b", date="2026-11-13", time="18:00", unit="TOOL", kicker="AI TOOLS",
 head=["4 AI Tools For", "Video And Audio", "Creators"],
 sub=["Edit, narrate, and publish without a", "studio or a big team."],
 slides=[
  T("01", "ElevenLabs", "E", "#8e7cf0", ["Natural-sounding voiceovers", "from plain text"],
    ["Narrate a video from a script", "Create audio versions of articles", "Try a new voice style in seconds"]),
  T("02", "Descript", "D", "#4a90e2", ["Editing video by editing", "the transcript"],
    ["Delete a sentence, cut the clip", "Remove filler words in one click", "Clean up recorded audio"]),
  T("03", "CapCut", "C", "#3bbfad", ["Short-form clips with", "auto captions"],
    ["Add captions to a Reel automatically", "Cut a long video into short clips", "Use templates for quick edits"]),
  T("04", "HeyGen", "H", "#f0a04b", ["Talking avatar videos", "from a script"],
    ["Turn a script into a presenter video", "Translate a video into other languages", "Create training or explainer clips"]),
 ],
 cta_head=["Which Would Save", "You The Most Time?"], cta_sub=["Save this before your next video", "project — then send it to a creator", "who edits at midnight."],
 hook="Editing used to be the slowest part of making video. Not anymore.",
 items=["ElevenLabs: voiceovers from text", "Descript: edit by editing the transcript", "CapCut: short clips with auto captions", "HeyGen: talking avatar videos"],
 ask="Which one would save you the most time? Comment the number 👇",
 tags="#LearnAIWithDoyin #AITools #VideoEditing #ContentCreation #AIVideo"))

# ---------- D6 A: concept — RAG ----------
C.append(dict(id="d6a", date="2026-11-14", time="08:00", unit="CONCEPT", kicker="AI CONCEPTS",
 head=["What Is RAG?", "How AI Uses", "Your Documents"],
 sub=["The idea behind \"chat with your PDF\"", "tools. Four steps, plain English."],
 slides=[
  B("01", ["The Problem", "RAG Solves"], ["AI only knows what it was trained on.", "It has never seen your files."],
    ["\"Explain why an AI model cannot answer", "questions about my company's private", "documents without extra help.\""], label="TRY IT YOURSELF"),
  B("02", ["Step One:", "Find The Right Pages"], ["Your question is matched to the most", "relevant chunks of your documents."],
    ["\"Explain how a search system finds the", "most relevant paragraphs in a large", "document. Use a library analogy.\""], label="TRY IT YOURSELF"),
  B("03", ["Step Two:", "Hand Them To The AI"], ["Those chunks are added to your question", "so the answer is grounded in your data."],
    ["\"Show a simple example: a question, the", "retrieved paragraphs, and the answer", "an AI would write from them.\""], label="TRY IT YOURSELF"),
  B("04", ["Why It Beats", "Retraining"], ["Update a document and the answers", "update. No expensive retraining needed."],
    ["\"Compare RAG with fine-tuning a model", "on cost, speed, and accuracy. Give me", "a table and a recommendation.\""], label="TRY IT YOURSELF"),
 ],
 cta_head=["Which Step Made", "It Click?"], cta_sub=["Save this the next time someone says", "\"RAG\" in a meeting — then send it", "to a teammate who nodded along."],
 hook="\"Chat with your PDF\" tools all use one idea. Here it is in four steps.",
 items=["The problem RAG solves", "Step one: find the right pages", "Step two: hand them to the AI", "Why it beats retraining"],
 ask="Which step made it click? Comment the number 👇",
 tags="#LearnAIWithDoyin #AIConcepts #RAG #AIForBeginners #GenerativeAI"))

# ---------- D6 B: practical — learn a skill ----------
C.append(dict(id="d6b", date="2026-11-14", time="18:00", unit="TASK", kicker="PRACTICAL AI",
 head=["Learn Any Skill", "In 30 Days With AI"],
 sub=["Four prompts that turn \"someday I will", "learn that\" into a daily routine."],
 slides=[
  B("01", ["Build Your", "30-Day Roadmap"], ["Start with a plan sized to the time", "you actually have."],
    ["\"I want to learn [skill] in 30 days with", "30 minutes a day. Build a day-by-day", "plan, ending in one real project.\""]),
  B("02", ["Find Your", "Starting Level"], ["Skip what you know. Focus on what you", "do not."],
    ["\"Ask me 8 questions to find my level in", "[skill]. Then tell me where to begin", "and what to skip.\""]),
  B("03", ["Practice With", "A Coach"], ["Get feedback on real attempts, not", "just explanations."],
    ["\"Act as my [skill] coach. Give me one", "exercise, wait for my attempt, then", "critique it and set the next one.\""]),
  B("04", ["Test What", "Actually Stuck"], ["Retrieval beats rereading. Quiz yourself", "weekly."],
    ["\"Quiz me on what I covered this week:", "[topics]. Mix easy and hard. Mark my", "answers and re-teach what I missed.\""]),
 ],
 cta_head=["What Will You", "Learn First?"], cta_sub=["Save this and start tonight — then", "send it to someone with a skill on", "their someday list."],
 hook="30 minutes a day for 30 days beats a year of \"someday\".",
 items=["Build your 30-day roadmap", "Find your starting level", "Practice with a coach", "Test what actually stuck"],
 ask="What skill are you learning? Tell me below 👇",
 tags="#LearnAIWithDoyin #PracticalAI #LearnNewSkills #SelfImprovement #AIForBeginners"))

# ---------- D7 A: tools — build apps ----------
C.append(dict(id="d7a", date="2026-11-15", time="08:00", unit="TOOL", kicker="AI TOOLS",
 head=["4 AI Tools To Build", "An App Without", "Coding"],
 sub=["Describe your idea. Watch it become", "something you can click and share."],
 slides=[
  T("01", "Lovable", "L", "#c86dd7", ["Full web apps from a", "plain-English description"],
    ["Describe an app, get a live preview", "Add a database and login", "Publish it with a shareable link"]),
  T("02", "Bolt", "B", "#4a90e2", ["Fast prototypes straight", "in the browser"],
    ["Turn a sketch into a working page", "Test a product idea in an hour", "Edit by chatting with it"]),
  T("03", "Cursor", "C", "#3bbfad", ["Writing code with an AI", "pair programmer"],
    ["Ask it to explain unfamiliar code", "Generate a function from a comment", "Fix bugs by describing them"]),
  T("04", "Replit", "R", "#f0a04b", ["Building and hosting in one", "place"],
    ["Start a project from a prompt", "Run and share it without setup", "Learn by editing working code"]),
 ],
 cta_head=["What Would You", "Build First?"], cta_sub=["Save this for when the idea won't", "leave you alone — then send it to", "someone who says \"I can't code\"."],
 hook="\"I can't code\" is not a blocker anymore. It is a starting point.",
 items=["Lovable: full web apps from a description", "Bolt: fast prototypes in the browser", "Cursor: an AI pair programmer", "Replit: build and host in one place"],
 ask="What would you build first? Tell me below 👇",
 tags="#LearnAIWithDoyin #AITools #NoCode #VibeCoding #BuildInPublic"))

# ---------- D7 B: practical — small business admin ----------
C.append(dict(id="d7b", date="2026-11-15", time="18:00", unit="TASK", kicker="PRACTICAL AI",
 head=["Run Your Small", "Business Admin", "With AI"],
 sub=["Four prompts for the jobs that eat", "your evenings."],
 slides=[
  B("01", ["Answer Customers", "In Your Tone"], ["Draft replies to common questions once,", "reuse them forever."],
    ["\"Write friendly replies to these 5 common", "customer questions: [list]. Keep each", "under 60 words and sign off as", "[name].\""]),
  B("02", ["Write Product", "Descriptions"], ["Turn rough notes into copy that sells", "without sounding generic."],
    ["\"Write a 50-word description for [product].", "Features: [list]. Audience: [who]. Tone:", "warm and clear. No hype words.\""]),
  B("03", ["Plan A Month", "Of Content"], ["A calendar with ideas, not blanks."],
    ["\"Create a 4-week content plan for a [type]", "business. 3 posts a week: one teaching,", "one proof, one offer.\""]),
  B("04", ["Chase Invoices", "Politely"], ["Get paid without the awkward email."],
    ["\"Write 3 follow-up emails for an unpaid", "invoice: a gentle nudge, a firm reminder,", "and a final notice. Keep each polite.\""]),
 ],
 cta_head=["Which Task Do You", "Hate Most?"], cta_sub=["Save this for your next admin night", "— then send it to a business owner", "who still does it all by hand."],
 hook="Admin is where small business owners lose their evenings. Hand it to AI.",
 items=["Answer customers in your tone", "Write product descriptions", "Plan a month of content", "Chase invoices politely"],
 ask="Which task do you hate most? Comment the number 👇",
 tags="#LearnAIWithDoyin #PracticalAI #SmallBusiness #Entrepreneur #AIForBusiness"))


def fb_caption(c):
    lines = [c["hook"], "", ]
    for i, t in enumerate(c["items"], 1):
        lines.append(f"0{i} | {t}")
    lines += ["", "Save this and send it to someone who needs it.", "", c["ask"], "", c["tags"]]
    return "\n".join(lines)

def li_caption(c):
    lines = [c["hook"], "", "In this carousel:"]
    for t in c["items"]:
        lines.append(f"→ {t}")
    lines += ["", "Save it for later and share it with someone on your team.", "",
              c["ask"].replace(" 👇", "").replace("Comment the number", "Tell me which number in the comments") if False else
              c["ask"].replace(" 👇", ""),
              "", " ".join(c["tags"].split()[:4])]
    return "\n".join(lines)


if __name__ == "__main__":
    only = sys.argv[1:]
    bg = build_background()
    manifest = []
    for c in C:
        if only and c["id"] not in only:
            continue
        d = f"{ROOT}/{c['date']}_{c['time'].replace(':','')}_{c['id']}"
        os.makedirs(d, exist_ok=True)
        for name, svg in build(c):
            png = cairosvg.svg2png(bytestring=svg.encode(), output_width=W, output_height=H)
            layer = Image.open(io.BytesIO(png)).convert("RGBA")
            Image.alpha_composite(bg.copy(), layer).convert("RGB").save(f"{d}/{name}.png", optimize=True)
        open(f"{d}/caption_facebook.txt", "w").write(fb_caption(c))
        open(f"{d}/caption_linkedin.txt", "w").write(li_caption(c))
        manifest.append({"id": c["id"], "date": c["date"], "time": c["time"], "dir": os.path.basename(d)})
        print("rendered", c["id"])
    json.dump(manifest, open(f"{ROOT}/manifest.json", "w"), indent=1)
