from graphviz import Digraph
import os

# ✅ FIX: Use BASE_DIR instead of os.getcwd() — safe inside Docker container
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSED_FOLDER = os.path.join(BASE_DIR, "processed")


# ✅ FIX: Function was defined TWICE — duplicate removed, kept the larger/better version
def generate_er_diagram_from_keymap(base_name: str, keymap: dict) -> bytes:
    dot = Digraph(comment="ER Diagram", format="png")
    dot.attr(rankdir="TB", splines="curved", nodesep="0.3", ranksep="0.5")
    dot.attr("graph", dpi="300")
    dot.attr("node", shape="plaintext", fontname="Helvetica", fontsize="20")

    table_border_color = "#4b555c"

    for table_name, key_info in keymap.items():
        attributes = key_info.get("attributes", [])
        primary_keys = set(key_info.get("primary_keys", []))
        foreign_keys = key_info.get("foreign_keys", {})

        label = f"""<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="10" CELLPADDING="18" COLOR="{table_border_color}" STYLE="ROUNDED">
            <TR>
                <TD BGCOLOR="{table_border_color}" ALIGN="CENTER" WIDTH="320" HEIGHT="20">
                    <FONT COLOR="white" POINT-SIZE="20"><B>{table_name}</B></FONT>
                </TD>
            </TR>
        """

        for attr in attributes:
            if attr in primary_keys:
                attr_label = f"<B>{attr} (PK)</B>"
            elif attr in foreign_keys:
                attr_label = f"<I>{attr} (FK)</I>"
            else:
                attr_label = attr
            label += f'<TR><TD PORT="{attr}" ALIGN="LEFT"><FONT POINT-SIZE="14">{attr_label}</FONT></TD></TR>'

        label += "</TABLE>>"
        dot.node(table_name, label=label)

    for table_name, key_info in keymap.items():
        foreign_keys = key_info.get("foreign_keys", {})

        for fk_attr, ref_info in foreign_keys.items():
            ref_table = ref_info.get("ref_table")
            ref_column = ref_info.get("ref_column")

            if ref_table in keymap:
                pk_attrs = set(keymap[ref_table].get("primary_keys", []))
                target_port = (
                    ref_column
                    if ref_column in pk_attrs
                    else (list(pk_attrs)[0] if pk_attrs else "")
                )
                if target_port:
                    dot.edge(
                        f"{table_name}:{fk_attr}",
                        f"{ref_table}:{target_port}",
                        color=table_border_color,
                        fontsize="10",
                        arrowhead="normal",
                    )
                else:
                    dot.edge(
                        table_name, ref_table, color=table_border_color, fontsize="10"
                    )

    temp_filepath = os.path.join(PROCESSED_FOLDER, f"{base_name}_temp")
    dot.render(filename=temp_filepath, cleanup=False)

    png_path = temp_filepath + ".png"
    with open(png_path, "rb") as img_file:
        image_bytes = img_file.read()

    for ext in [".png", ".gv"]:
        try:
            os.remove(temp_filepath + ext)
        except OSError:
            pass

    return image_bytes
