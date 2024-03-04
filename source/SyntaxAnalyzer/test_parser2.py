from source.SyntaxAnalyzer.parser2 import SyntaxAnalyzer as parse


def test_parameter():
    parser = parse()  # Create an instance of your parser

    # Test case 1: Valid parameter with identifier and more parameters
    tokens1 = ['int', 'Identifier', ',', 'Identifier']
    parser.set_tokens(tokens1)
    assert parser.parameter() == parser.success

    # Test case 2: Valid parameter with blank
    tokens2 = ['blank']
    parser.set_tokens(tokens2)
    assert parser.parameter() == parser.success

    # Test case 3: Invalid parameter with unexpected token
    tokens3 = ['float', 'Identifier', '(', 'Identifier']
    parser.set_tokens(tokens3)
    assert parser.parameter() == parser.failed()

    # Add more test cases here...

test_parameter()  # Run the test cases