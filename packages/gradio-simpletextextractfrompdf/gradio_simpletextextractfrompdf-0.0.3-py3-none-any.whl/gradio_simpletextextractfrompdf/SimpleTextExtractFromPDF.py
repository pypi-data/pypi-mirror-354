from __future__ import annotations

from gradio.components.base import Component
from typing import Any, Sequence, TYPE_CHECKING
from gradio.i18n import I18nData

if TYPE_CHECKING:
    from gradio.components import Timer


class SimpleTextExtractFromPDF(Component):
    """
    This component extracts text from a PDF file.
    The extracted text can be submitted as an input {string} to the function.
    Only the text is extracted. Images are not extracted and table structures are not preserved
    PDF file can be uploaded from user's device or from a URL.
    This component was designed to be used as an input component.
    As an output component, it will display {string} content in a textarea.
    """

    EVENTS = ["submit"]


    def __init__(
        self,
        value: str | None = None, *,
        every: Timer | float | None = None,
        label: str | I18nData | None = None,
        inputs: Component | Sequence[Component] | set[Component] | None = None,
        show_label: bool | None = None,
        scale: int | None = None,
        min_width: int = 160,
        interactive: bool | None = None,
        visible: bool = True,
        elem_id: str | None = None,
        elem_classes: list[str] | str | None = None,
        render: bool = True,
        key: int | str | tuple[int | str, ...] | None = None,
        preserved_by_key: list[str] | str | None = "value",
    ):
        """
        Parameters:
            value: The extracted text from the file. This value is set by the component and can be submitted as an input {string} to the function.
            label: the label for this component, displayed above the component if `show_label` is `True` and is also used as the header if there are a table of examples for this component. If None and used in a `gr.Interface`, the label will be the name of the parameter this component corresponds to.
            every: Continously calls `value` to recalculate it if `value` is a function (has no effect otherwise). Can provide a Timer whose tick resets `value`, or a float that provides the regular interval for the reset Timer.
            show_label: if True, will display label.
            scale: relative size compared to adjacent Components. For example if Components A and B are in a Row, and A has scale=2, and B has scale=1, A will be twice as wide as B. Should be an integer. scale applies in Rows, and to top-level Components in Blocks where fill_height=True.
            min_width: minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.
            interactive: if True, will be rendered as an editable textbox; if False, editing will be disabled. If not provided, this is inferred based on whether the component is used as an input or output.
            visible: If False, component will be hidden.
            elem_id: An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.
            elem_classes: An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.
            render: If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.
            key: in a gr.render, Components with the same key across re-renders are treated as the same component, not a new component. Properties set in 'preserved_by_key' are not reset across a re-render.
            preserved_by_key: A list of parameters from this component's constructor. Inside a gr.render() function, if a component is re-rendered with the same key, these (and only these) parameters will be preserved in the UI (if they have been changed by the user or an event listener) instead of re-rendered based on the values provided during constructor.
        """
        super().__init__(
            label=label,
            every=every,
            inputs=inputs,
            show_label=show_label,
            scale=scale,
            min_width=min_width,
            interactive=interactive,
            visible=visible,
            elem_id=elem_id,
            elem_classes=elem_classes,
            value=value,
            render=render,
            key=key,
            preserved_by_key=preserved_by_key,
        )


    def preprocess(self, payload: str | None ) -> str | None:
        """
        Parameters:
            payload: the text extracted from the PDF by the component - string
        Returns:
            Passes the extracted text into the function - string
        """
        return None if payload is None else str(payload)

    def postprocess(self, value: str | None) -> str | None:
        """
        Parameters:
            value: Expects a {string} returned from the function and sets component value to it.
        Returns:
            The value to display in the textarea.
        """
        return None if value is None else str(value)

    def example_payload(self) -> str:
        return "This is a sample payload"

    def example_value(self) -> str:
        return "This is a sample value"

    def api_info(self) -> dict[str, Any]:
        return {"type": "string"}
