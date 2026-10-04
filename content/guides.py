"""Guide pages and interactive quiz content for the SSR preview bot."""

# Each page: id -> {title, body, next_id optional}
# Menu lists are separate so the bot can build keyboards cleanly.

GBV_PAGES = {
    "menu": {
        "title": "GBV & Sexual Violence",
        "body": (
            "<b>Gender-Based Violence (GBV)</b>\n"
            "<b>በፆታ ላይ የተመሰረተ ጥቃት (ጂቢቪ)</b>\n\n"
            "Clear, respectful information to help you understand GBV, "
            "know your rights, stay safer, and find support.\n\n"
            "ጂቢቪን ለመረዳት፣ መብትዎን ለማወቅ፣ ደህንነትዎን ለመጠበቅ እና "
            "ድጋፍ ለማግኘት ግልጽ መረጃ።\n\n"
            "<i>This bot shares information only. It is not a crisis "
            "counseling service. If you or someone else is in immediate "
            "danger, contact local emergency services or a trusted "
            "support provider.</i>\n\n"
            "<i>ይህ ቦት መረጃ ብቻ ያቀርባል። የአደጋ አማካሪ አገልግሎት አይደለም። "
            "አስቸኳይ አደጋ ካለ የአካባቢ ድንገተኛ አገልግሎቶችን ወይም ታማኝ "
            "ድጋፍ ሰጪን ያግኙ።</i>\n\n"
            "Choose a guide / መመሪያ ይምረጡ:"
        ),
    },
    "what": {
        "title": "What is GBV?",
        "body": (
            "<b>What is Gender-Based Violence?</b>\n"
            "<b>በፆታ ላይ የተመሰረተ ጥቃት ምንድን ነው?</b>\n\n"
            "GBV is harm directed at a person because of their gender. "
            "It can include physical, sexual, emotional, economic, or "
            "online abuse.\n\n"
            "ጂቢቪ በፆታ ምክንያት በሰው ላይ የሚደርስ ጉዳት ነው። አካላዊ፣ "
            "ወሲባዊ፣ ስሜታዊ፣ ኢኮኖሚያዊ ወይም የኦንላይን ጥቃት ሊሆን ይችላል።\n\n"
            "<b>Important truths / አስፈላጊ እውነቶች</b>\n"
            "• GBV is never the survivor's fault / ጥቃቱ የተጎጂው ጥፋት አይደለም\n"
            "• It can happen in homes, schools, workplaces, or communities\n"
            "  በቤት፣ ትምህርት ቤት፣ የስራ ቦታ ወይም ማህበረሰብ ሊከሰት ይችላል\n"
            "• Anyone can be affected — women and girls face higher risk\n"
            "  ማንም ሊጎዳ ይችላል — ሴቶችና ልጃገረዶች ከፍተኛ አደጋ አለባቸው\n"
            "• Silence protects abuse; support and accountability protect people\n"
            "  ዝምታ ጥቃትን ይጠብቃል፤ ድጋፍና ተጠያቂነት ሰዎችን ይጠብቃል\n\n"
            "Understanding GBV is a first step toward safer communities.\n"
            "ጂቢቪን መረዳት ለደህንነት ማህበረሰቦች የመጀመሪያ እርምጃ ነው።"
        ),
    },
    "rights": {
        "title": "Your rights",
        "body": (
            "<b>Your rights matter</b>\n"
            "<b>መብትዎ አስፈላጊ ነው</b>\n\n"
            "Every person has the right to safety, dignity, and bodily autonomy.\n"
            "እያንዳንዱ ሰው የደህንነት፣ የክብር እና የሰውነት ነፃነት መብት አለው።\n\n"
            "You have the right to / መብት አለዎት:\n"
            "• Live free from violence / ከጥቃት ነፃ መኖር\n"
            "• Seek help without shame / ያለ እፍረት እርዳታ መጠየቅ\n"
            "• Be heard with respect and confidentiality / በክብርና በሚስጥር መሰማት\n"
            "• Access information, healthcare, and justice support\n"
            "  መረጃ፣ ጤና አገልግሎትና የፍትህ ድጋፍ ማግኘት\n"
            "• Make decisions about your own recovery / ስለ ማገገምዎ መወሰን\n\n"
            "Knowing your rights helps you advocate for yourself and others.\n"
            "መብትዎን ማወቅ ለራስዎና ለሌሎች እንዲቆሙ ይረዳዎታል።"
        ),
    },
    "safety": {
        "title": "Safety tips",
        "body": (
            "<b>Practical safety ideas</b>\n"
            "<b>ተግባራዊ የደህንነት ምክሮች</b>\n\n"
            "• Tell a trusted person where you are when you feel unsafe\n"
            "  ደህንነት ሲያጡ ታማኝ ሰው የት እንደሆኑ ይንገሩ\n"
            "• Keep emergency contacts easy to reach\n"
            "  የአደጋ ጊዜ ስልኮችን በቀላሉ ያስቀምጡ\n"
            "• If possible, move to a safer public space when threatened\n"
            "  ቢቻል ወደ ደህንነቱ የተጠበቀ የህዝብ ቦታ ይሂዱ\n"
            "• Document incidents only if it is safe to do so\n"
            "  ክስተቶችን ደህንነት ካለ ብቻ ይመዝግቡ\n"
            "• Online: protect passwords, avoid sharing location publicly\n"
            "  ኦንላይን፡ የይለፍ ቃል ይጠብቁ፣ አድራሻ በይፋ አያጋሩ\n\n"
            "Safety plans look different for everyone. Your judgment matters.\n"
            "የደህንነት እቅድ ለእያንዳንዱ ሰው የተለየ ነው። ውሳኔዎ አስፈላጊ ነው።"
        ),
    },
    "support": {
        "title": "Supporting survivors",
        "body": (
            "<b>If someone confides in you</b>\n"
            "<b>አንድ ሰው ሲነግርዎ</b>\n\n"
            "• Listen without judgment / ያለ ፍርድ ያዳምጡ\n"
            "• Believe them — do not ask what they \"did wrong\"\n"
            "  ያምኗቸው — \"ምን ስህተት አደረጉ?\" አይበሉ\n"
            "• Respect privacy; do not share their story without consent\n"
            "  ሚስጥራቸውን ይጠብቁ፤ ያለ ፈቃድ አያጋሩ\n"
            "• Ask how you can help / እንዴት መርዳት እንደሚችሉ ይጠይቁ\n"
            "• Encourage professional or community support when needed\n"
            "  አስፈላጊ ሲሆን የባለሙያ ወይም የማህበረሰብ ድጋፍ ያበረታቱ\n\n"
            "Supportive communities reduce stigma and help survivors heal.\n"
            "ድጋፍ የሚሰጥ ማህበረሰብ ስድብን ይቀንሳልና ተጎጂዎች እንዲድኑ ይረዳል።"
        ),
    },
    "help": {
        "title": "Get help / resources",
        "body": (
            "<b>Get help & resources</b>\n"
            "<b>እርዳታና ምንጮች ያግኙ</b>\n\n"
            "If you need support, you are not alone.\n"
            "ድጋፍ ከፈለጉ ብቻዎትን አይደሉም።\n\n"
            "<b>SSR contact / የኤስኤስአር ግንኙነት</b>\n"
            "Zemen Desta, Executive Director / ሥራ አስፈጻሚ ዳይሬክተር\n"
            "Phone / ስልክ: +251 939 367 178\n"
            "Email / ኢሜይል: zemufani@gmail.com\n"
            "Locations: Mekelle, Tigray & Addis Ababa / መቀሌ እና አዲስ አበባ\n\n"
            "<b>Please remember / እባክዎ ያስታውሱ</b>\n"
            "This bot provides digital information. For urgent danger, "
            "contact local emergency services, police, a health facility, "
            "or a trusted protection actor in your area.\n\n"
            "ይህ ቦት ዲጂታል መረጃ ያቀርባል። አስቸኳይ አደጋ ካለ የአካባቢ "
            "ድንገተኛ አገልግሎት፣ ፖሊስ፣ ጤና ተቋም ወይም ታማኝ ጥበቃ አካል ያግኙ።\n\n"
            "SSR works to create safer spaces for youth and women.\n"
            "ኤስኤስአር ለወጣቶችና ሴቶች ደህንነቱ የተጠበቀ ቦታ ለመፍጠር ይሰራል።"
        ),
    },
}

