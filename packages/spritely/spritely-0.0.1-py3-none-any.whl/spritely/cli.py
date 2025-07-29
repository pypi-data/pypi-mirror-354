from pathlib import Path
from typing import Dict, Type
import xml.etree.ElementTree as ET


from attrs import define, field
import click
import yaml


@define
class IconSpec:
    path: Path
    name: str

    @classmethod
    def from_dict(
        cls: Type["IconSpec"],
        root: Path,
        d: Dict,
    ) -> "IconSpec":
        return cls(
            path=root / d["file_name"],
            name=d["icon_name"],
        )

    def get_symbol(self):
        with self.path.open() as f:
            xml_doc = ET.parse(f)
        root = xml_doc.getroot()
        children = [c for c in root]
        symbol_el = ET.Element("{http://www.w3.org/2000/svg}symbol")
        symbol_el.set("id", self.name)
        symbol_el.set("viewBox", "0 0 512 512")
        [symbol_el.append(el) for el in children]
        return symbol_el


@define
class Sprite:
    svg_element = field(default=None)

    @classmethod
    def from_config(
        cls: Type["Sprite"],
        config: Path,
    ) -> "Sprite":
        SVG_NAMESPACE = "http://www.w3.org/2000/svg"
        ET.register_namespace("", SVG_NAMESPACE)
        with config.open() as f:
            config_ = yaml.safe_load(f)
        root = Path(config_["root_path"])
        icon_specs = [
            IconSpec.from_dict(
                root=root,
                d=source,
            )
            for source in config_["sources"]
        ]
        symbol_elements = [
            icon_spec.get_symbol() for icon_spec in icon_specs]
        svg_root = ET.Element("{http://www.w3.org/2000/svg}svg")
        for symbol_element in symbol_elements:
            svg_root.append(symbol_element)
        return cls(svg_element=svg_root)


@click.command()
@click.option(
    "--config",
    help="path to config file",
    required=True,
)
def main(
    config: str,
):
    sprite = Sprite.from_config(config=Path(config))
    svg = sprite.svg_element
    ET.indent(svg)
    outstream = click.get_binary_stream("stdout")
    outstream.write(ET.tostring(svg))


if __name__ == "__main__":
    main()
