"""Seen a nav error? These world-building data files have been put here deliberately for clarity.

SKILLS and ROOMS catalogues for sim-scenario-drafter.

All content is education-only simulation practice material.
It is NEVER medical advice and is intended for training environments only.

Each skill entry provides the offline template fallback: objectives,
patient statements (spoken by the simulated patient/actor), planned
distractions, props, expected actions, and debrief questions.
"""

SKILLS = {
    "hand-hygiene": {
        "id": "hand-hygiene",
        "title": "Hand Hygiene & Glove Use",
        "summary": "World Health Organization moments for hand hygiene, glove discipline, and maintaining a clean field during routine bedside care.",
        "objectives": [
            "Perform hand hygiene at every WHO '5 moments' during a simulated bedside encounter.",
            "Explain to the patient why hand hygiene is happening and what it protects.",
            "Demonstrate correct removal of gloves without self-contamination.",
            "Identify breaks in technique performed by others during the debrief.",
        ],
        "patient_statements": [
            "I saw the last nurse walk out without washing her hands. Does that happen a lot here?",
            "It's okay, you don't need gloves just to hand me water, right?",
            "My grandkid had that hospital superbug thing. I don't want that. I wash my hands a lot in here.",
            "Can you tell my son when he comes back he should use that gel by the door too?",
            "Thanks for doing all that. I know it takes you longer but I'd rather be safe.",
        ],
        "distractions": [
            "A call light rings from a neighboring room partway through the encounter.",
            "A family member enters mid-task and starts asking about lunch trays.",
            "A CNA stops at the doorway to hand the learner a stack of supplies at an awkward moment.",
        ],
        "props": [
            "Alcohol-based hand rub dispensers at door and bedside",
            "Non-sterile gloves, several sizes",
            "Water pitcher and cup",
            "Readable hand-hygiene reminder poster for the debrief",
        ],
        "expected_actions": [
            "Hand hygiene on entry, before contact, before clean tasks, after contamination, and on exit.",
            "Patient-friendly narration of what is being done and why.",
            "Gloving and gloving-off with no bare-hand contact of glove exterior during removal.",
            "Acknowledges the neighbor's call light politely and defers it or notifies someone.",
        ],
        "debrief_questions": [
            "Which of the five moments for hand hygiene were hardest to catch, and why?",
            "How did the family member's interruption affect your technique?",
            "What language did you use to involve the patient, and how did it land?",
            "What is one habit you will carry into your next real shift?",
        ],
    },
    "vital-signs": {
        "id": "vital-signs",
        "title": "Bedside Vital Signs & Interpretation",
        "summary": "Accurate measurement workflow plus a teach-back-style interpretation with the patient, including escalation judgement.",
        "objectives": [
            "Measure simulated vital signs using correct technique and document them accurately.",
            "Communicate results to the patient in plain language and check understanding.",
            "Apply given parameter ranges to decide when findings warrant escalation.",
            "Maintain comfort, dignity, and consistent patient engagement throughout.",
        ],
        "patient_statements": [
            "I feel kind of warm but had a blanket on, does that matter for the temp?",
            "My home machine always said 110 over 70, so if yours is different I'll be nervous.",
            "Can we do the blood pressure after I finish my coffee? It's fresh.",
            "Is 118 a bad heart rate? My friend says over 100 is scary.",
            "Thank you for explaining. Now, when do I get breakfast?",
        ],
        "distractions": [
            "The room's television is playing at high volume until the learner negotiates to lower it.",
            "The patient continuously narrates everything slower than the workflow needs.",
            "A phone call meant for the patient rings mid-measurement: 'it might be my daughter, please answer it.'",
        ],
        "props": [
            "Simulated blood pressure cuff and stethoscope",
            "Thermometer (with realistic simulated readings)",
            "Pulse oximeter clip",
            "Vital-sign flow sheet and pen",
            "Fictional parameter ranges card supplied to the learner",
        ],
        "expected_actions": [
            "Confirms identity using two identifiers before starting.",
            "Times a full minute manually for the radial pulse or states a counted 30-second doubling where appropriate.",
            "Re-measures at rest after the coffee request rather than with the cup in hand.",
            "Interprets results against the provided fictional ranges and states the escalation decision out loud.",
        ],
        "debrief_questions": [
            "Which artifact (blanket, speech, cup) most threatened your accuracy, and how did you handle it?",
            "How did you frame the numbers so the anxious patient stayed calm?",
            "What fictional value inside your ranges would have made you escalate, and what would you do first?",
            "What would good documentation for this encounter contain?",
        ],
    },
    "iv-insertion": {
        "id": "iv-insertion",
        "title": "Peripheral IV Start & Setup Check",
        "summary": "Communication, vein selection conversation, sterile technique, and a simulated pump/line setup on a task trainer arm.",
        "objectives": [
            "Set up an aseptic field and perform a full IV start narratively on a task trainer.",
            "Obtain consent and cooperation with clear, calm patient communication.",
            "Perform a simulated safety check of the pump settings and tubing, verbalizing each step aloud.",
            "Respond to vein-scare and needle anxiety from the patient.",
        ],
        "patient_statements": [
            "Oh, needles. I'm a hard stick. Usually takes three people four tries.",
            "Do you have a student doing this? I'd rather have the real nurse.",
            "My sister talked about a big bag of fluid from one of these... I don't remember the word.",
            "That warm feeling isn't bad. Is it supposed to be warm?",
            "Can you secure it so I can still use the bathroom without help?",
        ],
        "distractions": [
            "The task trainer arm's action figure supply pouch is out of the primary tape; a second run must happen.",
            "The patient keeps offering veins: 'my forearm is good' while a better site exists on the other arm.",
            "A courier honks a delivery cart past the door, and the patient's attention snaps to it.",
        ],
        "props": [
            "Task trainer arm with realistic vein placement",
            "Aseptic field supplies: tourniquet, alcohol wipe, gauze, transparent dressing, tape",
            "Simulated pump and tubing",
            "Fictional fluid order card",
        ],
        "expected_actions": [
            "Explains the procedure and obtains verbal consent from the anxious patient.",
            "Verbalizes vein selection rationale rather than silently acting.",
            "Verbalizes a full field setup, plus correct tourniquet time behavior.",
            "Completes a spoken pump-setting double-check against the fictional order card.",
        ],
        "debrief_questions": [
            "How did you address needle anxiety without over-promising?",
            "What verbal habits kept your technique consistent under interruptions?",
            "Why is the spoken pump double-check valuable even when alone?",
            "If your first attempt failed, what would your repair conversation with the patient be?",
        ],
    },
    "med-pass-po": {
        "id": "med-pass-po",
        "title": "Oral Medication Pass (Simulated)",
        "summary": "A rights-checked oral medication pass using simulation tags only — no real medications — on a standard med cart simulation.",
        "objectives": [
            "Complete all medication rights and a two-identifier check before any simulated administration.",
            "Verify a fictional medication against a fictional order card and flag a discrepancy if present.",
            "Communicate with the patient about purpose, timing, and side effects in plain language.",
            "Handle interruptions with the do-not-disturb habit during the pass.",
        ],
        "patient_statements": [
            "I usually take that little one, not the big one. You sure this is mine?",
            "My headache is better. Do I really need to take it now?",
            "Can I take it later with my apple juice instead of this water?",
            "The nurse at 7 gave me a red round one. Is that the same thing?",
            "Thanks. Should I write down that you gave that to me?",
        ],
        "distractions": [
            "The patient asks an off-topic question about a different medication they saw on television.",
            "A second nurse arrives mid-pass asking the learner for help with their own task.",
            "A visitor asks to sign a form the moment the learner opens the med drawer.",
        ],
        "props": [
            "Simulated medication cart with tagged 'med' (candy/blank tags — no real medications)",
            "Fictional medication order cards with one instrumented discrepancy",
            "Water cups and a passing tray",
            "Barcode scanner props or role-play stand-ins",
        ],
        "expected_actions": [
            "Performs and verbalizes the rights: patient, drug, dose, route, time, documentation.",
            "Catches the instrumented discrepancy in the order card and stops to resolve it.",
            "Declines to skip or swap times without consultation when the patient tries to reschedule.",
            "Uses a polite not-now guard against interruptions during the pass.",
        ],
        "debrief_questions": [
            "Which right was closest to being dropped, and what saved it?",
            "What exact language did you use to decline the 9 a.m. apple-juice reschedule?",
            "How did you balance being helpful to the second nurse with interrupting a med pass?",
            "What is your personal do-not-interrupt phrase going forward?",
        ],
    },
    "wound-care": {
        "id": "wound-care",
        "title": "Wound Assessment & Clean Dressing Change",
        "summary": "A narration-consistent assessment and clean dressing change on a simulated wound model, with teaching for home care.",
        "objectives": [
            "Perform and verbalize a structured wound assessment (location, size, tissue, edges, drainage) when data is simulated.",
            "Give home-care teaching in plain language and check comprehension by teach-back.",
            "Change a clean dressing on a simulated wound model without breaking technique.",
            "Add and use patient-friendly vocabulary for wound stages.",
        ],
        "patient_statements": [
            "It smelled a bit the other day. I think it's getting better though.",
            "My daughter changes this at home. She uses peroxide. Is that fine?",
            "It hurts more when the wet ones go on than the dry ones.",
            "What color is it? I can't see. Someone describe it to me.",
            "If it rains on my walk, will it get wet through the bandage?",
        ],
        "distractions": [
            "Wound-adjacent clothing straps get in the way until re-gowned.",
            "The patient cranes to look at the wound themselves mid-exam and moves wrong.",
            "The patient peroxide question triggers an unplanned, long teaching detour.",
        ],
        "props": [
            "Simulated wound model (artificial dressing base)",
            "Clean dressing supplies and simulated irrigation set-up",
            "Pain relief simulation card and rating scale",
            "Teaching handout prop (fictional)",
        ],
        "expected_actions": [
            "Uses a structured assessment script rather than jumping around.",
            "Corrects peroxide use gently with plain-English reasoning.",
            "Pre-warms technique for comfort and invites rating of the pain.",
            "Closes with teach-back: the patient repeats home instructions correctly.",
        ],
        "debrief_questions": [
            "How did you describe something the patient couldn't see, and what worked?",
            "What teaching detour came out of the peroxide question, and was it too long?",
            "Which assessment element would you most want before your first real patient, and why?",
            "What did you do to keep the patient from moving mid-exam without shame?",
        ],
    },
    "oxygen-therapy": {"id": "oxygen-therapy", "title": "Oxygen Delivery & Safety Check (Simulated)", "summary": "Setting up simulated oxygen delivery education, flow safety habits, and home-friendly modifications to teach.",
        "objectives": [
            "Assemble the simulated delivery device mentally and verbalize every step.",
            "Perform a spoken safety checklist (positioning, flow check, spares, tubing hazards).",
            "Educate the patient on no-smoking and trip avoidance with kind, non-scolding language.",
            "Complete a fictional document handoff of settings and times.",
        ],
        "patient_statements": [
            "The last person said don't smoke. My son is a smoker but he goes outside. Is that okay?",
            "The tubing keeps catching on my foot. It's dangerous, right?",
            "I get winded walking to the mailbox. Should I just carry the tank?",
            "My wife wears a lot of hairspray. Is that a problem?",
            "Two liters, right? Or was it three? I remember two.",
        ],
        "distractions": [
            "The patient gossips about a neighbor related to fires and safety while the setup proceeds.",
            "Tubing hazards are all over the room and need to be found without prompting.",
            "A phone with a work call-in makes the learner lose their place mid-checklist.",
        ],
        "props": [
            "Simulated cylinder tank or concentrator prop (visual only, no real gas)",
            "Simulated cannula and tubing",
            "Fictional order card for home liter flow",
            "Trip-hazard props (loose mats, tangled cords) planted in the room",
        ],
        "expected_actions": [
            "Goes through a spoken safety check before touching settings.",
            "Deflects the gossip kindly and returns to the checklist.",
            "Teaches the hairspray/no-flame rule with a plain, not-shameful explanation.",
            "Confirms the correct liter number with the patient and corrects memory drift.",
        ],
        "debrief_questions": [
            "What did your spoken safety checklist include, and which part is easiest to skip?",
            "How did you teach without shaming the family context (son, hairspray)?",
            "Which tubing or trip hazards did you find, and which did you miss?",
            "How would this checklist look at home in one short paragraph for the patient's fridge?",
        ],
    },
    "fall-risk": {
        "id": "fall-risk",
        "title": "Fall Risk Assessment & Bedside Safety Plan",
        "summary": "A teach-back safety conversation plus a scripted bedside environment scan and fall-risk patient statement handling.",
        "objectives": [
            "Conduct a fall-risk interview with a resistant patient who insists 'I'm fine.'",
            "Scan the bedside environment for hazards and correct them narratively.",
            "Agree on a shared safety plan (call light, toileting schedule, footwear).",
            "Document the fictional assessment with the risk level justified in plain terms.",
        ],
        "patient_statements": [
            "I've walked four miles a day my whole life. I'm not one of those faller people.",
            "I'm not using the call bell. I don't want to be a burden.",
            "Those socks are stupid. I'll wear my slippers.",
            "Okay okay, I'll ring when I need the bathroom. Deal?",
            "Don't put the rail up. That's a cage and I live on my own.",
        ],
        "distractions": [
            "The patient accidentally presses the call bell looking for the television remote.",
            "A neighbor's accented coding drill announcement echoes in the hallway.",
            "The patient tells a great unrelated story that is hard to exit politely.",
        ],
        "props": [
            "Fall-risk assessment card (fictional tool)",
            "Non-slip sock pair as a prop",
            "Call light prop",
            "Assorted bedside hazard props (loose cords, rolled rug edge, misplaced bed rail)",
        ],
        "expected_actions": [
            "Validates the patient's identity as a capable walker while reframing risk as situational.",
            "Negotiates rails and footwear rather than ordering.",
            "Finds and fixes at least two planted hazards aloud.",
            "Closes with an agreed plan and a kind exit from the long story.",
        ],
        "debrief_questions": [
            "How did you reframe fall risk for someone who sees it as an identity insult?",
            "Which planted hazards did you catch, and which one hid best?",
            "What did your exit strategy from the long story sound like?",
            "How would you document risk level without sounding alarmist or dismissive?",
        ],
    },
    "patient-teaching-discharge": {
        "id": "patient-teaching-discharge",
        "title": "Discharge Teaching & Teach-Back",
        "summary": "A simulated discharge conversation with medication, follow-up, and warning-sign teaching plus teach-back checking.",
        "objectives": [
            "Deliver fictional discharge instructions organized into meds, follow-up, and warning signs.",
            "Use teach-back to verify understanding without making the patient feel quizzed.",
            "Identify a barrier (transport, literacy, or home support) during the conversation.",
            "Close with an agreed next step and plain-language summary.",
        ],
        "patient_statements": [
            "This is a lot of papers. Is there just one thing I need to do first?",
            "So... skip the pill if I feel fine, right?",
            "My daughter drives, but she works days. How will I get to the follow-up?",
            "My pills look different at home. The pharmacy said the label is new.",
            "So if my leg swells up like a balloon, that's when I call, right?",
        ],
        "distractions": [
            "The patient's phone rings with a job-related call mid-teaching.",
            "The patient latches onto the wrong warning sign and needs gentle redirecting.",
            "A wheelchair tech arrives early and paces at the door.",
        ],
        "props": [
            "Fictional discharge instruction sheets (simple language)",
            "Simulated pill organizer",
            "Fictional follow-up appointment card",
            "Fictional provider phone number card (scripted)",
        ],
        "expected_actions": [
            "Leads with the one most important thing when asked 'what's first'.",
            "Catches the 'skip the pill if I feel fine' misconception.",
            "Surfaces the transportation barrier and proposes a scripted referral prop.",
            "Verifies warning-sign understanding by teach-back in the patient's own words.",
        ],
        "debrief_questions": [
            "How did you lead without burying the patient in paper?",
            "Which teach-back phrasing avoided a quiz-show feeling?",
            "What did the wrong warning-sign fixation teach you about pacing?",
            "How would you document the barrier you found and the referral you promised (in fiction)?",
        ],
    },
    "pressure-injury-prevention": {
        "id": "pressure-injury-prevention",
        "title": "Skin Pressure Checks & Repositioning Plan",
        "summary": "Simulated bedside skin check workflow plus a reposition schedule co-planned with the simulated patient.",
        "objectives": [
            "Perform a spoken, structured skin check over simulated pressure points.",
            "Co-create a repositioning and offloading plan the simulated patient will actually follow.",
            "Explain the why behind each reposition with non-lecture language.",
            "Document the fictional findings with the plan assigned and next check time.",
        ],
        "patient_statements": [
            "Turning all the time. I just fell asleep from laughing at my granddaughter.",
            "I've been sitting up to watch the game. Sitting up doesn't cause that, right?",
            "The pillowy thing slides off. I honestly prefer without it.",
            "My hip got sore where I lie all the time, so I switch to my back.",
            "When will the next turn be? I'll watch the clock myself if you show me.",
        ],
        "distractions": [
            "An on-time game artifact: the screen 'game preview' plays and the patient keeps glancing.",
            "The pillow wedge keeps sliding, testing the learner's problem-solving under time.",
            "The patient offers to conduct the next turns alone with a look at the clock.",
        ],
        "props": [
            "Simulated skin inspection 'chart' and pressure-point map prop",
            "Pillow wedge and easy-slide pillow setup",
            "Fictional reposition clock card",
            "Comfort props (blanket, pillow) that actually move",
        ],
        "expected_actions": [
            "Verbalizes point-by-point check instead of a general 'looks fine'.",
            "Admits back-lying as a risk and explains it rather than just 'sit less'.",
            "Fixes the sliding wedge with a no-blame repair.",
            "Leaves the patient with a clock plan they helped build.",
        ],
        "debrief_questions": [
            "How did you keep the structuring of a spoken skin check from feeling creepy or long?",
            "What language made sitting-up risk land without outright contradicting the patient?",
            "How did you co-build the clock plan instead of prescribing it?",
            "What would you chart about the wedge problem (fictionally)?",
        ],
    },
}