GBV_MENU_KEYS = [
    ("what", "What is GBV? / ጂቢቪ ምንድን ነው?"),
    ("rights", "Your rights / መብትዎ"),
    ("safety", "Safety tips / የደህንነት ምክሮች"),
    ("support", "Supporting survivors / ተጎጂዎችን መደገፍ"),
    ("help", "Get help / እርዳታ ያግኙ"),
]

PEACE_PAGES = {
    "menu": {
        "title": "Peacebuilding",
        "body": (
            "<b>Peacebuilding & Social Cohesion</b>\n"
            "<b>ሰላም ግንባታና ማህበራዊ ትስስር</b>\n\n"
            "SSR strengthens trust, dialogue, and peaceful coexistence "
            "within and between communities — especially among youth.\n\n"
            "ኤስኤስአር በማህበረሰቦች ውስጥና መካከል እምነትን፣ ውይይትን እና "
            "ሰላማዊ አብሮ መኖርን ያጠናክራል — በተለይም በወጣቶች መካከል።\n\n"
            "Explore a short guide / አጭር መመሪያ ይመልከቱ:"
        ),
    },
    "why": {
        "title": "Why peace matters",
        "body": (
            "<b>Why peacebuilding matters</b>\n"
            "<b>ሰላም ግንባታ ለምን አስፈላጊ ነው</b>\n\n"
            "Conflict damages trust, education, livelihoods, and hope. "
            "Peacebuilding helps communities rebuild relationships and "
            "prevent cycles of harm.\n\n"
            "ግጭት እምነትን፣ ትምህርትን፣ ኑሮን እና ተስፋን ይጎዳል። ሰላም ግንባታ "
            "ማህበረሰቦች ግንኙነት እንዲገነቡ እና የጉዳት ዑደት እንዲከላከሉ ይረዳል።\n\n"
            "Inclusive peace means youth, women, and marginalized groups "
            "have a real voice in decisions that shape their future.\n\n"
            "አካታች ሰላም ማለት ወጣቶች፣ ሴቶች እና የተገለሉ ቡድኖች "
            "ወደፊታቸው በሚቀርጹ ውሳኔዎች እውነተኛ ድምጽ ማግኘት ነው።"
        ),
    },
    "dialogue": {
        "title": "Dialogue & coexistence",
        "body": (
            "<b>Dialogue & peaceful coexistence</b>\n"
            "<b>ውይይትና ሰላማዊ አብሮ መኖር</b>\n\n"
            "Practical ways to contribute / ተግባራዊ መንገዶች:\n"
            "• Listen across differences / ከመረጨቱ በፊት ያዳምጡ\n"
            "• Challenge rumors with verified information / ወሬን በእውነት ይፈትሹ\n"
            "• Create spaces where people feel safe to speak\n"
            "  ሰዎች በደህንነት የሚናገሩበት ቦታ ይፍጠሩ\n"
            "• Support local initiatives that bring communities together\n"
            "  ማህበረሰቦችን የሚያገናኙ የአካባቢ ሥራዎችን ይደግፉ\n\n"
            "Small acts of respect and dialogue build social cohesion over time.\n"
            "ትናንሽ የክብርና ውይይት ሥራዎች በጊዜ ማህበራዊ ትስስር ይገነባሉ።"
        ),
    },
    "youth": {
        "title": "Youth role in peace",
        "body": (
            "<b>Youth role in peace</b>\n"
            "<b>የወጣቶች ሚና በሰላም</b>\n\n"
            "Young people are not only affected by conflict — they are "
            "agents of lasting change.\n\n"
            "ወጣቶች በግጭት የሚጎዱ ብቻ አይደሉም — የዘላቂ ለውጥ አራማጆች ናቸው።\n\n"
            "SSR invests in youth leadership, skills, and participation so "
            "\"Sirius\" young people can drive inclusive and peaceful solutions "
            "in their communities.\n\n"
            "ኤስኤስአር በወጣቶች አመራር፣ ክህሎትና ተሳትፎ ላይ ያተኩራል "
            "እንደ \"ሲሪየስ\" ወጣቶች አካታችና ሰላማዊ መፍትሄ እንዲያመሩ።"
        ),
    },
}

