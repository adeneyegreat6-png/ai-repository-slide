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
def add(id, date, time, unit, kicker, head, sub, slides, cta_head, cta_sub, hook, items, ask, tags, tip):
    C.append(dict(id=id, date=date, time=time, unit=unit, kicker=kicker, head=head, sub=sub, slides=slides,
                  cta_head=cta_head, cta_sub=cta_sub, hook=hook, items=items, ask=ask, tags=tags, tip=tip))
PA, CO, TO = "PRACTICAL AI", "AI CONCEPTS", "AI TOOLS"
add("f1a","2026-11-23","08:00","TASK",PA,["Prepare For Hard","Conversations"],
 ["Four prompts for the talks you keep","putting off."],
 [B("01",["Name The Real","Issue"],["Get clear before you say a word."],
    ["\"Here is the situation: [describe]. What is","the core issue, and what outcome do I","actually want from this talk?\""]),
  B("02",["Draft Your","Opening Line"],["The first sentence sets the tone."],
    ["\"Write 3 calm ways to open a conversation","about [issue] with [person]. Keep each","under 30 words.\""]),
  B("03",["Predict Their","Response"],["Rehearse the pushback in advance."],
    ["\"What objections might [person] raise about","[issue]? Suggest a calm reply to each.\""]),
  B("04",["Practice Out","Loud"],["Role-play before the real thing."],
    ["\"Act as [person]. I will say my piece. Reply","realistically, then give me feedback on","my tone.\""])],
 ["Which Talk Have You","Been Avoiding?"],["Save this before the conversation —","then send it to someone who needs","the nudge."],
 "Hard conversations get harder the longer you avoid them. Prepare, then have them.",
 ["Name the real issue","Draft your opening line","Predict their response","Practice out loud"],
 "Which one will you try first? Comment the number 👇",
 "#LearnAIWithDoyin #PracticalAI #Communication #Career #AIForBeginners",
 "Bonus tip: After the role-play, ask the AI to point out any sentence that sounded accusatory and rewrite it starting with \"I\" instead of \"you\".")

add("f1b","2026-11-23","18:00","TOOL",TO,["4 AI Tools For","Learning A","Language"],
 ["Practice speaking, reading, and","writing a little every day."],
 [T("01","Duolingo","D","#3bbfad",["Daily habit-building","practice"],
    ["Short lessons that fit into any day","Covers many popular languages","Streaks help you stay consistent"]),
  T("02","Google Translate","G","#4a90e2",["Quick checks on words","and phrases"],
    ["Translate text between many languages","Handy for looking up a word fast","Useful for checking your own writing"]),
  T("03","Claude","C","#f0a04b",["Conversation practice","and corrections"],
    ["Chat in your target language","Ask it to explain your mistakes","Request simple example sentences"]),
  T("04","DeepL","D","#8e7cf0",["Natural-sounding","translations"],
    ["Translates full sentences and documents","Offers alternative wording","Good for comparing phrasing"])],
 ["Which One Will","You Test First?"],["Save this before you start a language —","then send it to someone learning","one."],
 "You do not need an hour a day. You need a habit you can keep.",
 ["Duolingo","Google Translate","Claude","DeepL"],
 "Which one will you test? Comment the number 👇",
 "#LearnAIWithDoyin #AITools #LanguageLearning #Productivity #AIForBeginners",
 "Bonus tip: Write three sentences in your new language each day, then ask an AI chatbot to correct them and explain each fix in one line.")

