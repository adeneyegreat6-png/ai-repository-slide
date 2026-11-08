#!/usr/bin/env python3
import sys, os, io, json
sys.path.insert(0, "/home/claude/ai-repository-slide/tools")
from core import cover_slide, body_slide, tool_slide, cta_slide, build_background
import cairosvg
from PIL import Image

W, H = 1080, 1350
ROOT = "/home/claude/ai-repository-slide/slides"
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
TRY = "TRY IT YOURSELF"
def add(id, date, time, unit, kicker, head, sub, slides, cta_head, cta_sub, hook, items, ask, tags):
    C.append(dict(id=id, date=date, time=time, unit=unit, kicker=kicker, head=head, sub=sub, slides=slides,
                  cta_head=cta_head, cta_sub=cta_sub, hook=hook, items=items, ask=ask, tags=tags))
PA, CO, TO = "PRACTICAL AI", "AI CONCEPTS", "AI TOOLS"

add("e1a","2026-11-16","08:00","TASK",PA,["Clear Your Inbox","Faster With AI"],
 ["Four prompts for the emails that","pile up while you work."],
 [B("01",["Sort By Urgency"],["Know what needs you today and what","can wait."],
    ["\"Here are my unread emails: [paste].","Sort them into Reply Today, Reply","This Week, and No Reply Needed.\""]),
  B("02",["Reply In One","Minute"],["Give AI the point, keep your voice."],
    ["\"Reply to this email: [paste]. My answer","is [yes/no/maybe + reason]. Keep it","under 80 words and polite.\""]),
  B("03",["Say No Without","The Guilt"],["Decline clearly, keep the relationship."],
    ["\"Write a kind way to decline [request].","Give one short reason and offer an","alternative. Keep it under 70 words.\""]),
  B("04",["Follow Up Without","Nagging"],["Get the answer you are waiting for."],
    ["\"Write 2 follow-up emails for [topic]","sent [X] days ago. One friendly, one","direct. Keep each under 60 words.\""])],
 ["Which Email Do You","Dread Most?"],["Save this for Monday morning —","then send it to a colleague who","lives in their inbox."],
 "Your inbox is not a to-do list. Stop letting it run your day.",
 ["Sort by urgency","Reply in one minute","Say no without the guilt","Follow up without nagging"],
 "Which one will you try first? Comment the number 👇",
 "#LearnAIWithDoyin #PracticalAI #Productivity #EmailTips #AIForBeginners")

add("e1b","2026-11-16","18:00","CONCEPT",CO,["What Is An","AI Agent?"],
 ["A chatbot answers. An agent acts.","Four ideas, no jargon."],
 [B("01",["Agents Take","Steps"],["An agent plans, uses tools, and works","toward a goal, not just one reply."],
    ["\"Explain the difference between a chatbot","and an AI agent using a travel booking","example.\""],label=TRY),
  B("02",["Tools Are The","Hands"],["Agents can search, read files, or run","code when they are given access."],
    ["\"List 4 tools an AI agent might use to","research a topic, and what each one is","for.\""],label=TRY),
  B("03",["Loops, Not","One Shot"],["It tries, checks the result, and","adjusts before it finishes."],
    ["\"Describe how an agent checks its own","work in a loop. Use a simple everyday","example.\""],label=TRY),
  B("04",["Humans Still","Check The Work"],["More autonomy means review matters","more, not less."],
    ["\"What tasks are safe to delegate to an","AI agent, and which ones should I","always review myself?\""],label=TRY)],
 ["Which Idea Was","New To You?"],["Save this for the next time someone","says agents — then send it to a","curious friend."],
 "Everyone says AI agents. Few can explain what one actually is.",
 ["Agents take steps","Tools are the hands","Loops, not one shot","Humans still check the work"],
 "Which idea was new to you? Comment the number 👇",
 "#LearnAIWithDoyin #AIConcepts #AIAgents #AIExplained #AIForBeginners")

