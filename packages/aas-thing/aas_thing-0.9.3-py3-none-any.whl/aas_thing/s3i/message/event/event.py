from typing import Optional, Tuple, Union, List
from copy import deepcopy
from pydantic import Field, PrivateAttr, model_validator
from datetime import datetime
import datetime
from basyx.aas.model import datatypes, Submodel, SubmodelElement, Reference, Key, KeyTypes, datatypes, ReferenceElement, AnnotatedRelationshipElement, ModelReference, ExternalReference, BasicEventElement, Property, SubmodelElement, SubmodelElementCollection, SubmodelElementList
from aas_thing.s3i.message.reference import I40MessageGlobalReferenceKeys, I40MessageKeys
from aas_thing.s3i.message.frame import Frame, I40MessageType, ConversationPartner
from aas_thing.s3i.message.reference import I40MessageConversationRole
from aas_thing.s3i.message.message import I40Message

class I40EventMessage(I40Message):
    frame: Optional[Frame] = Field(None, alias=I40MessageKeys.frame.value)
    interactionElements: List[Union[Property, SubmodelElementCollection]] = Field(
        default_factory=list,
        alias=I40MessageKeys.interaction_elements.value
    )
    _topic: datatypes.String = PrivateAttr(default="")
    _timestamp: datatypes.DateTime = PrivateAttr(default="")
    _payload: SubmodelElementCollection = PrivateAttr(default_factory=dict)

    @model_validator(mode='after')
    def build_attributes(self):
        for element in self.interactionElements:
            if element.id_short == "topic":
                self._topic = element.value
            elif element.id_short == "timestamp":
                self._timestamp = element.value
            elif element.id_short == "payload":
                self._payload = element
        return self



class I40EventMessage_(I40Message):
    sender: str
    message_id: Optional[str]
    event_submodel_id: str
    event_id_short_path: Tuple[Key, ...]
    event_semantic_id: Optional[Reference]
    observable_submodel_id: str
    observable_id_short_path: Tuple[Key, ...]
    observable_semantic_id: Optional[Reference]
    topic: str
    payload: SubmodelElement

    def __init__(self,
                 event_submodel_id: str,
                 event_id_short_path: Tuple[Key, ...],
                 event_semantic_id: Optional[Reference],
                 observable_submodel_id: str,
                 observable_id_short_path: Tuple[Key, ...],
                 observable_semantic_id: Optional[Reference],
                 topic: str,
                 payload: SubmodelElement,
                 sender: str):

        self.event_submodel_id = event_submodel_id
        self.event_id_short_path = event_id_short_path
        self.event_semantic_id = event_semantic_id
        self.observable_submodel_id = observable_submodel_id
        self.observable_id_short_path = observable_id_short_path
        self.observable_semantic_id = observable_semantic_id
        self.topic = topic
        self.timestamp = datetime.now()
        self.payload = deepcopy(payload)
        self.sender = sender

        # Frame
        reference_key = I40MessageGlobalReferenceKeys.event_message 
        semantic_protocol = ExternalReference(key=(reference_key,))
        message_type = I40MessageType.event
        frame = Frame(
            semantic_protocol=semantic_protocol,
            message_type=message_type,
            sender=ConversationPartner(identification=sender, role=I40MessageConversationRole.emitter)
        )

        # Interaction Elements
        elements: List[Union[Submodel, SubmodelElement]] = []

        # add source element
        source_reference_key = I40MessageGlobalReferenceKeys.event_message_payload_source
        source_element = ReferenceElement(
            id_short="source",
            semantic_id=ExternalReference(key=(source_reference_key,)),
            value=ModelReference(
                type_=AnnotatedRelationshipElement,
                key=self.event_id_short_path,
            ),
        )
        elements.append(source_element)

        # add source semantic id if present
        if self.event_semantic_id:
            source_semantic_id_reference_key = I40MessageGlobalReferenceKeys.event_message_payload_source_semantic_id 
            source_semantic_id_element = ReferenceElement(
                id_short='sourceSemanticId',
                semantic_id=ExternalReference(key=(source_semantic_id_reference_key,)),
                value=self.event_semantic_id
            )
            elements.append(source_semantic_id_element)

        # add observable
        observable_reference_key = I40MessageGlobalReferenceKeys.event_message_payload_observable_reference
        observable_element = ReferenceElement(
            id_short='observableReference',
            semantic_id=ExternalReference(key=(observable_reference_key,)),
            value=ModelReference(type_=AnnotatedRelationshipElement, key=observable_id_short_path)
        )
        elements.append(observable_element)

        if self.observable_semantic_id:
            observable_semantic_id_reference_key = I40MessageGlobalReferenceKeys.event_message_payload_observable_semantic_id
            observable_semantic_id_element = ReferenceElement(
                id_short='observableSemanticId',
                semantic_id=ExternalReference(key=(observable_semantic_id_reference_key,)),
                value=self.observable_semantic_id
            )
            elements.append(observable_semantic_id_element)

        topic_semantic_protocol = I40MessageGlobalReferenceKeys.event_message_payload_topic
        topic_element = Property(
            value_type=datatypes.String,
            id_short='topic',
            semantic_id=ExternalReference(key=(topic_semantic_protocol,)),
            value=self.topic
        )
        elements.append(topic_element)

        timestamp_semantic_protocol = I40MessageGlobalReferenceKeys.event_message
        timestamp_element = Property(
            value_type=datatypes.DateTime,
            id_short='timestamp',
            semantic_id=ExternalReference(key=(timestamp_semantic_protocol,)),
            value=self.timestamp
        )
        elements.append(timestamp_element)

        payload_semantic_protocol = I40MessageGlobalReferenceKeys.event_message_payload_payload
        payload_element = SubmodelElementCollection(
            id_short='payload',
            semantic_id=ExternalReference(key=(payload_semantic_protocol,)),
        )
        payload_element.value = [self.payload]
        elements.append(payload_element)
        super().__init__(frame=frame, interaction_elements=elements)

    @classmethod
    def from_elements(cls,
                 event_element: BasicEventElement,
                 observable: Union[Property, SubmodelElementCollection, SubmodelElementList],
                 topic: str,
                 payload: SubmodelElement,
                 sender: str):

        event_element_model_reference = ModelReference.from_referable(event_element)
        for key in event_element_model_reference.key:
            if key.type == KeyTypes.SUBMODEL:
                event_submodel_id = key.value
        event_id_short_path = event_element_model_reference.key
        if event_submodel_id is None or event_id_short_path is None:
            raise ValueError("event_submodel_id or event_id_short_path is empty")

        event_semantic_id = event_element.semantic_id

        observable_model_reference = ModelReference.from_referable(observable)
        for key in observable_model_reference.key:
            if key.type == KeyTypes.SUBMODEL:
                observable_submodel_id = key.value
        observable_id_short_path = observable_model_reference.key
        if observable_submodel_id is None or observable_id_short_path is None:
            raise ValueError("observable_submodel_id or observable_id_short_path is empty")

        observable_semantic_id = observable.semantic_id

        return cls(event_submodel_id=event_submodel_id,
                             event_id_short_path=event_id_short_path,
                             event_semantic_id=event_semantic_id,
                             observable_submodel_id=observable_submodel_id,
                             observable_id_short_path=observable_id_short_path,
                             observable_semantic_id=observable_semantic_id,
                             topic=topic,
                             payload=payload,
                             sender=sender)

    @classmethod
    def from_json(cls, json):
        #TODO implement json parsing logic here
        pass         
