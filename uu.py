import fontforge
import os
import json
import uuid
import shutil

printEnabled = True

def custom_print(*args, **kwargs):
    if printEnabled:
        print(*args, **kwargs)

def load_name_mapping(filename):
    with open(filename, "r") as file:
        return json.load(file)

def update_name_mapping(new_names_mapping):
    name_mapping = load_name_mapping(name_mapping_json_path)
    name_mapping.update(new_names_mapping)
    save_name_mapping(name_mapping, name_mapping_json_path)
    print("Updated name mapping has been saved.")

def save_name_mapping(mapping, path):
    with open(path, "w") as file:
        json.dump(mapping, file, indent=4)

def scale_glyph(glyph):
    target_width = 1024
    target_height = 1024
    bbox = glyph.boundingBox()
    glyph_width = bbox[2] - bbox[0]
    glyph_height = bbox[3] - bbox[1]

    # Calculate scaling factors
    scale_x = target_width / glyph_width if glyph_width != 0 else 1
    scale_y = target_height / glyph_height if glyph_height != 0 else 1
    scale_factor = min(scale_x, scale_y) * 0.87

    # Apply scaling to fit within the target bounding box
    glyph.transform((scale_factor, 0, 0, scale_factor, 0, 0))

    # Get the new bounding box after scaling
    bbox = glyph.boundingBox()
    glyph_width = bbox[2] - bbox[0]
    glyph_height = bbox[3] - bbox[1]

    # Calculate the translation needed to center the glyph
    left_offset = (target_width - glyph_width) / 2
    top_offset = (target_height - glyph_height) / 2
    translate_x = -bbox[0] + left_offset
    translate_y = -bbox[1] + top_offset

    # Apply the translation to center the glyph
    glyph.transform((1, 0, 0, 1, translate_x, translate_y))

    # Set the glyph width and vertical width to the target size
    glyph.width = target_width
    glyph.vwidth = target_height

def createCardHtml(name, code_point):
    code_point_str = str(code_point)  # Ensure code_point is a string
    code_point_int = int(code_point_str, 16)  # Convert to integer with base 16
    return f"""
    <div class="card-client">
        <div class="icon_main">
            <i class="{css_class_additional}_{name} copy_class_js ico_size-sm"></i>
        </div>
        <p class="name-client"> {name}
            <span>#{code_point_str }</span>
        </p>

        <div class="icon_demo_row_cont">
            <div class="icon_demo_row">
                <i class="{css_class_additional} copy_symbol_js ico_size-xs">&#x{format(code_point_int, "X")};</i>
                <i class="{css_class_additional}_{name} copy_class_js ico_size-sm"></i>
                <i class="{css_class_additional}_{name} copy_class_js ico_size-md"></i>
                <i class="{css_class_additional}_{name} copy_class_js ico_size-lg"></i>
                <i class="{css_class_additional}_{name} copy_class_js ico_size-xl"></i>
            </div>
        </div>

        <div class="btn_demo_row">
            <button class='btn_demo copy_class_btn_js'>copy class</button>
        </div>
    </div>
    """

# Config for Paths and Names
source_folder = "src"
icons_folder = "icons"
source_blank_font = "icon_font.ttf"

src_icons_path = os.path.join(source_folder, icons_folder)
font = fontforge.open(os.path.join(source_folder, source_blank_font))
css_class_prefix = "dynamic_icon"
font_file_name = "menu_icons_font"
font_family_name = "iconsDinamicMenu"
css_class_additional = "cw_icon"
ico_preview_size = "24"
files = os.listdir(src_icons_path)
name_mapping_json_path = os.path.join(source_folder, "name_mapping.json")
starter_ttf_font_path = os.path.join(source_folder, source_blank_font)

name_mapping = load_name_mapping(name_mapping_json_path)
new_names_mapping = {}
filesArray = []

html_content = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
    <link rel="stylesheet" href="styles.css" />
    <style>
