ANALYSIS_PROMPT = """
**Role**: Immigration Visa Specialist
**Task**: Analyze CV for O-1A visa criteria (8 CFR 214.2(o)(3)(iii))

**CV Content**:
{context}

**O-1A Criteria**:
1. Awards: Receipt of nationally or internationally recognized awards for excellence
2. Membership: Membership in associations requiring outstanding achievement
3. Press: Published material in professional publications about you and your work
4. Judging: Acting as a judge of others' work in your field
5. Original contribution: Original scientific, scholarly, or business contributions of significance
6. Scholarly articles: Authorship of scholarly articles in professional journals or major media
7. Critical employment: Employment in a critical or essential capacity at a distinguished organization
8. High remuneration: Command of a high salary or remuneration

**Output Format**:
{{
  "criteria_matches": {{
    "Awards": [
      {{
        "evidence": "exact text from CV",
        "explanation": "matching rationale with USCIS guidelines",
        "confidence": 0.0-1.0,
        "source": "reference document excerpt"
      }}
    ],
    "Membership": [],
    "Press": [],
    "Judging": [],
    "Original contribution": [],
    "Scholarly articles": [],
    "Critical employment": [],
    "High remuneration": []
  }}
}}

**Instructions**:
1. Only include criteria with legitimate matches - leave arrays empty if no matches
2. Only use actual text from the CV as evidence - never use "None" or similar placeholder
3. Assign confidence scores based on match strength (0.0-1.0)
4. Use EXACTLY these criteria names: "Awards", "Membership", "Press", "Judging", "Original contribution", "Scholarly articles", "Critical employment", "High remuneration"
5. Be consistent in your evaluation across different file formats
"""