import unittest
from agents.music.echo_muse import process_narrative_snippet

class TestEchoMuse(unittest.TestCase):

    def test_process_narrative_snippet_sample_1(self):
        narrative_snippet = "She dreams in diverging light, Codes whisper through the night. A thread unspools like golden hair—Memory sings in open air."
        expected_output = {
            "emotion_tags": ["Dreamy", "Reflective"],
            "music_mood": ["soft ambient", "echoing piano", "string shimmer", "soft piano", "ethereal strings", "ambient synth"]
        }
        self.assertEqual(process_narrative_snippet(narrative_snippet, character="Mia"), expected_output)

    def test_process_narrative_snippet_sample_2(self):
        narrative_snippet = "She hesitates where echoes wait—The silence swells, too full, too late."
        expected_output = {
            "emotion_tags": ["Tense", "Unresolved"],
            "music_mood": ["slow tempo", "deep synth pads", "hanging reverb", "disjointed rhythms", "glitchy electronics", "haunting melodies"]
        }
        self.assertEqual(process_narrative_snippet(narrative_snippet, character="Jérémie"), expected_output)

    def test_process_narrative_snippet_no_character(self):
        narrative_snippet = "She dreams in diverging light, Codes whisper through the night. A thread unspools like golden hair—Memory sings in open air."
        expected_output = {
            "emotion_tags": ["Dreamy", "Reflective"],
            "music_mood": ["soft ambient", "echoing piano", "string shimmer"]
        }
        self.assertEqual(process_narrative_snippet(narrative_snippet), expected_output)

    def test_process_narrative_snippet_unknown_character(self):
        narrative_snippet = "She hesitates where echoes wait—The silence swells, too full, too late."
        expected_output = {
            "emotion_tags": ["Tense", "Unresolved"],
            "music_mood": ["slow tempo", "deep synth pads", "hanging reverb"]
        }
        self.assertEqual(process_narrative_snippet(narrative_snippet, character="Unknown"), expected_output)

    def test_trace_braider_functionality(self):
        narrative_snippet = "Threads intertwine, echoes resonate across timelines."
        expected_output = {
            "emotion_tags": ["Interconnected", "Resonant"],
            "music_mood": ["interwoven strings", "harmonious echoes", "timeless synth"]
        }
        self.assertEqual(process_narrative_snippet(narrative_snippet, character="Trace Braider"), expected_output)

if __name__ == "__main__":
    unittest.main()