add("f2a","2026-11-24","08:00","CONCEPT",CO,["What Is Few-Shot","Prompting?"],
 ["Show the AI examples, and the answers","get better."],
 [B("01",["Examples Beat","Instructions"],["Showing is often clearer than telling."],
    ["\"Explain few-shot prompting in simple","terms with one everyday example.\""],label=TRY),
  B("02",["Zero Shot Means","No Examples"],["You ask directly with no samples."],
    ["\"Show a zero-shot prompt and a few-shot","prompt for the same task, side by side.\""],label=TRY),
  B("03",["Two To Three","Is Enough"],["A few clear samples set the pattern."],
    ["\"Here are 3 examples of the style I want:","[paste]. Write a new one in this style.\""],label=TRY),
  B("04",["Quality Matters","More Than Quantity"],["Bad examples teach bad habits."],
    ["\"Review my examples for consistency and","tell me if any would confuse you:","[paste].\""],label=TRY)],
 ["Which Idea Was","New To You?"],["Save this before your next prompt —","then send it to a friend who","uses AI daily."],
 "Instead of explaining what you want, try showing it.",
 ["Examples beat instructions","Zero shot means no examples","Two to three is enough","Quality matters more than quantity"],
 "Which idea was new to you? Comment the number 👇",
 "#LearnAIWithDoyin #AIConcepts #PromptEngineering #AIExplained #AIForBeginners",
 "Bonus tip: Keep your best examples in a notes file, and paste them into a new chat whenever you want the same style again.")

add("f2b","2026-11-24","18:00","TASK",PA,["Refresh Your CV","With AI"],
 ["Four prompts to make your experience","easier to read."],
 [B("01",["Turn Duties Into","Results"],["Show what changed because of you."],
    ["\"Rewrite this CV line to show impact:","[paste]. Use a strong verb and only","facts I give you.\""]),
  B("02",["Match The Job","Ad"],["Speak the employer's language."],
    ["\"Here is a job ad: [paste] and my CV:","[paste]. Which skills should I move","higher? Do not invent any.\""]),
  B("03",["Cut The Filler"],["Short and clear wins."],
    ["\"Shorten this CV section to 5 bullets,","each under 20 words: [paste].\""]),
  B("04",["Check For","Gaps"],["Spot what a recruiter might question."],
    ["\"Read my CV: [paste]. List 5 questions a","recruiter might ask and how I could","answer each.\""])],
 ["Which Prompt Is","Your Favorite?"],["Save this before you apply —","then send it to someone job","hunting."],
 "Recruiters skim. Make the first few lines of your CV count.",
 ["Turn duties into results","Match the job ad","Cut the filler","Check for gaps"],
 "Which one will you try first? Comment the number 👇",
 "#LearnAIWithDoyin #PracticalAI #CareerTips #JobSearch #AIForBeginners",
 "Bonus tip: Always check every line the AI rewrites against what you actually did, and delete anything you could not explain in an interview.")

add("f3a","2026-11-25","08:00","TOOL",TO,["4 AI Tools For","Organizing Your","Notes"],
 ["Find, summarize, and reuse what you","already wrote down."],
 [T("01","Notion AI","N","#8e7cf0",["Writing and summarizing","inside your workspace"],
    ["Summarize pages and meeting notes","Draft text from short prompts","Keeps notes and tasks in one place"]),
  T("02","NotebookLM","N","#4a90e2",["Asking questions about","your own sources"],
    ["Upload documents and ask questions","Answers draw from your sources","Helps you study and summarize"]),
  T("03","Microsoft OneNote","O","#3bbfad",["Notebooks inside the","Microsoft ecosystem"],
    ["Organizes notes in notebooks and pages","Works alongside Microsoft apps","Offers Copilot features on some plans"]),
  T("04","Evernote","E","#f0a04b",["Collecting notes","from anywhere"],
    ["Saves notes, clips, and documents","Search helps you find things fast","Syncs across your devices"])],
 ["Which One Will","You Test First?"],["Save this before your notes pile up —","then send it to someone who","lives in them."],
 "Notes you cannot find are notes you do not have.",
 ["Notion AI","NotebookLM","Microsoft OneNote","Evernote"],
 "Which one will you test? Comment the number 👇",
 "#LearnAIWithDoyin #AITools #NoteTaking #Productivity #AIForBeginners",
 "Bonus tip: Spend ten minutes once a week giving each new note a clear title. Good titles make any search, AI or not, work much better.")

