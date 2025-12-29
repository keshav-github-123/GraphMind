"""System time tool."""
from datetime import datetime
from typing import Dict
from langchain.tools import tool

@tool
async def get_system_time() -> Dict[str, str]:
    """🕒 System Time Tool (Timezone-Aware)"""
    local_tz = datetime.now().astimezone().tzinfo
    now = datetime.now(tz=local_tz)
    return {
        "iso_datetime": now.isoformat(),
        "current_time": now.strftime("%I:%M:%S %p"),
        "current_date": now.strftime("%B %d, %Y"),
        "day_of_week": now.strftime("%A"),
        "timezone": str(local_tz),
        "utc_offset": now.strftime("%z")
    }

