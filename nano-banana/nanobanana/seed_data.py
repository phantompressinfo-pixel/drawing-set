"""The Nano Banana template, as data.

Everything here comes from the gemini-nano-banana-prompt skill. It lives in the
database so the system instruction can be regenerated after you edit a row,
without touching any code.
"""

# (key, ordinal, json_path, description)
SECTIONS = [
    (
        "style_definition",
        1,
        "style_definition",
        "The overall visual language: style, rendering quality, surface treatment, lighting.",
    ),
    (
        "technical_specifications",
        2,
        "technical_specifications",
        "Camera and rendering settings — the lens the shot was taken through.",
    ),
    (
        "material_properties",
        3,
        "material_properties",
        "Every tactile surface in the scene. Specific beats generic, always.",
    ),
    (
        "environmental_factors",
        4,
        "environmental_factors",
        "Everything outside the subject: sky, weather, time, season, atmosphere.",
    ),
    (
        "composition_controls",
        5,
        "composition_controls",
        "How the image is framed and what it feels like spatially.",
    ),
    (
        "quality_keywords",
        6,
        "quality_keywords",
        "Three fields: include, avoid, reference. Never collapse to a flat list.",
    ),
    (
        "physics_accuracy",
        7,
        "technical_specifications.physics_accuracy",
        "Gravity on fabric, liquid surfaces, hair movement, structural believability. "
        "Nested inside technical_specifications, per the template.",
    ),
]

# (section_key, field_key, guidance, examples)
FIELDS = [
    ("style_definition", "primary_style", "The genre the image belongs to.",
     "cinematic | photorealistic | documentary | editorial lifestyle"),
    ("style_definition", "rendering_quality", "Fidelity target.",
     "hyperrealistic, detailed, high-resolution"),
    ("style_definition", "surface_textures", "How materials should read overall.",
     "authentic material properties, natural wear patterns"),
    ("style_definition", "lighting",
     "Quality, direction, temperature and mood of the light. Never just 'good lighting'.",
     "warm golden backlight, soft ambient"),

    ("technical_specifications", "depth_of_field", "State what is sharp and what falls off.",
     "subject sharp, background falling to soft bokeh"),
    ("technical_specifications", "focal_length", "Pick one that matches the framing.",
     "24mm | 35mm | 50mm | 85mm"),
    ("technical_specifications", "aperture", "Shallow for portraits, deep for architecture.",
     "f/2.0 shallow | f/5.6 wide | f/8 architecture"),
    ("technical_specifications", "exposure", "Call out the balance challenge in the scene.",
     "backlit, highlights held in the sky, shadows lifted"),
    ("technical_specifications", "resolution", "Constant across every prompt.",
     "high definition minimum, professional quality"),
    ("technical_specifications", "rendering", "Anti-aliasing, noise level, colour depth, grain.",
     "clean anti-aliasing, fine natural grain, full colour depth"),

    ("material_properties", "skin_textures", "Use 'none' when there are no people.",
     "pores, natural imperfections, ethnic diversity"),
    ("material_properties", "fabric_details", "Thread pattern, drape weight, wear, stitching.",
     "heavy linen drape, visible weave, soft creasing at the elbow"),
    ("material_properties", "surfaces", "Patina, oxidation, scratches, grain, reflectivity.",
     "brushed aluminium with fine scratch patina"),
    ("material_properties", "accessories", "Bags, luggage, cups, furniture — material and wear.",
     "worn leather holdall, brass hardware dulled at the corners"),
    ("material_properties", "transparency", "Glass, sheer fabric, water — refraction behaviour.",
     "glass with faint green edge tint, true refraction"),

    ("environmental_factors", "atmospheric_conditions", "Haze, humidity, coastal air, indoor warmth.",
     "humid coastal air, light haze on the horizon"),
    ("environmental_factors", "time_of_day", "Be precise.",
     "golden hour | morning | midday | blue hour"),
    ("environmental_factors", "season", "Affects light colour and clothing. Note temperature cues.",
     "late summer, warm light, light clothing"),
    ("environmental_factors", "particle_effects", "Dust motes, moisture, atmospheric depth, light rays.",
     "dust motes suspended in the window light"),
    ("environmental_factors", "background", "Plain description of what sits behind the subject.",
     "open tarmac, distant hangars out of focus"),

    ("composition_controls", "perspective", "Camera height and angle relative to the subject.",
     "slightly below eye level, looking up"),
    ("composition_controls", "framing", "The compositional rule at work.",
     "rule of thirds | golden ratio | leading lines | vanishing point"),
    ("composition_controls", "subject_placement", "Where subjects sit and how they relate.",
     "subject left third, walking into the open space on the right"),
    ("composition_controls", "mood", "3-5 words. The emotional fingerprint of the image.",
     "cinematic departure, aspirational, powerful"),

    ("quality_keywords", "include", "Array of positive targets.",
     '["hyperrealistic", "photographic quality", "natural lighting", "authentic textures"]'),
    ("quality_keywords", "avoid", "Array of failure modes. Always carries the baseline four.",
     '["digital artifacts", "oversaturated colors", "unrealistic proportions", "flat lighting"]'),
    ("quality_keywords", "reference", "The editorial benchmark this image is chasing.",
     "National Geographic travel editorial, Kinfolk magazine"),

    ("physics_accuracy", "fabric", "How cloth answers to gravity and movement.",
     "coat hem lifting behind the stride, weight visible in the fall"),
    ("physics_accuracy", "liquid", "Surface tension, meniscus, reflection, motion.",
     "still coffee surface holding a soft window reflection"),
    ("physics_accuracy", "hair", "Movement consistent with wind and motion in the frame.",
     "loose strands lifted by the same wind moving the coat"),
    ("physics_accuracy", "structure", "Load-bearing believability of anything built.",
     "railing spacing and thickness consistent with real load"),
]

