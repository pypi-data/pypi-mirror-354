from django.core.exceptions import ImproperlyConfigured

from wagtail.blocks.struct_block import StructBlockValidationError

import pytest
from bs4 import BeautifulSoup
from pytest_django.asserts import assertHTMLEqual
from wagtail_factories import DocumentFactory, ImageFactory, PageFactory

from wagtail_cblocks import blocks
from wagtail_cblocks.blocks import (
    CSSClassMixin,
    LinkTargetBlockAdapter,
    Style,
    StylizedStructBlock,
)

from .models import BaseBlock, ColumnsBlock, RowColumnsBlock


class BlockTest:
    def render(self, data, block=None):
        if block is None:
            block = self.block
        return block.render(block.to_python(data))

    def render_html(self, *args, **kwargs):
        return BeautifulSoup(self.render(*args, **kwargs), "html.parser")


class TestCSSClassMixin:
    class Block(CSSClassMixin, blocks.ParagraphBlock):
        pass

    def test_in_meta(self):
        class Block(self.Block):
            class Meta:
                css_class = "lead"

        block = Block()
        context = block.get_context(block.to_python("<p>Paragraph</p>"))
        assert context["css_class"] == "lead"

    @pytest.mark.parametrize("value", ("lead", {"lead"}, ["lead"]))
    def test_at_init(self, value):
        block = self.Block(css_class=value)
        context = block.get_context(block.to_python("<p>Paragraph</p>"))
        assert context["css_class"] == "lead"

    def test_empty(self):
        block = self.Block()
        context = block.get_context(block.to_python("<p>Paragraph</p>"))
        assert context["css_class"] == ""


class TestStylizedStructBlock:
    STYLES = [
        Style("foo", "Foo", "is-foo"),
        Style("bar", "Bar", "is-bar"),
    ]

    def test_empty_styles(self):
        block = StylizedStructBlock()
        assert "style" not in block.child_blocks
        context = block.get_context(block.to_python({}))
        assert context["css_class"] == ""

    def test_styles_from_property(self):
        class Block(StylizedStructBlock):
            styles = self.STYLES

        value = Block().to_python({"style": "foo"})
        assert value.get("style").name == "foo"

    def test_style(self):
        block = StylizedStructBlock(styles=self.STYLES)
        value = block.to_python({"style": "foo"})
        assert block.get_prep_value(value) == {"style": "foo"}
        assert isinstance(value["style"], Style)
        assert value["style"].name == "foo"
        context = block.get_context(value)
        assert context["css_class"] == "is-foo"

    def test_style_with_css_class(self):
        block = StylizedStructBlock(styles=self.STYLES, css_class="block")
        context = block.get_context(block.to_python({"style": "foo"}))
        assert context["css_class"] == "block is-foo"

    def test_default_style(self):
        block = StylizedStructBlock(styles=self.STYLES, default_style="bar")
        value = block.to_python({})
        assert isinstance(value.get("style"), Style)
        assert value.get("style").name == "bar"
        context = block.get_context(value)
        assert context["css_class"] == "is-bar"

    def test_default_style_object(self):
        block = StylizedStructBlock(
            styles=self.STYLES, default_style=self.STYLES[1]
        )
        value = block.to_python({})
        assert isinstance(value.get("style"), Style)
        assert value.get("style").name == "bar"

    def test_unknown_style(self):
        block = StylizedStructBlock(styles=self.STYLES, default_style="bar")
        value = block.to_python({"style": "baz"})
        assert value.get("style") is None
        context = block.get_context(value)
        assert context["css_class"] == ""


class TestHeadingBlock(BlockTest):
    block = blocks.HeadingBlock()

    def test_render(self):
        assertHTMLEqual(
            self.render({"text": "Un titre !", "level": 2}),
            '<h2 id="un-titre">Un titre !</h2>',
        )


class TestParagraphBlock(BlockTest):
    block = blocks.ParagraphBlock()

    def test_features(self):
        assert self.block.features == blocks.ParagraphBlock.features

        block = blocks.ParagraphBlock(features=["bold", "italic"])
        assert block.features == ["bold", "italic"]

    def test_render(self):
        data = "<p><i>Un</i> paragraphe !</p>"
        assertHTMLEqual(self.render(data), data)


