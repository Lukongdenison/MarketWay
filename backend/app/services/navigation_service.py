from typing import Dict, Optional
from app.services.data_loader import data_loader

class NavigationService:
    def get_directions(self, line_name: str) -> Dict:
        line = data_loader.get_line_by_name(line_name)
        if not line:
            return {"error": "Line not found"}

        layout = line.get("layout", {})
        column = layout.get("column", "unknown")
        order = layout.get("order", 0)

        # Generate simple directions based on the layout
        # Assuming "Entrance" is the starting point
        
        direction_text = f"To get to {line['line_name']}: "
        
        if column == "left":
            direction_text += "Enter the market and turn LEFT. "
            if order == 1:
                direction_text += "It is the FIRST line on your left."
            elif order == 2:
                direction_text += "It is the SECOND line on your left."
            elif order == 3:
                direction_text += "It is the THIRD line on your left."
            else:
                direction_text += f"It is the {order}th line on your left."
        elif column == "right":
            direction_text += "Enter the market and turn RIGHT. "
            if order == 1:
                direction_text += "It is the FIRST line on your right."
            elif order == 2:
                direction_text += "It is the SECOND line on your right."
            elif order == 3:
                direction_text += "It is the THIRD line on your right."
            else:
                direction_text += f"It is the {order}th line on your right."
        else:
            direction_text += "The location is not clearly mapped."

        return {
            "line_name": line['line_name'],
            "directions": direction_text,
            "layout": layout
        }

navigation_service = NavigationService()
