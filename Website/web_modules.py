# Imports

from datetime import date, datetime

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
        ] = f"""
*{self.date}, {self.time}hrs*
*11 C41 BN, SIG*
*{self.type}*
        """

    def sect_1(self, nature):
        if nature == "TR":
            nature = "Training Related"
        else:
            nature = "Non-Training Related"
        self.sections[
            1
        ] = f"""
1) *Nature and Type of incident*:
{nature}
{self.symptoms.upper()}
        """

    def sect_2(self, NRIC, rank, fullname, service, sex, age):
        masked_NRIC = NRIC[:1] + "XXXX" + NRIC[5:]
        self.sections[
            2
        ] = f"""
2) *Particulars of Serviceman/men Involved*:
NRIC: {masked_NRIC.upper()}
Rank/Name: {rank.upper()} {fullname.upper()}
Svs Status: {service.upper()}
Sex/Age: {sex.upper()}/{age}
Coy/Pl: SIGNALS
        """

    def sect_3a(self, history):
        self.sections[
            3
        ] = f"""
3) *Brief Description of Incident*:
Serviceman has previously reported sick on the following dates:
{history}
        """

    def sect_3b(self, updates):
        self.sections[
            4
        ] = f"""
{updates}
        """

    def sect_3c(self, update_date, updates):
        self.sections[
            5
        ] = f"""
On {update_date},

{updates}
        """

    def sect_3d(self, overall, ART, PCR):
        swap_lib = {"X": "PENDING", "N": "NEGATIVE", "P": "POSITIVE"}
        self.sections[
            6
        ] = f"""
*Other Details*
- *SWAB Test Done*: *{swap_lib[overall]}* (ART - *{swap_lib[ART]}*, PCR - *{swap_lib[PCR]}*)
- Travelled Overseas in the past 14 days: NIL
- Close Contact with a confirmed case: NIL
- Stays in a foreign worker dormitory: NIL
- Works in a High-Risk Area: NIL
- Prolonged ARI with fever above 37.5C for 4 days and above: NIL
- Suspected Pneumonia: NIL
        """

    def sect_4(self, status, date_end):
        self.sections[
            7
        ] = f"""
4) *Current Status*:
{status} from {self.date} to {date_end}
        """

    def sect_5(self):
        self.sections[
            8
        ] = f"""
5) *Date & Time of Incident*:
{self.date}, {self.initial_time}hrs
        """

    def sect_6(self, location):
        if not location:
            location = "Pasir Laba Camp"
        self.sections[
            9
        ] = f"""
6) *Location of incident*:
{location}
        """

    def sect_7(self, actions):
        if actions == "URTI":
            actions = "Unit will continue to monitor serviceman’s condition. He will report back to camp when his MC ends or when his swab test result returns negative. Which ever is later."
        self.sections[
            10
        ] = f"""
7) *Follow Up Actions*:
{actions}
        """

    def sect_8(self):
        self.sections[
            11
        ] = f"""
8) *Details/Particulars of civilian involved, if any*: (For accidents)
NRIC (Masked): -
Name: -
Age: -
Gender: -
Contact No.: - 
        """

    def sect_9(self):
        self.sections[
            12
        ] = f"""
9) *Date & Time reported to GSOC*:
Verbal: -
ASIS: - 
        """

    def sect_10(self, POC_rank, POC_name, POC_rel, POC_phone):
        self.sections[
            13
        ] = f"""
10) *Reporting Officer*: 

*Point of Contact*:
{POC_rank} {POC_name}
{POC_rel}, SIG COY
{POC_phone}

*Vetted By*
        """

    def display(self):
        return "".join(self.sections)


# Web Bot (Main Program)
def site(form_data):
    form = Form(form_data["type"], form_data["initial_time"], form_data["symptoms"])
    form.sect_0()

    # Section 1
    form.sect_1(form_data["nature"])

    # Section 2
    form.sect_2(
        form_data["NRIC"],
        form_data["rank"],
        form_data["fullname"],
        "NSF",
        form_data["sex"],
        form_data["age"],
    )

    # Section 3a
    form.sect_3a(form_data["history_3a"])

    # Section 3b
    form.sect_3b(form_data["history_3b"])

    # Section 3d
    overall, ART, PCR, = (
        form_data["results_ALL"],
        form_data["results_ART"],
        form_data["results_PCR"],
    )
    form.sect_3d(overall, ART, PCR)

    # Section 4
    status = form_data["status"]
    date_end = form_data["date_end"]
    form.sect_4(status, date_end)

    # Section 5
    form.sect_5()

    # Section 6
    form.sect_6(form_data["location"])

    # Section 7
    form.sect_7("URTI")

    # Section 8
    form.sect_8()

    # Section 9
    form.sect_9()

    # Section 10
    POC_rank = "3SG"
    POC_name = form_data["POC_name"].strip().upper()
    POC_rel = "DET COMD"
    POC_phone = form_data["POC_phone"].strip()
    if len(POC_phone) == 8:
        POC_phone = POC_phone[:4] + " " + POC_phone[4:]
    form.sect_10(POC_rank, POC_name, POC_rel, POC_phone)

    return form.display()
