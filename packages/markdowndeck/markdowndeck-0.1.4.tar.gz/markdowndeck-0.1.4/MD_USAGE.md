# **MarkdownDeck Usage Documentation & Style Guide**

**Version:** 1.0
**Audience:** Developers and LLM Agents
**Purpose:** To provide a precise, rule-based guide for creating presentations using the MarkdownDeck system.

## **1. Core Philosophy: The Blank Canvas**

Before you begin, you must understand the core principle of MarkdownDeck: **You are in complete control.**

- **Blank Canvas First:** Every slide is created from a `BLANK` layout. There are no pre-existing themes, templates, or placeholders to inherit from.
- **Explicit is Better Than Implicit:** The system does not guess your intentions. All layout, spacing, and styling are controlled by you through Markdown structure and directives. If you don't specify spacing, there will be no spacing.
- **Structure Defines Layout:** The way you structure your Markdown with separators (`---`, `***`) directly translates to the layout hierarchy (stacks, columns).
- **Directives are Your Tools:** You control the final appearance using `[key=value]` directives. Mastering them is essential.

## **2. The Anatomy of a Presentation**

A presentation is a single text file. Slides are separated by `===`.

```markdown
# My First Slide

Content for the first slide.

===

# My Second Slide

Content for the second slide.
```

## **3. Slide Meta-Elements**

These are the special, top-level components of a slide. They must appear in this order.

- **Title (`#`)**: **Must be the first line** of a slide's content. Only the first `H1` is treated as the slide title.
  ```markdown
  # This is the Slide Title
  ```
- **Subtitle (`##`)**: **Must immediately follow the title line** (can be separated by blank lines).
  ```markdown
  # Slide Title

  ## This is the subtitle
  ```
- **Speaker Notes (`<!-- notes: ... -->`)**: Can be placed anywhere. The content inside will be added as speaker notes.
  ```markdown
  <!-- notes: Remember to talk about Q4 financial projections here. -->
  ```
- **Footer (`@@@`)**: All content after the `@@@` separator at the end of a slide is treated as footer text.

  ```markdown
  ## Content...

  More content...

  @@@
  Company Confidential - © 2025
  ```

## **4. The Layout System: Sections are Everything**

All body content on a slide **must** reside within sections. You cannot place elements directly on the slide. The entire body of the slide is treated as a single **`root_section`**. You then use separators to create a hierarchy of child sections within it.

#### **Vertical Stacks (`---`)**

The `---` separator divides content vertically, creating a stack of sections.

- **Example:** This creates a `root_section` with two child sections stacked one on top of the other.

  ```markdown
  Content for the top section.

  ---

  Content for the bottom section.
  ```

#### **Horizontal Rows (`\***`)\*\*

The `***` separator divides content horizontally, creating a row of columns.

- **Example:** This creates a `root_section` with one child section of `type: "row"`, which in turn contains two columns.

  ```markdown
  Content for the left column.

  ---

  Content for the right column.
  ```

#### **Nesting Layouts**

You can combine separators to create complex layouts.

- **Example:** A two-column layout below a header.

  ```markdown
  This is my header content, it spans the full width.

  ---

  [gap=20]
  This is the left column.

  ---

  This is the right column.
  ```

  - **How it Works:** The `---` creates a new vertical section for the columns. The `[gap=20]` directive applies to this new section. The `***` inside it creates two children (the columns), and the `gap` directive places 20 points of space between them.

## **5. Directives: The Control System**

Directives are how you control everything from size and position to color and font.

#### **A. Directive Syntax**

- **Basic:** `[key=value]`
- **Multiple:** `[key1=value1 key2=value2]`
- **No Spaces:** No spaces are allowed around the `=`. `[key= value]` is invalid.
- **Case-Insensitive Keys:** `[width=50%]` is the same as `[WIDTH=50%]`.

#### **B. The Two Scoping Rules (Most Important Concept)**

You **must** understand these two rules. They determine what your directives apply to.

1.  **The Proximity Rule (For a single Element):**

    - A directive on the **same line** as an element applies **exclusively** to that element.
    - **Use this for:** Styling a single line of text, an image, or a list item.
    - **Example:**
      ```markdown
      # This is a Blue Title [color=blue]

      ![An image with a border](url.png) [border=2pt solid black]

      - A red list item [color=red]
      ```

2.  **The Containment Rule (For a Section):**
    - A directive on its **own line** applies to the **smallest `Section` that contains it**.
    - **Use this for:** Layout control (`width`, `height`, `gap`), background colors, and default text styles for a whole block.
    - **Example:**
      ```markdown
      [background=#f0f0f0 width=60% align=center]
      This entire block of text will have a light gray background,
      be centered, and take up 60% of the available width.
      ```

#### **C. The Buffer Pattern (Advanced)**