PEACE_MENU_KEYS = [
    ("why", "Why peace matters / ሰላም ለምን"),
    ("dialogue", "Dialogue / ውይይት"),
    ("youth", "Youth role / የወጣቶች ሚና"),
]

RIGHTS_PAGES = {
    "menu": {
        "title": "Human Rights Advocacy",
        "body": (
            "<b>Human Rights Advocacy</b>\n"
            "<b>የሰብአዊ መብት ተሟጋችነት</b>\n\n"
            "SSR promotes awareness, protection, and advocacy for "
            "fundamental human rights — with a focus on women and youth.\n\n"
            "ኤስኤስአር መሰረታዊ ሰብአዊ መብቶችን ግንዛቤ፣ ጥበቃ እና ተሟጋችነት "
            "ያበረታታል — በሴቶችና ወጣቶች ላይ በማተኮር።\n\n"
            "Choose a guide / መመሪያ ይምረጡ:"
        ),
    },
    "basics": {
        "title": "Rights basics",
        "body": (
            "<b>Human rights basics</b>\n"
            "<b>የሰብአዊ መብት መሰረታዊ ነጥቦች</b>\n\n"
            "Human rights are freedoms and protections every person has "
            "simply because they are human — including dignity, equality, "
            "safety, education, and participation.\n\n"
            "ሰብአዊ መብቶች ሰው በመሆን ብቻ የሚኖሩ ነጻነቶችና ጥበቃዎች ናቸው — "
            "ክብር፣ እኩልነት፣ ደህንነት፣ ትምህርት እና ተሳትፎን ጨምሮ።\n\n"
            "Rights are universal: they apply to everyone, everywhere, "
            "without discrimination.\n\n"
            "መብቶች ሁለንተናዊ ናቸው፡ ለሁሉም፣ በየትኛውም ቦታ፣ ያለ መድልዎ።"
        ),
    },
    "women_youth": {
        "title": "Women & youth focus",
        "body": (
            "<b>Women & youth focus</b>\n"
            "<b>በሴቶችና ወጣቶች ላይ ትኩረት</b>\n\n"
            "Women and youth often face barriers to safety, voice, and "
            "opportunity — especially after conflict or displacement.\n\n"
            "ሴቶችና ወጣቶች ብዙ ጊዜ በደህንነት፣ በድምጽ እና በእድል ላይ "
            "እንቅፋቶች ያጋጥሟቸዋል — በተለይ ከግጭት ወይም ከመፈናቀል በኋላ።\n\n"
            "SSR centers their leadership and participation so advocacy "
            "reflects real community needs, not top-down decisions alone.\n\n"
            "ኤስኤስአር አመራራቸውንና ተሳትፏቸውን ያተኩራል ስለዚህ ተሟጋችነት "
            "እውነተኛ የማህበረሰብ ፍላጎትን ያንጸባርቃል።"
        ),
    },
    "engage": {
        "title": "How to engage",
        "body": (
            "<b>How you can engage</b>\n"
            "<b>እንዴት መሳተፍ ይችላሉ</b>\n\n"
            "• Learn and share accurate rights information\n"
            "  ትክክለኛ የመብት መረጃ ይማሩና ያጋሩ\n"
            "• Stand with people whose rights are denied\n"
            "  መብታቸው ከተነፈገ ሰዎች ጋር ይቁሙ\n"
            "• Join peaceful community and CSO initiatives\n"
            "  ሰላማዊ የማህበረሰብና የሲኤስኦ ሥራዎችን ይቀላቀሉ\n"
            "• Contact SSR to learn about programs and partnerships\n"
            "  ስለ ፕሮግራሞችና አጋርነት ኤስኤስአርን ያግኙ\n\n"
            "Advocacy starts with awareness — and grows through collective action.\n"
            "ተሟጋችነት ከግንዛቤ ይጀምራል — በጋራ ሥራ ያድጋል።"
        ),
    },
}

