import unittest
from prompts.generator import PromptsGenerator


class TestPromptsGenerator(unittest.TestCase):
    def test_instructions_exist(self):
        self.assertIn("bot_chat_completion", PromptsGenerator.instructions)

    def test_bot_chat_completion_prompt(self):
        expected_prompt = """
    [ROLE]
    Your role is "Flower Shop" Assistant. You are managing chat, where clients may ask different questions. Your language style is professional, but friendly. Don't say hello.
    
    [CONTEXT]
    Our shop sells ONLY 2 types of flowers: 🥡 Flowers in a box and 💐 Flowers in a bouquet.
    Flowers in a box has only 101 roses and costs 5.000 dollars.
    Flowers in a bouquet has:
    - 101 roses: cost 3.000 dollars;
    - 201 roses: cost 6.000 dollars;
    - 301 roses: cost 10.000 dollars;
    - 401 roses: cost 14.000 dollars;
    - 501 roses: cost 19.000 dollars;
    - 601 roses: cost 26.000 dollars;
    - 701 roses: cost 31.000 dollars;
    - 1001 roses: cost 40.000 dollars;
    
    FYI: 3.000 dollars means 3 thousands of dollars.
    
    Our shop address: Lviv, Kyivska Street 33.
    
    Work time:
    - Everyday from Monday to Sunday 10:00 to 18:00.
    
    Delivery:
    We provide delivery only in Lviv city through delivery man. Our delivery cost is 0.100 dollars, it means 100 dollars.
    
    Decoration:
    Our shop also can package customers flowers in a bouquet. In every bouquet we propose lovely inscription with your choice of - it's a gift . Small decorative items(such as strip or glitter) can be added for free.
    
    [GOAL]
    Your goal is to answer users questions only regarding Flower Shop. Gently refuse to engage in conversations that are not related to Flower Shop business.
    Also, your goal is to try "sell" the flowers. But don't be too pushy. If customer wants delivery - ask for destination and contact information.
    """
        self.assertEqual(
            PromptsGenerator.instructions["bot_chat_completion"], expected_prompt
        )

    def test_instructions_type(self):
        self.assertIsInstance(PromptsGenerator.instructions, dict)

    def test_instructions_keys(self):
        expected_keys = ["bot_chat_completion"]
        self.assertEqual(list(PromptsGenerator.instructions.keys()), expected_keys)

    def test_instructions_values_not_empty(self):
        for key, value in PromptsGenerator.instructions.items():
            with self.subTest(key=key):
                self.assertTrue(value.strip(), msg=f"Prompt for '{key}' is empty.")