add("e2a","2026-11-17","08:00","TOOL",TO,["4 AI Tools That","Improve Your","Writing"],
 ["Clearer sentences, fewer typos, and","faster first drafts."],
 [T("01","Grammarly","G","#3bbfad",["Catching errors and","tightening tone"],
    ["Fixes spelling and grammar as you type","Suggests clearer phrasing","Works inside email and browser"]),
  T("02","Claude","C","#f0a04b",["Drafting and editing","longer pieces"],
    ["Turn rough notes into a first draft","Ask for a shorter or warmer version","Get feedback on structure"]),
  T("03","ChatGPT","C","#4a90e2",["Brainstorming and","rewriting text"],
    ["Generate headline and angle ideas","Rewrite for a different audience","Summarize long drafts"]),
  T("04","Hemingway Editor","H","#8e7cf0",["Spotting hard-to-read","sentences"],
    ["Highlights long, complex sentences","Flags passive voice","Helps you write plainly"])],
 ["Which One Will","You Test First?"],["Save this before your next draft —","then send it to someone who writes","for work."],
 "Good writing is mostly editing. These tools make editing faster.",
 ["Grammarly","Claude","ChatGPT","Hemingway Editor"],
 "Which one will you test? Comment the number 👇",
 "#LearnAIWithDoyin #AITools #WritingTips #Productivity #AIForBeginners")

add("e2b","2026-11-17","18:00","TASK",PA,["Make Better","Decisions With AI"],
 ["Use AI as a sparring partner, not","the decision-maker."],
 [B("01",["List The Options"],["Lay everything out before you choose."],
    ["\"I am deciding between [A] and [B].","List pros, cons, and risks of each","in a simple table.\""]),
  B("02",["Argue The","Other Side"],["Test your own thinking for blind spots."],
    ["\"I am leaning toward [choice]. Argue","against it as strongly as you can,","then tell me what I may be missing.\""]),
  B("03",["Ask What","You Have Not Asked"],["Find the question hiding in the problem."],
    ["\"What questions should I answer before","deciding on [topic]? List the 5 most","important ones.\""]),
  B("04",["Set A Decision","Rule"],["Decide how you will decide."],
    ["\"Help me write 3 criteria for choosing","[topic], ranked by importance, so I can","score each option.\""])],
 ["What Decision Are","You Putting Off?"],["Save this for the next big choice —","then send it to someone stuck","between two options."],
 "Most bad decisions are not bad logic. They are missing perspective.",
 ["List the options","Argue the other side","Ask what you have not asked","Set a decision rule"],
 "Which one will you try first? Comment the number 👇",
 "#LearnAIWithDoyin #PracticalAI #DecisionMaking #Productivity #AIForBeginners")

add("e3a","2026-11-18","08:00","CONCEPT",CO,["What Does","Temperature Do?"],
 ["The setting that makes AI more","predictable or more creative."],
 [B("01",["A Dial For","Randomness"],["Temperature controls how much a model","varies its word choices."],
    ["\"Explain AI temperature settings like I am","12, using a dice or ice cream","analogy.\""],label=TRY),
  B("02",["Low Means","Predictable"],["Good for facts, summaries, and","consistent answers."],
    ["\"Give an example of a task where a low","temperature is the better choice, and","explain why.\""],label=TRY),
  B("03",["High Means","More Varied"],["Good for brainstorming, naming, and","creative writing."],
    ["\"Give an example of a task where a high","temperature helps, and what could go","wrong.\""],label=TRY),
  B("04",["Not Always","Adjustable"],["Many apps hide it. You can still steer","with how you prompt."],
    ["\"Rewrite this prompt to get more varied","ideas without changing a setting:","[paste prompt].\""],label=TRY)],
 ["Which Idea Was","New To You?"],["Save this for when answers feel too","repetitive or too wild — then send","it to a friend."],
 "Ever noticed AI give a different answer to the same question?",
 ["A dial for randomness","Low means predictable","High means more varied","Not always adjustable"],
 "Which idea was new to you? Comment the number 👇",
 "#LearnAIWithDoyin #AIConcepts #AIExplained #LLM #AIForBeginners")

