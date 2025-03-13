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

Need to change the logic of how I'm creating widgets in main frame using create_widgets:
    ~~Reason: when user selects a city from saved location there is user_index or cities list so we dont get the city info and weather info as well since we call that from cities_popup and not from create_widget

    So we need to have create_widgets call all the api fetching for city info and weather info.

    In the city select from list, rather than getting user_index and passing it to create_widgets, get the necessary info create_widgets migth need for data fetching like name, and cords and stuff and store it in self. variables so it can be directly accessed. 

    Create_widgets will directly use this~~ DONE


    


