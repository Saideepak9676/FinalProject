

# The User Management System Final Project: Your Epic Coding Adventure Awaits! 🎉✨🔥

## Introduction: Buckle Up for the Ride of a Lifetime 🚀🎬

Welcome to the User Management System project - an epic open-source adventure crafted by the legendary Professor Keith Williams for his rockstar students at NJIT! 🏫👨‍🏫⭐ This project is your gateway to coding glory, providing a bulletproof foundation for a user management system that will blow your mind! 🤯 You'll bridge the gap between the realms of seasoned software pros and aspiring student developers like yourselves. 


# Issue: Implement Robust Username Generation and Validation for Enhanced User Management            

## Description:
This section of the project implements robust username management features designed to enhance user experience and ensure data integrity. The implementation supports the automatic generation of unique, URL-safe nicknames for users during creation while allowing users to change their nicknames with validation. It enforces strict uniqueness and format constraints, ensuring compatibility with public-facing identifiers. This functionality improves user anonymity and privacy by assigning meaningful, anonymous nicknames based on a combination of words and numbers.            

## Features:
1. Username Generation:          

- Randomly generate nicknames upon user creation.              
- Use a combination of nouns, verbs, and a numeric suffix to ensure meaningful and diverse names.                  

2. Nickname Uniqueness:              
- Validate that no two users share the same nickname.               
- Handle duplicate nickname conflicts during both user creation and updates.
                    
3. URL-Safe Identifier:                  
- Ensure that nicknames are URL-safe, allowing them to be used in public contexts without encoding issues.                      
- Only allow alphanumeric characters, underscores, and hyphens in nicknames.
                          
4. User-Controlled Updates:               
- Allow users to update their nicknames, ensuring the new nickname is both valid and unique.           

5. Privacy and Anonymity:                        
- Assign anonymous nicknames by default to protect user identities.          
- Maintain privacy by validating nicknames against strict rules.          

6. Testing and Verification:                       
- The system includes comprehensive tests to ensure correctness, with plans for additional tests to cover edge cases and rare scenarios.          

## Expected Outcome                
- Users will always have unique nicknames, either system-generated or user-updated.                        
- Nicknames will be compliant with URL-safety standards, ensuring seamless usage in public links.                     
- Conflicts arising from duplicate nicknames during creation or updates will be handled gracefully.                    
- User privacy and anonymity will be safeguarded through anonymous nickname assignments.                       

## Resolution Steps               
The implementation of the nickname management and validation features involved updates to multiple components of the project, reflecting the complexity of the requirements. Below is a detailed explanation of the resolution steps and the specific changes made to each relevant file:

1. app/services/user_service.py                        
Changes Made:                   
Nickname Validation During Creation:                     
- Updated the create method to validate nicknames against database records.       
- Used the generate_nickname() function to generate random nicknames and ensure uniqueness before assigning them to users.            
- Integrated the validate_url_safe_username() function to check the format of nicknames.                      
- Handled duplicate nickname errors gracefully with proper logging and error messages.                       

Nickname Validation During Updates:               
- Updated the update method to enforce uniqueness for nicknames during updates.                                 
- Validated that nicknames meet URL-safety standards before saving changes.       

Purpose: Ensure that all nicknames are unique, valid, and compliant with URL-safe standards during user creation and updates.              

2. tests/test_api/test_users_api.py            
Changes Made:             
Test for Duplicate Nickname Creation:
- Added test_create_user_duplicate_nickname to ensure that creating a user with a duplicate nickname fails.                 
- Mocked external email service to focus on nickname validation logic.      

Test for Duplicate Nickname Updates:                          
- Added test_update_user_duplicate_nickname to validate that nickname updates with duplicates are rejected.               
- Used the test client to simulate API calls for creation and updates.          
Purpose: Verify that the API layer correctly handles nickname uniqueness and format validation.            

