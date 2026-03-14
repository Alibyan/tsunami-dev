# DEFINITION_OF_DONE

This file defines the minimum bar for calling a task complete in this project.

## Global rule

A task is only done when it is **working, reviewable, and handoff-safe**.

Code existing is not enough.

## Universal done criteria

Every completed task should satisfy all of the following:

1. **Runs locally**  
   The code executes on the intended local setup without hidden manual steps.

2. **Has a clear entry point**  
   There is an obvious script, command, function, or UI path for using the feature.

3. **Handles expected failure cases**  
   At minimum, missing network responses, empty data, bad rows, and invalid configuration are handled gracefully.

4. **Leaves artifacts behind**  
   The task produces something concrete: code, config, schema, screenshot, table, log, sample payload, or documentation.

5. **Matches the current phase**  
   The task does not quietly pull in stretch work that belongs to a later phase.

6. **Is understandable by the next agent**  
   The assumptions, inputs, outputs, and next handoff trigger are written down.

7. **Does not break the demo path**  
   The feature must not damage the MVP path, replay mode, or offline fallback.

## Code task done criteria

A code task is done when:

- the file compiles or runs
- imports resolve cleanly
- configuration variables are explicit
- naming is readable and stable
- obvious debug leftovers are removed
- one quick sanity check has been performed

## Data task done criteria

A data task is done when:

- the raw source is identified
- the normalized schema is documented
- null and missing values are accounted for
- duplicates are handled intentionally
- timestamp and units are normalized
- sample records are saved for replay or inspection

## Database task done criteria

A DB task is done when:

- schema exists in code or migration form
- keys and indexes are intentional
- inserts are idempotent where required
- a read path exists for the UI or replay mode
- at least one small query has been tested

## UI task done criteria

A UI task is done when:

- the click path works end to end
- empty and error states render cleanly
- labels use safe wording
- the component still works with cached or replay data
- the component adds value to the demo rather than noise

## Modeling or scoring task done criteria

A scoring or ML task is done when:

- the inputs are explicit
- the output can be inspected record by record
- the behavior is explainable
- the metric is named and appropriate
- the result is compared against a baseline
- wording does not imply certainty or official warning status

## Documentation task done criteria

A documentation task is done when:

- it reflects the current system rather than an aspirational one
- commands and file paths are correct
- assumptions and limitations are honest
- the next person can act on it without extra context

## Handoff note template

Every finished task should leave a short note in this format:

- what was completed
- what files changed
- what assumptions were made
- what still needs validation
- the next recommended owner agent
- the handoff trigger for that next task

## Refusal rule

Do not mark a task done if it only works:

- on one machine by accident
- with secret manual steps
- with hand-edited data
- in notebook-only form when the phase needs app integration
- when online only, if the phase requires replay or offline safety
