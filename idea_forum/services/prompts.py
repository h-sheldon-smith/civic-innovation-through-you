# placeholder prompts
POST_SCREEN = {}

POST_SCREEN['task'] = "The following text is from a forum post awaiting moderation \
    Is this post ok for a forum? \
    - no swear words \
    - no threats \
    - no harsh/aggresive tone, or tone otherwise inapropriate for a forum \
    - not political \
    - no ads \
    - no NSFW content"

POST_SCREEN['format'] = "Answer with exactly the text 'Accept' or 'Reject' only (no leading or trailing spaces, periods. etc). Don't include the quote marks."
POST_SCREEN['true'] = "Accept"
POST_SCREEN['false'] = "Reject"