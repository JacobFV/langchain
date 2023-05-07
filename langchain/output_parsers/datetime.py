import random
from datetime import datetime, timedelta

from langchain.schema import BaseOutputParser, OutputParserException
from langchain.utils.formatting import comma_list


def _generate_random_datetime_strings(
    pattern,
    n=3,
    start_date=datetime(1, 1, 1),
    end_date=datetime.now() + timedelta(days=3650),
):
    """
    Generates n random datetime strings conforming to the given pattern within the specified date range.
    Pattern should be a string containing the desired format codes.
    start_date and end_date should be datetime objects representing the start and end of the date range.
    """
    delta = end_date - start_date
    for i in range(n):
        random_delta = random.uniform(0, delta.total_seconds())
        dt = start_date + timedelta(seconds=random_delta)
        date_string = dt.strftime(pattern)
        yield date_string


class DatetimeOutputParser(BaseOutputParser[datetime]):
    format: str = "%Y-%m-%dT%H:%M:%S.%fZ"

    def get_format_instructions(self):
        return f"""Write a datetime string that matches the following pattern: "{self.format}". Examples: {comma_list(_generate_random_datetime_strings(self.format))}"""

    def parse(self, response) -> datetime:
        response = response.strip().strip('"').strip("'")
        if response not in self.options:
            raise OutputParserException(
                f"'{response}' does not match the expected format {self.format}."
            )
        return response
