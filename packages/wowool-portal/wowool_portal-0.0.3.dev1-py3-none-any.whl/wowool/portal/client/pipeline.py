import logging
from typing import List
from wowool.document import Document
from requests.exceptions import ReadTimeout
from wowool.document.document_interface import DocumentInterface
from wowool.document.analysis.document import AnalysisDocument
from wowool.portal.client.error import ClientError
from wowool.portal.client.httpcode import HttpCode
from wowool.portal.client.portal import Portal, _PortalMixin
from wowool.common.pipeline.objects import UUID, createUUID
from wowool.document.serialize import serialize


logger = logging.getLogger(__name__)

PLK_DATA = "data"

DocumentType = str | DocumentInterface


def _to_document(data: DocumentInterface) -> dict:
    return serialize(data)


def _to_documents(data: list[DocumentInterface]) -> List[dict]:
    return [_to_document(item) for item in data]


def check_if_playground_response(payload: dict) -> bool:
    for document_json in payload["documents"]:
        if "id" not in document_json:
            return True
        else:
            return False


def pipeline_to_payload(pipeline: str | list[str | dict | UUID]) -> list | str:
    if isinstance(pipeline, list):
        return [createUUID(p).to_json() for p in pipeline]
    elif isinstance(pipeline, str):
        return str(pipeline)
    else:
        raise ValueError(f"Invalid pipeline type '{type(pipeline)}'")


class Pipeline(_PortalMixin):
    """
    :class:`Pipeline` is a class used to process your documents.
    """

    def __init__(self, name: str | list[str | dict | UUID], portal: Portal | None = None, description=None, **kwargs):
        """
        Initialize a Pipeline instance

        :param name: Name of the Pipeline
        :type name: ``str``
        :param portal: Connection to the Portal server
        :type portal: :class:`Portal`

        :return: An initialized pipeline
        :rtype: :class:`Pipeline`

        .. note::
            If the given name does not exist, the Portal will try to generate one for you. For example, if the provided name is ``english,sentiment`` it will run the English language and ``english-sentiment`` domain
        """
        super(Pipeline, self).__init__(portal)
        if self.portal is None:
            # let try a default portal
            self.portal = Portal()

        assert (
            self.portal is not None
        ), "A Portal object must be provided, either directly by passing the 'portal' argument or by using the API through a context (with-statement)"

        self.name = name
        self.description = description
        self.meta = kwargs

    def process_bulk(self, data: list | None = None, **kwargs) -> List[AnalysisDocument]:
        """
        Functor to process one or more documents. For example:

        .. literalinclude:: init_pipeline_context.py
            :language: python

        :param data: Input data to process. This includes support for one of the :ref:`InputProviders <py_eot_wowool_io_input_providers>`
        :type data: Either a ``str``, ``dict``, :class:`Document <wowool.document.Document>`, :class:`InputProvider <wowool.io.InputProvider>` or a ``list`` of one of the former
        :param id: The ID you wish to associate with each document. By default, if a file is passed, the file's name is used. Similarly, if a string is passed, a hash of the string is used
        :type id: ``str``
        :param kwargs: additional kw arguments for the requests library

        :return: A ``list`` of :class:`Document <wowool.document.Document>` instances is returned.
        """

        try:
            assert self.portal, "Portal not passed and not available from context"
            payload = self.portal._service.post(
                url="pipeline/run",
                status_code=HttpCode.OK,
                data={
                    "apiKey": self.portal.api_key,
                    "pipeline": pipeline_to_payload(self.name),
                    "documents": _to_documents(data),
                },
                **kwargs,
            )

            if not payload or "documents" not in payload:
                raise ClientError("Portal returned an invalid response")

            if check_if_playground_response(payload):
                # for backward compatibility
                documents_json_patch = []
                for document_json in payload["documents"]:
                    document_json_patch = {}
                    document_json_patch["id"] = document_json["apps"]["wowool_analysis"]["results"]["id"]
                    document_json_patch["data_type"] = "analysis/json"
                    document_json_patch["data"] = document_json
                    documents_json_patch.append(document_json_patch)
                payload["documents"] = documents_json_patch

            documents = [AnalysisDocument.from_dict(document_json) for document_json in payload["documents"]]
            return documents
        except ReadTimeout as ex:
            raise ClientError(str(ex))

    def process(
        self,
        data: DocumentType,
        id: str | None = None,
        metadata: dict | None = None,
        **kwargs,
    ) -> AnalysisDocument:
        """
        Functor to process one document. For example:

        .. literalinclude:: init_pipeline_context.py
            :language: python

        :param data: Input data to process. This includes support for one of the :ref:`InputProviders <py_eot_wowool_io_input_providers>`
        :type data: Either a ``str``, ``dict``, :class:`Document <wowool.document.Document>`, :class:`InputProvider <wowool.io.InputProvider>`
        :param id: The ID you wish to associate with the document. By default, if a file is passed, the file's name is used. Similarly, if a string is passed, a hash of the string is used
        :type id: ``str``
        :param kwargs: additional for the requests library


        :return: :class:`Document <wowool.document.Document>` an instance is returned
        """

        if isinstance(data, str):
            input_document = Document(id=id, data=data, metadata=metadata, **kwargs)
        elif isinstance(data, DocumentInterface):
            input_document = data

        documents = self.process_bulk([input_document])
        assert len(documents) == 1
        return documents[0]

    def __call__(self, data: DocumentType, id: str | None = None, **kwargs) -> AnalysisDocument:
        """
        Functor to process one document. For example:

        .. literalinclude:: init_pipeline_context.py
            :language: python

        :param data: Input data to process. This includes support for one of the :ref:`InputProviders <py_eot_wowool_io_input_providers>`
        :type data: Either a ``str``, ``dict``, :class:`Document <wowool.document.Document>`, :class:`InputProvider <wowool.io.InputProvider>`
        :param id: The ID you wish to associate with the document. By default, if a file is passed, the file's name is used. Similarly, if a string is passed, a hash of the string is used
        :type id: ``str``
        :param kwargs: additional kwargument for the requests library


        :return: :class:`Document <wowool.document.Document>` an instance is returned
        """
        return self.process(data, id, **kwargs)

    def __eq__(self, other):
        is_same_type = Pipeline is type(other)
        is_same_name = self.name == other.name
        return is_same_type and is_same_name

    def __repr__(self):
        return f"""wowool.portal.Pipeline(name="{self.name}")"""
