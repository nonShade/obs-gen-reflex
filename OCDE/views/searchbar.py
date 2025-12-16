import reflex as rx
from ..backend.backend import State

def navbar_searchbar() -> rx.Component:
    return rx.box(
        rx.desktop_only(
            rx.hstack(
                rx.hstack(
                    rx.icon(
                        "user-round-search",
                        width="2.25em",
                        height="auto",
                        border_radius="25%",
                        size=24,
                        class_name="text-indigo-900"
                    ),
                    rx.vstack(
                        rx.heading(
                            "Investigadoras", size="7", weight="bold", class_name="text-indigo-900"
                        ),
                        rx.text("Proyectos y Publicaciones 2018 - 2024", size="5", class_name="text-indigo-900"),
                        spacing="0",
                    ),
                    # rx.badge(
                    #     "2018-2024",
                    #     rx.icon("calendar", size=24),
                    #     radius="full",
                    #     align="center",
                    #     color_scheme="blue",
                    #     variant="surface",
                    # ),
                    align_items="center",
                ),
                # rx.vstack(
                #     rx.input(
                #         rx.input.slot(rx.icon("search")),
                #         rx.input.slot(
                #             rx.icon("x", on_click=lambda: State.set_search_term("")),
                #             justify="end",
                #             cursor="pointer",
                #         ),
                #         value=State.search_term,
                #         placeholder="Buscar por nombre...",
                #         size="2",
                #         max_width="300px",
                #         width="100%",
                #         variant="classic",
                #         color_scheme="indigo",
                #         on_change=lambda val: State.set_search_term(val),
                #     ),
                #     rx.hstack(
                #         rx.input(
                #             value=State.min_proyectos,
                #             placeholder="Min. proyectos",
                #             size="2",
                #             width="140px",
                #             variant="classic",
                #             color_scheme="indigo",
                #             type="number",
                #             min="0",
                #             on_change=State.set_min_proyectos,
                #         ),
                #         rx.input(
                #             value=State.min_publicaciones,
                #             placeholder="Min. publicaciones",
                #             size="2",
                #             width="140px",
                #             variant="classic",
                #             color_scheme="indigo",
                #             type="number",
                #             min="0",
                #             on_change=State.set_min_publicaciones,
                #         ),
                #         spacing="2",
                #         max_width="300px",
                #     ),
                #     rx.input(
                #         value=State.search_rol,
                #         placeholder="Rol proyecto (IR, co-i, etc.)",
                #         size="2",
                #         max_width="300px",
                #         width="100%",
                #         variant="classic",
                #         color_scheme="indigo",
                #         on_change=State.set_search_rol,
                #     ),
                #     spacing="2",
                #     max_width="300px",
                # ),
                # justify="between",
                align_items="center",
                spacing="0",
                width="100%",
                top="0px",
                class_name="px-40",
            ),
        ),
        rx.mobile_and_tablet(
            rx.hstack(
                rx.hstack(
                    # rx.icon(
                    #     "user-round-search",
                    #     size=20,
                    #     width="2em",
                    #     height="auto",
                    #     border_radius="25%",
                    # ),
                    rx.vstack(
                        rx.heading(
                            "Investigadoras", size="4", weight="bold", class_name="text-indigo-900"
                        ),
                        rx.text("Proyectos y Publicaciones 2018-2024", size="1", class_name="text-indigo-900"),
                        spacing="0",
                    ),
                    align_items="center",
                ),
                rx.vstack(
                    rx.input(
                        rx.input.slot(rx.icon("search", size=15)),
                        rx.input.slot(
                            rx.icon("x", size=15),
                            justify="end",
                            cursor="pointer",
                        ),
                        value=State.search_term,
                        placeholder="Buscar nombre...",
                        size="1",
                        type="search",
                        width="100%",
                        variant="surface",
                        color_scheme="gray",
                        on_change=lambda val: State.set_search_term(val),
                    ),
                    rx.hstack(
                        rx.input(
                            value=State.min_proyectos,
                            placeholder="Min. proyectos",
                            size="1",
                            width="50%",
                            variant="surface",
                            color_scheme="gray",
                            type="number",
                            min="0",
                            on_change=State.set_min_proyectos,
                        ),
                        rx.input(
                            value=State.min_publicaciones,
                            placeholder="Min. publicaciones",
                            size="1",
                            width="50%",
                            variant="surface",
                            color_scheme="gray",
                            type="number",
                            min="0",
                            on_change=State.set_min_publicaciones,
                        ),
                        spacing="1",
                        width="100%",
                    ),
                    rx.input(
                        value=State.search_rol,
                        placeholder="Rol proyecto (IR, co-i, etc.)",
                        size="1",
                        width="100%",
                        variant="surface",
                        color_scheme="gray",
                        on_change=State.set_search_rol,
                    ),
                    spacing="1",
                    width="50%",
                ),
                justify="between",
                align_items="center",
                class_name="w-full",
            ),
        ),
        # bg=rx.color("accent", 3),
        # padding="1em",
        # position="fixed",
        top="0px",
        # z_index="5",
        width="100%",
        spacing="0",
        background_color="#a280f6",
        class_name="md:px-20 p-5",
    )


def navbar_searchbar_notsearch() -> rx.Component:
    return rx.box(
        rx.desktop_only(
            rx.hstack(
                rx.hstack(
                    rx.icon(
                        "user-round-search",
                        width="2.25em",
                        height="auto",
                        border_radius="25%",
                        size=24,
                        class_name="text-indigo-900"
                    ),
                    rx.vstack(
                        rx.heading(
                            "Investigadoras", size="7", weight="bold", class_name="text-indigo-900"
                        ),
                        rx.text("Proyectos y Publicaciones 2018 - 2024", size="5", class_name="text-indigo-900"),
                        spacing="0",
                    ),
                    # rx.badge(
                    #     "2018-2024",
                    #     rx.icon("calendar", size=24),
                    #     radius="full",
                    #     align="center",
                    #     color_scheme="blue",
                    #     variant="surface",
                    # ),
                    align_items="center",
                ),
                justify="between",
                align_items="center",
                spacing="0",
                top="0px",
                class_name="w-full px-10",
            ),
        ),
        rx.mobile_and_tablet(
            rx.hstack(
                rx.hstack(
                    rx.icon(
                        "user-round-search",
                        size=20,
                        width="2em",
                        height="auto",
                        border_radius="25%",
                        class_name="text-indigo-900"
                    ),
                    rx.vstack(
                        rx.heading(
                            "Investigadoras", size="4", weight="bold", class_name="text-indigo-900"
                        ),
                        rx.text("Proyectos y Publicaciones 2018-2024", size="1", class_name="text-indigo-900"),
                        spacing="0",
                    ),
                    align_items="center",
                ),
                justify="between",
                align_items="center",
                class_name="w-full",
            ),
        ),
        # bg=rx.color("accent", 3),
        # padding="1em",
        # position="fixed",
        top="0px",
        # z_index="5",
        width="100%",
        spacing="0",
        background_color="#a280f6",
        class_name="p-5",
    )
