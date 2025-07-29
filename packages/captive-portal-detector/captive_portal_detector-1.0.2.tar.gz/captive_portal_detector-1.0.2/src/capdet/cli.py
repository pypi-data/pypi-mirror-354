import logging

from capdet.detector import NetworkProbe

def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )

    logger = logging.getLogger(__name__)
    logger.info("Starting network probe from CLI...")

    result = NetworkProbe().network_health()
    print(result)
