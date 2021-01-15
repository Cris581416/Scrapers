
def get_course(sender: str) -> str: 
    """Returns course name 
    
    Searches through the argument value
    for a particular sender;
    Outputs corresponding course name or other string"""

    courses = { "Jason Nicholson": "Chem",
                "Ryan Williston": "SEHS",
                "William Pace": "HOTA",
                "Ronald Woods": "TOK",
                "Susana Valderrama": "Spanish",
                "Jason Neves": "Math",
                "Nikki Ahrenstorff": "English",
                "Tomoki Kuwana": "Jap"}

    for key in courses:
        if key in sender:
            return courses[key]
    
    return "Other"