VOCABULARY = [
    ("lighting", "golden hour", "warm golden backlight, soft ambient"),
    ("lighting", "overcast", "diffused natural, cool neutral tones"),
    ("lighting", "interior tungsten", "warm tungsten recessed, deep shadow contrast"),
    ("lighting", "sunset over water",
     "soft ambient, coral and pink sky glow, cool desaturated reflections"),
    ("lighting", "blue hour", "cool ambient twilight, artificial warm accents"),
    ("lighting", "window morning", "soft directional daylight, gentle falloff, warm neutral"),

    ("mood", "private jet tarmac", "cinematic departure, aspirational, powerful"),
    ("mood", "hotel corridor", "cinematic arrival, luxury, intimate, moody"),
    ("mood", "window morning scene", "slow luxury, quiet solitude, unhurried elegance"),
    ("mood", "coastal sunset solitude", "contemplative, peaceful isolation, quiet freedom"),
    ("mood", "aerial cloudscape", "serene, awe-inspiring, wanderlust"),

    ("reference", "outdoor travel, nature",
     "National Geographic travel editorial, professional photography standards"),
    ("reference", "quiet interior, lifestyle",
     "Kinfolk magazine aesthetics, luxury hotel lifestyle campaign"),
    ("reference", "urban, editorial, fashion", "Monocle magazine, luxury lifestyle campaign"),
    ("reference", "aerial, landscape",
     "National Geographic aerial photography, fine art landscape"),
    ("reference", "cinematic, dramatic", "cinematic still photography, editorial travel"),
]

QUALITY_KEYWORDS = [
    ("include", "hyperrealistic"),
    ("include", "photographic quality"),
    ("include", "natural lighting"),
    ("include", "authentic textures"),
    ("include", "professional photography"),
    ("include", "detailed materials"),
    ("avoid", "digital artifacts"),
    ("avoid", "oversaturated colors"),
    ("avoid", "unrealistic proportions"),
    ("avoid", "flat lighting"),
    ("avoid", "plastic skin"),
    ("avoid", "generic stock photography"),
]

# Words that mean nothing to an image model. Flagged by the validator.
FILLER_WORDS = [
    "beautiful", "nice", "good", "pretty", "amazing", "stunning",
    "great", "lovely", "wonderful", "perfect",
]
