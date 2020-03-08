from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from yowsup.layers import YowLayer

class EchoLayer(YowLayer):

    def receive(self, entity):
        if entity.getTag() == "message":
            self.onMessage(entity)

    def onMessage(self, entity):
        outEntity = TextMessageProtocolEntity(entity.getBody(), to=entity.getFrom())
        self.toLower(outEntity)