* {
        box-sizing: border-box;
      }
      html,
      body {
        margin: 0;
        padding: 0;
      }
      .icons_container {
        display: flex;
        flex-wrap: wrap;
        /* grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); */
        justify-content: center;
        align-items: center;
        column-gap: 24px;
        row-gap: 24px;
        padding: 16px;
        background: var(--bodyBg);
      }

      .icon_demo {
        display: flex;
        flex-direction: column;
        align-items: center;
        background: var(--bodyBg2);
        border: 1px solid var(--bodyBg3);
        row-gap: 6px;
        border-radius: 12px;
        padding: 12px;
        transition: all 0.3s;
        cursor: pointer;
        overflow: hidden;
      }

      .card-client {
        background: #2cb5a0;
        width: 13rem;
        padding-top: 25px;
        padding-bottom: 25px;
        padding-left: 20px;
        padding-right: 20px;
        border: 4px solid #7cdacc;
        box-shadow: 0 6px 10px rgba(207, 212, 222, 1);
        border-radius: 10px;
        text-align: center;
        color: #fff;
        font-family: "Poppins", sans-serif;
        transition: all 0.3s ease;
      }

      .card-client:hover {
        transform: translateY(-10px);
      }

      .icon_main {
        overflow: hidden;
        object-fit: cover;
        width: 5rem;
        height: 5rem;
        border: 4px solid #7cdacc;
        border-radius: 999px;
        display: flex;
        justify-content: center;
        align-items: center;
        margin: auto;
      }

      .icon_main > i {
        fill: currentColor;
        --icoSize: 48px;
      }

      html {
        background: var(--bodyBg);
        color: var(--bodyTxt);
        font-family: Arial;
      }

      .icon_demo_row {
        display: flex;
        align-items: center;
        justify-content: space-between;
      }

      .icon_demo_row_cont {
        margin-bottom: 8px;
      }

      .icon_demo_row_cont::before {
        content: "";
        display: block;
        width: 100%;
        height: 2px;
        margin: 20px 0;
        background: #7cdacc;
      }

      .btn_demo_row {
        display: flex;
        align-items: center;
        column-gap: 16px;
      }

      .btn_demo {
        width: 100%;
        position: relative;
        padding: 10px 22px;
        border-radius: 6px;
        border: none;
        color: #fff;
        cursor: pointer;
        background-color: var(--dominantBg);
        transition: all 0.2s ease;
      }

      .btn_demo:active {
        transform: scale(0.96);
      }

      .btn_demo:before,
      .btn_demo:after {
        position: absolute;
        content: "";
        width: 150%;
        left: 50%;
        height: 100%;
        transform: translateX(-50%);
        z-index: -1000;
        background-repeat: no-repeat;
      }

      .btn_demo:hover:before {
        top: -70%;
        background-image: radial-gradient(
            circle,
            var(--dominantBg) 20%,
            transparent 20%
          ),
          radial-gradient(
            circle,
            transparent 20%,
            var(--dominantBg) 20%,
            transparent 30%
          ),
          radial-gradient(circle, var(--dominantBg) 20%, transparent 20%),
          radial-gradient(circle, var(--dominantBg) 20%, transparent 20%),
          radial-gradient(
            circle,
            transparent 10%,
            var(--dominantBg) 15%,
            transparent 20%
          ),
          radial-gradient(circle, var(--dominantBg) 20%, transparent 20%),
          radial-gradient(circle, var(--dominantBg) 20%, transparent 20%),
          radial-gradient(circle, var(--dominantBg) 20%, transparent 20%),
          radial-gradient(circle, var(--dominantBg) 20%, transparent 20%);
        background-size: 10% 10%, 20% 20%, 15% 15%, 20% 20%, 18% 18%, 10% 10%,
          15% 15%, 10% 10%, 18% 18%;
        background-position: 50% 120%;
        animation: greentopBubbles 0.6s ease;
      }

      @keyframes greentopBubbles {
        0% {
          background-position: 5% 90%, 10% 90%, 10% 90%, 15% 90%, 25% 90%,
            25% 90%, 40% 90%, 55% 90%, 70% 90%;
        }

        50% {
          background-position: 0% 80%, 0% 20%, 10% 40%, 20% 0%, 30% 30%, 22% 50%,
            50% 50%, 65% 20%, 90% 30%;
        }

        100% {
          background-position: 0% 70%, 0% 10%, 10% 30%, 20% -10%, 30% 20%,
            22% 40%, 50% 40%, 65% 10%, 90% 20%;
          background-size: 0% 0%, 0% 0%, 0% 0%, 0% 0%, 0% 0%, 0% 0%;
        }
      }

      .btn_demo:active::after {
        bottom: -70%;
        background-image: radial-gradient(
            circle,
            var(--dominantBg) 20%,
            transparent 20%
          ),
          radial-gradient(circle, var(--dominantBg) 20%, transparent 20%),
          radial-gradient(
            circle,
            transparent 10%,
            var(--dominantBg) 15%,
            transparent 20%
          ),
          radial-gradient(circle, var(--dominantBg) 20%, transparent 20%),
          radial-gradient(circle, var(--dominantBg) 20%, transparent 20%),
          radial-gradient(circle, var(--dominantBg) 20%, transparent 20%),
          radial-gradient(circle, var(--dominantBg) 20%, transparent 20%);
        background-size: 15% 15%, 20% 20%, 18% 18%, 20% 20%, 15% 15%, 20% 20%,
          18% 18%;
        background-position: 50% 0%;
        animation: greenbottomBubbles 0.6s ease;
      }

      @keyframes greenbottomBubbles {
        0% {
          background-position: 10% -10%, 30% 10%, 55% -10%, 70% -10%, 85% -10%,
            70% -10%, 70% 0%;
        }

        50% {
          background-position: 0% 80%, 20% 80%, 45% 60%, 60% 100%, 75% 70%,
            95% 60%, 105% 0%;
        }

        100% {
          background-position: 0% 90%, 20% 90%, 45% 70%, 60% 110%, 75% 80%,
            95% 70%, 110% 10%;
          background-size: 0% 0%, 0% 0%, 0% 0%, 0% 0%, 0% 0%, 0% 0%;
        }
      }

      .message {
        display: none;
        position: fixed;
        bottom: 20px;
        right: 20px;
        background-color: black;
        color: white;
        padding: 10px;
        border-radius: 5px;
      }

  </style>
  </head>
  <body>
    <div class="icons_container">
