import hashlib
import hmac
import json
from operator import itemgetter
from typing import Any, Optional
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
def validate_auth_data(bot_token: str, auth_data: str) -> Optional[dict[str, Any]]:
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
      User data if the provided auth_data valid, None otherwise.
    """

    try:
        auth_data = auth_data.removeprefix("tma ")
        parsed_data = dict(parse_qsl(auth_data, strict_parsing=True))

        if "hash" not in parsed_data:
            return None

        # 1. Iterate over all key-value pairs and create an array of string values in format
        #    {key}={value}. Key hash should be excluded, but memoized. It represents the init
        #    data sign and will be used in the final step of the validation process.
        received_hash = parsed_data.pop("hash")

        # 2. Sort the computed array in the alphabetical order.
        sorted_vals = sorted(parsed_data.items(), key=itemgetter(0))

        # 3. Create HMAC-SHA256 using key WebAppData and apply it to the Telegram Bot token,
        #    that is bound to your Mini App.
        secret_key = hmac.new(b"WebAppData", msg=bot_token.encode(), digestmod=hashlib.sha256).digest()

        # 4. Create HMAC-SHA256 using the result of the previous step as a key. Apply it to the
        #    pairs array joined with linebreak (\n) received in the 2-nd step and present the
        #    result as hex symbols sequence.
        data_check_string = "\n".join(f"{k}={v}" for k, v in sorted_vals)

        # Calculate the HMAC of the data-check-string
        calculated_hash = hmac.new(secret_key, msg=data_check_string.encode(), digestmod=hashlib.sha256).hexdigest()

        if hmac.compare_digest(calculated_hash, received_hash):
            user_data_str = parsed_data.get("user")
            if user_data_str is not None:
                try:
                    user_data = json.loads(user_data_str)
                    if isinstance(user_data, dict):
                        return user_data
                except json.JSONDecodeError:
                    pass
            return None

        return None
    except Exception:
        return None