3. tests/test_services/test_user_service.py              
Changes Made:             
Test for Nickname Creation:           
- Added tests to ensure that generated nicknames are unique and comply with URL-safety rules.             
- Mocked email service to isolate the nickname generation and validation logic.                

Test for Duplicate Nickname Handling:               
- Added test_create_user_duplicate_nickname and test_update_user_duplicate_nickname to validate service-layer logic for handling duplicates.                 

Purpose: Test the internal service logic to ensure correctness and coverage of nickname generation and validation features.                  

4. app/utils/nickname_gen.py                
Changes Made:                  
- Implemented the generate_nickname() function to generate random combinations of nouns, verbs, and numbers.                
- Added utility functions to validate the format and uniqueness of nicknames.                  

- Purpose: Provide a reusable utility to create meaningful and unique nicknames while adhering to project constraints.            

5. app/utils/validators.py          
Changes Made:           
- Added the validate_url_safe_username() function to enforce URL-safe standards for nicknames.               

Purpose: Ensure that nicknames can safely be used as public-facing identifiers in URLs without encoding issues.            

6. tests/conftest.py              
Changes Made:              
- Added new test fixtures to create mock users with unique nicknames for testing.                
- Introduced an admin_user and manager_user fixture for role-based testing of API endpoints.                

Purpose: Facilitate testing of nickname uniqueness and validation in both API and service layers.               

7. app/models/user_model.py            
Changes Made:           
- Updated the User model to enforce uniqueness constraints on the nickname field at the database level.             

Purpose: Add an additional layer of protection against duplicate nicknames, even in concurrent user creation scenarios.             

## Test
Overview
This section outlines the tests implemented to verify the functionalities related to Username Generation and Validation. These tests ensure that the following features are correctly implemented and functional:             

- Username Generation: Automatically generates a random, unique username combining nouns, verbs, and numbers.            
- Uniqueness: Validates that usernames are unique during creation and updates.              
- Validation: Ensures usernames are URL-safe and adhere to format constraints.               
- User Privacy and Anonymity: Keeps usernames secure and private.           
- Edge Case Handling: Handles invalid data gracefully.              

Pytest

1. API Tests
File: tests/test_api/test_users_api.py          

Key Tests:          
- test_create_user_duplicate_nickname: Verifies that creating a user with a duplicate nickname fails.             
- test_update_user_duplicate_nickname: Ensures that updating a user to have a duplicate nickname fails.             
- test_create_user_invalid_data: Tests that invalid data (e.g., missing required fields) is handled properly.             


2. Service Tests              
File: tests/test_services/test_user_service.py          

Key Tests:             
- test_create_user_with_valid_data: Ensures valid user data creates a user successfully.                  
- test_create_user_duplicate_email: Confirms duplicate email detection and rejection.               
- test_update_user_duplicate_nickname: Validates that updating to a duplicate nickname is disallowed.                      
- test_update_user_invalid_data: Checks handling of invalid user update data.                     

### Test Results for API Tests
![Test API Results](images/test_api_readme.jpg)

### Test Results for User Service Tests
![Test User Service Results](images/user_service_readme.jpg)




### [Instructor Video - Project Overview and Tips](https://youtu.be/gairLNAp6mA) 🎥

- [Introduction to the system features and overview of the project - please read](system_documentation.md) 📚
- [Project Setup Instructions](setup.md) ⚒️
- [Features to Select From](features.md) 🛠️
- [About the Project](about.md)🔥🌟

## Goals and Objectives: Unlock Your Coding Superpowers 🎯🏆🌟

Get ready to ascend to new heights with this legendary project:

1. **Practical Experience**: Dive headfirst into a real-world codebase, collaborate with your teammates, and contribute to an open-source project like a seasoned pro! 💻👩‍💻🔥
2. **Quality Assurance**: Develop ninja-level skills in identifying and resolving bugs, ensuring your code quality and reliability are out of this world. 🐞🔍⚡
3. **Test Coverage**: Write additional tests to cover edge cases, error scenarios, and important functionalities - leave no stone unturned and no bug left behind! ✅🧪🕵️‍♂️
4. **Feature Implementation**: Implement a brand new, mind-blowing feature and make your epic mark on the project, following best practices for coding, testing, and documentation like a true artisan. ✨🚀🎆
5. **Collaboration**: Foster teamwork and collaboration through code reviews, issue tracking, and adhering to contribution guidelines - teamwork makes the dream work, and together you'll conquer worlds! 🤝💪🌍
6. **Industry Readiness**: Prepare for the software industry by working on a project that simulates real-world development scenarios - level up your skills to super hero status  and become an unstoppable coding force! 🔝🚀🏆⚡

## Submission and Grading: Your Chance to Shine 📝✏️📈

1. **Reflection Document**: Submit a 1-2 page Word document reflecting on your learnings throughout the course and your experience working on this epic project. Include links to the closed issues for the **5 QA issues, 10 NEW tests, and 1 Feature** you'll be graded on. Make sure your project successfully deploys to DockerHub and include a link to your Docker repository in the document - let your work speak for itself! 📄🔗💥

2. **Commit History**: Show off your consistent hard work through your commit history like a true coding warrior. **Projects with less than 10 commits will get an automatic 0 - ouch!** 😬⚠️ A significant part of your project's evaluation will be based on your use of issues, commits, and following a professional development process like a boss - prove your coding prowess! 💻🔄🔥

3. **Deployability**: Broken projects that don't deploy to Dockerhub or pass all the automated tests on GitHub actions will face point deductions - nobody likes a buggy app! 🐞☠️ Show the world your flawless coding skills!

## Managing the Project Workload: Stay Focused, Stay Victorious ⏱️🧠⚡

This project requires effective time management and a well-planned strategy, but fear not - you've got this! Follow these steps to ensure a successful (and sane!) project outcome:

1. **Select a Feature**: [Choose a feature](features.md) from the provided list of additional improvements that sparks your interest and aligns with your goals like a laser beam. ✨⭐🎯 This is your chance to shine!

2. **Quality Assurance (QA)**: Thoroughly test the system's major functionalities related to your chosen feature and identify at least 5 issues or bugs like a true detective. Create GitHub issues for each identified problem, providing detailed descriptions and steps to reproduce - the more detail, the merrier! 🔍🐞🕵️‍♀️ Leave no stone unturned!

3. **Test Coverage Improvement**: Review the existing test suite and identify gaps in test coverage like a pro. Create 10 additional tests to cover edge cases, error scenarios, and important functionalities related to your chosen feature. Focus on areas such as user registration, login, authorization, and database interactions. Simulate the setup of the system as the admin user, then creating users, and updating user accounts - leave no stone unturned, no bug left behind! ✅🧪🔍🔬 Become the master of testing!

4. **New Feature Implementation**: Implement your chosen feature, following the project's coding practices and architecture like a coding ninja. Write appropriate tests to ensure your new feature is functional and reliable like a rock. Document the new feature, including its usage, configuration, and any necessary migrations - future you will thank you profusely! 🚀✨📝👩‍💻⚡ Make your mark on this project!

5. **Maintain a Working Main Branch**: Throughout the project, ensure you always have a working main branch deploying to Docker like a well-oiled machine. This will prevent any last-minute headaches and ensure a smooth submission process - no tears allowed, only triumphs! 😊🚢⚓ Stay focused, stay victorious!

Remember, it's more important to make something work reliably and be reasonably complete than to implement an overly complex feature. Focus on creating a feature that you can build upon or demonstrate in an interview setting - show off your skills like a rockstar! 💪🚀🎓

Don't forget to always have a working main branch deploying to Docker at all times. If you always have a working main branch, you will never be in jeopardy of receiving a very disappointing grade :-). Keep that main branch shining bright!

Let's embark on this epic coding adventure together and conquer the world of software engineering! You've got this, coding rockstars! 🚀🌟✨