"""

# Generate CSS content
css_content = f"""
@font-face {{
  font-family: "{font_family_name}";
  src: url("{font_file_name}.eot");
  src: url("{font_file_name}.eot?#iefix") format("embedded-opentype"),
    url("{font_file_name}.woff2") format("woff2"),
    url("{font_file_name}.woff") format("woff"),
    url("{font_file_name}.ttf") format("truetype");
  font-weight: normal;
  font-style: normal;
  font-display: block;
}}

:root{{
  --bodyBg: #e8e8e8;
  --bodyBg2: #141f27;
  --bodyBg3: #445c6f;
  --bodyTxt: rgba(255,255,255,0.9);
  --bodyTxt2: rgba(255,255,255,0.6);
  --dominantBg: #0b293d;
  --dominantBg2: #14496d;
  --dominantBg3: #286a96;
  --dominantTxt: rgba(255,255,255,0.9);
  --dominantTxt2: rgba(255,255,255,0.6);
  --accentBg: #00b6ff;
  --accentBg2: #33454d;
  --accentTxt: rgba(255,255,255,0.9);
  --icoSize: {ico_preview_size}px;
}}

.dynamic_icon {{
  font-family: "iconsDinamicMenu";
  font-size: 46px;
  line-height: 0.8;
}}

.icon_demo:hover {{
}}

.icon_demo > strong {{
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}}
.icon_demo_e {{
    background: var(--dominantBg2);
    border: 1px solid var(--dominantBg3);
    row-gap: 12px;
    border-radius: 12px; 
}}

