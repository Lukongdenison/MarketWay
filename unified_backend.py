import os
from speech_service import SpeechService
from navigation_service import NavigationService

class UnifiedBackend:
    def __init__(self, db_path="market.db", whisper_model_size="tiny"):
        self.speech_service = SpeechService(model_size=whisper_model_size)
        self.navigation_service = NavigationService(db_path=db_path)

    def process_request(self, input_data, input_type='text', current_location_id=0):
        """
        Unified entry point for the backend.
        
        Args:
            input_data: Text string or path to audio file.
            input_type: 'text' or 'voice'.
            current_location_id: ID of the starting line (default 0 for Entrance).
            
        Returns:
            Dictionary containing:
            - query: The processed text query.
            - product: Found product name (or None).
            - target_location: Target line name (or None).
            - navigation: Navigation steps (or error message).
            - confidence: Confidence score of the search.
            - error: Error message if any.
        """
        response = {
            "query": None,
            "product": None,
            "target_location": None,
            "navigation": None,
            "confidence": 0.0,
            "error": None
        }

        # 1. Handle Input (Voice -> Text)
        if input_type == 'voice':
            print(f"Processing voice input from {input_data}...")
            transcribed_text = self.speech_service.transcribe(input_data)
            if not transcribed_text:
                response["error"] = "Failed to transcribe audio."
                return response
            response["query"] = transcribed_text
        else:
            response["query"] = input_data

        if not response["query"]:
            response["error"] = "Empty query."
            return response

        print(f"Processing query: '{response['query']}'")

        # 2. Search & Navigate
        # NavigationService now uses SearchService internally for 'find_product_line'
        # But to get the confidence score explicitly, we might want to use SearchService directly first?
        # Actually, NavigationService.navigate calls find_product_line which calls SearchService.
        # But NavigationService.navigate returns a dict. Let's see what it returns.
        # It returns { "product": ..., "target_location": ..., "total_distance": ..., "steps": ... } or { "error": ... }
        
        # To get the score, we might need to modify NavigationService to return it, 
        # or just trust the NavigationService's internal threshold.
        # Let's rely on NavigationService for now.
        
        nav_result = self.navigation_service.navigate(current_location_id, response["query"])
        
        if "error" in nav_result:
            response["error"] = nav_result["error"]
        else:
            response["product"] = nav_result["product"]
            response["target_location"] = nav_result["target_location"]
            response["navigation"] = {
                "distance": nav_result["total_distance"],
                "steps": nav_result["steps"]
            }
            # We don't have the raw score here easily without modifying NavigationService again, 
            # but we know it passed the threshold.
            response["confidence"] = "High (Threshold Passed)" 

        return response

    def close(self):
        self.navigation_service.close()

if __name__ == "__main__":
    # Test
    backend = UnifiedBackend()
    
    # Test Text
    print("\n--- Testing Text Input ---")
    result = backend.process_request("I want some organic bananas", input_type="text")
    print(result)
    
    # Test Voice (Mocking by passing a non-existent file to see error handling)
    print("\n--- Testing Voice Input (Error Case) ---")
    result = backend.process_request("dummy_audio.wav", input_type="voice")
    print(result)
    
    backend.close()
