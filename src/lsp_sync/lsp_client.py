from pylspclient.lsp_structs import TextDocumentIdentifier, Location, Position
from pylspclient.lsp_client import LspClient
from dacite import from_dict
from pprint import pprint


class LspClientExtended(LspClient):
    @staticmethod
    def getSignatureFromTooltip(hoverToolTip: str):
        lines = hoverToolTip.splitlines()
        return lines[2]


    def getTypeSignature(
        self,
        textDocument: TextDocumentIdentifier,
        position: Position
    ) -> list[Location]:
        """
        The goto type definition request is sent from the client to the server to resolve the hover.

        :param TextDocumentItem textDocument: The text document.
        :param Position position: The position inside the text document.
        """
        result_dict = self.lsp_endpoint.call_method("textDocument/hover", textDocument=textDocument, position=position)

        hoverToolTip = result_dict['contents']['value']

        return self.getSignatureFromTooltip(hoverToolTip)
    
    