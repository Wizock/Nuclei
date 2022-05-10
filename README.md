# Nuclei

## todays goals

- [ ] UI revamp
  - [ ] add individual media view
  - [ ] add individual media edit
  - [ ] implement tiled dashboard view

- [ ] security measures
  - [ ] create a admin/superuser dashboard page
  - [ ] create a admin/superuser protected edit page
  - [ ] create a admin/superuser protected view page
  - [ ] create a design models for the admin/superuser dashboard
  - [ ] implement password reset functionality
  - [ ] create password reset email
  - [ ] hash uncompressed images

- [ ] implement the video media player
  - [ ] create a video player
  - [ ] create a video player controls
  - [ ] create a video player controls container
  - [ ] implement video compression flow
  - [ ] design video media models
  - [ ] index video media

# File Structure
```bat

H:.
|   .gitattributes
|   .gitignore
|   main.py
|   monkeytype.sqlite3
|   poetry.lock
|   pyproject.toml
|   README.md
|   session_goals.md
|   tree_file.txt
|   tree_structure.py
|   
+---nuclei
|   |   config.py
|   |   __init__.py
|   |   
|   +---admin_interface
|   |   |   config.py
|   |   |   models.py
|   |   |   tests.py
|   |   |   views.py
|   |   |   __init__.py
|   |   |   
|   |           
|   +---authentication
|   |   |   config.py
|   |   |   models.py
|   |   |   tests.py
|   |   |   views.py
|   |   |   __init__.py
|   |   |   
|   |   +---static
|   |   +---templates
|   |   |       landing_page.html
|   |   |       login.html
|   |   |       register.html
|   |   |       
|   |           
|   +---compression_service
|   |   |   config.py
|   |   |   models.py
|   |   |   tests.py
|   |   |   views.py
|   |   |   __init__.py
|   |   |   
|   |   +---static
|   |   |   +---compressed
|   |   |   \---imgs
|   |   +---templates
|   |   |       dashboard.html
|   |   |       grouped_rendering.html
|   |   |       individual_display.html
|   |   |       upload_template.html
|   |   |       
|   |           
|   +---database
|   |       nuclei.db
|   |       
|   +---extension_globals
|   |   |   admin.py
|   |   |   cookies.py
|   |   |   database.py
|   |   |   praetorian.py
|   |   |   __init__.py
|   |   |   
|   |           

```