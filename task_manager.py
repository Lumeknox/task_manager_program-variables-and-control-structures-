"""
Start program
Import the 'datetime' module.
The program should ask the user to login using their details which are saved on the 'user.txt' file.
If the user is an admin they should have access to more options in the menu. 
They should be able to: register a user, add tasks, view all tasks, view their own tasks, edit task status, display statistics and exit the program.
The normal users should only be able to add tasks, view all tasks, view their own tasks and exit the program.
End program
"""


# Import the necessary library:
import datetime


# Create a login page to check if the user already registered. If the wrong credentials are entered display an error:
print("Please log in using your credentials:".upper())


# define a boolean variable to ensure that the program only proceeds further once the user enters the correct data.
logged_in = False


# Define an empty list for the entered username and passwords to be added to using append:
user_list = []


# Start a 'while loop' and ask the user to enter their username and password:
while not logged_in:
    username = input("Enter your username:\n")
    password = input("Enter your password:\n")


# Open the 'user.txt' file, read from it. Save the usernames and passwords from the 'user.txt' file to 'user_list':
    with open("user.txt" , "r") as user_file:
        for line in user_file:
            user_data = line.strip().split(", ")
            user_list.append(user_data)

# If the user enters the right credentials break the loop. If they enter the wrong credentials prompt an error message:
            if user_data[0] == username and user_data[1] == password:
                print("\nLogin successful!\n".upper())
                logged_in = True
                break
    if logged_in:
        break
    print("\nLogin Failed: Entered credentials are invalid. Please try again:\n".upper())


# If the logged in user is 'admin' display more options, which include registering new users and viewing statistics.
# Normal users are limited to adding new tasks, viewing all tasks, viewing their own tasks and exiting the program.
while logged_in:
    if username == "admin":
        menu = input('''Select one of the following options:
r - register a user
a - add task
va - view all tasks
vm - view my tasks
et - edit tasks
s - display statistics
e - exit
: ''').lower()
    else:
        menu = input('''Select one of the following options:
a - add task
va - view all tasks
vm - view my tasks
e - exit
: ''').lower()


# Ask the username and password of the new user to register them only if the person registering is 'admin':
    if menu == "r":
        if username == "admin":
            while True:
                new_username = input("\nPlease enter a username:\n")
                new_password = input("\nPlease enter a password:\n")
                confirm_password = input("\nRe-enter the password to confirm:\n")

# Check if user details exist in the 'user.txt' file:
                username_exists = False
                with open("user.txt", "r") as user_file:
                    for line in user_file:
                        if line.split(", ")[0] == new_username:
                            username_exists = True
                            break
                if username_exists:
                    print("\nUsername exists, please try another:\n".upper())

# Check if the new password and the re-entry of the password match. If the passwords do not match ask the user to re-enter the passwords:
                elif new_password == confirm_password:
                    with open("user.txt", "a") as user_file:
                        user_file.write(f"\n{new_username}, {new_password}")
                        print("\nNew user registered successfully!\n".upper())
                        break
                else:
                        print("\nPasswords do not match. Please try again:\n".upper())
        else:
            print("\nOnly the admin can register new users!\n".upper())


# If the user is "admin" then count the number of tasks and users:
    elif menu == "s":
            if username == "admin":
                with open ("tasks.txt", "r") as task_file:
                    total_tasks = sum(1 for line in task_file)
                with open ("user.txt", "r") as user_file:
                    total_users = sum(1 for line in user_file)

# Print out the statistics for the 'admin' user:
                print("\nStatistics:".upper())
                print(f"""
Total number of tasks: {total_tasks}
Total number of users: {total_users}
                    """)
            else:
                print("Only the admin can view statistics".upper())
            
            
# Ask the user to input all the required fields to add a new task:
    elif menu == 'a':

# Check if the user exists in the 'user.txt' file. If the user does not exist do not add the user and display and error message:
        task_username = input("\nPlease enter the username of the user the task is assigned to:\n")
        user_exists = False
        with open("user.txt", "r") as user_file:
            for line in user_file:
                if line.split(", ")[0] == task_username:
                    user_exists = True
                    break
        if not user_exists:
            print(f"\nError: User '{task_username}' does not exist. The task will not be added.\n".upper())
            continue

        task_title = input("\nPlease enter the title of the task:\n")
        task_description = input("\nPlease enter the description of the task:\n")
        current_date = (datetime.date.today().strftime("%d %b %Y"))

        while True:
                try:
                    due_date_input = input("\nPlease enter the due date of the task (DD MMM YYYY):\n")
                    task_due_date = datetime.datetime.strptime(due_date_input, "%d %b %Y")
                    task_due_date = task_due_date.strftime("%d %b %Y")
                    break
                except ValueError:
                    print("\nInput Error: Please use DD-MMM-YYYY\n".upper())
        
        task_complete = "No"

