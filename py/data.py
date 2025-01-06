# """
# Initialize the user interface components: buttons, table, and layout.
# """
userFormFields = [
    {"name": "username", "label": "Username:", "type": "text", "placeholder": "Enter username"},
    {"name": "full_name", "label": "Full Name:", "type": "text", "placeholder": "Enter full name"},
    {"name": "email", "label": "Email:", "type": "text", "placeholder": "Enter email"},
    {"name": "password", "label": "Password:", "type": "password", "placeholder": "Enter password"},
    {"name": "user_type", "label": "User Type:", "type": "combo", "options": ["User", "Admin", "Staff"]},
    {
    "name": "status",
    "label": "User Status:",
    "type": "combo",
    "options": [{"name": "Active", "id": 1}, {"name": "Inactive", "id": 0}]
    }
]

branchFormFields = [
    {"name": "branch_name", "label": "Branch Name:", "type": "text", "placeholder": "Enter Branch Name"},
    {"name": "branch_location", "label": "Branch Location:", "type": "text", "placeholder": "Branch Location"},
    {"name": "branch_phone", "label": "Branch Phone:", "type": "text", "placeholder": "Enter Branch Phone"},
    {
    "name": "status",
    "label": "Branch Status:",
    "type": "combo",
    "options": [{"name": "Active", "id": 1}, {"name": "Inactive", "id": 0}]
    }

]
