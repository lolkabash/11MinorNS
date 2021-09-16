from datetime import date, datetime


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