add("e3b","2026-11-18","18:00","TASK",PA,["Study Smarter","With AI"],
 ["Four prompts for learning faster","and remembering more."],
 [B("01",["Explain It","Simply"],["Get a clear picture before the details."],
    ["\"Explain [topic] in plain language, then","give one real-world example and one","common misunderstanding.\""]),
  B("02",["Quiz Yourself"],["Testing beats rereading."],
    ["\"Ask me 5 questions on [topic], one at a","time. Wait for my answer, then correct","me and explain.\""]),
  B("03",["Build A Study","Schedule"],["Spread the work so it sticks."],
    ["\"I have [X] days until my exam on [topic].","Make a daily plan with short sessions","and review days.\""]),
  B("04",["Find Your","Weak Spots"],["Focus time where it matters."],
    ["\"Here are my notes: [paste]. What are the","5 concepts I am most likely to confuse?","Test me on them.\""])],
 ["Which Prompt Is","Your Favorite?"],["Save this before exam season —","then send it to a student you","know."],
 "Rereading your notes feels like studying. It mostly is not.",
 ["Explain it simply","Quiz yourself","Build a study schedule","Find your weak spots"],
 "Which one will you try first? Comment the number 👇",
 "#LearnAIWithDoyin #PracticalAI #StudyTips #Students #AIForBeginners")

add("e4a","2026-11-19","08:00","TOOL",TO,["4 AI Tools For","Better Slides"],
 ["Go from blank page to a draft deck","in minutes."],
 [T("01","Gamma","G","#8e7cf0",["Generating a full deck","from a prompt"],
    ["Describe a topic, get a first draft","Edit layouts and text easily","Share as a link or export"]),
  T("02","Canva","C","#3bbfad",["Designing clean visuals","without a designer"],
    ["Large library of presentation templates","Drag-and-drop editing","Includes AI-assisted design features"]),
  T("03","Microsoft Copilot","M","#4a90e2",["Building slides inside","PowerPoint"],
    ["Draft slides from a document","Rework text and structure","Stays inside your Microsoft apps"]),
  T("04","Beautiful.ai","B","#f0a04b",["Keeping layouts tidy","automatically"],
    ["Smart templates adjust as you edit","Helps keep spacing consistent","Good for clean business decks"])],
 ["Which One Will","You Test First?"],["Save this before your next presentation","— then send it to someone who hates","making slides."],
 "The hardest slide is the first one. Let AI draft it for you.",
 ["Gamma","Canva","Microsoft Copilot","Beautiful.ai"],
 "Which one will you test? Comment the number 👇",
 "#LearnAIWithDoyin #AITools #Presentations #Productivity #AIForBeginners")

add("e4b","2026-11-19","18:00","CONCEPT",CO,["Fine-Tuning Or","Better Prompts?"],
 ["Two ways to improve AI results.","Know which one you need."],
 [B("01",["Prompting Changes","The Input"],["You guide the model with clearer","instructions and examples."],
    ["\"Explain prompting versus fine-tuning with","a cooking analogy. Keep it under 100","words.\""],label=TRY),
  B("02",["Fine-Tuning Changes","The Model"],["The model is trained further on","specific examples."],
    ["\"What does it mean to fine-tune a model?","Describe it simply, with one example.\""],label=TRY),
  B("03",["Start With","Prompting"],["It is faster, cheaper, and enough for","most everyday needs."],
    ["\"Give me 3 signs that better prompting","would solve my problem before I need","fine-tuning.\""],label=TRY),
  B("04",["When Tuning","Makes Sense"],["Consistent style or specialized tasks","at larger scale."],
    ["\"List 3 situations where fine-tuning a","model is worth the extra effort.\""],label=TRY)],
 ["Which Idea Was","New To You?"],["Save this before you chase a","complicated fix — then send it to","a builder friend."],
 "Before you train a model, try asking it better.",
 ["Prompting changes the input","Fine-tuning changes the model","Start with prompting","When tuning makes sense"],
 "Which idea was new to you? Comment the number 👇",
 "#LearnAIWithDoyin #AIConcepts #FineTuning #PromptEngineering #AIExplained")

