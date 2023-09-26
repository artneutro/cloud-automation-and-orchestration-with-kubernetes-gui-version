# 
# Author: Jose Lo Huang
# Creation Date: 22/12/2020
# Updates:
# 28/12/2020 - Add some functions and comments
# 29/12/2020 - Minor fixes
# 
# This code is to define the Kubernetes class
#


import os
import time
import Error


class Kubernetes:
    # 
    # The Kubernetes class will manage the kubernetes tasks
    # 

    def __init__ ( self ):
        #
        # A instantiation of Error class for error messages
        # 
        self.error = Error.Error()


    def list_pods ( self ):
        #
        # This function lists all the pods and returns the pod names
        # 
        try:
            all_pods = []
            os.system("kubectl get pods -o wide")
            for i in os.popen('kubectl get pods -o wide | awk \'{print $1}\'').read().split('\n'):
                all_pods.append(i)
            return all_pods[1:-1]
        except:
            self.error.error_kubernetes("listing the pods")


    def describe_pod ( self , pod_name ):
        #
        # This function describes a pod chosen by the user
        # Input:
        # * Pod name
        # 
        try:
            os.system("kubectl describe pod "+pod_name)
        except:
            self.error.error_kubernetes("describing the pod")
            

    def create_pod ( self , image_name ):
        #
        # This function creates a pod deployment using nginx or redis images.
        # Input:
        # * Image name
        # 
        try:
            if str(image_name) in ['1','nginx']:
                os.system("kubectl apply -f pods/nginx-deploy.yaml")
            elif str(image_name) in ['2','redis']:
                os.system("kubectl apply -f pods/redis-deploy.yaml")
            else:
                self.error.not_valid_value(image_name)
        except:
            self.error.error_kubernetes("creating the pod")


    def is_digit( self , i ):
        #
        # This function will return True if the character is a number
        #
        return (48<=ord(i)<=57)


    def scale_pods ( self , pod_number , image_name ):
        #
        # This function scales the number of pods of a particular type deployment.
        # Input:
        # * New number of pods
        # * Pod type
        # 
        try:
            for i in str(pod_number):
                if not self.is_digit(i):
                    self.error.not_valid_value(pod_number)
                    return
            if (int(pod_number)>5000):
                self.error.not_valid_value(pod_number)
                return
            if str(image_name) in ['1','nginx']:
                os.system("kubectl scale deployments/nginx-deployment --replicas="+str(pod_number))
            elif str(image_name) in ['2','redis']:
                os.system("kubectl scale deployments/redis-deployment --replicas="+str(pod_number))
            else:
                self.error.not_valid_value(image_name)
        except:
            self.error.error_kubernetes("scaling the pods")


    def execute_command_pod ( self , command , pod_name ):
        #
        # This function executes a command on a pod chosen by the user.
        # Input:
        # * Command
        # * Pod name
        # 
        try:
            os.system("kubectl exec "+pod_name+" -- "+command)
        except:
            self.error.error_kubernetes("executing the command on the pod")


    def  deploy_pods( self ):
        #
        # This function creates a pod daemonset using an example from:
        # https://theithollow.com/2019/08/13/kubernetes-daemonsets/
        # 
        try:
            os.system("kubectl apply -f pods/ds-busybox.yaml")
            time.sleep(10)
            self.list_pods()
        except:
            self.error.error_kubernetes("deploying the daemonset")
            

    def delete_pod ( self , pod_name ):
        #
        # This function deletes a pod.
        # Input:
        # * Pod name
        # 
        try:
            os.system("kubectl delete pod "+pod_name)
        except:
            self.error.error_kubernetes("deleting the pod")


    def create_architecture ( self ):
        #
        # This function creates a kubernetes architecture using Cluster IP and Load Balancer services.
        # From: https://kubernetes.io/docs/tutorials/stateless-application/guestbook/
        # 
        try:
            # Creating all the architecture. Total time 270 seconds.
            print()
            # Creating the Redis master
            print("******************************************************************")
            print("******************** CREATING REDIS MASTER ***********************")
            os.system("kubectl apply -f pods/redis-arch-master.yaml")
            time.sleep(30)
            os.system("kubectl get pods -o wide")
            # Cluster IP service
            print("******************************************************************")
            print("**************** CREATING REDIS MASTER SERVICE *******************")
            os.system("kubectl apply -f pods/redis-arch-master-service.yaml")
            time.sleep(30)
            os.system("kubectl get services")
            # Creating the Redis workers
            print("******************************************************************")
            print("******************* CREATING REDIS WORKERS ***********************")
            os.system("kubectl apply -f pods/redis-arch-workers.yaml")
            time.sleep(30)
            os.system("kubectl get pods -o wide")
            # Cluster IP service
            print("******************************************************************")
            print("**************** CREATING REDIS WORKERS SERVICE ******************")
            os.system("kubectl apply -f pods/redis-arch-workers-service.yaml")
            time.sleep(30)
            os.system("kubectl get services")
            # Creating the PHP guestbook
            print("******************************************************************")
            print("****************** CREATING PHP GUESTBOOK ************************")
            os.system("kubectl apply -f pods/php-redis.yaml")
            time.sleep(90)
            os.system("kubectl get pods -o wide")
            # Load Balancer service
            print("******************************************************************")
            print("********************* CREATING PHP SERVICE ***********************")
            os.system("kubectl apply -f pods/php-redis-service.yaml")
            time.sleep(30)
            os.system("kubectl get services")
            # Checking the architecture
            print("******************************************************************")
            print("******************** CHECKING PHP SERVICE ************************")
            time.sleep(30)
            ip = os.popen("kubectl get service frontend | tail -1 | awk '{print $3}'").read()
            print("curl http://"+str(ip))
            os.system("curl http://"+str(ip))
            time.sleep(1)
        except:
            self.error.error_kubernetes("creating the architecture")


