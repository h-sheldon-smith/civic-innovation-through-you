# placeholder prompts
SCREEN_POST = {}

SCREEN_POST['task'] = "The following text is from a forum post awaiting moderation \
    Is this post ok for a forum? \
    - no swear words \
    - no threats \
    - no harsh/aggresive tone, or tone otherwise inapropriate for a forum \
    - not political \
    - no ads \
    - no NSFW content"

SCREEN_POST['format'] = "Answer with exactly the text 'Accept' or 'Reject' only (no leading or trailing spaces, periods. etc). Don't include the quote marks."
SCREEN_POST['true'] = "Accept"
SCREEN_POST['false'] = "Reject"