"""
Summary management for devco
"""
from typing import Dict, Any
from .storage import DevDocStorage


class SummaryManager:
    """Manages project summary and sections"""
    
    def __init__(self, storage: DevDocStorage):
        self.storage = storage
    
    def _auto_embed(self):
        """Automatically regenerate embeddings after content changes"""
        try:
            from .embeddings import EmbeddingsManager
            embeddings_manager = EmbeddingsManager(self.storage)
            embeddings_manager.embed_all_content()
        except Exception as e:
            print(f"Warning: Could not auto-generate embeddings: {e}")
    
    def show_summary(self):
        """Show the current project summary and sections"""
        try:
            data = self.storage.load_summary()
            
            print("Project Summary:")
            print("=" * 50)
            
            if data.get('summary', '').strip():
                print(data['summary'])
            else:
                print("No summary defined yet. Set one with: devco summary replace")
            
            print("\nSections:")
            print("-" * 20)
            
            sections = data.get('sections', {})
            if sections:
                for name, content in sections.items():
                    print(f"\n{name}:")
                    if content.get('summary'):
                        print(f"  {content['summary']}")
                    else:
                        print("  No summary")
            else:
                print("No sections defined yet. Add one with: devco section add <name>")
        
        except FileNotFoundError:
            print("devco not initialized. Run 'devco init' first.")
    
    def replace_summary(self, text: str = None):
        """Replace the project summary with new content"""
        try:
            if text is None:
                summary_text = input("Enter project summary: ").strip()
            else:
                summary_text = text.strip()
            
            if not summary_text:
                print("Summary cannot be empty.")
                return
            
            # Load existing data
            data = self.storage.load_summary()
            data['summary'] = summary_text
            
            # Save updated data
            self.storage.save_summary(data)
            
            print("Summary updated successfully.")
            self._auto_embed()
        
        except FileNotFoundError:
            print("devco not initialized. Run 'devco init' first.")
        except KeyboardInterrupt:
            print("\nCancelled.")