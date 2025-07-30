import pytest

from wagtail_cblocks.blocks.migrations.operations import MergeLinkBlockOperation


class TestMergeLinkBlockOperation:
    def test_init(self):
        operation = MergeLinkBlockOperation()
        assert operation.operation_name_fragment == "merge_link_block"

    @pytest.mark.parametrize("value", [{}, {"target": []}])
    def test_no_value(self, value):
        operation = MergeLinkBlockOperation()
        assert operation.apply(value) == {}

    def test_migrate(self):
        operation = MergeLinkBlockOperation()
        assert operation.apply(
            {
                "target": [
                    {
                        "type": "anchor",
                        "value": "#pouet",
                        "id": "34a9cf54-3b56-4d10-8f8a-172ca33f57b3",
                    }
                ],
            }
        ) == {
            "type": "anchor",
            "anchor": "#pouet",
        }
