# Imports

import logging
from typing import Tuple, Dict, Any
from datetime import date, datetime
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackQueryHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

# State definitions for top level conversation
SELECTING_ACTION, ADDING_MEMBER, ADDING_SELF, DESCRIBING_SELF = map(chr, range(4))
# State definitions for second level conversation
SELECTING_LEVEL, SELECTING_GENDER = map(chr, range(4, 6))
# State definitions for descriptions conversation
SELECTING_FEATURE, TYPING = map(chr, range(6, 8))
# Meta states
STOPPING, SHOWING = map(chr, range(8, 10))
# Shortcut for ConversationHandler.END
END = ConversationHandler.END

# Different constants for this example
(
    SECT_1,
    SECT_3a,
    SECT_3b,
    SECT_3c,
    SECT_3d,
    SECT_4,
    SECT_6,
    SECT_7,
    SECT_10,
    CHILDREN,
    SELF,
    GENDER,
    MALE,
    FEMALE,
    AGE,
    NRIC,
    NAME,
    SVS,
    RANK,
    START_OVER,
    FEATURES,
    CURRENT_FEATURE,
    CURRENT_LEVEL,
) = map(chr, range(10, 33))


# Helper
def _name_switcher(level: str) -> Tuple[str, str]:
    if level == SECT_1:
        return "Father", "Mother"
    return "Brother", "Sister"


def request_update(date):
    updates = []
    # print(f'Send your Report Sick Updates as of {date}. Type "DONE" to submit!\n')
    while True:
        incident = "DONE"  # input().strip()
        if incident.strip().upper() == "DONE":
            break
        else:
            updates.append(incident)
    return "\n\n".join(updates)


# Main Form Class
class Form:
    def __init__(self, type, initial_time, sypmtoms):
        self.date = datetime.now().strftime("%d%m%y")
        self.time = datetime.now().strftime("%H%M")
        self.type = type
        self.initial_time = initial_time
        self.symptoms = sypmtoms
        self.sections = [""] * 14

    def sect_0(self):
        self.sections[
            0
        ] = f"*{self.date}, {self.time}hrs*\n*11 C41 BN, SIG*\n*{self.type}*"

    def sect_1(self, nature):
        if nature == "TR":
            nature = "Training Related"
        else:
            nature = "Non-Training Related"
        self.sections[
            1
        ] = f"1) *Nature and Type of incident*:\n{nature}\n{self.symptoms.upper()}"

    def sect_2(self, NRIC, rank, fullname, service, sex, age):
        masked_NRIC = NRIC[:1] + "XXXX" + NRIC[5:]
        self.sections[
            2
        ] = f"2) *Particulars of Serviceman/men Involved*:\nNRIC: {masked_NRIC.upper()}\nRank/Name: {rank.upper()} {fullname.upper()}\nSvs Status: {service.upper()}\nSex/Age: {sex.upper()}/{age}\nCoy/Pl: SIGNALS"

    def sect_3a(self, history):
        self.sections[
            3
        ] = f"3) *Brief Description of Incident*:\nServiceman has previously reported sick on the following dates:\n{history}"

    def sect_3b(self, updates):
        self.sections[
            4
        ] = f"On {self.date},\n\nAt {self.initial_time}, Serviceman requested to report sick for {self.symptoms}.\n\n{updates}"

    def sect_3c(self, update_date, updates):
        self.sections[5] = f"On {update_date},\n\n{updates}"

    def sect_3d(self, overall, ART, PCR):
        swap_lib = {"X": "PENDING", "N": "NEGATIVE", "P": "POSITIVE"}
        self.sections[
            6
        ] = f"*Other Details*\n- *SWAB Test Done*: *{swap_lib[overall]}* (ART - *{swap_lib[ART]}*, PCR - *{swap_lib[PCR]}*)\n- Travelled Overseas in the past 14 days: NIL\n- Close Contact with a confirmed case: NIL\n- Stays in a foreign worker dormitory: NIL\n- Works in a High-Risk Area: NIL\n- Prolonged ARI with fever above 37.5C for 4 days and above: NIL\n- Suspected Pneumonia: NIL"

    def sect_4(self, status, date_end):
        self.sections[
            7
        ] = f"4) *Current Status*:\n{status} from {self.date} to {date_end}"

    def sect_5(self):
        self.sections[
            8
        ] = f"5) *Date & Time of Incident*:\n{self.date}, {self.initial_time}hrs"

    def sect_6(self, location):
        if not location:
            location = "Pasir Laba Camp"
        self.sections[9] = f"6) *Location of incident*:\n{location}"

    def sect_7(self, actions):
        if actions == "URTI":
            actions = "Unit will continue to monitor serviceman’s condition. He will report back to camp when his MC ends or when his swab test result returns negative. Which ever is later."
        self.sections[10] = f"7) *Follow Up Actions*:\n{actions}"

    def sect_8(self):
        self.sections[
            11
        ] = f"8) *Details/Particulars of civilian involved, if any*: (For accidents)\nNRIC (Masked): -\nName: -\nAge: -\nGender: -\nContact No.: -"

    def sect_9(self):
        self.sections[12] = f"9) *Date & Time reported to GSOC*:\nVerbal: -\nASIS: -"

    def sect_10(self, POC_rank, POC_name, POC_rel, POC_phone):
        self.sections[
            13
        ] = f"10) *Reporting Officer*: \n\n*Point of Contact*:\n{POC_rank} {POC_name}\n{POC_rel}, SIG COY\n{POC_phone}\n\n*Vetted By*"

    def display(self):
        return "\n\n".join(self.sections)


