import networkMan
import webpage
from webpage import monitor_webserver
import _thread  # For threading
import time
import asyncio





# Run the main function

def setup():
    networkMan.run_connect()
    # web server setup
        # set up ajax for data transfer
        # i want to be able to update the wifi connection from the webpage
    # machine set up
        #oscillator
        #pins


if __name__ == '__main__':
    setup()
    # deploy_web_server() => call infinite while loop to check within webpage.py
    
    #create thread for logic


    #_thread.start_new_thread(webpage.webpage_deploy, ())
    #webpage.webpage_deploy()

    time.sleep(10)
    
    while True:
        print("deploying server")
        webpage.web_server()

    """
    try:
        while True:
            print("Main program is running.")
            time.sleep(2)  # Main loop delay
    except KeyboardInterrupt:
        print("Program stopped.")
        _thread.start_new_thread(webpage.web_server, ())
    """  
        
    #monitor_webserver()
        

    #print(webpage.active_functions, "    ", webpage.web_server.)
    #print("web_server" not in webpage.active_functions)
    #print(webpage.active_functions)

    #PLC cycle => Input read, logic, output set, housekeeping (webpage) or something?