To style only one section without affecting its siblings, create an empty "buffer" section using consecutive separators.

- **Example: Style only the top section**

  ```markdown
  [background=red]
  This text is on a red background.

  ---

  This text has a normal background. It is unaffected because the
  directive was contained within the first section.
  ```

## **6. Comprehensive Directive Reference**

#### **Sizing & Spacing**

| Directive       | Applies To       | Description                                                                                                                                     | Example              | Inherited |
| :-------------- | :--------------- | :---------------------------------------------------------------------------------------------------------------------------------------------- | :------------------- | :-------- |
| `width`         | Section, Element | **On a Section, it's an ABSOLUTE size.** **On an Element (Image, Table), it's a PREFERRED size** that will be scaled down to fit its container. | `[width=50%]`        | No        |
| `height`        | Section, Element | Same as `width`. On a Section, it can cause content to overflow, which is expected.                                                             | `[height=300pt]`     | No        |
| `padding`       | Section          | Inner spacing. Values: `top,right,bottom,left`.                                                                                                 | `[padding=20]`       | No        |
| `margin-top`    | Section          | Outer spacing on top.                                                                                                                           | `[margin-top=10]`    | No        |
| `margin-bottom` | Section          | Outer spacing on bottom.                                                                                                                        | `[margin-bottom=10]` | No        |
| `gap`           | Section          | Spacing **between direct children** of a section.                                                                                               | `[gap=20]`           | **No**    |

#### **Alignment**

| Directive | Applies To       | Description                                                                    | Example           | Inherited |
| :-------- | :--------------- | :----------------------------------------------------------------------------- | :---------------- | :-------- |
| `align`   | Section, Element | Horizontal alignment (`left`, `center`, `right`).                              | `[align=center]`  | Yes       |
| `valign`  | Section          | Vertical alignment (`top`, `middle`, `bottom`) of children within the section. | `[valign=middle]` | Yes       |

#### **Visuals & Typography**

| Directive     | Applies To       | Description                                         | Example                           | Inherited |
| :------------ | :--------------- | :-------------------------------------------------- | :-------------------------------- | :-------- |
| `background`  | Section          | Sets background color.                              | `[background=#eeeeee]`            | No        |
| `color`       | Section, Element | Sets text color.                                    | `[color=blue]`                    | Yes       |
| `fontsize`    | Section, Element | Sets font size in points.                           | `[fontsize=18]`                   | Yes       |
| `font-family` | Section, Element | Sets font family. Use quotes for names with spaces. | `[font-family="Times New Roman"]` | Yes       |
| `bold`        | Section, Element | Makes text bold.                                    | `[bold]`                          | Yes       |
| `italic`      | Section, Element | Makes text italic.                                  | `[italic]`                        | Yes       |
| `border`      | Section, Element | Adds a border.                                      | `[border=1pt solid #ccc]`         | No        |

## **7. What Not to Do: Common Pitfalls**

Avoiding these common errors will ensure your slides render as expected.

- **DO NOT assume default spacing.**

  - **Wrong:** Putting two paragraphs on separate lines and expecting space between them.
  - **Right:** Wrap the paragraphs in a section and add a `gap` directive: `[gap=15]\nParagraph 1\n\nParagraph 2`.

- **DO NOT use unsupported Markdown.**

  - Blockquotes (`> text`) are not supported and will be rendered as plain text.
  - Horizontal rules (`---` on its own) are reserved for section splitting.

- **DO NOT place directives after the content they are meant to style.**

  - **Wrong:** `Some Text\n[align=center]`
  - **Right:** `[align=center]\nSome Text`

- **DO NOT style code blocks on the fence line.**
  - **Wrong:** ` ```python [background=gray] `
  - **Right:** Wrap the code block in a `Section` with a directive: `[background=gray]\n\`\`\`python\n...`

## **8. Cheatsheet & Advanced Example**

#### **Quick Reference**

| Syntax        | Purpose                            |
| :------------ | :--------------------------------- |
| `===`         | New Slide                          |
| `# Title`     | Slide Title (must be first line)   |
| `## Subtitle` | Slide Subtitle (must follow title) |
| `---`         | Vertical Section (Stack)           |
| `***`         | Horizontal Section (Row/Columns)   |
| `[key=value]` | Control layout and styling         |
| `@@@`         | Footer Content                     |

#### **Advanced Layout: Image Next to Text**

This example creates a common, powerful layout.

```markdown
# Image and Text Layout

This is a header that sits above the two-column layout.

---

[gap=30]

[width=40%]
![An image of a mountain lake](https://source.unsplash.com/random/800x600?lake)

---

[width=60%]

## Data Analysis

- This column contains text content.
- It is wider than the image column.
- The `gap` directive on the parent section creates space between this column and the image.

This layout is achieved by combining vertical and horizontal separators with `width` and `gap` directives.
```
