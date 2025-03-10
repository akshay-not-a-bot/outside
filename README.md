# Next: # 
1. Replacing placeholder data with actual ones, 
2. Update weather paras pulling from OM api
    Remove: pressure and percipitation
    Add: Apparent temp, humidity
3. Search function in cities_popup TopLevel in not functional
4. Saved Locations feature

# Changelog/ Features: #
1. App will directly ask to search for a city if there is no default city set
2. in City search window, a search bar to search for a different city

# Notes: #
storing weather data
    ~~not working cause create_widget gets called first in __init__ before popup so self.weather doesn't exist at that time
    cause unless you search for city popup won't be called but this printing will still get executed.
    so I need to maybe call the popup window first at the time of app opening and halt the create_widgets with wait.window
    untill user selcets city.~~

    ~~OR there is a welcome screen on greetings and will prompt to select the city first and maybe store that in a file and
    only open this welcome screen if the file is empty~~ --> Checking is_default field in DB for this and prompting to search for a city if not found.

    


