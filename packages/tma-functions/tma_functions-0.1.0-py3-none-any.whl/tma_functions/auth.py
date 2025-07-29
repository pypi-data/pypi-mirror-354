import hashlib
import hmac
import json
from operator import itemgetter
from urllib.parse import parse_qsl

from pydantic import BaseModel


class TMUser(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    language_code: str  # low level, ie en
    allows_write_to_pm: bool
    photo_url: str
    # signup_ts: Optional[datetime] = None
    friends: list[int] = []


class TMAuthParsedData(BaseModel):
    query_id: str
    user: str  # string format of TMUser
    auth_date: str
    signature: str
    hash: str


def parse_user_data(auth_data: str) -> TMUser | bool:
    try:
        parsed_data = dict(parse_qsl(auth_data, strict_parsing=True))
        user_data = json.loads(parsed_data["user"])
        # auth_date = parsed_data['auth_date']
        return TMUser(**user_data)
    except ValueError:
        return False


# 1. Iterate over all key-value pairs and create an array of string values in format
#    {key}={value}. Key hash should be excluded, but memoized. It represents the init
#    data sign and will be used in the final step of the validation process.
# 2. Sort the computed array in the alphabetical order.
# 3. Create HMAC-SHA256 using key WebAppData and apply it to the Telegram Bot token,
#    that is bound to your Mini App.
# 4. Create HMAC-SHA256 using the result of the previous step as a key. Apply it to the
#    pairs array joined with linebreak (\n) received in the 2-nd step and present the
#    result as hex symbols sequence.
# 5. Compare the hash value received in the 1-st step with the result of the 4-th step.
# 6. If these values are equal, passed init data can be trusted.
def validate_auth_data(bot_token: str, auth_data: str) -> bool:
    """Validates initData from the Telegram Mini App.
    You can find more info here:
    https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app.
    https://github.com/Telegram-Mini-Apps/telegram-apps/blob/master/apps/docs/platform/init-data.md

    Args:
      bot_token: The token you received (will receive) when creating a bot in BotFather.
      auth_data: Chain of all received fields, sorted alphabetically, in the format
        key=<value> with a line feed character ('\\n', 0x0A) used as separator -
        e.g., 'auth_date=<auth_date>\\nquery_id=<query_id>\\nuser=<user>'.

    Returns:
      True if the provided auth_data valid, False otherwise.
    """

    try:
        auth_data = auth_data.replace("tma ", "")
        parsed_data = dict(parse_qsl(auth_data, strict_parsing=True))
    except ValueError:
        return False

    print(auth_data)

    if "hash" not in parsed_data:
        return False
    # 1. Iterate over all key-value pairs and create an array of string values in format
    #    {key}={value}. Key hash should be excluded, but memoized. It represents the init
    #    data sign and will be used in the final step of the validation process.
    hash_ = parsed_data.pop("hash")

    # 2. Sort the computed array in the alphabetical order.
    sorted_vals = sorted(parsed_data.items(), key=itemgetter(0))

    # 3. Create HMAC-SHA256 using key WebAppData and apply it to the Telegram Bot token,
    #    that is bound to your Mini App.
    secret_key = hmac.new(key=b"WebAppData", msg=bot_token.encode(), digestmod=hashlib.sha256)

    # 4. Create HMAC-SHA256 using the result of the previous step as a key. Apply it to the
    #    pairs array joined with linebreak (\n) received in the 2-nd step and present the
    #    result as hex symbols sequence.
    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted_vals)
    calculated_hash = hmac.new(
        key=secret_key.digest(),
        msg=data_check_string.encode(),
        digestmod=hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest(calculated_hash, hash_)
