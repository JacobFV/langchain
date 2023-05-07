from langchain.output_parsers.enum import EnumOutputParser
from langchain.schema import OutputParserException


def test_enum_output_parser_parse() -> None:
    class Colors:
        RED = "red"
        GREEN = "green"
        BLUE = "blue"

    parser = EnumOutputParser(Colors)

    # Test valid inputs
    result = parser.parse("red")
    assert result == Colors.RED

    result = parser.parse("green")
    assert result == Colors.GREEN

    result = parser.parse("blue")
    assert result == Colors.BLUE

    # Test invalid input
    try:
        parser.parse("INVALID")
        assert False, "Should have raised OutputParserException"
    except OutputParserException:
        pass
