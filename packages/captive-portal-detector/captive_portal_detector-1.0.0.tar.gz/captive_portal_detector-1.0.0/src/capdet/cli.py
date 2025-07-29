from capdet.detector import NetworkProbe

def main():
    result = NetworkProbe().network_health()
    print(result)
