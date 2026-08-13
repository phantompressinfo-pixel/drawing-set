"""Run with: python -m unittest discover -s tests  (from the nano-banana directory)"""

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from nanobanana import db, instruction, validator  # noqa: E402

GOOD = {
    "style_definition": {
        "primary_style": "cinematic",
        "rendering_quality": "hyperrealistic, detailed, high-resolution",
        "surface_textures": "authentic material properties, natural wear patterns",
        "lighting": "warm golden backlight, soft ambient, low sun behind the subject",
    },
    "technical_specifications": {
        "depth_of_field": "subject sharp, tarmac falling to soft bokeh",
        "focal_length": "35mm",
        "aperture": "f/2.0",
        "exposure": "backlit, highlights held in the sky",
        "resolution": "high definition minimum, professional quality",
        "rendering": "clean anti-aliasing, fine natural grain",
        "physics_accuracy": {
            "fabric": "coat hem lifting behind the stride",
            "liquid": "none",
            "hair": "loose strands moved by the same wind",
            "structure": "airstair treads spaced for real load",
        },
    },
    "material_properties": {
        "skin_textures": "pores, natural imperfections",
        "fabric_details": "heavy wool coat, visible twill weave",
        "surfaces": "brushed aluminium fuselage with fine scratch patina",
        "accessories": "worn leather holdall, brass hardware dulled at the corners",
        "transparency": "none",
    },
    "environmental_factors": {
        "atmospheric_conditions": "dry air, light haze on the horizon",
        "time_of_day": "golden hour",
        "season": "late autumn, cold light, heavy clothing",
        "particle_effects": "faint jet exhaust shimmer",
        "background": "open tarmac, distant hangars out of focus",
    },
    "composition_controls": {
        "perspective": "slightly below eye level, looking up",
        "framing": "rule of thirds",
        "subject_placement": "subject left third, walking right into open space",
        "mood": "cinematic departure, aspirational, powerful",
    },
    "quality_keywords": {
        "include": ["hyperrealistic", "photographic quality", "natural lighting"],
        "avoid": [
            "digital artifacts",
            "oversaturated colors",
            "unrealistic proportions",
            "flat lighting",
        ],
        "reference": "National Geographic travel editorial",
    },
}


class Base(unittest.TestCase):
    def setUp(self):
        self.conn = db.connect(":memory:")
        db.init(self.conn)

    def tearDown(self):
        self.conn.close()


class TestValidator(Base):
    def test_good_prompt_passes(self):
        report = validator.validate(json.loads(json.dumps(GOOD)), self.conn)
        self.assertTrue(report.ok, report)
        self.assertEqual(report.warnings, [], report)

    def test_missing_section_is_an_error(self):
        body = json.loads(json.dumps(GOOD))
        del body["environmental_factors"]
        report = validator.validate(body, self.conn)
        self.assertFalse(report.ok)
        self.assertIn("missing section `environmental_factors`", report.errors)

    def test_nested_physics_section_is_checked(self):
        body = json.loads(json.dumps(GOOD))
        del body["technical_specifications"]["physics_accuracy"]
        report = validator.validate(body, self.conn)
        self.assertIn(
            "missing section `technical_specifications.physics_accuracy`", report.errors
        )

    def test_mood_word_count_warns(self):
        body = json.loads(json.dumps(GOOD))
        body["composition_controls"]["mood"] = "moody"
        report = validator.validate(body, self.conn)
        self.assertTrue(any("3-5 descriptive words" in w for w in report.warnings))

    def test_filler_words_warn(self):
        body = json.loads(json.dumps(GOOD))
        body["style_definition"]["primary_style"] = "beautiful cinematic"
        report = validator.validate(body, self.conn)
        self.assertTrue(any("filler" in w for w in report.warnings))

    def test_commentary_is_not_scanned_for_filler(self):
        body = json.loads(json.dumps(GOOD))
        body["_commentary"] = "A beautiful, stunning departure scene."
        body.pop("_commentary")  # cli strips it before validating
        report = validator.validate(body, self.conn)
        self.assertEqual(report.warnings, [], report)

    def test_thin_materials_warn(self):
        body = json.loads(json.dumps(GOOD))
        body["material_properties"] = {
            "skin_textures": "none",
            "fabric_details": "none",
            "surfaces": "metal",
            "accessories": "none",
            "transparency": "none",
        }
        report = validator.validate(body, self.conn)
        self.assertTrue(any("material surface" in w for w in report.warnings))

    def test_lighting_without_temperature_warns(self):
        body = json.loads(json.dumps(GOOD))
        body["style_definition"]["lighting"] = "light from the side"
        report = validator.validate(body, self.conn)
        self.assertTrue(any("colour temperature" in w for w in report.warnings))

    def test_missing_avoid_baseline_warns(self):
        body = json.loads(json.dumps(GOOD))
        body["quality_keywords"]["avoid"] = ["digital artifacts"]
        report = validator.validate(body, self.conn)
        self.assertTrue(any("baseline terms" in w for w in report.warnings))


class TestInstruction(Base):
    def test_contains_every_section(self):
        text = instruction.build(self.conn)
        for section in db.sections(self.conn):
            self.assertIn(section["json_path"], text)

    def test_template_block_nests_physics_accuracy(self):
        text = instruction.build(self.conn)
        start = text.index("```json") + len("```json")
        skeleton = json.loads(text[start : text.index("```", start)])
        self.assertEqual(len(skeleton), 6, "six top-level keys")
        self.assertIn("physics_accuracy", skeleton["technical_specifications"])

    def test_reflects_database_edits(self):
        self.conn.execute(
            "INSERT INTO vocabulary (kind, trigger, value) VALUES (?, ?, ?)",
            ("mood", "desert highway", "wide open, restless, sun-bleached"),
        )
        self.conn.commit()
        self.assertIn("desert highway", instruction.build(self.conn))


class TestStorage(Base):
    def test_round_trip(self):
        prompt_id = db.save_prompt(
            self.conn, body=GOOD, model="gemini-2.5-flash", source_path="jet.jpg",
            image_sha=db.sha256(b"jet"), note="tarmac test",
        )
        row = db.get_prompt(self.conn, prompt_id)
        self.assertEqual(json.loads(row["body"]), GOOD)
        self.assertEqual(row["mood"], "cinematic departure, aspirational, powerful")
        self.assertEqual(row["scene_type"], "National Geographic travel editorial")

    def test_search_and_export(self):
        db.save_prompt(self.conn, body=GOOD, model="m", note="tarmac test")
        self.assertEqual(len(db.search_prompts(self.conn, "tarmac")), 1)
        self.assertEqual(len(db.search_prompts(self.conn, "nothing here")), 0)
        exported = db.export(self.conn, db.list_prompts(self.conn))
        self.assertEqual(json.loads(exported)["prompt"], GOOD)

    def test_renders_cascade(self):
        prompt_id = db.save_prompt(self.conn, body=GOOD, model="m")
        db.save_render(self.conn, prompt_id=prompt_id, model="img", output_path="a.png")
        self.assertEqual(len(db.renders_for(self.conn, prompt_id)), 1)
        self.conn.execute("DELETE FROM prompts WHERE id = ?", (prompt_id,))
        self.assertEqual(len(db.renders_for(self.conn, prompt_id)), 0)

    def test_init_is_idempotent(self):
        before = self.conn.execute("SELECT count(*) FROM fields").fetchone()[0]
        db.init(self.conn)
        self.assertEqual(self.conn.execute("SELECT count(*) FROM fields").fetchone()[0], before)


if __name__ == "__main__":
    unittest.main()