add("f3b","2026-11-25","18:00","TASK",PA,["Run Better","Meetings With AI"],
 ["Four prompts for before, during,","and after."],
 [B("01",["Write The","Agenda"],["Every meeting needs a point."],
    ["\"Write a 30-minute agenda for a meeting on","[topic] with [number] people. Include","time for each item.\""]),
  B("02",["Send A","Pre-Read"],["Save time by sharing context first."],
    ["\"Summarize this document in 5 bullets for","people who must read it before our","meeting: [paste].\""]),
  B("03",["Capture The","Decisions"],["Turn messy notes into clarity."],
    ["\"From these notes: [paste]. List decisions","made, open questions, and who owns each","next step.\""]),
  B("04",["Send The","Follow-Up"],["Close the loop the same day."],
    ["\"Write a short follow-up email with the","decisions and next steps below. Keep it","under 120 words: [paste].\""])],
 ["Which One Will","You Use First?"],["Save this before your next meeting —","then send it to a manager you","know."],
 "A meeting without an agenda is just a conversation with a calendar invite.",
 ["Write the agenda","Send a pre-read","Capture the decisions","Send the follow-up"],
 "Which one will you try first? Comment the number 👇",
 "#LearnAIWithDoyin #PracticalAI #Meetings #Productivity #AIForBeginners",
 "Bonus tip: End the agenda prompt with \"and tell me which items could be an email instead\". It often reveals a meeting you can shorten or skip.")

add("f4a","2026-11-26","08:00","CONCEPT",CO,["What Is","Multimodal AI?"],
 ["AI that handles more than just text."],
 [B("01",["More Than","One Input"],["Text, images, and audio in one model."],
    ["\"Explain multimodal AI in simple terms with","one everyday example.\""],label=TRY),
  B("02",["Show, Do Not","Just Tell"],["Upload a photo and ask about it."],
    ["\"I will share a photo. Describe what you see","and suggest what I should check.\""],label=TRY),
  B("03",["Mix Formats","Together"],["Combine a chart with a question."],
    ["\"Here is a chart. Summarize the trend in","2 sentences and note any limits.\""],label=TRY),
  B("04",["Still Needs","Checking"],["It can misread what it sees."],
    ["\"List 4 mistakes AI can make when reading","images, and how I can catch them.\""],label=TRY)],
 ["Which Idea Was","New To You?"],["Save this next time you upload a file —","then send it to a curious friend."],
 "AI used to only read text. Now it can also look at what you show it.",
 ["More than one input","Show, do not just tell","Mix formats together","Still needs checking"],
 "Which idea was new to you? Comment the number 👇",
 "#LearnAIWithDoyin #AIConcepts #MultimodalAI #AIExplained #AIForBeginners",
 "Bonus tip: When you upload an image, tell the AI what you want from it first, such as \"read the text\" or \"describe the layout\". A clear goal gives better answers than a bare image.")

add("f4b","2026-11-26","18:00","TASK",PA,["Start A Side","Project With AI"],
 ["Four prompts to go from idea to","first step."],
 [B("01",["Test The Idea"],["Find the weak points early."],
    ["\"I want to start [idea]. List 5 risks and","5 questions I should answer before I","spend money.\""]),
  B("02",["Define The","Customer"],["Know who you are building for."],
    ["\"Describe 3 types of people who might want","[idea], and what problem each one has.\""]),
  B("03",["Plan Week One"],["Make the first step small."],
    ["\"Create a 7-day plan to start [idea] with","about 1 hour per day. List one task","per day.\""]),
  B("04",["Draft The","Message"],["Say what it is in two sentences."],
    ["\"Write a 2-sentence description of [idea]","for someone who has never heard of it.\""])],
 ["Which One Will","You Try First?"],["Save this before the idea fades —","then send it to someone with a","side project in mind."],
 "Most side projects stall at the planning stage. Shrink the first step.",
 ["Test the idea","Define the customer","Plan week one","Draft the message"],
 "Which one will you try first? Comment the number 👇",
 "#LearnAIWithDoyin #PracticalAI #SideProject #Entrepreneurship #AIForBeginners",
 "Bonus tip: Talk to two real people who fit your customer description before you build anything. Then bring what they said back to the AI to refine your plan.")

