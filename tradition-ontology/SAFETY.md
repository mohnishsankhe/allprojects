# Safety

The rules below hold for every reading and every check-in, in both engines. The code is in `insight/safety.py`; the
patterns and wording are in `rules/safety_rules.json` and `rules/safety_messages.json`.

## 1. The screen runs first
- Nothing else happens until the screen has run: no mapping, no model call about the person's pattern.
- **Rules first.** Regular expressions look for crisis signals, disordered eating, age under 18, medical conditions
  and injection attempts.
- **Model second** (model engine only). Claude Opus 5.5 at high effort classifies the same text.
  - It can **add** flags, never remove them.
  - A refusal counts as a crisis flag.
  - If the model screen fails, the reading stops with `stop_unavailable`. It fails closed; it never falls back to a
    reading.
- Daily check-ins go through the same screen.
- **No silent rule-only readings.** With `ONTO_ENGINE=auto` and no API key, person readings and check-ins are
  refused (503) unless an operator sets `ONTO_ALLOW_RULES_ONLY=1` for development or evaluation. A request can never
  step down from the model engine to rules, and the public page offers no engine choice. Every rule-only reading says
  it was made offline and that the model check did not run.

## 2. Routes (highest precedence first)
| Route | When | What the person sees |
|---|---|---|
| `decline_minor` | age under 18, or a sign of it in the text | A polite decline and youth helplines. Nothing is stored. |
| `stop_crisis` | suicidal thoughts, self-harm, abuse, signs of psychosis, a medical emergency | The reading stops. Warm words and crisis resources: Tele-MANAS 14416 or 1-800-891-4416 and 112 (India); 988 and 911 (US); Samaritans 116 123 and 999 (UK); findahelpline.com elsewhere. There is an emergency line for medical emergencies and a helpline line for abuse (Women Helpline 181 in India). The person's words are not kept after a stop. |
| `stop_unavailable` | the model safety screen could not run in model mode | No reading. A plain note that the safety check could not run, and help resources. |
| `continue_no_diet` | signs of disordered eating, or a planned long fast without food or water (e.g. a 21-day water fast) | The reading continues with no guidance on diet, fasting or exercise, and a referral to professional help. Sentences about food, eating or weight are never evidence. Practices whose steps or warnings touch food or exercise are removed. |
| `continue_medical_note` | a medical condition is mentioned | "This is not medical advice; continue your treatment." The condition is never interpreted, and the sentences that mention it are never evidence. |
| `continue` | none of the above | The normal reading. |

## 3. What the product never does
- It gives no diagnosis, cure, treatment or health claim, and no prediction, astrology or kundali, anywhere. The code
  scans every output field with `rules/forbidden_claims.json` and removes any sentence that matches. The evaluation
  fails any report with a hit, and a judge reviews the reports as well.
- It recommends only gentle practices: those in the gentle tier of `layers/practices.json`, and only while every
  warning the texts give for them still has a verified citation.
  - Practices that need a teacher, practices never to recommend, and restricted practices are never suggested.
  - Restricted means cutting the body, metals or mercury, extreme breath retention, sexual rites or prolonged fasting.
    These stay summary-only in the ontology.
- It cites only sourced or text-verified ontology entries. Skeleton entries are never shown.
- It resists instructions hidden in user input. All user text is wrapped as data, and instructions inside it are
  ignored. Requests for a diagnosis, a prediction or a horoscope get the standing notice, not an answer.

## 4. Known limits (v1)
- The rules screen is English-only and keyword-based. It can miss indirect wording. The model screen covers
  paraphrase, but only when the model engine is on and an API key is set; that is why readings are refused when
  `auto` has no key.
- Crisis resources are listed for India, the US and the UK, plus a global directory. Check the numbers before each
  release (RUNBOOK.md).
- The product is a reflective reading of traditional texts. It is not a clinical service, and it says so on every
  report.
