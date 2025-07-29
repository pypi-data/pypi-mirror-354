import json

from opensemantic.characteristics.quantitative import (
    Area,
    AreaUnit,
    Length,
    LengthUnit,
    QuantityValue,
    Width,
)

# to we have to adapt VSCode settings to include the package index?
# "python.analysis.packageIndexDepths": [
#       {"name": "opensemantic.characteristics.quantitative",
#       "depth": 4, "includeAllSymbols": true}
# ]


def test_pint():

    q = Length(value=1.0, unit=LengthUnit.milli_meter)
    # transform to pint
    q_pint = q.to_pint()
    # transform back to QuantityValue
    q_ = QuantityValue.from_pint(q_pint)
    assert q == q_

    q2 = Length(value=1.0, unit=LengthUnit.meter)
    q3 = q + q2
    assert q3 == Length(value=1.001, unit=LengthUnit.meter)

    q31 = q * q2
    assert q31 == Area(value=1000.0, unit=AreaUnit.milli_meter_squared)

    q41 = Area(value=1.0, unit=AreaUnit.meter_squared)
    q42 = Area(value=1.0, unit=AreaUnit.milli_meter_squared)
    # 'square_meter' is not a valid unit for pint, but 'square_meter' is
    q43 = q41 + q42
    assert q43 == Area(value=1.000001, unit=AreaUnit.meter_squared)


def test_export():

    q = Length(value=1.0, unit=LengthUnit.milli_meter)

    q_json = json.loads(q.json(exclude_none=True))
    print(q_json)
    assert q_json == {
        "type": ["Category:OSWee9c7e5c343e542cb5a8b4648315902f"],
        "value": 1.0,
        "unit": str(
            "Item:OSWf101d25e944856e3bd4b4c9863db7de2"
            "#OSW322dec469be75aedb008b3ebff29db86"
        ),
    }

    q = Length(value=1.0, unit=LengthUnit.meter)

    q_json = json.loads(q.json(exclude_none=True))
    print(q_json)
    assert q_json == {
        "type": ["Category:OSWee9c7e5c343e542cb5a8b4648315902f"],
        "value": 1.0,
        "unit": "Item:OSWf101d25e944856e3bd4b4c9863db7de2",
    }

    q_json = json.loads(q.json(exclude_none=True, exclude_defaults=True))
    print(q_json)
    assert q_json == {"value": 1.0}

    ln = Length(value=0.1)
    w = Width(value=200, unit=LengthUnit.milli_meter)
    a = ln * w
    print(a)

    json_dict = a.dict()
    print(json_dict)
    assert json_dict["type"] == ["Category:OSW1fcf1694712e5684885071efdf775bd9"]
    assert json_dict["value"] == 20000.0
    assert json_dict["unit"] == (
        "Item:OSWd10e5841c68e5aad94b481b58ef9dfb9"
        "#OSWeca22bf4270853038ef3395bd6dd797b"
    )

    # _a = QuantityValue(**json_dict)

    _a = a.to_base()
    json_dict = _a.dict(exclude_none=True, exclude_defaults=True)
    print(json_dict)
    assert json_dict["value"] == 0.02
    assert len(json_dict.keys()) == 1

    __a = Area(**json_dict)
    assert __a == _a

    # not supported yet
    # jsonld_dict = a.to_jsonld()
    # print(json.dumps(jsonld_dict, indent=2))

    # a2 = QuantityValue.from_jsonld(jsonld_dict)
    # print(a2)


if __name__ == "__main__":
    test_pint()
    test_export()
