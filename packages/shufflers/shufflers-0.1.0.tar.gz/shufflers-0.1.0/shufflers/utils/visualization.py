"""
Visualization utilities for ShuffleLM generation process.
"""

from typing import Optional, List, Dict, Any, Tuple
import torch
import numpy as np
from dataclasses import dataclass
import json


@dataclass
class ShuffleStep:
    """Represents a single step in the shuffle process."""
    step_type: str  # 'generate', 'shuffle', 'filter'
    tokens: List[str]
    scores: Optional[List[float]] = None
    positions: Optional[List[int]] = None
    metadata: Optional[Dict[str, Any]] = None


class ShuffleVisualization:
    """
    Visualization class for ShuffleLM generation process.
    
    This class tracks and visualizes the step-by-step process of:
    1. Parallel token generation
    2. Token shuffling/reordering
    3. Filtering based on position scores
    """
    
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer
        self.steps: List[ShuffleStep] = []
        
    def visualize_generation(
        self,
        prompt: str,
        max_parallel_tokens: int = 30,
        save_animation: bool = False,
        output_path: Optional[str] = None
    ) -> 'ShuffleVisualization':
        """
        Visualize the complete generation process.
        
        Args:
            prompt: Input prompt
            max_parallel_tokens: Maximum tokens to generate in parallel
            save_animation: Whether to save as animation
            output_path: Path to save animation/visualization
            
        Returns:
            Self for method chaining
        """
        self.steps = []
        
        # Encode input
        inputs = self.tokenizer(prompt, return_tensors="pt")
        input_ids = inputs["input_ids"]
        
        # Step 1: Show initial prompt
        initial_tokens = self.tokenizer.convert_ids_to_tokens(input_ids[0])
        self.steps.append(ShuffleStep(
            step_type="initial",
            tokens=initial_tokens,
            metadata={"prompt": prompt}
        ))
        
        # Step 2: Generate parallel tokens (simulation)
        with torch.no_grad():
            # Get model outputs to analyze the process
            extended_ids = torch.cat([
                input_ids,
                torch.zeros(1, max_parallel_tokens, dtype=torch.long)
            ], dim=1)
            
            outputs = self.model.forward(extended_ids)
            logits = outputs.logits
            
            # Simulate parallel generation
            new_logits = logits[:, input_ids.size(1):input_ids.size(1) + max_parallel_tokens, :]
            new_tokens = torch.argmax(new_logits, dim=-1)
            
            # Convert to token strings
            generated_token_strings = [
                self.tokenizer.convert_ids_to_tokens([token_id.item()])[0]
                for token_id in new_tokens[0]
            ]
            
            # Get confidence scores
            confidence_scores = torch.softmax(new_logits, dim=-1).max(dim=-1)[0][0].tolist()
            
            self.steps.append(ShuffleStep(
                step_type="generate",
                tokens=generated_token_strings,
                scores=confidence_scores,
                positions=list(range(len(generated_token_strings))),
                metadata={"parallel_generation": True}
            ))
            
            # Step 3: Analyze position scores (simulate rotary regression)
            if hasattr(self.model, 'mixer') and hasattr(self.model, 'rotary_regression'):
                # Get mixer output
                hidden_states = outputs.hidden_states if hasattr(outputs, 'hidden_states') else None
                if hidden_states is not None:
                    mixer_output = self.model.mixer(hidden_states)
                    rotary_component = mixer_output[:, input_ids.size(1):, -1:]
                    
                    position_ids = torch.arange(max_parallel_tokens).unsqueeze(0)
                    position_scores = self.model.rotary_regression(rotary_component, position_ids)
                    position_scores_list = position_scores.squeeze().tolist()
                    
                    # Step 4: Show shuffling process
                    # Sort by position scores (higher scores = keep)
                    token_score_pairs = list(zip(generated_token_strings, position_scores_list))
                    sorted_pairs = sorted(token_score_pairs, key=lambda x: x[1], reverse=True)
                    
                    shuffled_tokens = [pair[0] for pair in sorted_pairs]
                    shuffled_scores = [pair[1] for pair in sorted_pairs]
                    
                    self.steps.append(ShuffleStep(
                        step_type="shuffle",
                        tokens=shuffled_tokens,
                        scores=shuffled_scores,
                        positions=list(range(len(shuffled_tokens))),
                        metadata={"sort_by": "position_scores"}
                    ))
                    
                    # Step 5: Filter tokens based on threshold
                    threshold = 0.3
                    filtered_tokens = []
                    filtered_scores = []
                    
                    for token, score in zip(shuffled_tokens, shuffled_scores):
                        if score > threshold:
                            filtered_tokens.append(token)
                            filtered_scores.append(score)
                    
                    self.steps.append(ShuffleStep(
                        step_type="filter",
                        tokens=filtered_tokens,
                        scores=filtered_scores,
                        positions=list(range(len(filtered_tokens))),
                        metadata={"threshold": threshold, "kept": len(filtered_tokens)}
                    ))
                    
                    # Final step: Combine with original prompt
                    final_tokens = initial_tokens + filtered_tokens
                    final_text = self.tokenizer.decode(
                        self.tokenizer.convert_tokens_to_ids(final_tokens),
                        skip_special_tokens=True
                    )
                    
                    self.steps.append(ShuffleStep(
                        step_type="final",
                        tokens=final_tokens,
                        metadata={"final_text": final_text}
                    ))
        
        if save_animation and output_path:
            self.save_animation(output_path)
        
        return self
    
    def save_animation(self, output_path: str) -> None:
        """Save visualization as animated GIF or video."""
        try:
            import matplotlib.pyplot as plt
            import matplotlib.animation as animation
            from matplotlib.patches import Rectangle
            
            fig, ax = plt.subplots(figsize=(12, 8))
            
            def animate(frame):
                ax.clear()
                
                if frame >= len(self.steps):
                    return
                
                step = self.steps[frame]
                
                # Set title based on step type
                title_map = {
                    "initial": "Initial Prompt",
                    "generate": "Parallel Token Generation",
                    "shuffle": "Token Shuffling by Position Score",
                    "filter": "Filtering Low-Score Tokens",
                    "final": "Final Output"
                }
                
                ax.set_title(f"Step {frame + 1}: {title_map.get(step.step_type, step.step_type)}", 
                           fontsize=16, fontweight='bold')
                
                # Draw tokens
                tokens = step.tokens
                scores = step.scores or [1.0] * len(tokens)
                
                for i, (token, score) in enumerate(zip(tokens, scores)):
                    # Color based on score
                    color = plt.cm.RdYlGn(score) if step.step_type != "initial" else 'lightblue'
                    
                    # Draw token box
                    rect = Rectangle((i, 0), 0.8, 1, facecolor=color, edgecolor='black')
                    ax.add_patch(rect)
                    
                    # Add token text
                    ax.text(i + 0.4, 0.5, token, ha='center', va='center', 
                           fontsize=10, fontweight='bold')
                    
                    # Add score text if available
                    if step.scores:
                        ax.text(i + 0.4, -0.3, f"{score:.2f}", ha='center', va='center', 
                               fontsize=8)
                
                ax.set_xlim(-0.5, len(tokens))
                ax.set_ylim(-0.5, 1.5)
                ax.set_aspect('equal')
                ax.axis('off')
                
                # Add metadata info
                if step.metadata:
                    info_text = []
                    for key, value in step.metadata.items():
                        if key not in ['final_text']:  # Skip long text
                            info_text.append(f"{key}: {value}")
                    
                    if info_text:
                        ax.text(0.02, 0.98, '\n'.join(info_text), 
                               transform=ax.transAxes, fontsize=10,
                               verticalalignment='top', 
                               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
            
            anim = animation.FuncAnimation(
                fig, animate, frames=len(self.steps), 
                interval=2000, repeat=True
            )
            
            if output_path.endswith('.gif'):
                anim.save(output_path, writer='pillow', fps=0.5)
            else:
                anim.save(output_path, writer='ffmpeg', fps=0.5)
                
            plt.close()
            
        except ImportError as e:
            print(f"Warning: Could not save animation due to missing dependencies: {e}")
            print("Please install matplotlib and pillow/ffmpeg for animation support")
    
    def print_steps(self) -> None:
        """Print a text-based visualization of the steps."""
        for i, step in enumerate(self.steps):
            print(f"\n=== Step {i + 1}: {step.step_type.upper()} ===")
            print(f"Tokens: {' '.join(step.tokens)}")
            
            if step.scores:
                print(f"Scores: {[f'{s:.3f}' for s in step.scores]}")
            
            if step.metadata:
                for key, value in step.metadata.items():
                    print(f"{key}: {value}")
    
    def to_json(self) -> str:
        """Export visualization data as JSON."""
        data = {
            "steps": [
                {
                    "step_type": step.step_type,
                    "tokens": step.tokens,
                    "scores": step.scores,
                    "positions": step.positions,
                    "metadata": step.metadata
                }
                for step in self.steps
            ]
        }
        return json.dumps(data, indent=2)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the generation process."""
        stats = {}
        
        for step in self.steps:
            step_type = step.step_type
            
            if step_type not in stats:
                stats[step_type] = {
                    "token_count": 0,
                    "avg_score": 0.0,
                    "min_score": float('inf'),
                    "max_score": float('-inf')
                }
            
            stats[step_type]["token_count"] = len(step.tokens)
            
            if step.scores:
                scores = step.scores
                stats[step_type]["avg_score"] = sum(scores) / len(scores)
                stats[step_type]["min_score"] = min(scores)
                stats[step_type]["max_score"] = max(scores)
        
        return stats


def visualize_shuffle(
    model,
    tokenizer,
    prompt: str,
    max_parallel_tokens: int = 30,
    save_animation: bool = False,
    output_path: Optional[str] = None
) -> ShuffleVisualization:
    """
    Convenience function to visualize shuffle generation process.
    
    Args:
        model: ShuffleLM model
        tokenizer: Tokenizer
        prompt: Input prompt
        max_parallel_tokens: Maximum parallel tokens
        save_animation: Whether to save animation
        output_path: Output path for animation
        
    Returns:
        ShuffleVisualization instance
    """
    viz = ShuffleVisualization(model, tokenizer)
    return viz.visualize_generation(
        prompt=prompt,
        max_parallel_tokens=max_parallel_tokens,
        save_animation=save_animation,
        output_path=output_path
    )


def compare_shuffle_strategies(
    model,
    tokenizer, 
    prompt: str,
    strategies: List[str] = ["rotary", "fixed"],
    max_parallel_tokens: int = 30
) -> Dict[str, ShuffleVisualization]:
    """
    Compare different shuffle strategies side by side.
    
    Args:
        model: ShuffleLM model
        tokenizer: Tokenizer
        prompt: Input prompt
        strategies: List of strategies to compare
        max_parallel_tokens: Maximum parallel tokens
        
    Returns:
        Dictionary mapping strategy names to visualizations
    """
    results = {}
    
    for strategy in strategies:
        # This would need to be implemented in the model
        # For now, we'll create a basic comparison
        viz = visualize_shuffle(
            model, tokenizer, prompt, max_parallel_tokens
        )
        results[strategy] = viz
    
    return results
