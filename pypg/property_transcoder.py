from typing import Any

from pypg import Property, PropertyClass, PropertyType, Trait
from pypg.traits.metadata import MetadataTrait
from pypg.transcode import Decoder, Encoder, default_locator


class PropertyClassEncoder(Encoder, handler_for=PropertyClass):
    def _encode(self, obj: PropertyClass):
        return {
            p.name: Encoder(p.get(obj), self).obj_id
            for p in type(obj).properties
        }

    @classmethod
    def _unpack(cls, data, obj_data: dict[str, str], locator=default_locator):
        return {
            name: Encoder.unpack(data, item_id, locator)
            for name, item_id in obj_data.items()
        }


class PropertyClassDecoder(Decoder, handler_for=PropertyClass):
    def _decode(self, obj_type: type, property_values: dict[str, Any]) -> Any:
        return obj_type(
            **{
                name: Decoder(
                    self.encoded_data, attr, self.locator, self
                ).instance
                for name, attr in property_values.items()
            }
        )


class PropertyEncoder(Encoder, handler_for=Property):
    def _encode(self, p: Property):
        return {
            "value_type": Encoder(p.value_type, self).obj_id,
            "traits": [Encoder(t, self).obj_id for t in p.traits],
        }


class TraitEncoder(Encoder, handler_for=Trait):
    def _encode(self, obj):
        return None


class MetadataTraitEncoder(Encoder, handler_for=MetadataTrait):
    def _encode(self, obj: MetadataTrait):
        return {"value": Encoder(obj.value, self).obj_id}


class PropertyTypeEncoder(Encoder, handler_for=PropertyType):
    def _encode(self, ptype: PropertyType):
        return {
            p.name: Encoder(getattr(ptype, p.name), self).obj_id
            for p in ptype.properties
        }
