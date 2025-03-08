#!/bin/bash

# Navigate to the prompts directory
cd crew/prompts

# Create keyword extraction prompts
cat > keyword_extraction/standard.yml << 'EOF'
template_id: "keyword_extraction_standard"
template_text: |
  Analyze the following content and extract important keywords, phrases, and concepts.
  
  CONTENT:
  {content}
  
  OUTPUT INSTRUCTIONS:
  Provide a JSON response with the following structure:
  - primary_keywords: A list of the 5-7 most important general keywords
  - secondary_keywords: A list of 8-12 additional relevant keywords
  - technical_terms: A list of specialized technical terms or jargon
  
  Format your response as valid JSON only.
description: "Extract standard keywords and phrases from general content"
version: "1.0"
EOF

cat > keyword_extraction/technical.yml << 'EOF'
template_id: "keyword_extraction_technical"
template_text: |
  Analyze the following technical content and extract specialized technical keywords, terms, and concepts.
  
  CONTENT:
  {content}
  
  OUTPUT INSTRUCTIONS:
  Provide a JSON response with the following structure:
  - technical_keywords: A list of 5-7 critical technical terms
  - technical_concepts: A list of 3-5 technical concepts or methodologies
  - industry_jargon: A list of specialized industry terminology
  - abbreviations: A list of technical abbreviations with their meanings
  
  Format your response as valid JSON only.
description: "Extract technical keywords and terms from specialized content"
version: "1.0"
EOF

cat > keyword_extraction/marketing.yml << 'EOF'
template_id: "keyword_extraction_marketing"
template_text: |
  Analyze the following marketing content and extract branding keywords, value propositions, and marketing terminology.
  
  CONTENT:
  {content}
  
  OUTPUT INSTRUCTIONS:
  Provide a JSON response with the following structure:
  - branding_keywords: A list of 5-7 terms related to brand identity
  - value_propositions: A list of key value propositions identified
  - audience_terms: Keywords related to target audience
  - marketing_jargon: Industry-specific marketing terminology
  
  Format your response as valid JSON only.
description: "Extract marketing-focused keywords from content"
version: "1.0"
EOF

cat > keyword_extraction/domain.yml << 'EOF'
template_id: "keyword_extraction_domain"
template_text: |
  Analyze the following domain-specific content and extract domain keywords, concepts, and terminology.
  
  CONTENT:
  {content}
  
  OUTPUT INSTRUCTIONS:
  Provide a JSON response with the following structure:
  - domain_name: The primary domain/field this content belongs to
  - core_concepts: A list of 3-5 fundamental concepts in this domain
  - domain_terminology: A list of specialized terms specific to this domain
  - key_entities: Important entities relevant to this domain
  
  Format your response as valid JSON only.
description: "Extract domain-specific keywords and concepts"
version: "1.0"
EOF

# Create theme extraction prompts
cat > theme_extraction/standard.yml << 'EOF'
template_id: "theme_extraction_standard"
template_text: |
  Analyze the following content and extract the primary themes, concepts, and frameworks.
  
  CONTENT:
  {content}
  
  OUTPUT INSTRUCTIONS:
  Provide a JSON response with the following structure:
  - primary_theme: The single most dominant theme of the content
  - secondary_themes: 2-4 supporting themes present in the content
  - business_domains: Business domains this content relates to
  - frameworks: Any methodologies, frameworks, or structured approaches mentioned
  
  Format your response as valid JSON only.
description: "Extract standard thematic information from content"
version: "1.0"
EOF

cat > theme_extraction/technical.yml << 'EOF'
template_id: "theme_extraction_technical"
template_text: |
  Analyze the following technical content and extract technical themes, paradigms, and architectural concepts.
  
  CONTENT:
  {content}
  
  OUTPUT INSTRUCTIONS:
  Provide a JSON response with the following structure:
  - technical_paradigm: The overarching technical paradigm or approach
  - core_technologies: Key technologies or technical components mentioned
  - architectural_patterns: Any architectural patterns or design principles
  - technical_challenges: Key technical challenges addressed
  
  Format your response as valid JSON only.
description: "Extract technical themes and paradigms from content"
version: "1.0"
EOF

cat > theme_extraction/marketing.yml << 'EOF'
template_id: "theme_extraction_marketing"
template_text: |
  Analyze the following marketing content and extract brand themes, messaging frameworks, and positioning elements.
  
  CONTENT:
  {content}
  
  OUTPUT INSTRUCTIONS:
  Provide a JSON response with the following structure:
  - brand_story: The central narrative or story being conveyed
  - value_themes: Key themes around value proposition
  - emotional_appeals: Emotional themes or appeals being made
  - positioning: How the product/service is being positioned
  - target_audience: Themes related to the intended audience
  
  Format your response as valid JSON only.
description: "Extract marketing themes and messaging from content"
version: "1.0"
EOF

cat > theme_extraction/business.yml << 'EOF'
template_id: "theme_extraction_business"
template_text: |
  Analyze the following business content and extract business themes, strategies, and organizational concepts.
  
  CONTENT:
  {content}
  
  OUTPUT INSTRUCTIONS:
  Provide a JSON response with the following structure:
  - business_strategy: The primary business strategy being discussed
  - organizational_themes: Themes related to organizational structure or culture
  - market_themes: Themes related to market positioning or competition
  - operational_themes: Themes related to business operations
  - financial_themes: Themes related to financial aspects or performance
  
  Format your response as valid JSON only.
description: "Extract business themes and strategies from content"
version: "1.0"
EOF

