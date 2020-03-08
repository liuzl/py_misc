from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback

class EchoLayer(YowInterfaceLayer):

    @ProtocolEntityCallback("message")
    def onMessage(self, entity):
        outEntity = TextMessageProtocolEntity(entity.getBody(), to=entity.getFrom())
        self.toLower(outEntity)
