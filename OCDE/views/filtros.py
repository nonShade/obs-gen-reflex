import reflex as rx
from ..backend.backend import State

# Chips y demás componentes
chip_props = {
    "radius": "full",
    "variant": "surface",
    "size": "3",
    "cursor": "pointer",
    # "style": {"_hover": {"opacity": 0.75}},
}


def selected_area_chip(area: str) -> rx.Component:
    return rx.badge(
        area,
        rx.icon("circle-x", size=18),
        color_scheme="indigo",
        **chip_props,
        on_click=State.remove_area(area),
        class_name="bg-white",
    )


def unselected_area_chip(area: str) -> rx.Component:
    return rx.cond(
        State.selected_areas.contains(area),
        rx.fragment(),
        rx.badge(
            area,
            rx.icon("circle-plus", size=18),
            color_scheme="indigo",
            **chip_props,
            on_click=State.add_area(area),
        ),
    )


def areas_selector() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.heading(
                "Filtrar por Disciplina OCDE nivel 2"
                + f" ({State.selected_areas.length()})",
                # size="4",
                class_name="text-sm sm:text-lg text-gray-700 font-semibold p-2",
            ),
            rx.hstack(
                # rx.button(
                #     rx.icon("plus", size=16),
                #     "Todas",
                #     variant="soft",
                #     size="2",
                #     on_click=State.select_all_areas,
                #     color_scheme="green",
                #     cursor="pointer",
                # ),
                rx.button(
                    rx.icon("trash", size=16),
                    "Limpiar",
                    variant="soft",
                    size="2",
                    on_click=State.clear_areas,
                    color_scheme="tomato",
                    cursor="pointer",
                ),
                spacing="2",
                class_name="px-2",
            ),
            justify="between",
            width="100%",
        ),
        rx.callout(
            "Pronto actualizaremos publicaciones, proyectos y perfiles de investigadoras.",
            icon="info",
            color_scheme="tomato",
            # role="alert",
        ),
        rx.text(
            """Este espacio reúne a las investigadoras de la Universidad de La Frontera, destacando su trayectoria académica y científica a través de sus proyectos entre 2018-2024 y publicaciones entre 2018-2023.
            El buscador permite explorar y filtrar perfiles según líneas de investigación, organizadas por disciplina OCDE nivel 2, facilitando la búsqueda de experticia específica en diversas áreas del conocimiento.
            """,
            class_name="text-sm sm:text-lg text-indigo-900 p-2",
        ),
        rx.vstack(
            rx.box(
                rx.hstack(
                    rx.box(
                        rx.icon("sparkles", size=16, color="white"),
                        style={
                            "backgroundColor": "#8b9cf7",
                            "borderRadius": "50%",
                            "width": "32px",
                            "height": "32px",
                            "display": "flex",
                            "alignItems": "center",
                            "justifyContent": "center",
                            "minWidth": "32px",
                            "marginLeft": "8px",
                        },
                    ),
                    rx.input(
                        placeholder="Describe lo que buscas: 'investigadoras en energías renovables' o 'expertas en biotecnología'...",
                        value=State.ai_search_input,  # Cambiado para usar input separado
                        on_change=State.set_ai_search_input,  # Solo actualiza texto, no busca
                        on_key_down=State.handle_ai_search_enter,
                        style={
                            "border": "none",
                            "outline": "none",
                            "background": "transparent",
                            "fontSize": "16px",
                            "flex": "1",
                            "padding": "0px 12px",
                            "minHeight": "44px",
                        },
                        class_name="placeholder:text-gray-500",
                    ),
                    rx.button(
                        rx.hstack(
                            rx.icon("search", size=16),
                            rx.text("Buscar", style={"fontSize": "14px"}),
                            spacing="1",
                            align="center",
                        ),
                        on_click=State.perform_ai_search,
                        style={
                            "backgroundColor": "#8b9cf7",
                            "color": "white",
                            "border": "none",
                            "borderRadius": "8px",
                            "padding": "10px 16px",
                            "fontSize": "14px",
                            "fontWeight": "600",
                            "cursor": "pointer",
                            "transition": "all 0.2s ease",
                            "height": "44px",
                            "minWidth": "100px",
                        },
                        class_name="hover:bg-indigo-500",
                        disabled=State.ai_search_loading,
                    ),
                    spacing="2",
                    align="center",
                    style={"width": "100%", "alignItems": "center"},
                ),
                style={
                    "backgroundColor": "white",
                    "border": "2px solid #e5e7eb",
                    "borderRadius": "12px",
                    "padding": "8px 12px",
                    "width": "100%",
                    "transition": "all 0.2s ease",
                    "boxShadow": "0 1px 3px rgba(0,0,0,0.1)",
                    "display": "flex",
                    "alignItems": "center",
                },
                class_name="hover:border-indigo-300 hover:shadow-md focus-within:border-indigo-500 focus-within:shadow-lg focus-within:ring-4 focus-within:ring-indigo-50",
            ),
            spacing="2",
            width="100%",
        ),
        rx.hstack(
            rx.divider(),
            rx.foreach(State.selected_areas, selected_area_chip),
            wrap="wrap",
            spacing="2",
            justify_content="start",
        ),
        rx.divider(),
        # rx.hstack(
        #     rx.foreach(State.all_areas, unselected_area_chip),
        #     wrap="wrap",
        #     spacing="2",
        #     justify_content="start",
        # ),
        # spacing="4",
        align_items="center",
        width="100%",
        class_name="bg-white shadow-lg lg:px-50 p-5 py-5",
    )
