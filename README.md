# ns-11-miner

Telegram chat bot to save time filling out a lengthy form.

## Basic Python Chatbot is up!

1. Run with `chat()` in `basic_chat.py`.
2. Input relevant details.

### Features/Usage:
1. For Section 1, `TR` means `Training Related` and NTR means `Non-Training Related`.
2. For Section 2, either a masked or non-masked NRIC can be inputted. Bot masks the NRIC in the output regardless.
3. For Section 3, once all updates for that section has been entered, type `DONE` to send it.
4. For Section 4, URTI results are keyed in with 3 characters. `X = Pending`, `N = Negative`, `P = Positive` E.g. `XNX` means `Overall - Pending`, `ART - Negative`, `PCR - Pending`.
5. Sections 5, 8, 9 are automatically generated and take in no input.
6. For Section 7, `URTI` can be entered to use the default URTI follow up actions instead of typing the full sentence out.
7. For Section 10, formatting is applied. E.g. Output is in block letters regardless of the input. Phone number will be formatted to contain a space, even if the number was not seperated.

### Output will automatically be formatted to include bolding and the relevant spacing! Basically copy-paste the output into WhatsApp.