@pytest.mark.django_db
class TestLinkTargetBlock:
    block = blocks.LinkTargetBlock()

    def get_value(self, link_type, value):
        return self.block.clean({"type": link_type, link_type: value})

    def test_not_required(self):
        block = blocks.LinkTargetBlock(required=False)
        assert block.required is False
        assert block.clean({}).href == ""

    def test_required(self):
        assert self.block.required is True

        with pytest.raises(StructBlockValidationError) as exc_info:
            self.block.clean({})
        assert exc_info.value.block_errors.keys() == {"type"}

    def test_value_page(self, root_page):
        page = PageFactory(parent=root_page, title="About", slug="about")
        value = self.get_value("page", page.id)
        assert value.href == "/about/"

    def test_clean_page_invalid(self):
        with pytest.raises(StructBlockValidationError) as exc_info:
            self.get_value("page", 1000)
        assert exc_info.value.block_errors.keys() == {"page"}

    def test_value_document(self):
        document = DocumentFactory()
        value = self.get_value("document", document.id)
        assert value.href == document.file.url

    def test_clean_document_invalid(self):
        with pytest.raises(StructBlockValidationError) as exc_info:
            self.get_value("document", 1000)
        assert exc_info.value.block_errors.keys() == {"document"}

    def test_value_image(self):
        image = ImageFactory()
        value = self.get_value("image", image.id)
        assert value.href == image.file.url

    def test_clean_image_invalid(self):
        with pytest.raises(StructBlockValidationError) as exc_info:
            self.get_value("image", 1000)
        assert exc_info.value.block_errors.keys() == {"image"}

    def test_value_external_url(self):
        url = "http://example.org/truc/"
        value = self.get_value("url", url)
        assert value.href == url

    def test_value_anchor(self):
        anchor = "#truc"
        value = self.get_value("anchor", anchor)
        assert value.href == anchor

    def test_clean_no_value(self):
        with pytest.raises(StructBlockValidationError) as exc_info:
            self.block.clean({"type": "page"})
        assert exc_info.value.block_errors.keys() == {"page"}

    def test_adapter(self):
        block = blocks.LinkTargetBlock()
        block.set_name("test_linkblock")

        js_args = LinkTargetBlockAdapter().js_args(block)
        assert js_args[0] == "test_linkblock"
        assert js_args[2]["required"] is True
        assert js_args[2]["blockTypes"] == [
            "page",
            "document",
            "image",
            "url",
            "anchor",
        ]
        assert "formTemplate" in js_args[2]


class TestButtonBlock(BlockTest):
    block = blocks.ButtonBlock()

    def test_render_link(self):
        url = "http://example.org/truc/"
        assertHTMLEqual(
            self.render(
                {
                    "text": "Lien",
                    "link": {"type": "url", "url": url},
                }
            ),
            f'<a class="btn mb-3" href="{url}">Lien</a>',
        )


@pytest.mark.django_db
class TestImageBlock(BlockTest):
    block = blocks.ImageBlock()

    def test_render(self):
        html = self.render_html(
            {
                "image": ImageFactory().id,
                "caption": "",
                "link": {},
            }
        )
        assert len(html.select("img.figure-img.img-fluid.mb-0")) == 1
        assert not html.select("figcaption")
        assert not html.select("a")

    def test_render_with_caption(self):
        html = self.render_html(
            {
                "image": ImageFactory().id,
                "caption": "Une légende en dessous.",
                "link": {},
            }
        )
        assert html.select_one("figcaption").text == "Une légende en dessous."
        assert not html.select("a")

    def test_render_with_link(self):
        url = "http://example.org/truc/"
        html = self.render_html(
            {
                "image": ImageFactory().id,
                "caption": "",
                "link": {"type": "url", "url": url},
            }
        )
        assert html.select_one("a").attrs["href"] == url
        assert not html.select("figcaption")


class TestColumnsBlock(BlockTest):
    block = blocks.ColumnsBlock(BaseBlock())

    def test_columns_block_order(self):
        assert list(self.block.child_blocks.keys())[0] == "columns"

    def test_render(self):
        url = "http://example.org/truc/"
        data = {
            "columns": [
                [
                    {
                        "type": "button_block",
                        "value": {
                            "text": "Lien",
                            "link": {"type": "url", "url": url},
                            "style": "primary",
                        },
                    },
                    {
                        "type": "paragraph_block",
                        "value": "<p>A first paragraph.</p>",
                    },
                ],
                [
                    {
                        "type": "paragraph_block",
                        "value": "<p>Another paragraph.</p>",
                    },
                ],
            ],
            "horizontal_align": "center",
        }
        assertHTMLEqual(
            self.render(data),
            (
                '<div class="row text-center">'
                '<div class="col-sm">{}{}</div>'
                '<div class="col-sm">{}</div>'
                "</div>"
            ).format(
                f'<a class="btn btn-primary mb-3" href="{url}">Lien</a>',
                "<p>A first paragraph.</p>",
                "<p>Another paragraph.</p>",
            ),
        )

    def test_sublcass_render(self):
        data = {
            "columns": [
                [
                    {
                        "type": "paragraph_block",
                        "value": "<p>A first paragraph.</p>",
                    },
                ],
            ],
            "layout": "auto",
        }
        assertHTMLEqual(
            self.render(data, RowColumnsBlock()),
            (
                '<div class="row row-cols-auto">'
                '<div class="col"><p>A first paragraph.</p></div>'
                "</div>"
            ),
        )

    def test_required_column_block(self):
        with pytest.raises(ImproperlyConfigured):

            class DummyColumnsBlock(ColumnsBlock):
                pass

            DummyColumnsBlock()
