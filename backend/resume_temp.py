from docxtpl import DocxTemplate

def generate_resume(template_path, output_path, data):
    """
    Generates a resume using a Word template by replacing placeholders with provided data.

    :param template_path: Path to the .docx template file
    :param output_path: Path to save the generated resume
    :param data: Dictionary containing keys and values to populate the template
    """
    doc = DocxTemplate(template_path)
    doc.render(data)  # Automatically replaces placeholders
    doc.save(output_path)
    print(f"Resume generated successfully: {output_path}")

# Example Usage:
# Provide any dictionary as input
user_input_data = {
    "name": "John Doe",
    "role": "Software Engineer",
    "phone": "+123-456-7890",
    "email": "john.doe@example.com",
    "address": "456 Tech Lane, Silicon Valley",
    "website": "www.johndoe.com",
    "profile": "Experienced software engineer specializing in AI and cloud computing.",
    "education": [
        {"degree": "B.Sc. Computer Science", "year": "2018-2022", "university": "MIT"},
        {"degree": "M.Sc. Artificial Intelligence", "year": "2022-2024", "university": "Stanford University"}
    ],
    "skills": ["Python", "Machine Learning", "Cloud Computing", "Data Science"],
    "languages": ["English", "Spanish"],
    "work_experience": [
        {
            "company": "Google",
            "role": "AI Engineer",
            "years": "2024 - Present",
            "responsibilities": ["Developed AI models", "Led research projects"]
        },
        {
            "company": "Microsoft",
            "role": "Software Developer",
            "years": "2022 - 2024",
            "responsibilities": ["Built cloud-based applications", "Managed software releases"]
        }
    ],
    "references": [
        {"name": "Alice Smith", "phone": "+987-654-3210", "email": "alice.smith@company.com", "position": "CTO at OpenAI"},
        {"name": "Bob Johnson", "phone": "+555-123-4567", "email": "bob.johnson@startup.com", "position": "CEO at AI Startup"}
    ]
}

# Call the function with user-provided data
generate_resume("resume_template.docx", "output_resume.docx", user_input_data)
