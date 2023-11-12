import pytest

from randonneur import migrate_exchanges


@pytest.fixture
def generic():
    return [
        {
            "name": "n",
            "reference product": "rp",
            "unit": "u",
            "location": "l",
            "exchanges": [
                {"name": "babur"},
                {
                    "name": "akbar",
                    "amount": 10,
                },
                {
                    "name": "shah jahan",
                    "amount": 10,
                },
                {
                    "name": "azam shah",
                    "amount": 100,
                },
            ],
        }
    ]


@pytest.fixture
def migrate_all():
    return {
        "delete": [{"name": "babur"}],
        "create-exchanges": [
            {
                "dataset": {"name": "n"},
                "source": {"name": "humayun"},
            }
        ],
        "replace": [
            {
                "source": {"name": "akbar"},
                "target": {"name": "jahangir", "allocation": 0.5},
            }
        ],
        "update": [
            {
                "source": {"name": "shah jahan"},
                "target": {"name": "alamgir"},
            }
        ],
        "disaggregate": [
            {
                "source": {"name": "azam shah"},
                "targets": [
                    {"name": "bahadur shah", "allocation": 0.25},
                    {"name": "jahandar shah", "allocation": 0.75},
                ],
            }
        ],
    }


def test_migrate_exchanges_integration(generic, migrate_all):
    expected = [
        {
            "name": "n",
            "reference product": "rp",
            "unit": "u",
            "location": "l",
            "exchanges": [
                {
                    "name": "alamgir",
                    "amount": 10,
                },
                {"name": "humayun"},
                {
                    "name": "jahangir",
                    "amount": 5,
                },
                {
                    "name": "bahadur shah",
                    "amount": 25,
                },
                {
                    "name": "jahandar shah",
                    "amount": 75,
                },
            ],
        }
    ]
    result = migrate_exchanges(migrate_all, generic)
    assert result == expected

def test_empty_transformation(generic):
    mapper = {
        
    }

    expected = [
        {
            "name": "n",
            "reference product": "rp",
            "unit": "u",
            "location": "l",
            "exchanges": [
                {
                    "name": "babur"
                },
                {
                    "name": "akbar",
                    "amount": 10,
                },
                {
                    "name": "shah jahan",
                    "amount": 10,
                },
                {
                    "name": "azam shah",
                    "amount": 100,
                },
            ],
        }
    ]
    result = migrate_exchanges(mapper, generic)
    assert result == expected

def test_disaggregate(generic):
    mapper = {
        "disaggregate": [
            {
                "source": {"name": "azam shah"},
                "targets": [
                    {"name": "bahadur shah", "allocation": 0.25},
                    {"name": "jahandar shah", "allocation": 0.75},
                ],
            }
        ],
    }

    expected = [
        {
            "name": "n",
            "reference product": "rp",
            "unit": "u",
            "location": "l",
            "exchanges": [
                {
                    "name": "babur"
                },
                {
                    "name": "akbar",
                    "amount": 10,
                },
                {
                    "name": "shah jahan",
                    "amount": 10,
                },
                {
                    "name": "bahadur shah",
                    "amount": 25,
                },
                {
                    "name": "jahandar shah",
                    "amount": 75,
                },
            ],
        }
    ]
    result = migrate_exchanges(mapper, generic)
    assert result == expected

def test_update(generic):
    mapper = {
        "update": [
            {
                "source": {"name": "shah jahan"},
                "target": {"name": "alamgir"},
            }
        ],
    }

    expected = [
        {
            "name": "n",
            "reference product": "rp",
            "unit": "u",
            "location": "l",
            "exchanges": [
                {
                    "name": "babur"
                },
                {
                    "name": "akbar",
                    "amount": 10,
                },
                {
                    "name": "alamgir",
                    "amount": 10,
                },
                {
                    "name": "azam shah",
                    "amount": 100,
                },
            ],
        }
    ]
    result = migrate_exchanges(mapper, generic)
    assert result == expected

def test_replace(generic):
    mapper = {
        "replace": [
            {
                "source": {"name": "akbar"},
                "target": {"name": "jahangir", "allocation": 0.5},
            }
        ],
    }

    expected = [
        {
            "name": "n",
            "reference product": "rp",
            "unit": "u",
            "location": "l",
            "exchanges": [
                {
                    "name": "babur"
                },
                {
                    "name": "shah jahan",
                    "amount": 10,
                },
                {
                    "name": "azam shah",
                    "amount": 100,
                },
                {
                    "name": "jahangir",
                    "amount": 5,
                },
            ],
        }
    ]
    result = migrate_exchanges(mapper, generic)
    assert result == expected

def test_create_exchanges(generic):
    mapper = {
        "create-exchanges": [
            {
                "dataset": {"name": "n"},
                "source": {"name": "humayun"},
            }
        ]
    }

    expected = [
        {
            "name": "n",
            "reference product": "rp",
            "unit": "u",
            "location": "l",
            "exchanges": [
                {
                    "name": "babur"
                },
                {
                    "name": "akbar",
                    "amount": 10,
                },
                {
                    "name": "shah jahan",
                    "amount": 10,
                },
                {
                    "name": "azam shah",
                    "amount": 100,
                },
                {
                    "name": "humayun"
                },
            ],
        }
    ]
    result = migrate_exchanges(mapper, generic)
    assert result == expected

def test_delete(generic):
    mapper = {
        "delete": [{"name": "babur"}],
    }

    expected = [
        {
            "name": "n",
            "reference product": "rp",
            "unit": "u",
            "location": "l",
            "exchanges": [
                {
                    "name": "akbar",
                    "amount": 10,
                },
                {
                    "name": "shah jahan",
                    "amount": 10,
                },
                {
                    "name": "azam shah",
                    "amount": 100,
                },
            ],
        }
    ]
    result = migrate_exchanges(mapper, generic)
    assert result == expected