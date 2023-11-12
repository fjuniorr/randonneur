from pprint import pprint
from deepdiff import DeepDiff
from randonneur import migrate_datasets, migrate_exchanges

def test_migrate_exchanges_dataset_filter():
    
    generic = [
        {
            "name": "n1",
            "reference product": "rp1",
            "location": "l1",
            "unit": "u1",
            "foo": "foo1",
            "exchanges": [
                {
                    "name": "akbar",
                    "amount": 10,
                },
                {
                    "name": "akbar",
                    "amount": 30,
                },
            ],
        },
        {
            "name": "n2",
            "reference product": "rp2",
            "location": "l2",
            "unit": "u2",
            "foo": "foo2",
            "exchanges": [
                {
                    "name": "akbar",
                    "amount": 20,
                },
            ],
        },
    ]
    
    update = {
        "update": [
            {
                "source": {"name": "akbar"},
                "target": {"name": "new_name"},
            },
            ]
    }
    
    expected = [
        {
            "name": "n1",
            "reference product": "rp1",
            "location": "l1",
            "unit": "u1",
            "foo": "foo1",
            "exchanges": [
                {
                    "name": "new_name",
                    "amount": 10,
                },
                {
                    "name": "new_name",
                    "amount": 30,
                },
            ],
        },
        {
            "name": "n2",
            "reference product": "rp2",
            "location": "l2",
            "unit": "u2",
            "foo": "foo2",
            "exchanges": [
                {
                    "name": "akbar",
                    "amount": 20,
                },
            ],
        },
    ]
    
    actual = migrate_exchanges(update, generic, dataset_filter=lambda x: x['name'] == 'n1')
    diff = DeepDiff(actual, expected, ignore_order=True)
    assert not diff