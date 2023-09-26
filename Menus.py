# 
# Author: Jose Lo Huang
# Creation Date: 22/12/2020
# Updates:
# 28/12/2020: Add the tkinter class
# 29/12/2020: Add more functions for tkinter management
# 
# This code is to maintain all the management menus in the same place.
# From this code, the specific Kubernetes tasks are triggered.
# 

import Kubernetes
import Error
import tkinter as tk
from tkinter import *

# Instantiate the Error class
error = Error.Error()

# Instantiate the Kubernetes class
kubernetes = Kubernetes.Kubernetes()

# Instatiate the tkinter class for root menu
root = tk.Tk()
v = tk.IntVar()

# Global variable to choose pods for kubernetes actions
pod_name = ""

# Global variable to choose image type for kubernetes actions
type_name = ""

# Global variable to choose number of pods to scale
scale_number = ""

# Global variable to choose the command to execute on a pod
command_name = ""


def task_finished ():
    #
    # This method prints a message after the completion of each task
    # 
    print("******************************************************************")
    print("Task completed. Please, choose your next task in the window.      ")
    print("******************************************************************")


def get_command ():
    # 
    # Get command menu:
    # This function request the user command to execute on a pod.
    #
    try:
        
        pod_list = Toplevel()
        pod_option = StringVar()

        # Set the window title
        pod_list.title("***** COMMAND TO EXECUTE *****")

        # Set the window label
        tk.Label(pod_list, text="""Please insert the command to execute and click the 'EXECUTE' button:""",
             justify = tk.LEFT,
             padx = 20).pack()

        # Create the entry box
        entry = tk.Entry(pod_list)        
        entry.pack()

        def pod_clicked ():
            # 
            # This function will store the command chosen on the global variable
            # and destroy the top level window.
            #
            global command_name
            command_name = str(entry.get())
            print(command_name)
            pod_list.destroy()
            pod_list.quit()
            pod_list.update()

        # Create the Execute button
        btn = tk.Button(pod_list, text="EXECUTE", fg='green', command=pod_clicked).pack()
        
        # Wait for user input
        pod_list.mainloop()
        
    except:
        error.general_error("creating the get command menu")  


def get_number ():
    # 
    # Get number menu:
    # This function request the user value for scale operation.
    #
    try:
        
        pod_list = Toplevel()
        pod_option = IntVar()

        # Set the window title
        pod_list.title("***** SCALE VALUE *****")

        # Set the window label
        tk.Label(pod_list, text="""Please select the new number of pods and click the 'EXECUTE' button:""",
             justify = tk.LEFT,
             padx = 20).pack()

        # Create the entry box
        entry = tk.Entry(pod_list)        
        entry.pack()

        def pod_clicked ():
            # 
            # This function will store the number chosen on the global variable
            # and destroy the top level window.
            #
            global scale_number
            scale_number = str(entry.get())
            print(scale_number)
            pod_list.destroy()
            pod_list.quit()
            pod_list.update()

        # Show the Execute button
        btn = tk.Button(pod_list, text="EXECUTE", fg='green', command=pod_clicked).pack()
        
        # Wait for user input
        pod_list.mainloop()
        
    except:
        error.general_error("creating the get number menu")  


def show_types ():
    # 
    # Show image types menu:
    # This function shows the pod types and request the user option.
    #
    try:
        
        pod_list = Toplevel()
        pod_option = IntVar()

        # Set the window title
        pod_list.title("***** NGINX or REDIS *****")

        # Set the window label
        tk.Label(pod_list, text="""Please select the pod type and click the 'EXECUTE' button:""",
             justify = tk.LEFT,
             padx = 20).pack()

        # Get the option list
        options = [('nginx',1),('redis',2)]

        # Wrap all the pods and values in tuples and show them
        for option, val in options:
            tk.Radiobutton(pod_list, 
                       text=option,
                       padx = 20, 
                       variable=pod_option,
                       value=val).pack(anchor=tk.W)

        def pod_clicked ():
            # 
            # This function will store the pod name chosen on the global variable
            # and destroy the top level window.
            #
            global type_name
            
            type_name, value = options[int(pod_option.get())-1]
            print(type_name)
            pod_list.destroy()
            pod_list.quit()
            pod_list.update()

        # Show the Execute button
        btn = tk.Button(pod_list, text="EXECUTE", fg='green', command=pod_clicked).pack()
        
        # Wait for user input
        pod_list.mainloop()
        
    except:
        error.general_error("creating the type menu")  


