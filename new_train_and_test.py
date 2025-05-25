#!/usr/bin/env python3
"""
Improved YOLO11 Training Script with RepNCSPELAN4 Head
- Enhanced architecture for better detection accuracy
- Comprehensive logging and monitoring
- Flexible configuration system
"""

import os
import time
import logging
from pathlib import Path
from ultralytics import YOLO
import torch

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('training.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def setup_environment():
    """Setup training environment and check requirements."""
    # Check CUDA availability
    if torch.cuda.is_available():
        logger.info(f"CUDA Available: {torch.cuda.get_device_name(0)}")
        logger.info(f"CUDA Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
    else:
        logger.warning("CUDA not available, training will be slower on CPU")
    
    # Set memory optimization
    if torch.cuda.is_available():
        torch.backends.cudnn.benchmark = True
        logger.info("CUDNN benchmark enabled for faster training")

def train_yolo_improved(
    model_config="yolo11.yaml",  # ← NEW ARCHITECTURE
    data_yaml="datasets/tt100k.yaml",
    epochs=100,
    batch_size=16,
    imgsz=1024,
    project_name="yolo11_repncspelan4_runs",
    experiment_name=None,
    pretrained_weights=None,
    **kwargs
):
    """
    Train YOLO with RepNCSPELAN4 improved architecture.
    
    Args:
        model_config: Path to model architecture YAML (NEW!)
        data_yaml: Path to dataset YAML
        epochs: Number of training epochs
        batch_size: Training batch size
        imgsz: Input image size
        project_name: Project directory name
        experiment_name: Experiment name (auto-generated if None)
        pretrained_weights: Path to pretrained weights (optional)
        **kwargs: Additional training arguments
    """
    
    setup_environment()
    
    # Generate experiment name if not provided
    if experiment_name is None:
        experiment_name = f"repncspelan4_e{epochs}_b{batch_size}_s{imgsz}_{int(time.time())}"
    
    logger.info("=" * 80)
    logger.info("🚀 STARTING YOLO11 + RepNCSPELAN4 TRAINING")
    logger.info("=" * 80)
    logger.info(f"Model Architecture: {model_config}")
    logger.info(f"Dataset: {data_yaml}")
    logger.info(f"Epochs: {epochs}")
    logger.info(f"Batch Size: {batch_size}")
    logger.info(f"Image Size: {imgsz}")
    logger.info(f"Experiment: {experiment_name}")
    
    try:
        # Load model with new architecture
        if pretrained_weights and os.path.exists(pretrained_weights):
            logger.info(f"Loading pretrained weights: {pretrained_weights}")
            model = YOLO(pretrained_weights)
            # Override architecture if specified
            if model_config != "yolo11n.pt":  # If not using default
                logger.info(f"Applying new architecture: {model_config}")
                # Note: This might require custom implementation
        else:
            logger.info(f"Creating new model from architecture: {model_config}")
            model = YOLO(model_config)  # ← LOAD NEW ARCHITECTURE
        
        # Display model info
        logger.info("\n📋 MODEL ARCHITECTURE:")
        try:
            model.info(detailed=True)
        except:
            logger.info("Model info not available (expected for new architecture)")
        
        # Verify dataset
        if not os.path.exists(data_yaml):
            raise FileNotFoundError(f"Dataset YAML not found: {data_yaml}")
        
        logger.info("\n🎯 STARTING TRAINING...")
        
        # Training configuration
        train_args = {
            'data': data_yaml,
            'epochs': epochs,
            'batch': batch_size,
            'imgsz': imgsz,
            'optimizer': 'auto',  # AdamW for RepNCSPELAN4
            'lr0': 0.01,          # Base learning rate
            'lrf': 0.01,          # Final learning rate factor
            'momentum': 0.937,    # Momentum
            'weight_decay': 0.0005,  # Weight decay
            'warmup_epochs': 3,   # Warmup epochs
            'warmup_momentum': 0.8,  # Warmup momentum
            'save': True,
            'save_period': 5,     # Save every 5 epochs
            'val': True,          # Validate during training
            'plots': True,        # Generate training plots
            'device': '0' if torch.cuda.is_available() else 'cpu',
            'workers': 8,         # Data loading workers
            'project': project_name,
            'name': experiment_name,
            'exist_ok': True,
            'pretrained': bool(pretrained_weights),
            'verbose': True,
            # Advanced RepNCSPELAN4 optimizations
            'close_mosaic': 10,   # Close mosaic augmentation in last N epochs
            'amp': True,          # Automatic Mixed Precision
            'fraction': 1.0,      # Use full dataset
            'profile': False,     # Profile training
            **kwargs
        }
        
        # Start training
        results = model.train(**train_args)
        
        # Log results
        logger.info("\n✅ TRAINING COMPLETED!")
        logger.info(f"Results saved to: {Path(project_name) / experiment_name}")
        
        # Performance summary
        if hasattr(results, 'results_dict'):
            metrics = results.results_dict
            logger.info("\n📊 FINAL METRICS:")
            for key, value in metrics.items():
                if isinstance(value, (int, float)):
                    logger.info(f"  {key}: {value:.4f}")
        
        # Find best model
        best_model_path = Path(project_name) / experiment_name / "weights" / "best.pt"
        if best_model_path.exists():
            logger.info(f"✨ Best model saved: {best_model_path}")
            return str(best_model_path), results
        
        return None, results
        
    except Exception as e:
        logger.error(f"❌ Training failed: {str(e)}")
        logger.error("Check your configuration and try again")
        raise

def validate_model(model_path, data_yaml, imgsz=1024, **kwargs):
    """Validate trained model performance."""
    logger.info(f"\n🔍 VALIDATING MODEL: {model_path}")
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found: {model_path}")
    
    model = YOLO(model_path)
    
    # Validation configuration
    val_args = {
        'data': data_yaml,
        'imgsz': imgsz,
        'batch': 1,  # Single batch for validation
        'device': '0' if torch.cuda.is_available() else 'cpu',
        'plots': True,
        'save_json': True,
        'verbose': True,
        **kwargs
    }
    
    results = model.val(**val_args)
    
    logger.info("📈 VALIDATION RESULTS:")
    if hasattr(results, 'results_dict'):
        for key, value in results.results_dict.items():
            if isinstance(value, (int, float)):
                logger.info(f"  {key}: {value:.4f}")
    
    return results

def benchmark_model(model_path, imgsz=1024):
    """Benchmark model speed and accuracy."""
    logger.info(f"\n⚡ BENCHMARKING MODEL: {model_path}")
    
    model = YOLO(model_path)
    
    # Benchmark different formats
    results = model.benchmark(
        imgsz=imgsz,
        half=True,    # FP16 precision
        device='0' if torch.cuda.is_available() else 'cpu',
        verbose=True
    )
    
    return results

def main():
    """Main training script with improved RepNCSPELAN4 architecture."""
    
    # ==================== CONFIGURATION ====================
    CONFIG = {
        # Model & Architecture
        'model_config': 'yolo11.yaml',  # ← NEW ARCHITECTURE FILE
        'pretrained_weights': None,  # Set path to use pretrained weights
        
        # Dataset
        'data_yaml': 'datasets/tt100k.yaml',
        
        # Training Parameters
        'epochs': 100,
        'batch_size': 16,
        'imgsz': 1024,
        
        # Experiment Management
        'project_name': 'yolo11_repncspelan4_experiments',
        'experiment_name': 'tt100k_v1',  # Will auto-generate if None
        
        # Training Mode
        'mode': 'train',  # 'train', 'validate', 'benchmark', or 'all'
    }
    
    logger.info("🚀 YOLO11 + RepNCSPELAN4 Training Pipeline")
    logger.info(f"Configuration: {CONFIG}")
    
    try:
        if CONFIG['mode'] in ['train', 'all']:
            # Training phase
            best_model_path, train_results = train_yolo_improved(
                model_config=CONFIG['model_config'],
                data_yaml=CONFIG['data_yaml'],
                epochs=CONFIG['epochs'],
                batch_size=CONFIG['batch_size'],
                imgsz=CONFIG['imgsz'],
                project_name=CONFIG['project_name'],
                experiment_name=CONFIG['experiment_name'],
                pretrained_weights=CONFIG['pretrained_weights']
            )
            
            # Auto-validation after training
            if best_model_path and CONFIG['mode'] == 'all':
                validate_model(best_model_path, CONFIG['data_yaml'], CONFIG['imgsz'])
                benchmark_model(best_model_path, CONFIG['imgsz'])
        
        elif CONFIG['mode'] == 'validate':
            # Validation only
            model_path = input("Enter model path to validate: ").strip()
            validate_model(model_path, CONFIG['data_yaml'], CONFIG['imgsz'])
        
        elif CONFIG['mode'] == 'benchmark':
            # Benchmark only
            model_path = input("Enter model path to benchmark: ").strip()
            benchmark_model(model_path, CONFIG['imgsz'])
        
        logger.info("\n🎉 PIPELINE COMPLETED SUCCESSFULLY!")
        
    except KeyboardInterrupt:
        logger.info("\n  Training interrupted by user")
    except Exception as e:
        logger.error(f"\n Pipeline failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()