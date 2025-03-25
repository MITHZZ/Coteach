import ollama
from research import search_web, get_wikipedia_summary

def research_agent(brief, target_audience):
    """Fetch relevant sources from DuckDuckGo & Wikipedia"""
    sources = search_web(brief)
    summary = get_wikipedia_summary(brief)
    return summary, sources

def llm_generate(prompt):
    """Generates content using a local LLM ("""
    # response = ollama.chat(model="mistral", messages=[
    response = ollama.chat(model="gemma:2b", messages=[
        {"role": "system", "content": "You are an expert course creator."},
        {"role": "user", "content": prompt[:500]}
    ])
    return response['message']['content']

def course_generator(brief, target_audience):
    """Main function that orchestrates all agents."""
    # ResearchPhase
    summary, sources = research_agent(brief, target_audience)

    # Course Structure Phase 
    outline_prompt = f"""
    Create a structured 6-module course for "{brief}".
    The target audience is {target_audience}.
    Make sure the content is beginner-friendly and engaging.
    """
    course_outline = llm_generate(outline_prompt)
    
    # Generate Content for Each Module
    modules = []
    for i, module in enumerate(course_outline.split("\n")):
        if module.strip():
            content_prompt = f"""
            Expand "{module.strip()}" into 3 detailed lessons.
            Tailor the explanations for {target_audience}.
            """
            lesson_content = llm_generate(content_prompt)
            
            modules.append({
                "title": module.strip(),
                "lessons": lesson_content.strip().split("\n")
            })

    return {
        "course_title": brief.title(),
        "description": summary,
        "target_audience": target_audience,
        "modules": modules,
        "references": sources
    }


#print( course_generator("Introduction to Microfinance", "Beginners"))
#print( course_generator("Introduction to Inheritence OOPS", "Beginners"))