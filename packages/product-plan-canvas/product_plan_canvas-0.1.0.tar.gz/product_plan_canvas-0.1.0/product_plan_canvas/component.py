from typing import Dict, List, Optional, Any
import gradio as gr
import json

class ProductPlanCanvas(gr.Blocks):
    """
    A custom Gradio component for product planning with a 4-column drag-and-drop board.
    """
    events = {}  # Workaround for Gradio CLI build bug
    
    def __init__(
        self,
        value: Optional[List[Dict[str, Any]]] = None,
        label: Optional[str] = None,
        show_label: bool = True,
        interactive: bool = True,
        **kwargs
    ):
        """
        Initialize the ProductPlanCanvas component.
        
        Args:
            value: Initial state of the board
            label: Label for the component
            show_label: Whether to show the label
            interactive: Whether the component is interactive
        """
        super().__init__(**kwargs)
        
        self.value = value or []
        self.label = label
        self.show_label = show_label
        self.interactive = interactive
        
        with self:
            with gr.Row():
                # Create the 4 columns
                self.columns = {
                    "idea": gr.Column(scale=1),
                    "features": gr.Column(scale=1),
                    "timeline": gr.Column(scale=1),
                    "stories": gr.Column(scale=1)
                }
                
                # Add column headers
                for col_name in self.columns:
                    with self.columns[col_name]:
                        gr.Markdown(f"### {col_name.title()}")
                
                # Create drop zones for each column
                self.drop_zones = {}
                for col_name, column in self.columns.items():
                    with column:
                        self.drop_zones[col_name] = gr.Dropdown(
                            label=f"{col_name.title()} Items",
                            multiselect=True,
                            interactive=self.interactive
                        )
                
                # Add action buttons
                with gr.Row():
                    self.add_btn = gr.Button("Add Item")
                    self.edit_btn = gr.Button("Edit Item")
                    self.remove_btn = gr.Button("Remove Item")
                    self.regenerate_btn = gr.Button("Regenerate")
                
                # Add state management
                self.state = gr.State(self.value)
                
                # Set up event handlers
                self._setup_event_handlers()
    
    def _setup_event_handlers(self):
        """Set up event handlers for the component."""
        def add_item(item: str, column: str):
            if not item:
                return self.value
            
            new_item = {
                "id": len(self.value),
                "content": item,
                "column": column
            }
            self.value.append(new_item)
            return self.value
        
        def edit_item(item_id: int, new_content: str):
            for item in self.value:
                if item["id"] == item_id:
                    item["content"] = new_content
                    break
            return self.value
        
        def remove_item(item_id: int):
            self.value = [item for item in self.value if item["id"] != item_id]
            return self.value
        
        def regenerate_items():
            # In a real implementation, this would call an LLM to regenerate content
            # For now, we'll just return the current state
            return self.value
        
        # Connect event handlers
        self.add_btn.click(
            fn=add_item,
            inputs=[gr.Textbox(), gr.Dropdown(choices=list(self.columns.keys()))],
            outputs=[self.state]
        )
        
        self.edit_btn.click(
            fn=edit_item,
            inputs=[gr.Number(), gr.Textbox()],
            outputs=[self.state]
        )
        
        self.remove_btn.click(
            fn=remove_item,
            inputs=[gr.Number()],
            outputs=[self.state]
        )
        
        self.regenerate_btn.click(
            fn=regenerate_items,
            outputs=[self.state]
        )
    
    def get_config(self):
        """Get the component configuration."""
        return {
            "value": self.value,
            "label": self.label,
            "show_label": self.show_label,
            "interactive": self.interactive
        }
    
    def get_value(self):
        """Get the current value of the component."""
        return self.value
    
    def set_value(self, value: List[Dict[str, Any]]):
        """Set the value of the component."""
        self.value = value
        return self.value 