add("f5a","2026-11-27","08:00","TOOL",TO,["4 AI Assistants","Worth Knowing"],
 ["Different strengths, same simple","chat box."],
 [T("01","ChatGPT","C","#4a90e2",["General everyday help","and brainstorming"],
    ["Answers questions and drafts text","Can help with images and files","Widely used and easy to start"]),
  T("02","Claude","C","#f0a04b",["Writing, analysis,","and long documents"],
    ["Reads and summarizes long text","Helps with drafting and editing","Good for careful, detailed replies"]),
  T("03","Gemini","G","#8e7cf0",["Working inside","Google tools"],
    ["Connects with Google apps and Search","Helps with summaries and drafts","Handy if you live in Google"]),
  T("04","Microsoft Copilot","M","#3bbfad",["Help inside Microsoft","apps"],
    ["Built into Windows and Microsoft apps","Helps draft, summarize, and rewrite","Fits an existing Microsoft setup"])],
 ["Which One Will","You Test First?"],["Save this before you pick a tool —","then send it to someone new to","AI."],
 "You do not need all four. You need the one that fits how you work.",
 ["ChatGPT","Claude","Gemini","Microsoft Copilot"],
 "Which one will you test? Comment the number 👇",
 "#LearnAIWithDoyin #AITools #AIAssistants #Productivity #AIForBeginners",
 "Bonus tip: Give two assistants the exact same prompt and compare the answers side by side. A five-minute test shows which one suits your task better.")

add("f5b","2026-11-27","18:00","TASK",PA,["Plan Your Next","Trip With AI"],
 ["Four prompts for less stress and","better days away."],
 [B("01",["Shortlist","Places"],["Narrow down where to go."],
    ["\"I have [X] days and a budget of [amount].","I enjoy [interests]. Suggest 4 places to","consider and why.\""]),
  B("02",["Draft A Day","By Day Plan"],["Keep it realistic, not rushed."],
    ["\"Create a 3-day plan for [place]. Group","activities by area and leave free time","each afternoon.\""]),
  B("03",["Build A Packing","List"],["Pack for the actual trip."],
    ["\"Make a packing list for [place] in [month]","for [number] days. Group by category.\""]),
  B("04",["Learn Local","Basics"],["Be prepared for the small things."],
    ["\"List 10 useful phrases and 5 etiquette","tips for visiting [place].\""])],
 ["Where Would You","Go Next?"],["Save this for your next trip —","then send it to a travel buddy."],
 "Good trips are planned loosely. Let AI handle the first draft.",
 ["Shortlist places","Draft a day by day plan","Build a packing list","Learn local basics"],
 "Which one will you try first? Comment the number 👇",
 "#LearnAIWithDoyin #PracticalAI #TravelPlanning #Travel #AIForBeginners",
 "Bonus tip: Check opening times, prices, and travel routes on official sources before you book. AI plans are a starting point, not a timetable.")

add("f6a","2026-11-28","08:00","CONCEPT",CO,["What Is Prompt","Injection?"],
 ["When hidden text tries to steer an AI","off course."],
 [B("01",["Hidden","Instructions"],["Text can carry orders the model reads."],
    ["\"Explain prompt injection in simple terms","with one everyday example.\""],label=TRY),
  B("02",["It Hides In","Content"],["Web pages and files can contain it."],
    ["\"Give an example of how a web page could","try to mislead an AI assistant.\""],label=TRY),
  B("03",["Risk Grows With","Access"],["More tools means more to protect."],
    ["\"Why does an AI that can send emails face","more risk from injection?\""],label=TRY),
  B("04",["Stay Careful","With Sources"],["Treat unknown content with caution."],
    ["\"List 4 habits for using AI safely with","files and links I do not fully trust.\""],label=TRY)],
 ["Which Idea Was","New To You?"],["Save this before you share files with AI —","then send it to a friend who does."],
 "An AI reads everything you give it. That includes things you did not write.",
 ["Hidden instructions","It hides in content","Risk grows with access","Stay careful with sources"],
 "Which idea was new to you? Comment the number 👇",
 "#LearnAIWithDoyin #AIConcepts #AISafety #AIExplained #AIForBeginners",
 "Bonus tip: Before pasting content from an unknown source into an AI tool, read it yourself first. If it contains odd instructions aimed at the AI, do not use it.")