add("e5a","2026-11-20","08:00","TASK",PA,["Win More Freelance","Work With AI"],
 ["Four prompts for pitching, scoping,","and getting paid."],
 [B("01",["Read The Brief","Properly"],["Spot what the client really wants."],
    ["\"Here is a client brief: [paste]. List the","goals, unclear points, and 5 questions","I should ask before quoting.\""]),
  B("02",["Write A Short","Proposal"],["Clear, confident, and easy to say yes to."],
    ["\"Write a one-page proposal for [project].","Include scope, timeline, and next","steps. Keep the tone professional.\""]),
  B("03",["Define The","Scope"],["Prevent surprise extra work."],
    ["\"List what is included and not included","in this project: [describe]. Add a clause","for extra revisions.\""]),
  B("04",["Ask For Feedback","And Referrals"],["Turn finished work into new work."],
    ["\"Write a polite message asking [client]","for a short testimonial and an intro","to others who might need my help.\""])],
 ["Which One Will","You Use First?"],["Save this for your next pitch —","then send it to a freelancer","you know."],
 "Freelancing is half the work and half the paperwork. Fix the paperwork.",
 ["Read the brief properly","Write a short proposal","Define the scope","Ask for feedback and referrals"],
 "Which one will you try first? Comment the number 👇",
 "#LearnAIWithDoyin #PracticalAI #Freelancing #SideHustle #AIForBeginners")

add("e5b","2026-11-20","18:00","TOOL",TO,["4 AI Tools For","Meeting Notes"],
 ["Stop typing while you should be","listening."],
 [T("01","Otter","O","#4a90e2",["Live transcripts and","summaries"],
    ["Transcribes conversations in real time","Generates summaries afterward","Lets you search past meetings"]),
  T("02","Fireflies","F","#8e7cf0",["Recording and searching","meeting history"],
    ["Joins calls to capture the discussion","Pulls out action items","Search across all your meetings"]),
  T("03","Fathom","F","#3bbfad",["Quick call summaries","you can share"],
    ["Records and summarizes video calls","Highlight key moments","Share notes after the call"]),
  T("04","Zoom AI Companion","Z","#f0a04b",["Summaries inside","Zoom itself"],
    ["Summarizes meetings you host in Zoom","Helps you catch up if you join late","No extra app to add"])],
 ["Which One Will","You Test First?"],["Save this before your next meeting —","then send it to someone drowning in","calls."],
 "If you cannot remember what was said, the meeting did not happen.",
 ["Otter","Fireflies","Fathom","Zoom AI Companion"],
 "Which one will you test? Comment the number 👇",
 "#LearnAIWithDoyin #AITools #Meetings #Productivity #AIForBeginners")

add("e6a","2026-11-21","08:00","CONCEPT",CO,["Can AI Be","Biased?"],
 ["Yes. Here is where it comes from","and what you can do."],
 [B("01",["It Learns From","Human Data"],["Models reflect patterns in the text","and images they were trained on."],
    ["\"Explain in simple terms how bias can","appear in AI systems that learn from","human-written data.\""],label=TRY),
  B("02",["Bias Is Not","Always Obvious"],["It can show up in tone, examples, or","who gets left out."],
    ["\"Give 3 subtle examples of how an AI","answer could leave out or stereotype","a group of people.\""],label=TRY),
  B("03",["You Can","Spot It"],["Ask the same question in different ways","and compare answers."],
    ["\"Review your last answer for assumptions.","What perspectives might be missing?\""],label=TRY),
  B("04",["Keep A Human","In The Loop"],["Check important outputs, especially","about people."],
    ["\"List 4 checks I should run before using","AI output in hiring, grading, or","decisions about people.\""],label=TRY)],
 ["Which Idea Was","New To You?"],["Save this before you trust an answer","blindly — then send it to a friend","who uses AI daily."],
 "AI does not have opinions. It does inherit patterns. Those are different.",
 ["It learns from human data","Bias is not always obvious","You can spot it","Keep a human in the loop"],
 "Which idea was new to you? Comment the number 👇",
 "#LearnAIWithDoyin #AIConcepts #ResponsibleAI #AIEthics #AIExplained")