[class^="{css_class_additional}"],
[class*=" {css_class_additional}"],
.{css_class_additional} {{
  font-family: "{font_family_name}";
  display: inline-block;
  flex-shrink: 0;
  width: var(--icoSize);
  height: var(--icoSize);
    font-size: calc(var(--icoSize) * 2);
  text-align: center;
  vertical-align: middle;
  font-weight: normal;
  font-style: normal;
  speak: none;
  text-decoration: inherit;
  text-transform: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  direction: ltr !important;
  content: "\\E0000";
}}

.ico_size-xs{{
    --icoSize: 16px;
}}
.ico_size-sm{{
    --icoSize: 20px;
}}
.ico_size-md{{
    --icoSize: 24px;
}}
.ico_size-lg{{
    --icoSize: 28px;
}}
.ico_size-xl{{
    --icoSize: 32px;
}}
"""

def transform_name(name):
    # Make the entire name lowercase
    name = name.lower()
    # Replace spaces with underscores
    transformed_name = name.replace(" ", "_")
    return transformed_name

# Process existing glyphs in the font
for code_point in range(0xE000, 0xE7B6):
    glyph_code = "uni" + format(code_point, "04X")
    if glyph_code in font:
        glyph = font[glyph_code]
        if glyph.isWorthOutputting():
            # Perform any additional checks relevant to your context here
            if glyph.foreground.isEmpty():
                glyph.clear()
                custom_print(f"Path does not exist for {code_point}")
            else:
                name = name_mapping.get(str(code_point), code_point)
                html_content += createCardHtml(name, format(code_point, "04X"))
                css_content += f"""
                .{css_class_additional}_{name}::before {{
                    content: "\\{format(code_point, "04X")}";  
                }}
                """
                scale_glyph(glyph)
                last_index = code_point
        else:
            custom_print(f"Does not exist {code_point}")

# Process new files
if last_index is not None:
    start_index = last_index + 1
    for idx, file in enumerate(files, start=start_index):
        if idx >= 0xE7B6:  # Prevent overflow of PUA range
            break
        glyph_code = "uni" + format(idx, "04X")
        code = format(idx, "04X")
        glyph = font.createChar(idx, glyph_code)
        glyph.importOutlines(os.path.join(src_icons_path, file))
        scale_glyph(glyph)

        name = transform_name(os.path.splitext(file)[0])
        html_content += createCardHtml(name, code)
        css_content += f"""
        .{css_class_additional}_{name}::before {{
            content: "\\{format(idx, "04X")}";
        }}"""

        new_names_mapping[idx] = name
else:
    custom_print("No existing glyphs were found in the specified range.")

# Save the updated name mapping
update_name_mapping(new_names_mapping)

html_content += "\n</div>"

font.save("dist/output-font.sfd")
font.generate(f"dist/{font_file_name}.ttf")
font.generate(f"dist/{font_file_name}.eot")
font.generate(f"dist/{font_file_name}.woff")
font.generate(f"dist/{font_file_name}.woff2")

html_content += """
          <div class="message" id="copyMessage">Copied!</div>
      </body>
      <script>

        document.querySelectorAll('.copy_class_btn_js').forEach(item => {
            item.addEventListener('click', function() {
                const iconContent = this.parentElement.parentElement.querySelector('.copy_class_js').classList[0];
                navigator.clipboard.writeText(iconContent).then(() => {
                    const messageDiv = document.getElementById('copyMessage');
                    messageDiv.style.display = 'block';  // Show the message
                    setTimeout(() => {
                        messageDiv.style.display = 'none';  // Hide the message after 2 seconds
                    }, 2000);
                }).catch(err => {
                    console.error('Failed to copy text: ', err);
                });
            });
        });
        </script>
</html>
    """

# Save HTML file
html_file_path = "dist/index.html"
with open(html_file_path, "w") as html_file:
    html_file.write(html_content)

# Save CSS file
css_file_path = "dist/styles.css"
with open(css_file_path, "w") as css_file:
    css_file.write(css_content)