# Open the 'task.txt' file and add the new data to it:
        with open("tasks.txt", "a") as task_file:
                task_file.write(f"\n{task_username}, {task_title}, {task_description}, {current_date}, {task_due_date}, {task_complete}")

        print("\nThe task has been added successfully!\n".upper())


    elif menu == "va":
        print("\nHere are all the tasks:\n".upper())

# Read the 'tasks.txt' file and loop through it. Use the 'strip' and 'split' functions to break the data up into the correct sections:
        with open ("tasks.txt", "r") as task_file:
                for i in task_file:
                    task_sections = i.strip().split(", ")
                    if len(task_sections) == 6:                   
                        print(f"""
____________________________________________________________________________________________________                                           
Task:                   {task_sections[1]}
Assigned to:            {task_sections[0]}
Date assigned:          {task_sections[3]}
Due date:               {task_sections[4]}
Task completed?         {task_sections[5]}
Task description:       {task_sections[2]}
____________________________________________________________________________________________________
                     """)
                    else:
                        print(f"Skipping incorrect formatted task: {i}".upper())


# Here the user will be able to view their specific tasks which are assigned to their usernames:
    elif menu == 'vm':
        print(f"\nHere are all the tasks assigned to you ({username}):\n".upper())
        
        found_task = False
        with open ("tasks.txt", "r") as task_file:
            for i in task_file:
                task_data = i.strip().split(", ")
                if task_data[0] == username:
                    found_task = True
                    print(f"""
____________________________________________________________________________________________________                                       
Task:                   {task_data[1]}
Assigned to:            {task_data[0]}
Date assigned:          {task_data[3]}
Due date:               {task_data[4]}
Task completed?         {task_data[5]}
Task description:       {task_data[2]}
____________________________________________________________________________________________________
                     """)
        if not found_task:
            print("\nYou do not have any tasks assigned to you.\n".upper())


# Provide a section where the admin can change the status of a task:
# NB my friend Mark gave some advice and guidance in this section:

    elif menu == "et":
        if username == "admin":
            print("\nEdit the completion status of the tasks:\n")

# Initialise an empty list for the tasks to be added to:
            all_tasks = []

            with open("tasks.txt", "r") as task_file:
                for line in task_file:
                    all_tasks.append(line.strip().split(", "))

# Display all the tasks with numbers:
                for i, task in enumerate(all_tasks, 1):
                    print(f"""
{i})
Task: {task[1]}
Assigned to: {task[0]}
Completed: {task[5]}
                        """)


# Add a section to have 'admin' choose which task to update and have the selected task be updated:   
                if all_tasks:
                    while True:
                        try:
                            task_num = int(input("\nPlease enter the number of the task you wish to update - Enter '0' to exit:\n"))
                            if task_num == 0:
                                break
                            if 1 <= task_num <=len(all_tasks):
                                task_to_edit = all_tasks[task_num -1]
                                print(f"\n Status of task {task_to_edit[1]} : {task_to_edit[5]}")
                                new_status = input("\nIs the task complete? (Yes/No):\n").lower()
                                if new_status in ["yes", "no"]:
                                    task_to_edit[5] = new_status
                                    print(f"The task has been updated to: {new_status}")

# Write the updated tasks to the 'tasks.txt' file:
                                    with open("tasks.txt", "w") as task_file:
                                        for i, line in enumerate(all_tasks):
                                            task_file.write(", ".join(line))
                                            if i < len(all_tasks) - 1:
                                                task_file.write("\n") 
                                else:
                                    print("\nInput Error - input is invalid. The status has not changed\n".upper())
                                break
                            else:
                                print("\nThe task number is invalid, please try again:\n".upper())
                        except ValueError:
                            print("\nInput Error - Please enter a valid number:\n".upper())
                else:
                    print("\nThere are no available tasks to edit.\n".upper())
        else:
            print("\nOnly the admin can edit task statuses\n".upper())
            
                
# Exit the program:
    elif menu == "e":
        print("\nGoodbye!!!\n".upper())
        break

# If the user enters the wrong input regarding the menu this message must be displayed:
    else:
        print("\nYou have entered an invalid input. Please try again:\n".upper())
