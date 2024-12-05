
import datetime
import pytz
from tools.base_tool import Tool


class TimeTool(Tool):
    def name(self):
        return "Time Tool"

    def description(self):
        return "Provides the current time for a given city's timezone like Asia/Kolkata, America/New_York etc. If no timezone is provided, it returns the local time."

    def use(self, *args, **kwargs):
        format = "%Y-%m-%d %H:%M:%S %Z%z"
        current_time = datetime.datetime.now()
        input_timezone = args[0]
        if input_timezone:
            print("TimeZone", input_timezone)
            current_time =  datetime.datetime.now(pytz.timezone(input_timezone))
        return f"The current time is {current_time}."