import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Quiz data (same as before)
quiz_questions = [
    {
        "question":
        "In which of the following kinds of situation is translation usually the recipient of a lot of exposure?",
        "options": [
            'Academic conferences', 'Technical papers',
            'Television programming', 'Ambassador meetings'
        ],
        "correct":
        "C"
    },
    {
        "question":
        "The difference between declarative knowledge and procedural knowledge as applied to translation is which of the following?",
        "options": [
            'Procedural knowledge is needed for interpreting and declarative knowledge is used for writing texts',
            'Declarative knowledge is about subject of translation and procedural knowledge is about the act of translation',
            'Declarative knowledge refers to the translator’s speaking ability and procedural knowledge is concerned with the translation tools',
            'Procedural knowledge involves the physical aspects of translation and declarative knowledge the mental characteristics'
        ],
        "correct":
        "B"
    },
    {
        "question":
        "Which of the following is NOT one of the components of Translation competence?",
        "options": [
            'Passive knowledge of their working language',
            'Active working language competence',
            'Surface knowledge of the subject of Translation',
            'Declarative and procedural knowledge of Translation'
        ],
        "correct":
        "C"
    },
    {
        "question":
        "In Translation categories which level that would require the most competence?",
        "options": ['Technical', 'Conference', 'Social', 'Market'],
        "correct": "A"
    },
    {
        "question":
        "Which of the following types of Translation requires professional editorial skills?",
        "options": ['Business', 'Technical', 'Social', 'Conference'],
        "correct": "B"
    },
    {
        "question":
        "Which type of translation courses are favored by practicing Translators?",
        "options": ['University', 'Self-taught', 'Workshops', 'Formal'],
        "correct": "C"
    },
    {
        "question":
        "In-house Translator training has which of the following advantages?",
        "options": [
            'Instructor-student ratio is low',
            'Instructors have pedagogical skills',
            'Assignment content is universal and varied',
            'Relevancy is unnecessary'
        ],
        "correct":
        "A"
    },
    {
        "question":
        "Which of the following happens in process-oriented Translator training?",
        "options": [
            'Commentary on the correctness of translations',
            'Suggestions on linguistic choices',
            'Annotations on student exercises',
            'Problem identification and awareness'
        ],
        "correct":
        "D"
    },
    {
        "question":
        "Process-oriented Translation training concentrates of which of the following?",
        "options": [
            'Specific work solutions', 'Language structure',
            'Tactics and skills', 'Fidelity standards'
        ],
        "correct":
        "C"
    },
    {
        "question":
        "Product-oriented Translation has greater concentration on which of the following?",
        "options": [
            'Fidelity standards', 'Problem solving', 'Linguistic principles',
            'Error explanation'
        ],
        "correct":
        "A"
    },
    {
        "question":
        "What can be learned from Translation theoretical approaches?",
        "options": [
            'Skill application in the field', 'Language’s mental processes',
            'Historical inputs to language formation',
            'Analytical research tools'
        ],
        "correct":
        "B"
    },
    {
        "question":
        "According to the author, which of the following is NOT an advantage to knowing the theoretical components of Translation?",
        "options": [
            'Avoidance of time wasting activities',
            'Selection of appropriate tactics',
            'Generalizability to new situations',
            'Using outside forces to make decisions'
        ],
        "correct":
        "D"
    },
    {
        "question":
        "Translators can avoid falling into less efficient and less productive strategies and practices by understanding and using which of the following?",
        "options": [
            'Linguistic principles', 'Fidelity standards',
            'Theoretical concepts', 'Structured Syllabi'
        ],
        "correct":
        "C"
    },
    {
        "question":
        "Which concept increases the translation student’s receptiveness by demonstrating the relevance of theoretical components?",
        "options":
        ['Pedagogy', 'Sensitization', 'Representation', 'Interference'],
        "correct": "B"
    },
    {
        "question":
        "Theories that are directly applicable to a concrete action and can be easily recalled are classified as which of the following?",
        "options": [
            'Classically explainable', 'Practically definable',
            'Didactically effective', 'Developmentally adoptable'
        ],
        "correct":
        "C"
    },
    {
        "question":
        "Which model in the text explains the circumstances where Translation has a choice between target and source language informational differences?",
        "options": ['Fidelity', 'Effort', 'Gravitational', 'Technical'],
        "correct": "A"
    },
    {
        "question":
        "Which model of written translation stresses methodological principles, reformulation, and testing in phases?",
        "options":
        ['Fidelity', 'Sequential', 'Gravitational', 'Communications'],
        "correct": "B"
    },
    {
        "question":
        "Which translation model is based on the human mind’s limited processing capacity?",
        "options":
        ['Fidelity', 'Sequential', 'Gravitational', 'Communications'],
        "correct": "C"
    },
    {
        "question":
        "True or False?  Interpreters and translators must have adequate world knowledge.",
        "options": ['True', 'False'],
        "correct": "A"
    },
    {
        "question":
        "True or False?  Result-oriented translation approaches are unnecessary.",
        "options": ['True', 'False'],
        "correct": "B"
    },
    {
        "question":
        "Which of the following explains professional Translation?",
        "options": [
            'Interpreting the text and words in a different language',
            'Service activity with communication functionality',
            'Communication activity for source and target languages',
            'Service actions performed by translation schools'
        ],
        "correct":
        "B"
    },
    {
        "question":
        "School translation and interpreting about both categorized as which of the following?",
        "options": [
            'Translation activity', 'Professional translation',
            'Non-professional translation', 'Translation models'
        ],
        "correct":
        "A"
    },
    {
        "question":
        "True or False?  School translation differs from professional Translation in that professional Translation is facilitation and school Translation is more direct communication.",
        "options": ['True', 'False'],
        "correct": "A"
    },
    {
        "question":
        "In the communications model for Translation what is the correct name for the Target Language Receiver?",
        "options": ['Author', 'Reader', 'Client', 'Agent'],
        "correct": "C"
    },
    {
        "question":
        "The client of Translation is very often which of the following?",
        "options":
        ['An audience', 'An organization', 'The school', 'The speaker'],
        "correct": "B"
    },
    {
        "question":
        "An awareness of Translation can have which of the following effects?",
        "options": [
            'Clients will pay higher amounts',
            'Senders will use different terms and simplify',
            'Receivers will ignore mistakes',
            'Senders will display the feelings involved'
        ],
        "correct":
        "B"
    },
    {
        "question":
        "If the target language listeners form a small part of the audience, the interpreter may, in order to avoid interference, do which of the following?",
        "options": [
            'Stop translating', 'Sit quietly with the listeners',
            'Summarize main points',
            'Provide a one-on-one session with speaker'
        ],
        "correct":
        "C"
    },
    {
        "question":
        "The case of Translation of a sender’s notes to him/herself is complicated because of which of the following?",
        "options": [
            'The original receiver is the sender',
            'The sender’s intentions are well known',
            'The receiver has no need for the notes',
            'The sender’s notes are insignificant'
        ],
        "correct":
        "A"
    },
    {
        "question":
        "What is the name for the communication layer whose purpose is to release emotions?",
        "options": ['Phatic', 'Cathartic', 'Informative', 'Infusive'],
        "correct": "B"
    },
    {
        "question":
        "The communication layer that consists of messages with the intention of building a personal relationship is called which of the following?",
        "options": ['Phatic', 'Cathartic', 'Informative', 'Infusive'],
        "correct": "A"
    },
    {
        "question":
        "Conveying data, explaining, persuading, and making receivers do something are all types of which of the following?",
        "options": [
            'Literary Texts', 'Technical Texts', 'Informational Texts',
            'Explanatory Texts'
        ],
        "correct":
        "C"
    },
    {
        "question":
        "Micro- and macro-level aims of the sender refers to which of the following?",
        "options": [
            'Messages have different levels of details',
            'Messages are expressed in different word choices',
            'Message senders have varying intentions',
            'Messages are expandable'
        ],
        "correct":
        "C"
    },
    {
        "question":
        "Listing the sender’s accomplishments in a speech about new engineering standards for automobiles may have a macro-level aim of which of the following?",
        "options": [
            'Introducing credentials', 'Improving credibility',
            'Informing employers', 'Institutionalizing standards'
        ],
        "correct":
        "B"
    },
    {
        "question":
        "Providing translations of technological research articles is an example of which kind of translation service aim?",
        "options": [
            'Serving a Text', 'Serving a Source Language',
            'Serving potential readers', 'Serving the original sender'
        ],
        "correct":
        "C"
    },
    {
        "question":
        "From a reader’s perspective, a translation that reproduces the message including the message’s original grammatical error is which of the following?",
        "options": [
            'Poor quality message translation',
            'Informative message translation',
            'Less valuable message translation',
            'Overly interpreted message translation'
        ],
        "correct":
        "B"
    },
    {
        "question":
        "Packaging as well as content is included in which type of verbal communication?",
        "options": ['Graphical', 'Textual', 'Written', 'Verbal'],
        "correct": "D"
    },
    {
        "question":
        "Which of the following would be classified as packaging in verbal communication?",
        "options": [
            'Medical vocabulary', 'Specialty terms', 'Technical content',
            'Explanations'
        ],
        "correct":
        "B"
    },
    {
        "question":
        "Whom does a Translator usually represent when translating Informational texts?",
        "options": ['Sender', 'Client', 'Receiver', 'Publisher'],
        "correct": "C"
    },
    {
        "question":
        "Whom does a Translator usually represent when translating conference speakers?",
        "options": ['Sender', 'Client', 'Receiver', 'Organizers'],
        "correct": "A"
    },
    {
        "question":
        "True or False?  Transparent Neutrality as taught in schools is technically possible.",
        "options": ['True', 'False'],
        "correct": "B"
    },
    {
        "question":
        "Transparent Neutrality in Translation is commonly affected by which of the following?",
        "options": [
            'Translator loyalty', 'Translator choices',
            'Translator experience', 'Translator education'
        ],
        "correct":
        "B"
    },
    {
        "question":
        "Whom does a Translator represent when translating in a court?",
        "options": ['Sender', 'Client', 'Receiver', 'Rules'],
        "correct": "A"
    },
    {
        "question":
        "Which of the following is the most fundamental and most discussed Translation component?",
        "options": ['Simultaneous', 'Didactics', 'Linguistics', 'Fidelity'],
        "correct": "D"
    },
    {
        "question":
        "In which of the following contexts for translation are fidelity principles applied most strictly?",
        "options": [
            'Health interpreting', 'Conference interpreting',
            'Psychological counseling', 'Signed language'
        ],
        "correct":
        "B"
    },
    {
        "question":
        "In the context of translation of informational texts, the term message refers to which of the following?",
        "options": [
            'The statement produced by sender',
            'The statement intended by sender',
            'The statement defined by sender',
            'The statement verbalized by sender'
        ],
        "correct":
        "B"
    },
    {
        "question":
        "The difference between information content given in one sentence as compared to that given in another sentence (as explained in the textbook experiment) is described as which of the following?",
        "options": [
            'Redundant information', 'Informational presence or absence',
            'Informational gains or losses', 'Information known and unknown'
        ],
        "correct":
        "C"
    },
    {
        "question":
        "Which of the following phrases contains simple Framing Information regarding when one might arrive at a destination?",
        "options":
        ['60 more minutes', '60 minutes', 'time is 60', 'passed 60'],
        "correct": "A"
    },
    {
        "question":
        "Which of the following phrases contains simple Framing Information regarding the score needed to pass an exam?",
        "options": ['65', '65 percent', 'Average', 'Above average'],
        "correct": "B"
    },
    {
        "question":
        "When might certain contextual information be excluded from the communication?",
        "options": [
            'The message sender has no clear translatable form',
            'The expressions are too idiomatic',
            'The receiver knows that information',
            'The receiver is uneducated in the subject'
        ],
        "correct":
        "C"
    },
    {
        "question":
        "Which of the following describes Framing Information?",
        "options": [
            'Word selections that receiver has used',
            'Selections by sender that sender knows',
            'Selected messages that have new meanings',
            'Word Selections that help receiver understand'
        ],
        "correct":
        "D"
    },
    {
        "question":
        "Which of the following can result in informational gains during translation?",
        "options": [
            'Source language linguistic structure',
            'Target language linguistic rules', 'Sender’s informational needs',
            'Ignorance of target language linguistic structures'
        ],
        "correct":
        "B"
    },
    {
        "question":
        "Which of the following is an example of culturally induced information?",
        "options": [
            'Using forms of address', 'Inclusion of measurement terms',
            'Keeping to the future tense', 'Modifying personal information'
        ],
        "correct":
        "A"
    },
    {
        "question":
        "Word choice that reflects the sender’s educational background are considered which type of information?",
        "options": ['Framing', 'Linguistic', 'Personal', 'Cultural'],
        "correct": "C"
    },
    {
        "question":
        "The model: Message +(FI+LCII+PI) represents which of the following?",
        "options": [
            'Personal translation', 'Sentence information',
            'Cultural relevance', 'Comprehension'
        ],
        "correct":
        "B"
    },
    {
        "question":
        "Sender loyalty dictates that the Translator make minor corrections in all cases EXCEPT which of the following Translation types?",
        "options": ['Conference', 'Court', 'Scientific', 'Literary'],
        "correct": "B"
    },
    {
        "question":
        "Framing Information is appropriate in which of the following situations?",
        "options": [
            'French geographical locales to the French Parliament',
            'Currency type and equivalents to international traders',
            'Physical fitness terms to new gym members',
            'Dates and times to conference organizers'
        ],
        "correct":
        "C"
    },
    {
        "question":
        "The sender’s personal information may be an appropriate consideration in which of the following types of Translation?",
        "options": ['Technical', 'Business', 'Scientific', 'Literary'],
        "correct": "D"
    },
    {
        "question":
        "The relationship of linguistically/culturally induced information (LCII) to the sender is found in which of the following statements?",
        "options": [
            'Senders naturally choose the message that best fits the target audience',
            'Senders naturally use and integrate the source text culturally induced information',
            'Senders include source text explanations covering source text cultural differences',
            'Senders choose one from several linguistic options with the target language as a priority'
        ],
        "correct":
        "B"
    },
    {
        "question":
        "A reason to ignore Sender personal information during Translation is which of the following?",
        "options": [
            'Sender personal information is irrelevant to the message',
            'Sender personal information makes the translation more colorful',
            'Sender personal information adversely affects the message',
            'Sender personal information resulted in a stressed message tone'
        ],
        "correct":
        "A"
    },
    {
        "question":
        "True or False?  The verbalization experiment from the text demonstrated that there are no differences in individual senders’ information content.",
        "options": ['True', 'False'],
        "correct": "B"
    },
    {
        "question":
        "True or False?  Authors and speakers are conscious of the choices they have made for the word selection.",
        "options": ['True', 'False'],
        "correct": "B"
    },
    {
        "question":
        "Inform, explain, persuade, make receiver do something, make receiver refrain from doing something are all categories of which message attribute?",
        "options": ['Intention', 'Frame', 'Fidelity', 'Context'],
        "correct": "A"
    },
    {
        "question":
        "Which of the following is part of the definition of non-trivial comprehension of source language text and verbalization?",
        "options": [
            'Simple recognition of words',
            'Basic linguistic structure knowledge',
            'Extra-linguistic knowledge',
            'Competence in the skill of translation'
        ],
        "correct":
        "C"
    },
    {
        "question":
        "“Word for Word” translation is referred to as which of the following terms?",
        "options": ['Discourse', 'Transcoding', 'Encoding', 'Automatic'],
        "correct": "B"
    },
    {
        "question":
        "Extra-linguistic knowledge refers to which type of knowledge?",
        "options": ['Literary', 'Scientific', 'Encyclopaedic', 'Interpretive'],
        "correct": "C"
    },
    {
        "question":
        "In the textbook’s equation, C=KL+ELK+A, KL stands for which of the following?",
        "options": [
            'Kinesthetic learning', 'Knowledge of language',
            'Knowledge of lexicography', 'Knowledge links'
        ],
        "correct":
        "B"
    },
    {
        "question":
        "In the textbook’s equation, C=KL+ELK+A, C stands for which of the following?",
        "options":
        ['Comprehension', 'Conventional', 'Completeness', 'Contextual'],
        "correct": "A"
    },
    {
        "question":
        "Complementarity between linguistic knowledge and extra-linguistic knowledge refers to which of the following descriptions?",
        "options": [
            'Weakness in one type will result in more weakness in the other',
            'Strength in one type will compensate for lacks in the other',
            'Weakness causes the second type to be stronger',
            'Strength in high levels depends on the strength of the other type.'
        ],
        "correct":
        "B"
    },
    {
        "question":
        "In the textbook’s equation, C=KL+ELK+A, A stands for which of the following?",
        "options": ['Accuracy', 'Argument', 'Application', 'Analysis'],
        "correct": "D"
    },
    {
        "question":
        "Full comprehension levels will include different conceptual understandings of which of the following?",
        "options": [
            'Semantic content and connotations',
            'Textual roles and lexical meaning',
            'Social interplay and lexical meaning',
            'Connotative meanings and specialized roles'
        ],
        "correct":
        "A"
    },
    {
        "question":
        "The functional requirements of the Receiver include which of the following?",
        "options": [
            'Length and complexity', 'Technical terms', 'Actions required',
            'Familiar text formulations'
        ],
        "correct":
        "C"
    },
    {
        "question":
        "Which type of speech requires little stylistic or cultural knowledge?",
        "options": ['Psychological', 'Socio-legal', 'Business', 'Technical'],
        "correct": "D"
    },
    {
        "question":
        "An element included in analysis for translation of oral presentations is which of the following?",
        "options": [
            'Sender’s first language', 'Receiver’s motivations',
            'Time pressures', 'Legal requirements'
        ],
        "correct":
        "A"
    },
    {
        "question":
        "Which of the following questions addressed to a translator will initiate greater analysis?",
        "options": [
            'Where does the translation take place?',
            'Does the translation make sense?',
            'Which target language words were chosen?',
            'How many errors were found?'
        ],
        "correct":
        "B"
    },
    {
        "question":
        "Deconstruction of informative sentences into its parts becomes which of the following?",
        "options": [
            'Semantic networks', 'Nominal entities', 'Attributes',
            'Linkages and comparisons'
        ],
        "correct":
        "A"
    },
    {
        "question":
        "In semantic networks, persons, objects, ideas, and actions are categorized as which of the following?",
        "options": ['Links', 'Attributes', 'Nominal entities', 'Comparisons'],
        "correct": "C"
    },
    {
        "question":
        "In semantic networks, sentence structures and rules of grammar are categorized as which of the following?",
        "options": ['Links', 'Attributes', 'Nominal entities', 'Comparisons'],
        "correct": "A"
    },
    {
        "question":
        "If the following sentence was viewed as a semantic network, which of the following is the link?",
        "options": ['There', 'Are', 'Paradoxes', 'Work'],
        "correct": "B"
    },
    {
        "question":
        "Elementary-level segments of semantic networks are referred to as which of the following?",
        "options":
        ['Pure message', 'Sub-assemblies', 'Propositions', 'Verbalizations'],
        "correct":
        "C"
    },
    {
        "question":
        "True or False?  In highly specialized texts, Attributes and Links are very different and have more complexity than non-technical informative texts.",
        "options": ['True', 'False'],
        "correct": "B"
    },
    {
        "question":
        "The difference between a Translator’s knowledge of specialized texts and the specialist’s knowledge of the specialized text is which of the following?",
        "options": [
            'The specialist can use equivalents',
            'The specialist has more precise understanding',
            'The specialist uses extra-linguistic knowledge',
            'The specialist has the use of semantic networks'
        ],
        "correct":
        "B"
    },
    {
        "question":
        "Which of the following is the beginning step in the sequential model of written translation once the translation unit is identified?",
        "options": [
            'Meaning hypothesis', 'Basic linguistic knowledge',
            'Extra-linguistic knowledge', 'Reformulation'
        ],
        "correct":
        "A"
    },
    {
        "question":
        "The Translator applies which type of test to the meaning hypothesis?",
        "options": ['Ad hoc', 'Plausibility', 'Comprehension', 'Conceptual'],
        "correct": "B"
    },
    {
        "question":
        "If the Meaning Hypothesis does pass the plausibility test, which is the next step in the sequential model of written translation?",
        "options": [
            'Basic linguistic knowledge', 'Extra-linguistic knowledge',
            'Reformulation', 'Return to translation unit'
        ],
        "correct":
        "C"
    },
    {
        "question":
        "In the reformulation phase of the sequential model of written translation what happens to the Target-Text segment?",
        "options": [
            'Fidelity requirements are applied',
            'Plausibility test is applied',
            'The meaning hypothesis is rechecked',
            'It is verbalized using knowledge bases'
        ],
        "correct":
        "D"
    },
    {
        "question":
        "The Comprehension Loop and the Reformulation Loop differ from each other in which of the following manners?",
        "options": [
            'The Reformulation Loop aims for a higher quality of text production',
            'The Comprehension Loop is a systematic step toward production',
            'The Reformulation Loop acts on a different text message',
            'The Comprehension Loop follows message production'
        ],
        "correct":
        "A"
    },
    {
        "question":
        "If ad hoc Knowledge Acquisition takes place previous to the use of the Sequential Model, which of the following is needed?",
        "options": [
            'The basic flow changes to incorporate the ad hoc Knowledge',
            'The basic flow is interrupted to accommodate the ad hoc Knowledge',
            'The basic flow is followed regardless of the ad hoc Knowledge',
            'The basic flow begins with the Reformulation phase'
        ],
        "correct":
        "C"
    },
    {
        "question":
        "Which of the following situations would NOT result in the use of provisional target-language reformulation?",
        "options": [
            'Uncertainty of plausibility', 'Many ambiguous terms',
            'Constructed Meaning hypothesis', 'Incomprehensible structure'
        ],
        "correct":
        "C"
    },
    {
        "question":
        "Which of the following is recommended as an instructional strategy when teaching the Sequential Model?",
        "options": [
            'Use assignments where the “right \u200c method can be applied',
            'Make the assignment challenging and needful of many alternative decisions',
            'Have the students choose their own assignments according to self-analysis',
            'Encourage the students to make efficient changes to the basic flow'
        ],
        "correct":
        "A"
    },
    {
        "question":
        "Basically the skill that the Translator must use repeatedly during the Sequential Model is which of the following?",
        "options":
        ['Flexibility', 'Memorization', 'Pattern making', 'Decision making'],
        "correct":
        "D"
    },
    {
        "question":
        "In which of the following Translation contexts should Risk of Error be kept low?",
        "options": [
            'Window installations', 'Gaming instructions',
            'Computer repair manuals', 'Grocery buying tips'
        ],
        "correct":
        "C"
    },
    {
        "question":
        "The Meaning Hypothesis is followed by which of the following?",
        "options": ['Correction', 'Verbalization', 'Testing', 'Validation'],
        "correct": "C"
    },
    {
        "question":
        "The Meaning Hypothesis is corrected if which of the following occurs?",
        "options": [
            'Incongruence with other Target text portions',
            'Extra-linguistic matching to similar text',
            'Knowledge base relevance is apparent',
            'Beginner translators are involved'
        ],
        "correct":
        "A"
    },
    {
        "question":
        "True or False? The Translator’s knowledge base is augmented by the use of experts and dictionaries.",
        "options": ['True', 'False'],
        "correct": "A"
    },
    {
        "question":
        "Most editors of Translations focus on testing the text for which of the following?",
        "options": ['Fidelity', 'Acceptability', 'Relevance', 'Readability'],
        "correct": "B"
    },
    {
        "question":
        "An important difference in the use of the Sequential Model for interpreting is which of the following?",
        "options":
        ['Fidelity', 'Flow of model', 'Time constraints', 'Low risk'],
        "correct": "C"
    },
    {
        "question":
        "An important difference between written translation and interpreting is which of the following?",
        "options": [
            'Written translation requires a larger knowledge base',
            'Interpreting is usually final',
            'Interpreting requires extra-linguistic knowledge',
            'Written translation is very stressful'
        ],
        "correct":
        "B"
    },
    {
        "question":
        "Another important difference between written translators and interpreters when using the Sequential Model is which of the following?",
        "options": [
            'The decisions being made', 'The knowledge base used',
            'The translation segment size', 'The fidelity testing'
        ],
        "correct":
        "C"
    },
    {
        "question":
        "An instructional resource recommended for discussions about using the Sequential Model is which of the following?",
        "options": [
            'Simple unambiguous test segments taken from previous classes',
            'Text segments containing logical statements with grammatical errors',
            'Grammatically correct text containing implausible reasoning',
            'Unrelated text segments from a previous assignment'
        ],
        "correct":
        "C"
    },
    {
        "question":
        "Which of the following is the rationale for an instructor to introduce the Comprehension and Reformulation loops separately?",
        "options": [
            'Problems in reformulation can affect comprehension',
            'Comprehension problems affect reformulation',
            'Comprehension is unrelated to reformulation',
            'Reformulation is impossible to diagnose'
        ],
        "correct":
        "B"
    },
    {
        "question":
        "A strength of the Sequential Model as a pedagogical tool is its use for which of the following?",
        "options": [
            'Alternative Translation examples',
            'Selective Translation and analysis',
            'Error analysis and procedural methods',
            'Editorializing methods from past classes'
        ],
        "correct":
        "C"
    },
    {
        "question":
        "When does knowledge acquisition normally take place for an interpreter?",
        "options": [
            'Before the task', 'During the task', 'During and after the task',
            'After the task'
        ],
        "correct":
        "A"
    },
    {
        "question":
        "When does knowledge acquisition normally take place for a Translator?",
        "options": [
            'Before the task', 'During the task', 'During and after the task',
            'After the task'
        ],
        "correct":
        "B"
    },
    {
        "question":
        "A user manual would be classified as which of the following information sources?",
        "options":
        ['Essential', 'Fundamental', 'Terminological', 'Non-Terminological'],
        "correct":
        "D"
    },
    {
        "question":
        "A glossary would be classified as which of the following information sources?",
        "options":
        ['Essential', 'Fundamental', 'Terminological', 'Non-Terminological'],
        "correct":
        "C"
    },
    {
        "question":
        "Magazine articles would be classified as which of the following information sources?",
        "options":
        ['Essential', 'Fundamental', 'Terminological', 'Non-Terminological'],
        "correct":
        "D"
    },
    {
        "question":
        "When referring to time needed to locate and buy the source, it is called which of the following terms?",
        "options": ['Existence', 'External Access', 'Coverage', 'Reliability'],
        "correct": "B"
    },
    {
        "question":
        "If one is referring to the way a source is organized and searched, it is called which of the following terms?",
        "options":
        ['External Access', 'Internal Access', 'Coverage', 'Reliability'],
        "correct":
        "B"
    },
    {
        "question":
        "If one is looking for information on substance which information source variable would be important?",
        "options":
        ['External Access', 'Internal Access', 'Coverage', 'Reliability'],
        "correct":
        "D"
    },
    {
        "question":
        "Which type of information source faces the production challenges of available time, resources, selectivity, and keeping up-to-date?",
        "options": [
            'Paper terminological', 'Digital Terminological',
            'Functional terminological', 'Non-Terminological'
        ],
        "correct":
        "A"
    },
    {
        "question":
        "A match between the type of Text used as a source and the type of Text being translated is a sub-function of which of the following terms?",
        "options":
        ['External Access', 'Internal Access', 'Coverage', 'Reliability'],
        "correct":
        "D"
    },
    {
        "question":
        "Generally, a translated information source is which of the following?",
        "options": [
            'Hard to access', 'To be avoided', 'Comparable to other sources',
            'Expensive'
        ],
        "correct":
        "B"
    },
    {
        "question":
        "A strategy to overcome the problems of access to hard copy and human sources is to do which of the following?",
        "options": [
            'Employ free-lancers', 'Invest in dictionaries',
            'Translator specialization', 'Use an intermediate source'
        ],
        "correct":
        "C"
    },
    {
        "question":
        "Which of the following does the text infer is a profitable strategy in regard to terminological information?",
        "options": [
            'Use general language text books', 'Use glossaries in text books',
            'Use many sources', 'Use the table of contents'
        ],
        "correct":
        "B"
    },
    {
        "question":
        "Which of the following is a challenge when using electronic sources?",
        "options": ['Validity', 'Access', 'Reliability', 'Specialization'],
        "correct": "C"
    },
    {
        "question":
        "Which of the following functions of digital sources is very valuable to Translators?",
        "options": ['Index', 'Sorting', 'Architecture', 'Search'],
        "correct": "D"
    },
    {
        "question":
        "Potentially, the most powerful source of all for translation is which of the following?",
        "options":
        ['Terminological', 'Non-Terminological', 'Human', 'Digital'],
        "correct": "C"
    },
    {
        "question":
        "The biggest challenge with using human sources for translation assistance and information is which of the following?",
        "options": ['Validity', 'Reliability', 'Costs', 'Access'],
        "correct": "D"
    },
    {
        "question":
        "In strategizing for conference translation, advance preparation would NOT usually include which of the following?",
        "options": [
            'Contacting fellow translators', 'Obtaining conference documents',
            'Taking part in briefings', 'Obtaining drafts of articles'
        ],
        "correct":
        "A"
    },
    {
        "question":
        "Micro-computers, text processing and spread sheet software assist conference translators by allowing them to do which of the following?",
        "options": [
            'Increase their terminological knowledge',
            'Build their own drafts of speeches',
            'Build specialized, accessible glossaries',
            'Increase the time allowed for interpreting'
        ],
        "correct":
        "C"
    },
    {
        "question":
        "The underlying intuitive ideas which resulted in the Effort Models assume which of the following is required for interpreting?",
        "options": [
            'Physical energy', 'Mental energy', 'Working memory',
            'Short-term memory'
        ],
        "correct":
        "B"
    },
    {
        "question":
        "A difference between non-automatic and automatic cognitive operations is which of the following?",
        "options": [
            'Automatic operations require processing capacity',
            'Non-Automatic operations require processing capacity',
            'Automatic operations take more time',
            'Non-Automatic operations have an unlimited supply of time'
        ],
        "correct":
        "B"
    },
    {
        "question":
        "Performance can deteriorate if which of the following occurs?",
        "options": [
            'Processing capacity is insufficient', 'Operations are automated',
            'Familiar stimuli are encountered',
            'Processing requirements are reduced'
        ],
        "correct":
        "A"
    },
    {
        "question":
        "Which of the following is an example of the involvement of an automatic cognitive operation?",
        "options": [
            'Counting by 3s', 'Making buying decisions',
            'Identifying colors on billboards',
            'Selecting book titles from shelves'
        ],
        "correct":
        "C"
    },
    {
        "question":
        "Which of the following is an example of the involvement of a non-automatic cognitive operation?",
        "options": [
            'Tying one’s shoe laces', 'Reciting rote passages',
            'Brushing teeth', 'Paying a cashier'
        ],
        "correct":
        "D"
    },
    {
        "question":
        "Responses to “Decoding a familiar stimulus presented under favourable conditions” is a description of which of the following?",
        "options": [
            'Metacognitive operations', 'Automatic operations',
            'Non-automatic operations', 'Cognitive construction'
        ],
        "correct":
        "B"
    },
    {
        "question":
        "Listening and analysis, speech production and short-term memory are components of which of the following?",
        "options": [
            'Translation effort', 'Automatic effort', 'Interpreting effort',
            'Processing effort'
        ],
        "correct":
        "C"
    },
    {
        "question":
        "Listening and analysis during interpretation includes which of the following?",
        "options": ['Chaining', 'Comparing', 'Anticipating', 'Sequencing'],
        "correct": "C"
    },
    {
        "question":
        "Machine translation programs based on linguistic analysis fail to use which type of knowledge?",
        "options": ['Semantic', 'World', 'Logical', 'Lexical'],
        "correct": "B"
    },
    {
        "question":
        "Which of the following is NOT found in the interpreter’s Production Effort?",
        "options": [
            'Mental representation', 'Speech planning', 'Self-monitoring',
            'Meaning analysis'
        ],
        "correct":
        "D"
    },
    {
        "question":
        "Linguistic interference is most commonly associated with which of the following?",
        "options": [
            'Transcoding', 'Self-monitoring', 'Speech planning',
            'Lexical choices'
        ],
        "correct":
        "A"
    },
    {
        "question":
        "Most interpreting instructors advise producing the target-language speech using which of the following?",
        "options": [
            'Source language words', 'Source language meaning',
            'Target language usage', 'Target language words'
        ],
        "correct":
        "B"
    },
    {
        "question":
        "Memory Effort involves which of the following?",
        "options": [
            'Identifying phonetic features', 'Mentally representing meanings',
            'Self-correction', 'Speech planning'
        ],
        "correct":
        "A"
    },
    {
        "question":
        "True or False?  The sequential linearity simplification of the Effort Model assumes that production can focus on one segment of the source speech while another segment is being analyzed.",
        "options": ['True', 'False'],
        "correct": "A"
    },
    {
        "question":
        "Anticipation during sequential interpreting can result in which of the following?",
        "options": [
            'Information order changes',
            'Misrepresentation of speaker’s thoughts',
            'Long-term memory faults',
            'Syntactic differences from source to target'
        ],
        "correct":
        "B"
    },
    {
        "question":
        "The Effort Model for interpreting indicates that which of the following takes place?",
        "options": [
            'Speech analysis and speech comprehension have equal influence',
            'Speech comprehension is guided by the processing capacity',
            'Speech comprehension and speech production share working memory',
            'Speech production is delayed significantly by processing capacity'
        ],
        "correct":
        "C"
    },
    {
        "question":
        "True or False?  The clarity of the speaker’s material and voice has no effect on cognitive load.",
        "options": ['True', 'False'],
        "correct": "B"
    },
    {
        "question":
        "True or False?  In the formula SI = L + P + M + C, the plus sign refers to mathematical addition.",
        "options": ['True', 'False'],
        "correct": "B"
    },
    {
        "question":
        "The equal sign in the formula SI = L + P + M + C has which meaning?",
        "options": ['Equivalence', 'Consists of', 'Results from', 'Completes'],
        "correct": "B"
    },
    {
        "question":
        "In the Effort Model, TR=LR+MR+PR+CR, M represents which of the following?",
        "options": ['Metacognitive', 'Mental', 'Memory', 'Maintenance'],
        "correct": "C"
    },
    {
        "question":
        "In the Effort Model, TR=LR+MR+PR+CR, R represents which of the following?",
        "options": ['Regulator', 'Requirement', 'Receiver', 'Reproduction'],
        "correct": "B"
    },
    {
        "question":
        "Extremely fast speech and complex sentence structures along with a uncommon vocabulary would first affect which of the processing requirements?",
        "options": [
            'Listening and production', 'Listening and memory',
            'Production and memory', 'Memory and operational'
        ],
        "correct":
        "B"
    },
    {
        "question":
        "Omissions and errors are classified as which type of processing capacity problems?",
        "options": ['Contextual', 'Delivery', 'Content', 'Distortion'],
        "correct": "C"
    },
    {
        "question":
        "Which of the following does NOT commonly result in the loss of segments during interpreting?",
        "options":
        ['Numbers', 'Long names', 'Elegant wording', 'Standard wording'],
        "correct": "D"
    },
    {
        "question":
        "The use of a noun following an article or adjective in English is an example of which of the following?",
        "options": [
            'Transitional probability', 'Standard phraseology',
            'Processing anticipation', 'Production anticipation'
        ],
        "correct":
        "A"
    },
    {
        "question":
        "In certain conditions the interpreting may rely on which type of anticipation even if it is an inexact prediction?",
        "options": [
            'Transitional probability', 'Extra-linguistic anticipation',
            'Processing anticipation', 'Production anticipation'
        ],
        "correct":
        "B"
    },
    {
        "question":
        "The result of the reduction of uncertainty through anticipation will be which of the following?",
        "options": [
            'Mental Saturation', 'Stricter Analysis', 'Cognitive relief',
            'Listening relief'
        ],
        "correct":
        "C"
    },
    {
        "question":
        "Consecutive interpreting is defined in which of the following statements?",
        "options": [
            'The uninterrupted speech is dealt with one sentence at a time',
            'The uninterrupted speech contains more than one sentence',
            'The uninterrupted speech of several sentences that distracts from note taking',
            'The uninterrupted speech contains a few sentences and allows note taking.'
        ],
        "correct":
        "D"
    },
    {
        "question":
        "In the Effort Model for consecutive interpreting, Interpreting = L+N+M+C, the N stands for which of the following?",
        "options": ['Narrative', 'Note taking', 'Non-sequential', 'Native'],
        "correct": "B"
    },
    {
        "question":
        "In the Effort Model for consecutive interpreting, Interpreting = L+N+M+C, the C stands for which of the following?",
        "options": ['Cognition', 'Clarity', 'Coordination', 'Condensation'],
        "correct": "C"
    },
    {
        "question":
        "Listening and Analysis Effort becomes Reading Effort in which type of interpreting?",
        "options": ['Consecutive', 'Segment', 'Sight', 'Simultaneous'],
        "correct": "C"
    },
    {
        "question":
        "Simultaneous interpreting with text adds which extra component to the Effort Model of Interpreting differing it from the consecutive interpreting?",
        "options": ['Listening', 'Reading', 'Note taking', 'Memory'],
        "correct": "B"
    },
    {
        "question":
        "In the Tightrope Hypothesis which of the following is true?",
        "options": [
            'Interpreters balance their processing loads',
            'Interpreters problem solve while producing',
            'Interpreters process close to saturation',
            'Interpreters work with the available capacity'
        ],
        "correct":
        "C"
    },
    {
        "question":
        "True or False?  The risk of processing capacity saturation lower in written translation.",
        "options": ['True', 'False'],
        "correct": "A"
    },
    {
        "question":
        "True or False?  Processing capacity differences can explain why some translators have problems with simultaneous interpreting?",
        "options": ['True', 'False'],
        "correct": "A"
    },
    {
        "question":
        "Consideration of which of the following can help in the allocation of processing capacity during various efforts?",
        "options": [
            'Capacity requirements', 'Capacity performance',
            'Capacity management', 'Capacity discovery'
        ],
        "correct":
        "C"
    },
    {
        "question":
        "Attention-division exercises is a tactic for which of the following?",
        "options": [
            'Capacity requirements', 'Capacity performance',
            'Capacity management', 'Capacity discovery'
        ],
        "correct":
        "C"
    },
    {
        "question":
        "True or False?  Classroom exercises and practice show little improvement in component skill training of interpreters.",
        "options": ['True', 'False'],
        "correct": "B"
    },
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message with a 'Begin Quiz' button."""
    keyboard = [[
        InlineKeyboardButton("Begin Quiz", callback_data="start_quiz")
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Welcome to the Quiz Bot! Type anything or click the button to begin the quiz.",
        reply_markup=reply_markup)


async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the first question."""
    context.user_data['score'] = 0  # Initialize score
    context.user_data['total_questions'] = len(
        quiz_questions)  # Total questions
    context.user_data['question_index'] = 0  # Start at the first question
    question_index = 0
    await ask_question(update, context, question_index)


async def ask_question(update, context, question_index):
    """Send a question with answer options."""
    question = quiz_questions[question_index]
    total_questions = context.user_data['total_questions']

    keyboard = [
        [
            InlineKeyboardButton(
                opt, callback_data=f"answer|{question_index}|{opt[:30]}")
        ]  # Limiting option size if necessary
        for opt in question["options"]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(
            f"Question {question_index + 1} of {total_questions}\n{question['question']}",
            reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.reply_text(
            f"Question {question_index + 1} of {total_questions}\n{question['question']}",
            reply_markup=reply_markup)


async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the answer selection."""
    query = update.callback_query
    await query.answer()

    _, question_index, selected_option = query.data.split('|')
    question_index = int(question_index)
    question = quiz_questions[question_index]
    correct_answer = question["correct"]
    correct_option = question["options"][ord(correct_answer) - ord('A')]

    if selected_option == correct_option:
        context.user_data['score'] += 1
        await query.edit_message_text(
            f"Question {question_index + 1} of {len(quiz_questions)}\n{question['question']}\n\nCorrect! ✅ The answer is: {correct_option}"
        )
    else:
        await query.edit_message_text(
            f"Question {question_index + 1} of {len(quiz_questions)}\n{question['question']}\n\nWrong! ❌ The correct answer was: {correct_option}"
        )

    if question_index + 1 < len(quiz_questions):
        context.user_data['question_index'] = question_index + 1
        await ask_question(update, context, question_index + 1)
    else:
        score = context.user_data['score']
        total_questions = context.user_data['total_questions']

        if score == total_questions:
            await query.message.reply_text(
                f"Quiz completed! 🎉\nYour score: {score}/{total_questions}\nWell done! 🎉"
            )
        else:
            keyboard = [[
                InlineKeyboardButton("Try Again", callback_data="start_quiz")
            ]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(
                f"Quiz completed! 🎉\nYour score: {score}/{total_questions}\nKeep practicing to achieve full marks! حظاً سعيداً في الاختبار - مع تحيات خالد",
                reply_markup=reply_markup)


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle 'Begin Quiz' and 'Try Again' actions."""
    query = update.callback_query
    await query.answer()

    if query.data == "start_quiz":
        await quiz(update, context)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle any message to start the quiz."""
    await quiz(update, context)


def main():
    """Run the bot."""
    application = Application.builder().token(
        "7589625226:AAHhbcS82YRT8F4niSuoNjfiYUbWW_LGZ8o").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(
        CallbackQueryHandler(handle_callback, pattern="^start_quiz$"))
    application.add_handler(
        CallbackQueryHandler(handle_answer, pattern="^answer\\|"))

    application.run_polling()


if __name__ == "__main__":
    main()