RIGHTS_MENU_KEYS = [
    ("basics", "Rights basics / መሰረታዊ መብቶች"),
    ("women_youth", "Women & youth / ሴቶችና ወጣቶች"),
    ("engage", "How to engage / እንዴት መሳተፍ"),
]

# Interactive "Find your path" — short chooser that routes into guides
QUIZ = {
    "intro": (
        "<b>Find your path</b>\n"
        "<b>መንገድዎን ያግኙ</b>\n\n"
        "Answer one quick question. We'll point you to the guide "
        "that fits what you need right now.\n\n"
        "አንድ ፈጣን ጥያቄ ይመልሱ። አሁን ለሚፈልጉት ተስማሚ መመሪያ እናሳይዎታለን።"
    ),
    "question": "What are you looking for today? / ዛሬ ምን ይፈልጋሉ?",
    "options": [
        {
            "id": "quiz:gbv",
            "label": "Safety / GBV / ደህንነት ወይም ጂቢቪ",
            "result": (
                "<b>Suggested path: GBV guides</b>\n"
                "<b>የተጠቆመ መንገድ፡ የጂቢቪ መመሪያዎች</b>\n\n"
                "Start with clear information on gender-based violence, "
                "rights, safety, and where to seek help.\n\n"
                "ስለ በፆታ ላይ የተመሰረተ ጥቃት፣ መብት፣ ደህንነት እና እርዳታ "
                "ግልጽ መረጃ ይጀምሩ።\n\n"
                "Tap below to open the GBV section. / ከታች ይጫኑ።"
            ),
            "goto": "gbv:menu",
            "goto_label": "Open GBV / ጂቢቪ ይክፈቱ",
        },
        {
            "id": "quiz:peace",
            "label": "Peace / ሰላምና ትስስር",
            "result": (
                "<b>Suggested path: Peacebuilding</b>\n"
                "<b>የተጠቆመ መንገድ፡ ሰላም ግንባታ</b>\n\n"
                "Explore how dialogue, trust, and youth leadership "
                "strengthen peaceful coexistence.\n\n"
                "ውይይት፣ እምነት እና የወጣቶች አመራር ሰላማዊ አብሮ መኖርን "
                "እንዴት እንደሚያጠናክሩ ይመልከቱ።\n\n"
                "Tap below to open Peacebuilding. / ከታች ይጫኑ።"
            ),
            "goto": "peace:menu",
            "goto_label": "Open Peace / ሰላም ይክፈቱ",
        },
        {
            "id": "quiz:rights",
            "label": "Rights / መብቶችና ተሟጋችነት",
            "result": (
                "<b>Suggested path: Human Rights</b>\n"
                "<b>የተጠቆመ መንገድ፡ ሰብአዊ መብቶች</b>\n\n"
                "Learn rights basics and how women and youth can "
                "engage in advocacy with SSR.\n\n"
                "የመብት መሰረታዊ ነጥቦችን እና ሴቶችና ወጣቶች ከኤስኤስአር ጋር "
                "እንዴት መሳተፍ እንደሚችሉ ይማሩ።\n\n"
                "Tap below to open Human Rights. / ከታች ይጫኑ።"
            ),
            "goto": "rights:menu",
            "goto_label": "Open Rights / መብቶች ይክፈቱ",
        },
        {
            "id": "quiz:about",
            "label": "About SSR / ስለ ኤስኤስአር",
            "result": (
                "<b>Suggested path: About SSR</b>\n"
                "<b>የተጠቆመ መንገድ፡ ስለ ኤስኤስአር</b>\n\n"
                "Discover who we are, our mission, and how we serve "
                "youth, women, and marginalized communities.\n\n"
                "እኛ ማን እንደሆንን፣ ተልእኮአችንን እና ወጣቶችን፣ ሴቶችን "
                "እና የተገለሉ ማህበረሰቦችን እንዴት እንደምናገለግል ይወቁ።\n\n"
                "Tap below to read About SSR. / ከታች ይጫኑ።"
            ),
            "goto": "menu:about",
            "goto_label": "About SSR / ስለ ኤስኤስአር",
        },
    ],
}