ROOMS = {
    "med-surg-double": {
        "id": "med-surg-double",
        "title": "Med-Surg Double Room",
        "summary": "A two-bed hospital room with a curtain divider, shared phone, extra motion, and a very alive neighbor.",
        "description": (
            "Two beds with a curtain that actually moves, a shared television, two call lights, "
            "and a lot of hallway noise from outside the door. The second bed is occupied in the "
            "simulation by a 'quiet' role-played neighbor (no lines, but present)."
        ),
        "room_props": [
            "Divider curtain (real, moves)",
            "Two wall-mounted call lights",
            "Shared television prop",
            "Second occupied bed with a non-speaking neighbor role",
        ],
        "ambient": "Hallway conversations, occasional loud paging, curtain rings scraping.",
    },
    "ambulatory-exam": {
        "id": "ambulatory-exam",
        "title": "Ambulatory Exam Room",
        "summary": "An outpatient clinic room: small footprint, quick pace, lots of hallway foot traffic.",
        "description": (
            "A compact room with an exam chair instead of a bed, a rolling stool, a small counter "
            "with a computer on it, and a paper gown basket. The simulation assumes a 15-minute visit."
        ),
        "room_props": [
            "Exam chair with paper-roll dispenser",
            "Rolling stool",
            "Counter with a computer stand-in",
            "Paper gowns and a step stool",
        ],
        "ambient": "Front-desk phone rings, squeaky hallway floor, hand-washing timer beeps.",
    },
    "long-term-care": {
        "id": "long-term-care",
        "title": "Long-Term Care Room",
        "summary": "A homier room with more personal items, realistic clutter, and a slower, relational pace.",
        "description": (
            "Bed plus a recliner, framed family photos, a television the resident controls, and a "
            "shelf of personal knickknacks. The resident has lived here long enough to know the routine "
            "better than the staff changeover schedule."
        ),
        "room_props": [
            "Recliner and over-bed table",
            "Family photo frames on the wall",
            "Knickknack shelf",
            "Personal television remote",
        ],
        "ambient": "Wheelchair traffic, a handyman's drill somewhere far away, low music from down the hall.",
    },
    "home-health-bedroom": {
        "id": "home-health-bedroom",
        "title": "Home Health Bedroom",
        "summary": "A private home bedroom: pets, cords, improvised surfaces, and real-life personality.",
        "description": (
            "A bedroom that is a home, not a clinic. A soft mattress, a dresser doing double duty as a "
            "supplies counter, a cat that 'comes in' during the simulation, and a rug with a curling edge."
        ),
        "room_props": [
            "Dresser doubling as a supply surface",
            "Pet role card (cat/entry at mid-encounter)",
            "Rug with a curling edge",
            "Fictional home med bottles in a paper bag",
        ],
        "ambient": "Doorbell, a kettle in the kitchen, neighbor's dog, hair dryer from the bathroom.",
    },
    "pre-op-holding": {
        "id": "pre-op-holding",
        "title": "Pre-Op Holding Bay",
        "summary": "A curtained pre-op area: checklists, forms, fast questions, and countdown energy.",
        "description": (
            "A bay in a curtained holding area, a rolling cart of forms, wristband supplies, and a "
            "countdown clock feel. The patient role is full of pre-op questions that arrive out of order."
        ),
        "room_props": [
            "Curtain bay (only partial privacy)",
            "Forms cart with fictional consent and checklist pages",
            "Wristband and marker supplies",
            "Fictional surgical countdown board",
        ],
        "ambient": "Monitors beeping behind curtains, cart wheels, muffled announcements from the OR desk.",
    },
    "skills-lab": {
        "id": "skills-lab",
        "title": "Skills Lab Station",
        "summary": "A deliberate practice space: task trainers, mirrors, a stopwatch, and easier permission to restart.",
        "description": (
            "A dedicated simulation lab with a task trainer arm, a bedside table mirror, a stopwatch, and "
            "a small stack of editable index cards. Best for first attempts and do-overs without patient risk trauma."
        ),
        "room_props": [
            "Task trainer arm and hand model",
            "Bedside table mirror",
            "Stopwatch",
            "Editable index and checklist cards",
        ],
        "ambient": "Other pairs practicing behind you, marker squeaks, occasional laughter from a debrief in progress.",
    },
}

DISCLAIMER = (
    "FOR PRACTICE — EDUCATION TRAINING MATERIAL ONLY. NOT MEDICAL ADVICE. "
    "All patient statements, findings, medications, and orders in this packet are "
    "fictional simulation content for training. Never apply any of it to a real person."
)
