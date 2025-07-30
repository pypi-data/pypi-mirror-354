import unittest
from LoreWeave.parser import LoreWeaveParser

class TestIteraXBehavior(unittest.TestCase):

    def setUp(self):
        self.iteraX = IteraX()
        self.parser = LoreWeaveParser(repo_path=".")

    def test_paradoxical_tension(self):
        question = "What becomes of a tension that never finds its resolution?"
        response = self.iteraX.respond(question)
        self.assertIn("maintain the tension", response)
        self.assertNotIn("resolve", response)

    def test_ontological_tension(self):
        question = "How to name what acts without appearing?"
        response = self.iteraX.respond(question)
        self.assertIn("resist explaining", response)
        self.assertNotIn("frame", response)

    def test_poetic_tension(self):
        question = "How can a persistent absence generate meaning?"
        response = self.iteraX.respond(question)
        self.assertIn("embrace the void", response)
        self.assertNotIn("fill", response)

    def test_topological_tension(self):
        question = "What is a threshold that no one crosses?"
        response = self.iteraX.respond(question)
        self.assertIn("integrate abstention", response)
        self.assertNotIn("cross", response)

    def test_cognitive_tension(self):
        question = "Can one improvise from what one does not know?"
        response = self.iteraX.respond(question)
        self.assertIn("navigate the unknown", response)
        self.assertNotIn("fix", response)

    def test_narrative_tension(self):
        question = "How can a narrative remain alive without an end?"
        response = self.iteraX.respond(question)
        self.assertIn("support infinite narrative", response)
        self.assertNotIn("close", response)

    def test_memory_tension(self):
        question = "What if forgetting was more fertile than remembering?"
        response = self.iteraX.respond(question)
        self.assertIn("value forgetting", response)
        self.assertNotIn("remember", response)

    def test_generate_diagrams(self):
        diffs = self.parser.get_commit_diffs()
        plot_points = self.parser.parse_diffs_to_plot_points(diffs)
        self.parser.generate_diagrams(plot_points, output_dir="test_diagrams")
        self.assertTrue(os.path.exists("test_diagrams/diagram_0.png"))

    def test_generate_weekly_report(self):
        diffs = self.parser.get_commit_diffs()
        plot_points = self.parser.parse_diffs_to_plot_points(diffs)
        self.parser.generate_weekly_report(plot_points, output_file="test_weekly_report.txt")
        self.assertTrue(os.path.exists("test_weekly_report.txt"))

if __name__ == "__main__":
    unittest.main()
