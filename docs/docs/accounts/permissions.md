# Permissions

User permissions depend on the role they have in a particular group or project.

For public groups and its public projects, all users will inherit the role `Reader`. If a group visibility level is private, all its projects will be considered as private too.

## Group permissions

Action | Reader | Admin | Owner
------ | ------ | ----- | -----
View group projects | &check; | &check; | &check;
Change group settings | &cross; | &check; | &check;
Manage group collaborators | &cross; | &check; | &check;
Create group projects | &cross; | &check; | &check;
Delete group | &cross; | &cross; | &check;
Change visibility level | &cross; | &cross; | &check;

## Project permissions

The roles defined on a group's project are automatically inherited by the project. If a user is a collaborator to a group's project and the project itself, the highest role level is used.

Action | Reader | Admin | Owner
------ | ------ | ----- | -----
View project details | &check; | &check; | &check;
View project documentation  | &check; | &check; | &check;
Change project settings | &cross; | &check; | &check;
Manage project collaborators | &cross; | &check; | &check;
Upload project documentation | &cross; | &check; | &check;
Delete project | &cross; | &cross; | &check;
Change visibility level | &cross; | &cross; | &check;