# Top level conversation callbacks
def start(update: Update, context: CallbackContext) -> str:
    """Select an action: Editing 11 Liner Sections or Show 11 Liner."""
    text = "You may choose to edit the 11 Liner, edit your info, show the gathered data, or end the conversation. To abort, simply type /stop"

    buttons = [
        [
            InlineKeyboardButton(
                text="Edit 11 Liner", callback_data=str(ADDING_MEMBER)
            ),
            InlineKeyboardButton(
                text="Edit Personal Data", callback_data=str(ADDING_SELF)
            ),
        ],
        [
            InlineKeyboardButton(text="Show 11 Liner", callback_data=str(SHOWING)),
            InlineKeyboardButton(text="Done", callback_data=str(END)),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    # If we're starting over we don't need to send a new message
    if context.user_data.get(START_OVER):
        update.callback_query.answer()
        update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    else:
        update.message.reply_text(
            "Hi, I'm 11 Liner Bot and I'm here to help you with formatting your 11 Liner."
        )
        update.message.reply_text(text=text, reply_markup=keyboard)

    context.user_data[START_OVER] = False
    return SELECTING_ACTION


"""
EDIT THIS SHIT TO FIT MORE DETAILS
"""


def adding_self(update: Update, context: CallbackContext) -> str:
    """Add information about yourself."""
    context.user_data[CURRENT_LEVEL] = SELF
    text = "Okay, please tell me about yourself."
    button = InlineKeyboardButton(text="Add info", callback_data=str(MALE))
    keyboard = InlineKeyboardMarkup.from_button(button)

    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    return DESCRIBING_SELF


"""
EDIT THIS SHIT TO FIT THE 11 LINER DISPLAY
"""

# Chat Bot (Main Program)
def generate_blank():
    # print("""Generating 11 Minor! Please input details as requested.""")

    # Header
    # print("== HEADER ==\n")
    s1_type = "-"  # input("NEW/FINAL: ").strip()
    s1_initial_time = "XXXX"  # input("TIME [HHMM] REPORTED SICK: ").strip()
    s1_symptoms = "-"  # input("LIST SYMPTOMS: ").strip()
    form = Form(s1_type, s1_initial_time, s1_symptoms)
    form.sect_0()

    # Section 1
    # print("== SECTION 1 ==\n")
    nature = "-"  # input("TR/NTR: ").strip()
    form.sect_1(nature)

    # Section 2
    # print("== SECTION 2 ==\n")
    s2_nric = "TXXXX456Z"  # input("NRIC: ").strip()
    s2_rank = "-"  # input("RANK: ").strip()
    s2_fullname = "-"  # input("FULLNAME: ").strip()
    s2_service = "-"  # input("NSF/REG: ").strip()
    s2_sex = "-"  # input("M/F: ").strip()
    s2_age = "-"  # input("AGE: ").strip()
    form.sect_2(s2_nric, s2_rank, s2_fullname, s2_service, s2_sex, s2_age)

    # Section 3a
    # print("== SECTION 3A ==\n")
    s3a_history = []
    count = 1
    # print('Send your Report Sick History. Type "DONE" to submit!\n')
    while count != 0:
        incident = "DONE"
        if incident.strip().upper() == "DONE":
            count = 0
        else:
            s3a_history.append(f"{count}. {incident}")
            count += 1
    form.sect_3a("\n".join(s3a_history))

    # Section 3b
    date = datetime.now().strftime("%d%m%y")
    # print("== SECTION 3B ==\n")
    form.sect_3b(request_update(date))

    # Section 3c
    if type == "FINAL":
        date = "XXXXXX"  # input("FINAL UPDATE DATE: ").strip()
        # print("== SECTION 3C ==\n")
        form.sect_3c(date, request_update(date))

    # Section 3d
    # print("== SECTION 3D ==\n")
    # results = list(input("URTI TEST RESULTS (X/N/P): ").strip())
    s3d_overall, s3d_ART, s3d_PCR = "X", "X", "X"  # (results[0],results[1],results[2],)
    form.sect_3d(s3d_overall, s3d_ART, s3d_PCR)

    # Section 4
    # print("== SECTION 4 ==\n")
    status = "-"  # input("STATUS: ").strip()
    date_end = "XXXXXX"  # input("ENDDATE: ").strip()
    form.sect_4(status, date_end)

    # Section 5
    form.sect_5()

    # Section 6
    # print("== SECTION 6 ==\n")
    form.sect_6("-")  # input("LOCATION: ").strip()

    # Section 7
    # print("== SECTION 7 ==\n")
    form.sect_7("URTI")  # input("FOLLOW UP ACTIONS: ").strip()

    # Section 8
    form.sect_8()

    # Section 9
    form.sect_9()

    # Section 10
    # print("== SECTION 10 ==\n")
    POC_rank = "3SG"  # input("POC RANK: ").strip().upper()
    POC_name = "-"  # input("POC NAME: ").strip().upper()
    POC_rel = "DET COMD"  # input("POC RELATION: ").strip().upper()
    POC_phone = "XXXX XXXX"  # input("POC PHONE: ").strip()
    if len(POC_phone) == 8:
        POC_phone = POC_phone[:4] + " " + POC_phone[4:]
    form.sect_10(POC_rank, POC_name, POC_rel, POC_phone)

    return form.display()


def show_data(update: Update, context: CallbackContext) -> str:
    """Pretty print gathered data."""

    # def prettyprint(user_data: Dict[str, Any], level: str) -> str:
    #     people = user_data.get(level)
    #     if not people:
    #         return "\nNo information yet."

    #     text = ""
    #     if level == SELF:
    #         for person in user_data[level]:
    #             text += f"\nName: {person.get(NAME, '-')}, Age: {person.get(AGE, '-')}"
    #     else:
    #         male, female = _name_switcher(level)

    #         for person in user_data[level]:
    #             gender = female if person[GENDER] == FEMALE else male
    #             text += f"\n{gender}: Name: {person.get(NAME, '-')}, Age: {person.get(AGE, '-')}"
    #     return text

    user_data = context.user_data
    # text = f"Yourself:{prettyprint(user_data, SELF)}"
    # text += f"\n\nParents:{prettyprint(user_data, SECT_1)}"
    # text += f"\n\nChildren:{prettyprint(user_data, CHILDREN)}"

    text = generate_blank()
    print(repr(text))

    buttons = [[InlineKeyboardButton(text="Back", callback_data=str(END))]]
    keyboard = InlineKeyboardMarkup(buttons)

    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    user_data[START_OVER] = True

    return SHOWING


# DONE
def stop(update: Update, context: CallbackContext) -> int:
    """End Conversation by command."""
    update.message.reply_text("See you next time.")

    return END


# DONE
def end(update: Update, context: CallbackContext) -> int:
    """End conversation from InlineKeyboardButton."""
    update.callback_query.answer()

    text = "See you around!"
    update.callback_query.edit_message_text(text=text)

    return END


# Second level conversation callbacks
def select_level(update: Update, context: CallbackContext) -> str:
    """Choose a Section of the 11 Liner to Edit."""
    text = "Choose a Section of the 11 Liner to Edit. Also you can show the gathered data or go back."
    buttons = [
        [
            InlineKeyboardButton(text="Section 1", callback_data=str(SECT_1)),
            InlineKeyboardButton(text="Section 3", callback_data=str(SECT_3a)),
            InlineKeyboardButton(text="Section 4", callback_data=str(SECT_4)),
            InlineKeyboardButton(text="Section 6", callback_data=str(SECT_6)),
        ],
        [
            InlineKeyboardButton(text="Section 7", callback_data=str(SECT_7)),
            InlineKeyboardButton(text="Section 10", callback_data=str(SECT_10)),
            InlineKeyboardButton(text="Show data", callback_data=str(SHOWING)),
            InlineKeyboardButton(text="Back", callback_data=str(END)),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    return SELECTING_LEVEL


def select_gender(update: Update, context: CallbackContext) -> str:
    """Choose to add mother or father."""
    level = update.callback_query.data
    context.user_data[CURRENT_LEVEL] = level

    text = "Please choose, whom to add."

    male, female = _name_switcher(level)

    buttons = [
        [
            InlineKeyboardButton(text=f"Add {male}", callback_data=str(MALE)),
            InlineKeyboardButton(text=f"Add {female}", callback_data=str(FEMALE)),
        ],
        [
            InlineKeyboardButton(text="Show data", callback_data=str(SHOWING)),
            InlineKeyboardButton(text="Back", callback_data=str(END)),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    return SELECTING_GENDER


# DONE
def end_second_level(update: Update, context: CallbackContext) -> int:
    """Return to top level conversation."""
    context.user_data[START_OVER] = True
    start(update, context)

    return END


# Third level callbacks
def select_feature(update: Update, context: CallbackContext) -> str:
    """Select a feature to update for the person."""
    buttons = [
        [
            InlineKeyboardButton(text="NRIC", callback_data=str(NRIC)),
            InlineKeyboardButton(text="Rank", callback_data=str(RANK)),
        ],
        [
            InlineKeyboardButton(text="Fullname", callback_data=str(NAME)),
            InlineKeyboardButton(text="Svs Status", callback_data=str(SVS)),
        ],
        [
            InlineKeyboardButton(text="Age", callback_data=str(AGE)),
            InlineKeyboardButton(text="Done", callback_data=str(END)),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    # If we collect features for a new person, clear the cache and save the gender
    if not context.user_data.get(START_OVER):
        context.user_data[FEATURES] = {GENDER: update.callback_query.data}
        text = "Please select a feature to update."

        update.callback_query.answer()
        update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    # But after we do that, we need to send a new message
    else:
        text = "Got it! Please select a feature to update."
        update.message.reply_text(text=text, reply_markup=keyboard)

    context.user_data[START_OVER] = False
    return SELECTING_FEATURE


# DONE
def ask_for_input(update: Update, context: CallbackContext) -> str:
    """Prompt user to input data for selected feature."""
    context.user_data[CURRENT_FEATURE] = update.callback_query.data
    text = "Okay, tell me."

    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text)

    return TYPING


# DONE
def save_input(update: Update, context: CallbackContext) -> str:
    """Save input for feature and return to feature selection."""
    user_data = context.user_data
    user_data[FEATURES][user_data[CURRENT_FEATURE]] = update.message.text

    user_data[START_OVER] = True

    return select_feature(update, context)


# DONE
def end_describing(update: Update, context: CallbackContext) -> int:
    """End gathering of features and return to parent conversation."""
    user_data = context.user_data
    level = user_data[CURRENT_LEVEL]
    if not user_data.get(level):
        user_data[level] = []
    user_data[level].append(user_data[FEATURES])

    # Print upper level menu
    if level == SELF:
        user_data[START_OVER] = True
        start(update, context)
    else:
        select_level(update, context)

    return END


# DONE
def stop_nested(update: Update, context: CallbackContext) -> str:
    """Completely end conversation from within nested conversation."""
    update.message.reply_text("See you next time.")

    return STOPPING


# DONE
def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("1867473854:AAEpabnZ1l7HOK0Oth7tQHRpIjAW8WiXPTk")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Set up third level ConversationHandler (collecting features)
    description_conv = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                select_feature, pattern="^" + str(MALE) + "$|^" + str(FEMALE) + "$"
            )
        ],
        states={
            SELECTING_FEATURE: [
                CallbackQueryHandler(ask_for_input, pattern="^(?!" + str(END) + ").*$")
            ],
            TYPING: [MessageHandler(Filters.text & ~Filters.command, save_input)],
        },
        fallbacks=[
            CallbackQueryHandler(end_describing, pattern="^" + str(END) + "$"),
            CommandHandler("stop", stop_nested),
        ],
        map_to_parent={
            # Return to second level menu
            END: SELECTING_LEVEL,
            # End conversation altogether
            STOPPING: STOPPING,
        },
    )

    # Set up second level ConversationHandler (adding a person)
    add_member_conv = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(select_level, pattern="^" + str(ADDING_MEMBER) + "$")
        ],
        states={
            SELECTING_LEVEL: [
                CallbackQueryHandler(select_gender, pattern=f"^{SECT_1}$|^{CHILDREN}$")
            ],
            SELECTING_GENDER: [description_conv],
        },
        fallbacks=[
            CallbackQueryHandler(show_data, pattern="^" + str(SHOWING) + "$"),
            CallbackQueryHandler(end_second_level, pattern="^" + str(END) + "$"),
            CommandHandler("stop", stop_nested),
        ],
        map_to_parent={
            # After showing data return to top level menu
            SHOWING: SHOWING,
            # Return to top level menu
            END: SELECTING_ACTION,
            # End conversation altogether
            STOPPING: END,
        },
    )

    # Set up top level ConversationHandler (selecting action)
    # Because the states of the third level conversation map to the ones of the second level
    # conversation, we need to make sure the top level conversation can also handle them
    selection_handlers = [
        add_member_conv,
        CallbackQueryHandler(show_data, pattern="^" + str(SHOWING) + "$"),
        CallbackQueryHandler(adding_self, pattern="^" + str(ADDING_SELF) + "$"),
        CallbackQueryHandler(end, pattern="^" + str(END) + "$"),
    ]
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SHOWING: [CallbackQueryHandler(start, pattern="^" + str(END) + "$")],
            SELECTING_ACTION: selection_handlers,
            SELECTING_LEVEL: selection_handlers,
            DESCRIBING_SELF: [description_conv],
            STOPPING: [CommandHandler("start", start)],
        },
        fallbacks=[CommandHandler("stop", stop)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()