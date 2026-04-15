# Wk 8 Applied AI System: PawPal+ w/ Automatic Pet Task Suggester 

## Summary: 
The Co-Tasker Agent helps the user create pet tasks faster by automatically suggesting tasks based on what type of pet the user enters. The user has the choice of accepting it into their schedule, editing it, or rejecting it. 

## Architecture Overview: 
1. Input: CO Tasker Agent takes in the user's pet names and type of animal and any other additional information from the pet database. 
2. Process: 
- Makes 3 tasks that makes sense for each pet (composted of 1 generic task like "Feeding" and the other two are pet specifice like "Walk the Dog"
3. Output:
- Display the task one at a time to the user for each pet
4. User's Intervention:
  - The user has 3 choices of accepting, modifying, or rejecting the task
  - If the task is saved in the scheduler, the next task for either the same or next pet is shown

## Setup Instructions: 
1. Open the terminal and write ```streamlit run app.py```

Sample Interactions: Include at least 2-3 examples of inputs and the resulting AI outputs to demonstrate the system is functional.
Design Decisions: Why you built it this way, and what trade-offs you made.
Testing Summary: What worked, what didn't, and what you learned.
Reflection: What this project taught you about AI and problem-solving.


## TF Checklist 
## Phase 0: Repo Preparation (Spot Check)
TFs should:
 - [x] Understand expected repo structure
 - [x] Set up a new repo with the previous project chosen. (Module 2 - PawPal+ ) 


## Phase 1: Functionality Extension (Assign)
TFs should:
- [x] Identify  new AI feature: (Fine-Tuned / Specialized Model) For a pet task scheduler, having the app be able to automatically make suggested tasks based on what type of pet the user enters.
- [x] Verify the feature is actually used in logic
- [x] Detect shallow or fake integrations
- [x] Trace data flow end‑to‑end
- [x] New concepts introduced:
- [x] System integration thinking
- [x] Feature authenticity

# Phase 2: Architecture Diagram (Review)
TFs should:
- [x]  Create a system diagram: See [Pet Task Generator Digram](assets/pet_task_generation.png)
- [x] Confirm alignment with code
- [x] Flag mismatches

## Phase 3: Documentation (Review)
TFs should:
- [x] Understand what is going in the README
TFs may skip:
Writing a full README

## Phase 4: Reliability and Testing (Assigned)
TFs should:
Identify what reliability signal is used
Include at least one way to test or measure its reliability
- [x] Automated tests
- [x] Confidence scoring
- [ ] Logging and error handling
- [x] Human evaluation
- [x] Be able to document your findings from your testing.


## Phase 5/6: Reflection and Portfolio (Review)
TFs should:
- [x] Understand rubric expectations
TFs may skip:
Presentation polish
Portfolio writing
