## Software requirements

### Purpose

This software allows the user to track their performance in an online shooter game _recoil control_. In many online shooter games, the user can try to counteract the recoil by moving their mouse in a specific way.

### Users/Entities
- Has support for multiple users who can log in with a username and password. Users have their separate data from each other.

### Functionality
- Application startup:
	- [x] A way for the user to either create an account or log in
	- User can allow automatic login -> the user doesn't need to log in to their account on every application startup
	- [x] Multiple users can't have the same username
	- [x] Both username and password must be at least 3 characters long
	- [x] User is notified of invalid credentials
- Logged in:
	- User sees some basic statistics of their recent records if any exist
		- Average score in the last hour/day/week/month
		- Changes in percentages during the last hour/day/week/month
	- User can open a window or view for data entry
		- Multiple fields, such as weapon name, damage, accuracy, etc.
		- User can click submit the data by clicking a button.
		- User is notified of missing or invalid fields.


### Possible future developments
- Users can allow to share the information about their performance with others.
- Users can compare their performance with other users.
- Game specific presets for equipment and weapons
