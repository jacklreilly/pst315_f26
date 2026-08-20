"""
Fabricated sample dataset used to generate every worked example on the site.

Skills Win Coaching Organization (SWCO) is a real Syracuse University program, so
these numbers are INVENTED. No actual SWCO survey data appears here or anywhere
on the public site. Every generated example is labelled as illustrative.

Edit the values here and re-run tools/build_examples.py to regenerate everything.
"""

PROJECT   = "Site Session Satisfaction Survey"
AGENCY    = "Skills Win Coaching Organization"
AUTHOR    = "Jordan Alvarez"
DATE      = "November 2026"
SOURCE    = ("Sample data collected and analyzed by Jordan Alvarez for the Skills Win "
             "Coaching Organization, Community Link Project, November 2026.")

TARGET_POPULATION = 460      # students who attended site sessions
SAMPLING_FRAME    = 430      # students present on survey day
SAMPLE            = 214      # respondents
RESPONSE_RATE     = "50%"

SITES = ["Site A", "Site B", "Site C"]

CODEBOOK = [
    ("A", "ID",      "Respondent's unique identification number",
                     "Code is identical to identification number"),
    ("B", "SITE",    "Which site session did you attend?",
                     "1 = Site A\n2 = Site B\n3 = Site C\n99 = No response"),
    ("C", "GRADE",   "What grade are you in?",
                     "1 = 9th\n2 = 10th\n3 = 11th\n4 = 12th\n99 = No response"),
    ("D", "COACH",   "The coaches were helpful.",
                     "1 = Strongly disagree\n2 = Disagree\n3 = Neutral\n"
                     "4 = Agree\n5 = Strongly agree\n99 = No response"),
    ("E", "ENGAGE",  "The exercises were engaging.",
                     "1 = Strongly disagree\n2 = Disagree\n3 = Neutral\n"
                     "4 = Agree\n5 = Strongly agree\n99 = No response"),
    ("F", "IMPROVE", "What could be improved at your site sessions?",
                     "Open ended response:\n1 = More activities\n2 = More time\n"
                     "3 = Smaller groups\n4 = Better materials\n5 = Nothing\n99 = No response"),
]

# Finding 1 - coaches helpful (5 or fewer bars -> vertical)
F1 = {"title": "Respondents' Views on Whether Coaches Were Helpful",
      "xlabel": "Response", "n": 214,
      "cats": ["Not helpful", "Neutral", "Helpful"], "vals": [8, 21, 71]}

# Finding 2 - engagement by site (aggregate)
F2 = {"title": "Respondents Who Agreed the Exercises Were Engaging, by Site",
      "xlabel": "Site", "n": 214,
      "cats": ["Site A", "Site B", "Site C"], "vals": [64, 78, 55]}

# Finding 3 - open ended, single category
F3 = {"title": "What Respondents Felt Could Be Improved",
      "xlabel": "Category", "n": 196,
      "cats": ["More activities", "More time", "Smaller groups",
               "Better materials", "Nothing"], "vals": [34, 27, 18, 12, 9]}

# Open-ended responses, by category (fabricated; no real respondent text)
OPEN_ENDED = [
    ("More activities", 8, [
        "More hands on activities would be good.",
        "add more group activities",
        "More activities like the resume one.",
        "i liked the practice interviews, do more of those",
        "More team exercises.",
        "more activities",
        "Do more of the role playing exercises.",
        "More things to actually practice.",
    ]),
    ("More time", 6, [
        "The sessions felt rushed at the end.",
        "more time for each activity",
        "Longer sessions.",
        "We needed more time to finish.",
        "more time please",
        "Sessions should be longer than an hour.",
    ]),
    ("Smaller groups", 4, [
        "The groups were too big.",
        "smaller groups so everyone can talk",
        "Too many people at my table.",
        "Smaller groups would help.",
    ]),
    ("Better materials", 3, [
        "The handouts were hard to read.",
        "better worksheets",
        "The packet had typos in it.",
    ]),
    ("Nothing", 2, [
        "Nothing, it was great.",
        "nothing",
    ]),
]

RESEARCH_QUESTIONS = [
    "How helpful did students find the site session coaches?",
    "How engaging did students find the site session exercises?",
    "Did student views on the exercises differ by site?",
    "What do students feel could be improved about the site sessions?",
    "How many sessions did students attend over the semester?",
    "Would students recommend the site sessions to a friend?",
    "Which session topics did students find most useful?",
]

# Frequency tables (Appendix II)
FREQ_SURVEY = ("The coaches were helpful.",
               [("Strongly agree", 89, "42%"), ("Agree", 63, "29%"),
                ("Neutral", 44, "21%"), ("Disagree", 12, "6%"),
                ("Strongly disagree", 5, "2%"), ("No response", 1, "<1%")])

FREQ_RECORDS = ("Sessions delivered by site, Fall 2026",
                [("Site A", 14, "39%"), ("Site B", 12, "33%"), ("Site C", 10, "28%")])
