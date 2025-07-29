"""
Methods to turn a KicadTheme into a CSS style.

SPDX-License-Identifier: EUPL-1.2
"""

from textwrap import dedent

import svg

from edea_draw.themes.types import BoardTheme, SchematicTheme


def board_theme_to_style(theme: BoardTheme) -> svg.Style:
    style_str = dedent(
        """
            .kicad_svg_layer {
                stroke: white;
                fill: white;
                stroke-opacity: 0.8;
                fill-opacity: 0.8;
            }
            .stroked-text {
                fill-opacity: 0;
            }
            """
    )

    for key, value in theme.model_dump().items():
        if key == "copper":
            style_str += "\n".join(
                [
                    dedent(
                        f"""
                .kicad_svg_layer.copper.{key} {{
                   stroke: {value};
                   fill: {value};
                }}"""
                    )
                    for key, value in value.items()
                ]
            )
        else:
            style_str += dedent(
                f"""
                .kicad_svg_layer.{key} {{
                   stroke: {value};
                   fill: {value};
                }}"""
            )

    return svg.Style(text=style_str)


def sch_theme_to_style(theme: SchematicTheme) -> svg.Style:
    """
    Returns a svg.py `svg.Style` for a `edea_draw.themes.model.SchematicTheme`.
    """
    return svg.Style(
        text=dedent(
            f"""
                svg {{
                    background-color: {theme.background};
                }}
                rect, polyline, circle, path {{
                    stroke: {theme.component_outline};
                    stroke-opacity: 1.0;
                    stroke-width: 0.1524;
                    stroke-linecap: round;
                    stroke-linejoin: round;
                }}
                .fill-none {{
                    fill: none;
                }}
                .fill-background {{
                    fill: {theme.component_body};
                    fill-opacity: 0.6;
                }}
                .fill-outline {{
                    fill: {theme.component_outline};
                    fill-opacity: 1;
                }}
                polyline.wire {{
                    stroke: {theme.wire};
                    stroke-width: 0.1524;
                }}
                polyline.bus {{
                    stroke: {theme.bus};
                    stroke-width: 0.3048;
                }}
                text.property {{
                    fill: {theme.fields};
                }}
                text.property.prop-reference {{
                    fill: {theme.reference};
                }}
                text.property.prop-value {{
                    fill: {theme.value};
                }}
                text.pin-number {{
                    fill: {theme.pin_number};
                }}
                text.pin-name {{
                    fill: {theme.pin_name};
                }}
                circle.junction {{
                    stroke: none;
                    fill: {theme.junction};
                }}
                circle.junction.junction-bus {{
                    fill: {theme.bus_junction};
                }}
                .pin-line {{
                    stroke: {theme.pin};
                    stroke-width: 0.1524;
                }}
                .label-local {{
                    fill: {theme.label_local};
                }}
                .label-global {{
                    fill: {theme.label_global};
                }}
                .label-hierarchical {{
                    fill: {theme.label_hier};
                }}
                .no-connect {{
                    stroke: {theme.no_connect};
                    stroke-width: 0.1524;
                }}
            """
        )
    )
