# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

## 0.5.2 - 2025-06-11
### Fixed
- Set empty dict when block's value to migrate with `MergeLinkBlockOperation`
  is empty

## 0.5.1 - 2024-08-09
### Fixed
- Update `LinkTargetBlock` JavaScript code to support Wagtail >=6.1

## 0.5.0 - 2024-06-05
### Changed
- **Breaking:** Merge `LinkBlock` to `LinkTargetBlock` and change it to a
  `StructBlock`.

  A migration operation is provided to migrate your current blocks and prevent
  data loss but you will have to apply it manually:
  1. Switch to this new `wagtail_cblocks` version
  2. Update your code to use `LinkTargetBlock` instead of `LinkBlock`
  3. Create migration(s) for you app(s) - it will update `Streamfield` blocks
  4. Edit this new migration file
  5. Add the following imports at the top:
     ```python
     from wagtail.blocks.migrations.migrate_operation import MigrateStreamData
     from wagtail_cblocks.blocks.migrations.operations import MergeLinkBlockOperation
     ```
  6. Use the `MergeLinkBlockOperation` to migrate all of your `StreamField` which
     are impacted - i.e. which have a `LinkBlock` somewhere - as described in the
     [Wagtail's documentation](https://docs.wagtail.org/en/latest/advanced_topics/streamfield_migrations.html#basic-usage).
     Note that the block path must be the full path of the `LinkBlock`, for
     example:
     ```python
     operations = [
         MigrateStreamData(
             app_name="myapp",
             model_name="contentpage",
             field_name="body",
             operations_and_block_paths=[
                 (
                     MergeLinkBlockOperation(),
                     "button_block.link",
                 ),
                 (
                     MergeLinkBlockOperation(),
                     "image_block.link",
                 ),
                 (
                     MergeLinkBlockOperation(),
                     "columns_block.columns.button_block.link",
                 ),
                 (
                     MergeLinkBlockOperation(),
                     "columns_block.columns.image_block.link",
                 ),
             ],
         ),
         # …
     ]
     ```

## 0.4.2 - 2024-05-23
### Changed
- Require Django >=4.2 and Wagtail >=5.2

## 0.4.1 - 2023-05-04

This release only removes the Wagtail's maximum supported version to prevent
conflicting dependencies.

## 0.4.0 - 2023-04-02
### Changed
- Drop support for Wagtail < 4.1 LTS

### Fixed
- Update CSS tweaks in the admin for `LinkBlock` and remove `ColumnsBlock` ones
- Remove the help icon from the admin form of `LinkBlock` to fit default rendering

## 0.3.5 - 2022-12-30
### Fixed
- Do not generate a label from the name for `LinkBlock` and define a template to
  render this block in the admin without an empty label

## 0.3.4 - 2022-10-27

This release only adds Wagtail 4.0 to supported versions.

## 0.3.3 - 2022-05-17

This release only adds Wagtail 3.0 to supported versions due to a versioning
scheme change.

## 0.3.2 - 2022-03-31
### Changed
- Collapse `ColumnsBlock.columns` by default

## 0.3.1 - 2021-10-04
### Fixed
- Format the value for and from forms in stylized blocks to fix the page preview

## 0.3.0 - 2021-08-17
### Added
- CSSClassMixin to define CSS classes of a block at initialization or in its
  meta through `css_class`
- StylizedStructBlock to define an element with different styles in a generic
  way at initialization or in its properties through `styles`

### Changed
- Ease ColumnsBlock subclassing by searching for the sub-block's definition of
  a column in `Meta.column_block`
- Inherit ButtonBlock from StylizedStructBlock to accept optional styles
- Move the columns definition at first in ColumnsBlock
- Always define the `target` block of a LinkBlock

## 0.2.1 - 2021-03-11
### Changed
- Improve Makefile documentation and targets with release facilities

## 0.2.0 - 2021-03-10
### Added
- ColumnsBlock with optional horizontal alignment
- Factories for HeadingBlock and ParagraphBlock to ease tests using
  [wagtail-factories](https://pypi.org/project/wagtail-factories/)

### Changed
- Display image in a centered block in the default template

## 0.1.0 - 2021-03-05
### Added
- HeadingBlock, ParagraphBlock, ButtonBlock and ImageBlock blocks with
  Bootstrap 5 templates
- French translations
