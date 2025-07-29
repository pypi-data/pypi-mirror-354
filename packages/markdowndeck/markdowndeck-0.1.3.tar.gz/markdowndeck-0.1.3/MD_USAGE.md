# MarkdownDeck Usage Guide

Welcome to MarkdownDeck! This guide explains how to use our special flavor of Markdown to create beautiful and complex Google Slides presentations with ease.

## Core Concepts

### Slides

Slides are the fundamental building blocks of your presentation. You separate one slide from the next using a triple equals sign (`===`) on its own line.

```markdown
# This is Slide 1

# Content for the first slide.

# This is Slide 2

Content for the second slide.
```

### Title, Subtitle, and Footer

- **Title**: The first H1 heading (`#`) on a slide is treated as its title.
- **Subtitle**: An H2 heading (`##`) immediately following the title is treated as the slide's subtitle.
- **Footer**: Content placed after a triple at-sign (`@@@`) separator at the end of a slide becomes the slide's footer.

```markdown
# My Awesome Presentation

## A deep dive into cool things

This is the main content.

@@@
© 2024 My Company | Confidential
```

### Speaker Notes

You can add speaker notes anywhere on a slide using an HTML comment.

```markdown
<!-- notes: Remember to mention the Q3 results here. -->
```

### Sections: The Building Blocks of Layout

Within a single slide, you can structure your content into sections. Sections are the primary way to control layout.

- **Vertical Sections**: Use a triple dash (`---`) to split content into vertical sections that stack on top of each other.
- **Horizontal Sections (Columns)**: Use a triple asterisk (`***`) to split content within a vertical section into horizontal columns.

```markdown
## Two Vertical Sections

## Top content area.

Bottom content area.

===

## Three Horizontal Columns

[width=1/3]
Left Column

---

[width=1/3]
Middle Column

---

[width=1/3]
Right Column
```

## Directives: The Core of Control

Directives are the most powerful feature of MarkdownDeck. They allow you to control the layout, spacing, and styling of your content. A directive is a key-value pair enclosed in square brackets: `[key=value]`.

### Directive Scoping: Where do they apply?

Understanding where a directive applies is key. MarkdownDeck has three simple, hierarchical rules:

#### 1. Element-Scoped Directives (Same-Line)

A directive placed on the **same line** as an element applies **only to that element**. This is the most specific way to target something.

````markdown
# My Title [color=blue]

![An image](url.png) [border=2pt solid red]```

#### 2. Section-Scoped Directives (Own-Line)

A directive placed on its **own line** applies to the **smallest section that contains it**.

```markdown
### This whole section is centered

[align=center]
This text is centered.
And this text is also centered.

---

### This section is not

This text is left-aligned by default.
```
````

This is powerful for layouts. To style a specific column, place the directive inside it:

```markdown
Left Column

---

[background=#f0f0f0]
This column has a gray background.
```

#### 3. List Item-Scoped Directives

A directive on its **own line immediately before a list item** applies **only to that list item** and any of its nested children.

```markdown
- First item (default style).
  [color=red]
- Second item (this will be red).
  - Nested item (also red).
- Third item (default style).
```

### Directive Reference

| Directive       | Description                                   | Example                                        |
| :-------------- | :-------------------------------------------- | :--------------------------------------------- |
| **Sizing**      |                                               |                                                |
| `width`         | Sets width. Accepts `px`, `%`, or fractions.  | `[width=50%]` `[width=300]` `[width=1/2]`      |
| `height`        | Sets height. Accepts `px`, `%`, or fractions. | `[height=100]` `[height=50%]`                  |
| **Alignment**   |                                               |                                                |
| `align`         | Horizontal alignment of content.              | `[align=center]` `[align=right]`               |
| `valign`        | Vertical alignment within a section.          | `[valign=middle]` `[valign=bottom]`            |
| **Spacing**     |                                               |                                                |
| `padding`       | Inner spacing of a section or element.        | `[padding=20]`                                 |
| `margin`        | Outer spacing of an element.                  | `[margin=10]`                                  |
| **Visuals**     |                                               |                                                |
| `background`    | Sets background color or image.               | `[background=#f0f0f0]` `[background=url(...)]` |
| `color`         | Sets text color.                              | `[color=red]` `[color=#333333]`                |
| `border`        | Sets a border around a section or element.    | `[border=2pt dashed blue]`                     |
| `border-radius` | Rounds the corners of a section or element.   | `[border-radius=8]`                            |
| `opacity`       | Sets transparency (0.0 to 1.0).               | `[opacity=0.8]`                                |
| **Typography**  |                                               |                                                |
| `fontsize`      | Sets the font size in points.                 | `[fontsize=24]`                                |
| `font-family`   | Sets the font family.                         | `[font-family="Georgia"]`                      |
| `line-spacing`  | Sets the line spacing multiplier.             | `[line-spacing=1.5]`                           |
| **Tables**      |                                               |                                                |
| `column-widths` | Sets explicit widths for table columns.       | `[column-widths=100,200,50]`                   |
| `cell-align`    | Sets alignment for cells in a range.          | `[cell-align=right]`                           |

---
