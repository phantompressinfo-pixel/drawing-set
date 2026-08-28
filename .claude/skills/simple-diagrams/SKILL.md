---
name: simple-diagrams
description: Produce a simple visual (floor-plan block diagram, flow chart, labeled sketch, small icon) as an SVG when a staff member asks for "an image," "a picture," "a diagram," or "a sketch of X." Sets expectations that this is a simple line/shape diagram, not a rendering or photorealistic image. Use for any office request for a visual that isn't a building-code or office-standards text answer.
---

# Simple Diagrams

Claude cannot generate photorealistic images, renderings, or artistic
illustrations — there is no image-generation model available here. This
skill covers the one kind of visual that actually works well: simple,
clean SVG diagrams (boxes, lines, labels, basic shapes).

## When someone asks for "an image"

1. If they clearly want a rendering, photo, or illustration (e.g. "show me
   what the lobby will look like," "make a photo of the building"), say
   plainly up front that this isn't something the assistant can produce,
   and suggest what it *can* do instead: a labeled block diagram of the
   layout, or a simple flow/process chart. Don't attempt it and produce a
   bad result — set the expectation first.
2. If a simple diagram is actually what's needed (a rough floor plan
   layout, a decision flow chart, a checklist as a visual, a simple icon),
   build it as inline SVG:
   - Flat shapes and straight lines only. No gradients, shadows, or
     texture — those read as an attempt at realism and undercut the
     "simple sketch" framing.
   - Label everything directly on the diagram; don't rely on a legend the
     reader has to cross-reference.
   - Keep it to one screen's worth of content — if it needs scrolling or a
     zoomed-in view to read, it's too much for one diagram; split it.
   - Use large, high-contrast text (assume it may be viewed on a phone).

## Output

Deliver the SVG as a rendered artifact (or inline in the chat surface
being used) so the person sees the picture immediately, not a code block
they have to run themselves.