def show_pods ():
    # 
    # Show pods menu:
    # This function shows the pods and request the user option.
    #
    try:

        global kubernetes

        # Get the pod list
        pods = kubernetes.list_pods()
        options = []
        for i in range(len(pods)):
            options.append((pods[i],i+1))

        #print(options)
        if len(options) == 0:
            print("******************************************************************")
            print(" THERE ARE NO PODS! CREATE ONE FIRST. >>>>>>>>>>>>>>>>>>>>>>>>>>> ")
            print("******************************************************************")
            return
        
        pod_list = Toplevel()
        pod_option = IntVar()

        # Set the window title
        pod_list.title("***** ALL PODS *****")

        # Set the window label
        tk.Label(pod_list, text="""Please select the pod and click the 'EXECUTE' button:""",
             justify = tk.LEFT,
             padx = 20).pack()

        # Wrap all the pods and values in tuples and show them
        for option, val in options:
            tk.Radiobutton(pod_list, 
                       text=option,
                       padx = 20, 
                       variable=pod_option,
                       value=val).pack(anchor=tk.W)

        def pod_clicked ():
            # 
            # This function will store the pod name chosen on the global variable
            # and destroy the top level window.
            #
            global pod_name
            
            pod_name = pods[int(pod_option.get())-1]
            print(pod_name)
            pod_list.destroy()
            pod_list.quit()
            pod_list.update()

        # Show the Execute button
        btn = tk.Button(pod_list, text="EXECUTE", fg='green', command=pod_clicked).pack()
        
        # Wait for user input
        pod_list.mainloop()
        
    except:
        error.general_error("creating the pod menu")  


def router ():
    # 
    # Router menu:
    # This procedure is in charge of route the user to the different kubernetes functions
    # depending on the chosen options.
    #
    global kubernetes
    global pod_name
    global type_name
    global scale_number
    global command_name
    
    option = str(v.get())
    print()
    # List all pods
    if (option == "1"):
        print("******************************************************************")
        print(" ALL PODS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ")
        print("******************************************************************")
        kubernetes.list_pods()
        task_finished()
    # Describe a pod
    elif (option == "2"):
        print("******************************************************************")
        print(" DESCRIBE A POD >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ")
        print("******************************************************************")
        show_pods()
        kubernetes.describe_pod(pod_name)
        task_finished()
    # Create a pod
    elif (option == "3"):
        print("******************************************************************")
        print(" CREATE A POD >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ")
        print("******************************************************************")
        show_types()
        kubernetes.create_pod(type_name)
        task_finished()
    # Scale the number of pods
    elif (option == "4"):
        print("******************************************************************")
        print(" SCALE PODS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ")
        print("******************************************************************")
        get_number()
        show_types()
        kubernetes.scale_pods(scale_number, type_name)
        task_finished()
    # Execute a command on a pod
    elif (option == "5"):
        print("******************************************************************")
        print(" EXECUTE COMMAND ON POD >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ")
        print("******************************************************************")
        get_command()
        show_pods()
        kubernetes.execute_command_pod(command_name,pod_name)
        task_finished()
    # Deploy a pod to every node
    elif (option == "6"):
        print("******************************************************************")
        print(" DEPLOY POD TO EVERY NODE >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ")
        print("******************************************************************")
        kubernetes.deploy_pods()
        task_finished()
    # Delete a pod
    elif (option == "7"):
        print("******************************************************************")
        print(" DELETE A POD >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ")
        print("******************************************************************")
        show_pods()
        kubernetes.delete_pod(pod_name)
        task_finished()
    # Create a new architecture with cluster IP and load balancer
    elif (option == "8"):
        print("******************************************************************")
        print(" CREATE ARCHITECTURE WITH CLUSTER IP AND LOAD BALANCER >>>>>>>>>> ")
        print("******************************************************************")
        kubernetes.create_architecture()
        task_finished()
    # Exit program 
    elif (option == "9"):
        del kubernetes
        root.destroy()
        print("******************************************************************")
        print("Program completed. Close all the windows to finish.")
        print("******************************************************************")
    else:
        print(option)
        error.not_valid_value(option)
    return


def menu ():
    # 
    # Main Menu:
    # This function shows the main menu and request the user option.
    #
    try:

        # Set main window titkle
        root.title("***** KUBERNETES MENU *****")

        # Set main window label
        tk.Label(root, text="""KUBERNETES MANAGER V2.0. Author: Jose Lo Huang.\nPlease select the action to execute and click the 'EXECUTE' button:""",
             justify = tk.LEFT,
             padx = 20).pack()

        options = [("1. List all pods", 1),
                   ("2. Describe a pod", 2),
                   ("3. Create a pod", 3),
                   ("4. Scale the number of pods", 4),
                   ("5. Execute a command on a pod", 5),
                   ("6. Deploy a pod to every node", 6),
                   ("7. Delete a pod", 7),
                   ("8. Create a new architecture with Cluster IPs and Load Balancer", 8),
                   ("9. Exit", 9)]

        # Create radio buttons for each option in the main menu
        for option, val in options:
            tk.Radiobutton(root, 
                       text=option,
                       padx = 20, 
                       variable=v,
                       value=val).pack(anchor=tk.W)

        # Show the main menu
        btn = tk.Button(root, text="EXECUTE", fg='green', command=router).pack()

        # Wait for user input
        root.mainloop()
        
    except:
        error.general_error("creating the menu")




