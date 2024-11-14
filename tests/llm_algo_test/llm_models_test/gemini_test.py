import unittest
from llm_algo import AskGemini

class AskGeminiTest(unittest.TestCase):
    async def testsetup(self):
        self.ag = AskGemini()
    
    async def testgeminiresponse(self):
        test_q = "what is name of our solar system?"
        test_ans = "Solar system"
        result = await self.ag.gemini_response(user_input=test_q)
        self.assertIn(test_ans,result)
    
if __name__ == '__main__': 
    unittest.main()
