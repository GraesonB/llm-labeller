from xml.etree import ElementTree as ET
import json


def parse_tags(html_tag: str, json_output: bool = True) -> dict:
    try:
        # Parse the HTML tag
        root = ET.fromstring(html_tag)
        # Get the tag name
        tag_name = root.tag
        # Get the content of the tag
        tag_content = ET.tostring(root, encoding="unicode", method="text")
        output = json.loads(tag_content.strip()) if json_output else tag_content.strip()
        return {tag_name: output}
    except ET.ParseError:
        return {"error": "Invalid HTML tag"}