add("e6b","2026-11-21","18:00","TASK",PA,["Repurpose One","Idea Four Ways"],
 ["Create once. Publish in several","formats."],
 [B("01",["Article To","Social Posts"],["Pull the best points out of long writing."],
    ["\"From this article: [paste]. Write 3","short social posts, each with one","clear takeaway.\""]),
  B("02",["Post To","Newsletter"],["Expand a good idea into a full note."],
    ["\"Turn this post into a 200-word email","newsletter with a subject line and","one call to action: [paste].\""]),
  B("03",["Talk To","Checklist"],["Turn a recording into something usable."],
    ["\"From this transcript: [paste]. Create a","step-by-step checklist of the main","advice, in plain language.\""]),
  B("04",["Idea To","Carousel Outline"],["Plan slides before you design them."],
    ["\"Turn this idea into a 6-slide carousel","outline: a hook, 4 points, and a","closing question: [idea].\""])],
 ["Which One Will","You Try First?"],["Save this for your next piece of content","— then send it to a creator who","starts from scratch every time."],
 "You do not need more ideas. You need more formats for the ones you have.",
 ["Article to social posts","Post to newsletter","Talk to checklist","Idea to carousel outline"],
 "Which one will you try first? Comment the number 👇",
 "#LearnAIWithDoyin #PracticalAI #ContentCreation #ContentStrategy #AIForBeginners")

add("e7a","2026-11-22","08:00","TOOL",TO,["4 AI Coding","Assistants"],
 ["Build, fix, and learn code with","help beside you."],
 [T("01","GitHub Copilot","G","#8e7cf0",["Suggestions inside","your editor"],
    ["Completes code as you type","Explains unfamiliar code","Works in popular editors"]),
  T("02","Cursor","C","#4a90e2",["An editor built around","AI"],
    ["Chat with your codebase","Edit multiple files with prompts","Based on a familiar code editor"]),
  T("03","Claude","C","#f0a04b",["Explaining and debugging","code"],
    ["Paste an error, ask what it means","Request plain-English walkthroughs","Draft functions and tests"]),
  T("04","Replit","R","#3bbfad",["Building and running","in the browser"],
    ["Write and run code with no setup","Share projects with a link","Good for quick experiments"])],
 ["Which One Will","You Test First?"],["Save this before your next project —","then send it to someone learning to","code."],
 "You do not have to memorize syntax anymore. You do have to understand it.",
 ["GitHub Copilot","Cursor","Claude","Replit"],
 "Which one will you test? Comment the number 👇",
 "#LearnAIWithDoyin #AITools #Coding #LearnToCode #AIForBeginners")

add("e7b","2026-11-22","18:00","TASK",PA,["Plan Your Week","At Home With AI"],
 ["Four prompts for meals, budgets,","and household routines."],
 [B("01",["Meal Plan From","What You Have"],["Cook from your fridge, not a list."],
    ["\"I have [ingredients]. Suggest 4 simple","dinners using them, with short steps and","what else I would need to buy.\""]),
  B("02",["Build A Grocery","List"],["Organize by store section."],
    ["\"Turn this meal plan into a grocery list","grouped by section: produce, dairy,","pantry, frozen: [paste].\""]),
  B("03",["Plan A Realistic","Budget"],["See where the money actually goes."],
    ["\"Here are my monthly expenses: [list].","Group them into needs, wants, and","savings. Point out what stands out.\""]),
  B("04",["Set A Chores","Rotation"],["Share the load fairly."],
    ["\"Create a weekly chores rotation for","[number] people, balanced by effort,","as a simple table.\""])],
 ["Which One Will","You Try First?"],["Save this for Sunday planning —","then send it to someone running","a busy household."],
 "A calmer week usually starts with a plan made on Sunday.",
 ["Meal plan from what you have","Build a grocery list","Plan a realistic budget","Set a chores rotation"],
 "Which one will you try first? Comment the number 👇",
 "#LearnAIWithDoyin #PracticalAI #HomeLife #Budgeting #AIForBeginners")

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
    json.dump(manifest, open("/tmp/manifest2.json", "w"), indent=1)
