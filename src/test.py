import unittest
import os
import json
import asyncio
from schema import make_schema



class TestMakeSchema(unittest.TestCase):
    def setUp(self):
        self.test_data = {
                "name": "John",
                "age": 30,
                "city": "New York",
                "friends": ["Jane"],
                "address": {
                    "street": "Main Street",
                },
                "alive": True,
                "weight": 80.5,
            }
        
        self.test_file = "test_data.json"
        with open(self.test_file, "w") as f:
            json.dump(self.test_data, f,indent=2)

    def tearDown(self):
        os.remove(self.test_file)
        os.remove("test_schema.json")

    def test_make_schema(self):
        asyncio.run(
            make_schema(
                source=self.test_file,
                depth=-1,
                select_attr=None,
                target="test_schema.json",
                skip=True,
            )
        )

        with open("test_schema.json", "r") as f:
            schema_data = json.load(f)
            # schema_data = schema_data[0]
        self.assertEqual(schema_data["key_one"]["tag"], "name")
        self.assertEqual(schema_data["key_one"]["type"], "STRING")
        self.assertEqual(schema_data["key_two"]["tag"], "age")
        self.assertEqual(schema_data["key_two"]["type"], "INTEGER")
        self.assertEqual(schema_data["key_three"]["tag"], "city")
        self.assertEqual(schema_data["key_three"]["type"], "STRING")
        self.assertEqual(schema_data["key_four"]["tag"], "friends")
        self.assertEqual(schema_data["key_four"]["type"], "ENUM")
        self.assertEqual(schema_data["key_five"]["tag"], "0")
        self.assertEqual(schema_data["key_five"]["type"], "STRING")
        self.assertEqual(schema_data["key_six"]["tag"], "address")
        self.assertEqual(schema_data["key_six"]["type"], "ARRAY")
        self.assertEqual(schema_data["key_seven"]["tag"], "street")
        self.assertEqual(schema_data["key_seven"]["type"], "STRING")
        self.assertEqual(schema_data["key_eight"]["tag"], "alive")
        self.assertEqual(schema_data["key_eight"]["type"], "BOOLEAN")
        self.assertEqual(schema_data["key_nine"]["tag"], "weight")
        self.assertEqual(schema_data["key_nine"]["type"], "INTEGER")

    def test_make_schema_with_select_attr(self):
        asyncio.run(
            make_schema(
                source=self.test_file,
                depth=-1,
                select_attr="address",
                target="test_schema.json",
            )
        )
        with open("test_schema.json", "r") as f:
            schema_data = json.load(f)
            # schema_data = schema_data[0]
        self.assertEqual(schema_data["key_one"]["tag"], "street")
        self.assertEqual(schema_data["key_one"]["type"], "STRING")

    def test_make_schema_with_depth(self):
        asyncio.run(
            make_schema(
                source=self.test_file,
                depth=2,
                select_attr=None,
                target="test_schema.json",
            )
        )
        with open("test_schema.json", "r") as f:
            schema_data = json.load(f)
            # schema_data = schema_data[0]
        self.assertEqual(schema_data["key_one"]["tag"], "name")
        self.assertEqual(schema_data["key_one"]["type"], "STRING")
        self.assertEqual(schema_data["key_two"]["tag"], "age")
        self.assertEqual(schema_data["key_two"]["type"], "INTEGER")
        self.assertEqual(schema_data["key_three"]["tag"], "city")
        self.assertEqual(schema_data["key_three"]["type"], "STRING")
        self.assertEqual(schema_data["key_four"]["tag"], "friends")
        self.assertEqual(schema_data["key_four"]["type"], "ENUM")
        self.assertEqual(schema_data["key_five"]["tag"], "address")
        self.assertEqual(schema_data["key_five"]["type"], "ARRAY")
        self.assertEqual(schema_data["key_six"]["tag"], "alive")
        self.assertEqual(schema_data["key_six"]["type"], "BOOLEAN")
        self.assertEqual(schema_data["key_seven"]["tag"], "weight")
        self.assertEqual(schema_data["key_seven"]["type"], "INTEGER")

if __name__ == "__main__":
    unittest.main()
