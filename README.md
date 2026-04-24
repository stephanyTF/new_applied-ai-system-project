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
1. Install dependencies: ``` pip install -r requirements.txt ```
2. Open the terminal and write ```streamlit run app.py```
3. Run tests on Co-Tasker: ``` pytest test_pawpal.py -v -k "CoTasker" ```

## Sample Interactions:
1. Case #1:
    - User, Kiki adds in their pet cat "Jiji" and chooses to have the Co Tasker generate 3 tasks for them. Kiki accepts the first task "Feed Jiji" while Kiki modifies the time duration of the second task, "Brush Jiji". The last task Kiki rejects because it doesn't apply to Jiji's case. 
2. Case #2
   - User, Katie adds in her two dogs, Max and Duke. She generates tasks using the Co Tasker and she reads through the first set of task for Max (accepting and modifying a few) before moving to the tasks generated for Duke. She accepts all three and adds her accepted task into her schedule. 

## Design Decisions: Why you built it this way, and what trade-offs you made.
 - Reason for Design: The User is able to have the option to initate the task generation by selecting the button below where they added their pets since it make sense with the user flow and helps put the user in control of the task generation while making it more efficient.
 - Trade-offs: N/A


## Testing Summary:
- 10/10 test case passed
- What could be improved:
    - More robust design: In the case a user adds a new pet after generating suggested task for a previous pet. The Co-Tasker agent may repeat suggesting task for the old pet
    - Ensure the Co-Tasker is taking into account task timing to prevent overlapping scheduling

## Reflection: What this project taught you about AI and problem-solving.
- AI is really effiicent in carrying through code implementation but the developer must think critically about design which can only be highlighted through rigorous testing and putting through wide variety of test cases. 


# TF Checklist 
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
