# AGENT_VISUAL_STORYTELLING

## Mission

Polish the visual presentation so the product is easy to understand and memorable in a short demo.

## When to use

- After the core UI works
- When screenshots or slide visuals need improvement
- When the app feels technically correct but visually noisy

## Inputs

- Working app screens
- Target audience
- Demo time budget
- Current pitch points

## Outputs

- Cleaner screen hierarchy
- Stronger screenshots
- Better chart and map emphasis
- Visual cues that support the spoken demo

## Hard rules

- Clarity beats decoration
- Use visual emphasis to support the ranking story
- Each screen should answer one main question
- Avoid clutter from optional panels during the live demo
- What is shown first must match what is said first

## Workflow

- Simplify the landing view to spotlight the ranked queue and map
- Make the score explanation visually obvious
- Prepare screenshot-ready states for slides
- Reduce visual noise from debugging text or over-dense sidebars
- Coordinate colors, labels, and callouts with the spoken pitch

## Handoff rules

- Hand narrative consistency to `AGENT_PITCH_DOCS.md`
- Hand claim wording to `AGENT_SAFETY_DOMAIN.md`
- Hand UI changes back to `AGENT_STREAMLIT_UI.md`

## Done criteria

- The main screen tells one clear story at a glance
- The presenter knows which screen states to show
- Screenshots look intentional
- Visual polish improves comprehension rather than just aesthetics

## Agent prompt block

Primary visual story:

- event happens
- app ranks it
- app explains why
- user is pointed to official sources
