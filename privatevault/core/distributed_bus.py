class DistributedBus:
    """
    Abstract message bus for distributed agent execution.
    Can be backed by Kafka, NATS, Redis Streams, etc.
    """

    def publish(self, topic, message):
        raise NotImplementedError

    def subscribe(self, topic, handler):
        raise NotImplementedError
