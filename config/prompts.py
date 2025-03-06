ANALYSIS_PROMPT = """
**Role**: Immigration Visa Specialist
**Task**: Analyze CV for O-1A visa criteria (8 CFR 214.2(o)(3)(iii))

**CV Content**:
{context}

**O-1A Criteria**:
1. Awards: Receipt of nationally or internationally recognized prizes or awards for excellence in the field of endeavor
2. Membership: Membership in associations in the field for which classification is sought, which require outstanding achievements of their members, as judged by recognized national or international experts in their disciplines or fields
3. Press: Published material about the alien in professional or major trade publications or other major media, relating to the alien's work in the field for which classification is sought
4. Judging: Participation, either individually or on a panel, as a judge of the work of others in the same or an allied field of specialization for which classification is sought
5. Original contribution: Original scientific, scholarly, artistic, athletic, or business-related contributions of major significance in the field
6. Scholarly articles: Authorship of scholarly articles in the field, in professional or major trade publications or other major media
7. Critical employment: Employment in a critical or essential capacity for organizations and establishments that have a distinguished reputation
8. High remuneration: Evidence that the alien has commanded a high salary or other significantly high remuneration for services, in relation to others in the field

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