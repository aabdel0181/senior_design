import threading
import time
import boto3
import random  # random module to gen test values
from datetime import datetime, timezone
from decimal import Decimal

# init DynamoDB
dynamodb = boto3.resource(
    "dynamodb",
    region_name="us-east-1",
    # put key and secret key here
)
table = dynamodb.Table('senior_design_dummy')

# function to simulate GPU metrics with random numbers
def gpu_prober():
    device_id = "test-device-uuid" 
    while True:
        # Generate random test values
        temperature = random.randint(30, 90)  # temp in C
        clock_speed = random.randint(1000, 2000)  # clock speed in MHz
        power_usage = round(random.uniform(50.0, 300.0), 2)  # power usage in W
        memory_used = round(random.uniform(1000.0, 8000.0), 2)  # mem used in MB

        print(f"Temp: {temperature} C, Clock: {clock_speed} MHz, Power: {power_usage} W, Memory Used: {memory_used} MB")
        
        # store generated metrics in DynamoDB
        store_metrics(
            device_id=device_id,
            temperature=temperature,
            clock_speed=clock_speed,
            power_usage=power_usage,
            memory_used=memory_used
        )
        
        time.sleep(1)

# function to store metrics in DynamoDB table
def store_metrics(device_id, temperature, clock_speed, power_usage, memory_used):
    timestamp = datetime.now(timezone.utc)
    
    table.put_item(
        Item={
            'DeviceId': device_id,
            'Timestamp': timestamp.isoformat(),  # convert timestamp to a string format
            'Temperature': Decimal(temperature),
            'ClockSpeed': Decimal(clock_speed),
            'PowerUsage': Decimal(str(power_usage)),  # convert to string first to handle float to Decimal
            'MemoryUsed': Decimal(str(memory_used))   # convert to string first to handle float to Decimal
        }
    )

def execute_workload():
    print("Executing sample workload...")

def main():
    # run the simulated GPU odometer in its own separate thread
    odometer_thread = threading.Thread(target=gpu_prober)
    odometer_thread.daemon = True  # make sure thread will not block the main process from exiting
    odometer_thread.start()

    execute_workload()

    # keep the main thread alive so the odometer continues running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting")

if __name__ == "__main__":
    main()


# import threading
# import time
# import boto3
# from datetime import datetime, timezone
# # Note use nvidia official release nvidia-ml-py, not unofficial 
# import pynvml
# from pynvml import *

# # init DynamoDB 
# dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
# table = dynamodb.Table('senior_design_dummy')

# def initialize():
#     # Initialize NVML
#     pynvml.nvmlInit()

#     # Get number of devices
#     device_count = pynvml.nvmlDeviceGetCount()

#     # This will show us all the devices on our system. Will automatically select the highest index device
#     for i in range(device_count): 
#         handle = pynvml.nvmlDeviceGetHandleByIndex(i)
#         name = pynvml.nvmlDeviceGetName(handle); 
#         print(f"Device {i}: {name}")  

#     driver_version = pynvml.nvmlSystemGetDriverVersion()
#     print(f"Driver version: {driver_version}")

#     return handle
    
# # Function to probe GPU metrics 8=D
# def gpu_prober(handle):
#     device_id = nvmlDeviceGetUUID(handle)
#     last_power_reading = None
    
#     while True:
#         temperature = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
#         clock_speed = pynvml.nvmlDeviceGetClockInfo(handle, pynvml.NVML_CLOCK_GRAPHICS)
#         memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
#         # power_management_enabled = pynvml.nvmlDeviceGetPowerManagementMode(handle)
#         # print(f"Power management enabled: {power_management_enabled}")
#         # Cacheing last successful power value
#         try:
#             power = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000.0 # mW to W
#             last_power_reading = power
#         except pynvml.NVMLError as err:
#             if isinstance(err, pynvml.NVMLError_NoData):
#                 power = last_power_reading if last_power_reading is not None else "N/A"
#             else:
#                 raise

#         print(f"Temp: {temperature} C, Clock: {clock_speed} MHz, Power: {last_power_reading} W, Memory Used: {memory_info.used / (1024 ** 2)} MB")
        
#         # store data in DynamoDB table
#         store_metrics(
#             device_id=device_id,
#             temperature=temperature,
#             clock_speed=clock_speed,
#             power_usage=last_power_reading,
#             memory_used=memory_info.used / (1024 ** 2)
#         )
        
#         # Poll regularly
#         time.sleep(1)
        
# # Function to store metrics in DynamoDB table
# def store_metrics(device_id, temperature, clock_speed, power_usage, memory_used):
#     timestamp = datetime.now(timezone.utc)
    
#     table.put_item(
#         Item={
#             'DeviceId': device_id,
#             'Timestamp': timestamp,
#             'Temperature': temperature,
#             'ClockSpeed': clock_speed,
#             'PowerUsage': power_usage,
#             'MemoryUsed': memory_used
#         }
#     )

# # Our main thread can handle our GPU workloads
# def execute_workload():
#     print("executing our sample workload...")

# def main():
#     handle = initialize()
   
#     # Run the GPU odometer in it's own separate thread
#     odometer_thread = threading.Thread(target=gpu_prober, args=(handle,))
#     odometer_thread.daemon = True  # make sure thread will not block the main process from exiting
#     odometer_thread.start()

#     execute_workload()

#     # Keep our main thread alive so the odometer continues running
#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         print("Exiting")

#     # We need to shutdown the nvml interface 
#     pynvml.nvmlShutdown()


# if __name__ == "__main__":
#     main()
    