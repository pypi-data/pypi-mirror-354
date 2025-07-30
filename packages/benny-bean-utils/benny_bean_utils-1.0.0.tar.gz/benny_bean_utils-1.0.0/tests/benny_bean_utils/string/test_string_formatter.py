from benny_bean_utils.string import StringFormatter

TEST_DATA_TO_SNAKE_CASE = [
    ("Hello World", "hello_world"),
    ("Python Script", "python_script"),
    ("éèêëàçôù", "eeeeacou"),
    ("Crème Brûlée", "creme_brulee"),
    ("garçon élève", "garcon_eleve"),
    ("Éléphant à l’école", "elephant_a_lecole"),
]

class TestStringFormatter:
    def test_get_snake_of_text(self):
        for input_text, expected_output in TEST_DATA_TO_SNAKE_CASE:
            assert StringFormatter.get_snake_case_of_text(input_text) == expected_output