"""Convergence criteria for optimization algorithms."""

import numpy as np
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union, Tuple
import seaborn as sns



def plot_convergence(
    loss_history: Union[List[float], np.ndarray],
    title: str = "Convergence Plot",
    xlabel: str = "Iteration", 
    ylabel: str = "Loss",
    log_scale: bool = True,
    figsize: Tuple[int, int] = (10, 6),
    save_path: Optional[str] = None
) -> plt.Figure:
    """Plot convergence history of optimization."""
    fig, ax = plt.subplots(figsize=figsize)
    
    ax.plot(loss_history, linewidth=2)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    
    if log_scale:
        ax.set_yscale('log')
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig


class ConvergenceCriterion(ABC):
    """Abstract base class for convergence criteria."""
    
    def __init__(self, tol: float = 1e-6, patience: int = 5):
        self.tol = tol
        self.patience = patience
        self.wait_count = 0
    
    @abstractmethod
    def __call__(self, current_loss: float, loss_history: List[float]) -> bool:
        """Check if convergence criteria is met."""
        pass


class RelativeChangeCriterion(ConvergenceCriterion):
    """Convergence based on relative change in loss."""
    
    def __call__(self, current_loss: float, loss_history: List[float]) -> bool:
        """Check convergence based on relative change."""
        if len(loss_history) < 2:
            return False
            
        prev_loss = loss_history[-2]
        rel_change = abs(current_loss - prev_loss) / (abs(prev_loss) + 1e-8)
        
        if rel_change < self.tol:
            self.wait_count += 1
        else:
            self.wait_count = 0
            
        return self.wait_count >= self.patience


class AbsoluteChangeCriterion(ConvergenceCriterion):
    """Convergence based on absolute change in loss."""
    
    def __call__(self, current_loss: float, loss_history: List[float]) -> bool:
        """Check convergence based on absolute change."""
        if len(loss_history) < 2:
            return False
            
        prev_loss = loss_history[-2]
        abs_change = abs(current_loss - prev_loss)
        
        if abs_change < self.tol:
            self.wait_count += 1
        else:
            self.wait_count = 0
            
        return self.wait_count >= self.patience