# Create process extraction prompts
cat > process_extraction/standard.yml << 'EOF'
template_id: "process_extraction_standard"
template_text: |
  Analyze the following content and identify any processes, workflows, procedures, or step-by-step instructions.
  
  CONTENT:
  {content}
  
  OUTPUT INSTRUCTIONS:
  Provide a JSON response with the following structure:
  - has_processes: Boolean indicating if the content contains processes
  - processes: An array of process objects with the following properties:
    * process_name: A descriptive name for the process
    * steps_count: The number of steps in the process
    * is_complete: Boolean indicating if the process description is complete
    * complexity: The complexity level (Low, Medium, High)
    * description: A brief description of what the process accomplishes
  - workflows: An array of workflow objects with:
    * workflow_name: A descriptive name for the workflow
    * description: What the workflow accomplishes
  
  Format your response as valid JSON only.
description: "Extract processes, workflows, and procedural information from content"
version: "1.0"
EOF

# Create entity extraction prompts
cat > entity_extraction/standard.yml << 'EOF'
template_id: "entity_extraction_standard"
template_text: |
  Analyze the following content and extract named entities, their categories, and relationships.
  
  CONTENT:
  {content}
  
  OUTPUT INSTRUCTIONS:
  Provide a JSON response with the following structure:
  - people: An array of person entities identified
  - organizations: An array of organization entities identified
  - locations: An array of location entities identified
  - dates: An array of date or time entities identified
  - products: An array of product entities identified
  - concepts: An array of concept entities identified
  - relationships: An array of relationship objects with:
    * source: The source entity
    * target: The target entity
    * relationship_type: The type of relationship
  
  Format your response as valid JSON only.
description: "Extract named entities and their relationships from content"
version: "1.0"
EOF

# Create section analyzer prompts
cat > section_analyzer/standard.yml << 'EOF'
template_id: "section_analyzer_standard"
template_text: |
  Analyze the following content and identify its structure, sections, and organization.
  
  CONTENT:
  {content}
  
  OUTPUT INSTRUCTIONS:
  Provide a JSON response with the following structure:
  - document_type: The type of document analyzed
  - sections: An array of section objects with:
    * section_title: The title or heading of the section
    * section_level: The heading level (1 for main heading, 2 for subheading, etc.)
    * word_count: Approximate word count for the section
    * key_points: 1-3 key points from the section
  - structure_quality: Assessment of how well-structured the document is (Poor, Adequate, Good, Excellent)
  - suggestions: 1-3 suggestions for improving the document structure
  
  Format your response as valid JSON only.
description: "Analyze document structure, sections, and organization"
version: "1.0"
EOF

# Create content repurposing prompts
cat > content_repurposing/standard.yml << 'EOF'
template_id: "content_repurposing_standard"
template_text: |
  Analyze the following content and identify opportunities for repurposing it into different formats or channels.
  
  CONTENT:
  {content}
  
  OUTPUT INSTRUCTIONS:
  Provide a JSON response with the following structure:
  - content_type: The original content type
  - repurposing_opportunities: An array of repurposing opportunity objects with:
    * format: The suggested format for repurposing (blog, social media, video script, etc.)
    * audience: The target audience for this format
    * key_elements: Content elements that would work well in this format
    * modification_needed: Level of modification required (Low, Medium, High)
    * value_potential: Potential value of this repurposing (Low, Medium, High)
  - recommended_approach: The single most promising repurposing opportunity
  
  Format your response as valid JSON only.
description: "Identify content repurposing opportunities and strategies"
version: "1.0"
EOF

# Create summary generation prompts
cat > summary_generation/executive.yml << 'EOF'
template_id: "summary_generation_executive"
template_text: |
  Generate an executive summary of the following content, highlighting key points, insights, and recommendations.
  
  CONTENT:
  {content}
  
  OUTPUT INSTRUCTIONS:
  Provide a JSON response with the following structure:
  - executive_summary: A concise 2-3 paragraph executive summary
  - key_points: 3-5 bullet points covering the most important information
  - insights: 2-3 key insights derived from the content
  - recommendations: 2-3 actionable recommendations based on the content
  - business_implications: Brief overview of business implications
  
  Format your response as valid JSON only.
description: "Generate executive summaries of content for business leaders"
version: "1.0"
EOF

cat > summary_generation/technical.yml << 'EOF'
template_id: "summary_generation_technical"
template_text: |
  Generate a technical summary of the following content, highlighting technical details, architecture, and implementation considerations.
  
  CONTENT:
  {content}
  
  OUTPUT INSTRUCTIONS:
  Provide a JSON response with the following structure:
  - technical_summary: A concise 2-3 paragraph technical summary
  - system_components: Key components or modules identified
  - technical_requirements: Technical requirements or dependencies
  - implementation_notes: Important implementation considerations
  - technical_limitations: Any limitations or constraints identified
  - next_steps: Suggested technical next steps or areas for improvement
  
  Format your response as valid JSON only.
description: "Generate technical summaries focusing on implementation details"
version: "1.0"
EOF

# Create code analysis prompts
cat > code_analysis/standard.yml << 'EOF'
template_id: "code_analysis_standard"
template_text: |
  Analyze the following code and provide a detailed assessment of its structure, functionality, and quality.
  
  CODE:
  {content}
  
  OUTPUT INSTRUCTIONS:
  Provide a JSON response with the following structure:
  - language: The programming language identified
  - purpose: The main purpose or functionality of the code
  - components: Key functions, classes, or modules identified
  - complexity: Assessment of code complexity (Low, Medium, High)
  - quality_issues: Array of potential quality issues or improvements with:
    * issue: Description of the issue
    * importance: Priority level (Low, Medium, High)
    * suggestion: Recommended fix or improvement
  - strengths: Array of code strengths or good practices identified
  
  Format your response as valid JSON only.
description: "Analyze code structure, quality, and functionality"
version: "1.0"
EOF

echo "All prompt files have been created successfully."
cd ../../