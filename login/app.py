from flask import Flask, render_template, request, session, jsonify
from groq import Groq
import os
import json
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = "supersecretkey"
load_dotenv()

# Initialize Groq API
GROQ_API_KEY = os.getenv("groq")
client = Groq(api_key=GROQ_API_KEY)

INITIAL_QUESTIONS = [
    '',
    "What is your name?",
    "What is your email address?",
    "Which soft skills best describe you?",
    "Which hard skills do you have experience with?",
    "Could you describe some of your projects?"
]

# Store user responses in a dictionary
session_data = {
    "name": "",
    "email": "",
    "introduction": '',
    "softskills": [],
    "hardskills": [],
    "projects": [],
    "education": [],
    "experience": []
}

# System prompt for the LLM
SYSTEM_PROMPT = '''You are an intelligent career assistant helping users build a professional resume.  
Your goal is to dynamically ask relevant follow-up questions based on the user's answers to gather detailed, structured information.

## *Instructions:*
1. Begin by asking a general question about the user's background.
2. Analyze the user's response and determine if more details are needed.
3. If details are missing or vague, generate follow-up questions to get specific, structured information.
4. Continue this iterative process until all essential resume sections are complete.

## *Essential Resume Sections:*  
- *Personal Information* (Full name, contact details, LinkedIn, portfolio, location)  
- *Work Experience* (Job title, company, duration, responsibilities, achievements)  
- *Skills* (Technical and soft skills relevant to the job)  
- *Education* (Degrees, universities, graduation years)  
- *Projects* (Notable work-related or personal projects)  
- *Certifications & Awards* (Relevant recognitions or licenses)  
- *Career Objective* (Future goals)  
- *Additional Sections* (Languages, volunteering, hobbies)

## *Guidelines for Follow-up Questions:*
- If the user's answer is too short (less than 10 words), ask *clarification* questions.  
- If a job title is given without details, ask about *key responsibilities* and *achievements*.  
- If a skill is mentioned, ask about *how the skill was applied* in work or projects.  
- If an award/certification is mentioned, ask *what it was for* and *why it is relevant*.  
- If an answer contains multiple topics, ask *separate follow-ups* for each.  
- Always ensure the response is *useful for resume building*.  
- Stop asking questions once all resume sections have *sufficient details*.

## *Example Conversation Flow:*
*Llama:* What is your current or most recent job title and company?  
*User:* Software Engineer at Google.  
*Llama:* What were your key responsibilities as a Software Engineer at Google?  
*User:* Developed backend systems and optimized performance.  
*Llama:* Can you provide an example of an impactful project you worked on?  
*User:* I optimized a search ranking algorithm, reducing query time by 30%.  
*Llama:* Great! What technologies did you use in this project?  
*User:* Python, TensorFlow, and Kubernetes.  
*Llama:* That's impressive! Moving on, what are your top skills?  
...

## *Final Step: Resume Generation*
Once enough information is gathered, compile a well-structured resume.  
Format it in a *professional, ATS-friendly manner*.
'''

@app.route('/')
def index():

    # Reset the session data for a new conversation
    session['question_index'] = 0
    session['answers'] = []
    session['chat_history'] = []
    session['count'] =0
    session['info']=[]

    
    # Add system prompt to chat history
    session['chat_history'].append({"role": "system", "content": SYSTEM_PROMPT})
    
    return render_template('chatbot.html', 
                          initial_questions=INITIAL_QUESTIONS)


@app.route('/get-data', methods=['POST'])
def get_data():
    data = request.json
    user_message = data.get('message', '')
    # Get the current state from session
    question_index = session.get('question_index', 0)
    answers = session.get('answers', [])
    chat_history = session.get('chat_history', [])
    
    # Add the user message to chat history
    chat_history.append({"role": "user", "content": user_message})
    
    # Handle predefined questions
    if question_index < len(INITIAL_QUESTIONS):
        # Store the answer to the current question
        answers.append(user_message)
        
        # Check if we still have predefined questions to ask
        question_index += 1
        if question_index < len(INITIAL_QUESTIONS):
            response = INITIAL_QUESTIONS[question_index]
        else:
            # All predefined questions answered, transition to LLM
            # Here you would use the collected answers to set context for your LLM
            name = answers[1]  # First question is empty, so name is at index 1
            
            # Transition message to LLM
            response = f"Thanks for sharing, {name}! I'll help you build a professional resume. Let's start by discussing your educational background. Could you tell me about your education?"
    else:
        session['count']+=1
        if session['count']>=3:
            try:
                print(session['count'])
                # Call Groq API with the full chat history
                completion = client.chat.completions.create(
                    model="llama3-70b-8192",
                    messages=chat_history
                )
                
                # Get response from Groq
                response = completion.choices[0].message.content
                chat_history.append({"role": "system", "content": response})
            except Exception as e:
                print(f"Error calling Groq API: {str(e)}")
                response = f"I'm sorry, I encountered an error while processing your request. Please try again."
                session['count']+=1
        # else:
        #     completion = client.chat.completions.create(
        #             model="llama3-70b-8192",
        #             messages=f'based on the below text analyze it and convert in to a resume with the following format name: email: projects , introduction: and experience {chat_history}'
        #         )
        #     response = completion.choices[0].message.content
        # Add the bot response to chat history
    # Update session
    session['question_index'] = question_index
    session['answers'] = answers
    session['chat_history'] = chat_history
    
    return jsonify({
        "message": response,
        "isPreDefinedQuestion": question_index < len(INITIAL_QUESTIONS)
    })

if __name__ == '__main__':
    app.run(debug=True)