from django.urls import reverse

from wagtail.test.utils.form_data import (
    nested_form_data,
    rich_text,
    streamfield,
)

import pytest
from pytest_django.asserts import assertContains

from .models import StandardPage


@pytest.mark.django_db
def test_hero_block_preview(admin_client, root_page):
    add_url = reverse(
        "wagtailadmin_pages:add",
        args=("tests", "standardpage", root_page.id),
    )

    form_data = nested_form_data(
        {
            "title": "A page",
            "body": streamfield(
                [
                    (
                        "hero_block",
                        {
                            "style": "centered",
                            "blocks": streamfield(
                                [
                                    (
                                        "paragraph_block",
                                        rich_text("<p>Lorem ipsum</p>"),
                                    ),
                                ]
                            ),
                        },
                    ),
                ]
            ),
        }
    )
    form_data["slug"] = "a-page"
    response = admin_client.post(add_url, data=form_data)
    assert response.status_code == 302

    page = StandardPage.objects.get(slug="a-page")
    preview_url = reverse("wagtailadmin_pages:view_draft", args=(page.id,))

    response = admin_client.get(preview_url)
    assert response.status_code == 200
    assertContains(response, "hero-centered")
    assertContains(response, "Lorem ipsum")


@pytest.mark.django_db
def test_link_target_block_media(admin_client, root_page):
    add_url = reverse(
        "wagtailadmin_pages:add",
        args=("tests", "standardpage", root_page.id),
    )
    content = str(admin_client.get(add_url).content)
    assert "wagtail_cblocks/admin/css/link-target-block.css" in content
    assert "wagtail_cblocks/admin/js/link-target-block.js" in content