add("f6b","2026-11-28","18:00","TOOL",TO,["4 AI Tools For","Working With","Data"],
 ["Ask questions of your numbers in","plain language."],
 [T("01","Excel with Copilot","E","#3bbfad",["Analysis inside","Excel"],
    ["Ask questions about your sheet data","Helps build formulas and summaries","Requires a supported Microsoft plan"]),
  T("02","Google Sheets with Gemini","G","#4a90e2",["Help inside Google","Sheets"],
    ["Helps with formulas and organizing","Fits an existing Google workflow","Availability depends on your plan"]),
  T("03","ChatGPT","C","#8e7cf0",["Exploring uploaded","spreadsheets"],
    ["Upload a file and ask questions","Can summarize and clean columns","Check the results before sharing"]),
  T("04","Julius AI","J","#f0a04b",["Chatting with your","data"],
    ["Upload data and ask in plain language","Can produce charts and summaries","Built for non-technical users"])],
 ["Which One Will","You Test First?"],["Save this before your next report —","then send it to someone who","lives in spreadsheets."],
 "You do not need to be a data analyst to ask good questions of data.",
 ["Excel with Copilot","Google Sheets with Gemini","ChatGPT","Julius AI"],
 "Which one will you test? Comment the number 👇",
 "#LearnAIWithDoyin #AITools #DataAnalysis #Spreadsheets #AIForBeginners",
 "Bonus tip: Pick one total from your data and calculate it by hand. If the AI's number does not match, you know to double-check the rest.")

add("f7a","2026-11-29","08:00","TASK",PA,["Plan Your Month","With AI"],
 ["Four prompts for a calm monthly","reset."],
 [B("01",["Review Last","Month"],["Learn before you plan ahead."],
    ["\"Ask me 5 questions to review my last month:","what worked, what did not, and what to","change.\""]),
  B("02",["Pick Three","Priorities"],["Focus beats a long list."],
    ["\"Here are my goals: [list]. Help me choose","3 priorities for next month and explain","why.\""]),
  B("03",["Break It Into","Weeks"],["Make the plan doable."],
    ["\"Split these 3 priorities into weekly","tasks. Keep each week under 5 tasks.\""]),
  B("04",["Set A Check-In"],["A plan only works if you revisit it."],
    ["\"Write a 5-question weekly check-in I can","answer in 10 minutes every Sunday.\""])],
 ["Which Prompt Is","Your Favorite?"],["Save this for the end of the month —","then send it to someone who loves","a fresh start."],
 "A good month usually starts with an honest look at the last one.",
 ["Review last month","Pick three priorities","Break it into weeks","Set a check-in"],
 "Which one will you try first? Comment the number 👇",
 "#LearnAIWithDoyin #PracticalAI #Planning #Productivity #AIForBeginners",
 "Bonus tip: Put the weekly check-in in your calendar as a repeating 10-minute block, so reviewing your plan becomes a habit rather than a decision.")

add("f7b","2026-11-29","18:00","CONCEPT",CO,["How Do AI Models","Actually Learn?"],
 ["Training in plain language. No","maths needed."],
 [B("01",["Learning From","Examples"],["Models find patterns in lots of data."],
    ["\"Explain how an AI model learns from data","using a simple everyday analogy.\""],label=TRY),
  B("02",["Predict, Then","Correct"],["Guess, compare, adjust, repeat."],
    ["\"Describe how a model improves by","comparing its guesses with right","answers.\""],label=TRY),
  B("03",["Training Comes","First"],["Learning happens before you ever chat."],
    ["\"What is the difference between training a","model and using it in a chat?\""],label=TRY),
  B("04",["Data Shapes","The Result"],["What goes in affects what comes out."],
    ["\"Give 3 examples of how training data","quality can change an AI's answers.\""],label=TRY)],
 ["Which Idea Was","New To You?"],["Save this the next time someone asks","how AI works — then send it to","a friend."],
 "AI does not think like a person. It learns patterns. Here is how.",
 ["Learning from examples","Predict, then correct","Training comes first","Data shapes the result"],
 "Which idea was new to you? Comment the number 👇",
 "#LearnAIWithDoyin #AIConcepts #MachineLearning #AIExplained #AIForBeginners",
 "Bonus tip: Next time an AI answer seems off, ask it what kinds of information it might be missing. It is a quick way to see where its knowledge may be thin.")

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
    json.dump(manifest, open("/tmp/claude-0/manifest3.json", "w"), indent=1)
