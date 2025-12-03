import reflex as rx
from ..backend.backend import State


def chatbot_assistant():
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.box(
                    rx.icon("sparkle", size=24),
                    class_name="bg-[#fef2f2] p-2 rounded-full",
                    style={"color": "#dc2626"},
                ),
                rx.vstack(
                    rx.heading(
                        "Asistente Inteligente de Repositorio",
                        size="6",
                        weight="bold",
                        style={"color": "#1f2937"},
                    ),
                    rx.text(
                        "Pregúntame sobre reportes, documentos o datos del observatorio.",
                        size="2",
                        style={"color": "#6b7280", "line_height": "1.5"},
                    ),
                    spacing="1",
                    align_items="flex-start",
                ),
                align_items="flex-start",
                spacing="3",
            ),
            rx.box(
                rx.vstack(
                    rx.foreach(
                        State.chatbot_messages,
                        lambda msg: rx.box(
                            rx.hstack(
                                rx.cond(
                                    msg["role"] == "assistant",
                                    rx.box(
                                        rx.icon("sparkle", size=16),
                                        class_name="bg-[#dc2626] p-1.5 rounded-full",
                                        style={
                                            "color": "white",
                                            "min_width": "32px",
                                            "height": "32px",
                                        },
                                    ),
                                    rx.box(),
                                ),
                                rx.text(
                                    msg["content"],
                                    size="2",
                                    style={
                                        "color": "#374151",
                                        "line_height": "1.5",
                                    },
                                ),
                                align_items="flex-start",
                                spacing="2",
                            ),
                            width="100%",
                            class_name="p-3",
                        ),
                    ),
                    rx.cond(
                        State.chatbot_is_loading,
                        rx.box(
                            rx.hstack(
                                rx.box(
                                    rx.icon("sparkle", size=16),
                                    class_name="bg-[#dc2626] p-1.5 rounded-full",
                                    style={
                                        "color": "white",
                                        "min_width": "32px",
                                        "height": "32px",
                                    },
                                ),
                                rx.spinner(size="1"),
                                rx.text(
                                    "Pensando...", size="2", style={"color": "#6b7280"}
                                ),
                                align_items="center",
                                spacing="2",
                            ),
                            width="100%",
                            class_name="p-3",
                        ),
                    ),
                    spacing="0",
                    width="100%",
                ),
                class_name="bg-[#f8fafc] rounded-lg",
                style={
                    "min_height": "400px",
                    "max_height": "500px",
                    "overflow_y": "auto",
                },
                width="100%",
            ),
            rx.hstack(
                rx.input(
                    placeholder="Escribe tu pregunta aquí...",
                    value=State.chatbot_input,
                    on_change=State.set_chatbot_input,
                    class_name="flex-1",
                    style={
                        "border": "1px solid #e5e7eb",
                        "border_radius": "8px",
                        "padding": "12px",
                        "background": "white",
                        "height": "48px",
                        "font_size": "16px",
                    },
                ),
                rx.button(
                    rx.icon("send", size=16),
                    on_click=State.handle_send_chatbot_message,
                    disabled=State.chatbot_input == "",
                    class_name="bg-[#dc2626] hover:bg-[#b91c1c] text-white p-3 rounded-lg",
                    style={"min_width": "48px", "height": "48px"},
                ),
                spacing="2",
                width="100%",
            ),
            rx.cond(
                State.chatbot_error != "",
                rx.text(State.chatbot_error, size="1", style={"color": "#dc2626"}),
            ),
            spacing="4",
            width="100%",
        ),
        width="100%",
        class_name="bg-white rounded-xl border border-gray-200 p-6 shadow-sm",
        on_mount=State.initialize_chatbot,
    )
