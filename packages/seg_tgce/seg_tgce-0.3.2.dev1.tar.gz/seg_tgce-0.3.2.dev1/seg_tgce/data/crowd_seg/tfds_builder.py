import logging
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds
from keras.preprocessing.image import img_to_array, load_img
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap, to_rgb

from seg_tgce.data.crowd_seg.__retrieve import (
    _BUCKET_NAME,
    MASKS_OBJECT_NAME,
    PATCHES_OBJECT_NAME,
)

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARNING)


CLASSES_DEFINITION = {
    0: "Ignore",
    1: "Other",
    2: "Tumor",
    3: "Stroma",
    4: "Benign Inflammation",
    5: "Necrosis",
}

REAL_SCORERS = [
    "NP1",
    "NP2",
    "NP3",
    "NP4",
    "NP5",
    "NP6",
    "NP7",
    "NP8",
    "NP9",
    "NP10",
    "NP11",
    "NP12",
    "NP13",
    "NP14",
    "NP15",
    "NP16",
    "NP17",
    "NP18",
    "NP19",
    "NP20",
    "NP21",
]

AGGREGATED_SCORERS = ["MV", "STAPLE"]

ALL_SCORER_TAGS = REAL_SCORERS + AGGREGATED_SCORERS + ["ground_truth"]

DEFAULT_IMG_SIZE = (512, 512)
METADATA_PATH = Path(__file__).resolve().parent / "metadata"

NUM_CLASSES = len(CLASSES_DEFINITION)
NUM_REAL_SCORERS = len(REAL_SCORERS)


def normalize_image(image: tf.Tensor) -> tf.Tensor:
    return tf.cast(image, tf.float32) / 255.0


def create_one_hot_mask(mask: tf.Tensor) -> tf.Tensor:
    mask = tf.cast(mask, tf.uint8)
    return tf.one_hot(mask, NUM_CLASSES, dtype=tf.float32)


def create_labeler_mask(labelers: tf.Tensor) -> tf.Tensor:
    labeler_mask = tf.zeros(NUM_REAL_SCORERS, dtype=tf.float32)

    for i, scorer in enumerate(REAL_SCORERS):
        labeler_mask = tf.tensor_scatter_nd_update(
            labeler_mask,
            [[i]],
            [tf.cast(tf.reduce_any(tf.equal(labelers, scorer)), tf.uint8)],
        )

    return labeler_mask


def process_sample(
    sample: Dict[str, tf.Tensor], image_size: Tuple[int, int]
) -> Dict[str, tf.Tensor]:
    image = normalize_image(sample["image"])

    real_scorer_indices = tf.where(
        tf.reduce_any(
            tf.equal(tf.expand_dims(sample["labelers"], 1), tf.constant(REAL_SCORERS)),
            axis=1,
        )
    )

    masks = tf.squeeze(
        tf.squeeze(tf.gather(sample["masks"], real_scorer_indices), axis=1), axis=-1
    )
    labelers = tf.gather(sample["labelers"], real_scorer_indices)

    masks = tf.map_fn(
        create_one_hot_mask,
        masks,
        fn_output_signature=tf.TensorSpec(
            shape=(*image_size, NUM_CLASSES), dtype=tf.float32
        ),
    )

    labeler_mask = create_labeler_mask(labelers)

    expanded_masks = tf.zeros(
        (NUM_REAL_SCORERS, *image_size, NUM_CLASSES), dtype=tf.float32
    )

    active_indices = tf.where(tf.equal(labeler_mask, 1))[:, 0]

    active_indices = tf.reshape(active_indices, [-1, 1])

    masks = tf.reshape(masks, [-1, *image_size, NUM_CLASSES])

    expanded_masks = tf.tensor_scatter_nd_update(expanded_masks, active_indices, masks)

    expanded_masks = tf.transpose(expanded_masks, perm=[1, 2, 3, 0])

    # Get the expert mask (last mask in the sequence)
    expert_mask = sample["masks"][-1]
    # Ensure the expert mask has the correct shape before one-hot encoding
    expert_mask = tf.reshape(expert_mask, image_size)

    return {
        "image": image,
        "masks": expanded_masks,
        "labelers_mask": labeler_mask,
        "ground_truth": create_one_hot_mask(expert_mask),
    }


class CrowdSegDataset(tfds.core.GeneratorBasedBuilder):
    """DatasetBuilder for crowd segmentation dataset."""

    VERSION = tfds.core.Version("1.0.0")
    RELEASE_NOTES = {
        "1.0.0": "Initial release.",
    }

    def __init__(
        self,
        *,
        image_size: Tuple[int, int] = DEFAULT_IMG_SIZE,
    ):
        """Initialize the dataset builder.

        Args:
            image_size: Tuple[int, int] = DEFAULT_IMG_SIZE: Image size for the dataset.
        """
        self.image_size = image_size
        super().__init__()

    def _info(self) -> tfds.core.DatasetInfo:
        return tfds.core.DatasetInfo(
            builder=self,
            description="Crowd segmentation dataset for histology images.",
            features=tfds.features.FeaturesDict(
                {
                    "image": tfds.features.Image(shape=(*self.image_size, 3)),
                    "masks": tfds.features.Sequence(
                        tfds.features.Tensor(
                            shape=(*self.image_size, 1), dtype=tf.uint8
                        )
                    ),
                    "labelers": tfds.features.Sequence(tfds.features.Text()),
                }
            ),
            supervised_keys=("image", "masks"),
            homepage="https://github.com/your-repo/crowd-seg",
            citation="""@article{your-citation}""",
        )

    def _split_generators(self, dl_manager: tfds.download.DownloadManager):
        patches_url = f"https://{_BUCKET_NAME}.s3.amazonaws.com/{PATCHES_OBJECT_NAME}"
        masks_url = f"https://{_BUCKET_NAME}.s3.amazonaws.com/{MASKS_OBJECT_NAME}"

        patches_path = dl_manager.download_and_extract(patches_url)
        masks_path = dl_manager.download_and_extract(masks_url)

        patches_dir = os.path.join(patches_path, "patches")
        masks_dir = os.path.join(masks_path, "masks")

        return {
            "train": self._generate_examples(
                os.path.join(patches_dir, "Train"),
                os.path.join(masks_dir, "Train"),
            ),
            "validation": self._generate_examples(
                os.path.join(patches_dir, "Valid"),
                os.path.join(masks_dir, "Valid"),
            ),
            "test": self._generate_examples(
                os.path.join(patches_dir, "Test"),
                os.path.join(masks_dir, "Test"),
            ),
        }

    def _generate_examples(self, image_dir: str, mask_dir: str):
        image_filenames = self._get_image_filenames(image_dir)

        for filename in image_filenames:
            image, masks, labelers = self._load_sample(filename, image_dir, mask_dir)
            yield filename, {
                "image": image,
                "masks": masks,
                "labelers": labelers,
            }

    def _get_image_filenames(self, image_dir: str) -> List[str]:
        return sorted(
            [
                filename
                for filename in os.listdir(image_dir)
                if filename.endswith(".png")
            ]
        )

    def _load_sample(
        self,
        filename: str,
        image_dir: str,
        mask_dir: str,
    ) -> Tuple[np.ndarray, List[np.ndarray], List[str]]:
        img_path = os.path.join(image_dir, filename)
        image = load_img(img_path, target_size=self.image_size)
        image = img_to_array(image, dtype=np.uint8)

        masks = []
        labelers = []

        for scorer_dir in ALL_SCORER_TAGS:
            scorer_mask_dir = os.path.join(mask_dir, scorer_dir)

            # Initialize a blank mask for this scorer
            scorer_mask = np.zeros(self.image_size, dtype=np.uint8)

            # Load each class mask and combine them
            for class_idx in range(NUM_CLASSES):
                class_dir = os.path.join(scorer_mask_dir, f"class_{class_idx}")
                mask_path = os.path.join(class_dir, filename)

                if os.path.exists(mask_path):
                    mask_raw = load_img(
                        mask_path,
                        color_mode="grayscale",
                        target_size=self.image_size,
                    )
                    class_mask = img_to_array(mask_raw, dtype=np.uint8)
                    # Convert 3D array to 2D by taking the first channel
                    class_mask = class_mask[:, :, 0]
                    # Set the class value where the mask is non-zero
                    scorer_mask[class_mask > 0] = class_idx

            # Only add the mask if it contains any annotations
            if np.any(scorer_mask > 0):
                # Add an extra dimension to match the expected shape
                scorer_mask = scorer_mask[..., np.newaxis]
                masks.append(scorer_mask)
                labelers.append(scorer_dir)

        return image, masks, labelers


def visualize_sample(
    dataset: tf.data.Dataset,
    image_size: Tuple[int, int],
    batch_index: int = 0,
    sample_indexes: Optional[List[int]] = None,
) -> plt.Figure:
    """
    Visualizes a sample from the dataset.

    Args:
        dataset: TensorFlow dataset to visualize from
        image_size: Tuple[int, int]: Size of the images in the dataset
        batch_index: Index of the batch to visualize
        sample_indexes: List of sample indexes to visualize. If None, shows first 4 samples.
    """
    if sample_indexes is None:
        sample_indexes = [0, 1, 2, 3]

    # Get a batch from the dataset
    batch = next(iter(dataset.skip(batch_index).take(1)))

    images = batch["image"]
    masks = batch["masks"]
    labeler_mask = batch["labelers_mask"]
    ground_truth = batch["ground_truth"]

    # Convert one-hot encoded masks to class indices for visualization
    masks_class = tf.argmax(masks, axis=-2)
    ground_truth_class = tf.argmax(ground_truth, axis=-1)

    # Find unique labelers in the batch
    unique_labelers = []
    for sample_idx in sample_indexes:
        present_labelers = tf.where(labeler_mask[sample_idx] == 1)[:, 0]
        unique_labelers.extend(present_labelers.numpy())
    unique_labelers = sorted(set(unique_labelers))

    fig = plt.figure(figsize=(12, 3 * len(sample_indexes)))

    gs = fig.add_gridspec(
        len(sample_indexes),
        len(unique_labelers) + 3,  # +3 for image, ground truth, and colorbar
        width_ratios=[1] * (len(unique_labelers) + 2) + [0.3],
        wspace=0.3,
    )

    axes = np.array(
        [
            [fig.add_subplot(gs[i, j]) for j in range(len(unique_labelers) + 3)]
            for i in range(len(sample_indexes))
        ]
    )

    for ax in axes.flatten():
        ax.axis("off")

    axes[0, 0].set_title("Slide", fontsize=12, pad=10)
    axes[0, 1].set_title("Ground Truth", fontsize=12, pad=10)
    _ = [
        axes[0, i + 2].set_title(
            f"Label for {REAL_SCORERS[labeler_idx]}", fontsize=12, pad=10
        )
        for i, labeler_idx in enumerate(unique_labelers)
    ]

    class_colors = {
        0: "#440154",  # Dark purple for Ignore
        1: "#414487",  # Deep blue for Other
        2: "#2a788e",  # Teal for Tumor
        3: "#22a884",  # Turquoise for Stroma
        4: "#44bf70",  # Green for Benign Inflammation
        5: "#fde725",  # Yellow for Necrosis
    }

    colors = [to_rgb(class_colors[i]) for i in range(NUM_CLASSES)]
    cmap = ListedColormap(colors)

    im = None

    for i, sample_index in enumerate(sample_indexes):
        axes[i, 0].imshow(images[sample_index])
        # Show ground truth
        axes[i, 1].imshow(
            ground_truth_class[sample_index],
            cmap=cmap,
            vmin=0,
            vmax=NUM_CLASSES - 1,
        )
        for j, labeler_idx in enumerate(unique_labelers):
            if labeler_mask[sample_index, labeler_idx] == 1:
                sample_mask = masks_class[sample_index, ..., labeler_idx]
                im = axes[i, j + 2].imshow(
                    sample_mask,
                    cmap=cmap,
                    vmin=0,
                    vmax=NUM_CLASSES - 1,
                )
            else:
                axes[i, j + 2].imshow(np.zeros(image_size), cmap="gray")

    if im is not None:
        cbar_ax = axes[0, -1]
        cbar_ax.axis("on")
        cbar = fig.colorbar(
            im, cax=cbar_ax, ticks=range(NUM_CLASSES), orientation="vertical"
        )
        cbar.ax.tick_params(labelsize=10)
        cbar.set_ticklabels(
            [CLASSES_DEFINITION[i] for i in range(NUM_CLASSES)], fontsize=10
        )

        cbar_ax.set_title("Classes", fontsize=12, pad=20)

    plt.tight_layout()
    return fig


def get_crowd_seg_dataset_tfds(
    image_size: Tuple[int, int] = DEFAULT_IMG_SIZE,
) -> Tuple[tf.data.Dataset, tf.data.Dataset, tf.data.Dataset]:
    """Get crowd segmentation dataset.

    Args:
        image_size: Tuple[int, int] = DEFAULT_IMG_SIZE: Image size for the dataset.

    Returns:
        Tuple[tf.data.Dataset, tf.data.Dataset, tf.data.Dataset]: TensorFlow datasets for train, validation, and test.
    """
    builder = CrowdSegDataset(
        image_size=image_size,
    )
    builder.download_and_prepare()

    return builder.as_dataset(split=("train", "validation", "test"))


def get_training_augmentation(
    brightness_limit: float = 0.2,
    contrast_limit: float = 0.2,
    hue_shift_limit: float = 0.05,
    sat_shift_limit: float = 0.1,
) -> tf.keras.Sequential:
    augmentation = tf.keras.Sequential(
        [
            # Random horizontal flip
            tf.keras.layers.RandomFlip("horizontal"),
            # Random vertical flip
            tf.keras.layers.RandomFlip("vertical"),
            # Random rotation (90 degrees)
            tf.keras.layers.RandomRotation(0.25),  # 0.25 = 90 degrees
            # Gaussian blur
            tf.keras.layers.GaussianNoise(0.1),  # Simulating blur effect
            # Random brightness and contrast
            tf.keras.layers.RandomBrightness(brightness_limit),
            tf.keras.layers.RandomContrast(contrast_limit),
            # Random hue and saturation
            tf.keras.layers.RandomSaturation(sat_shift_limit),
            tf.keras.layers.RandomHue(hue_shift_limit),
            # Convert back to uint8
            tf.keras.layers.Lambda(
                lambda x: tf.cast(tf.clip_by_value(x * 255, 0, 255), tf.uint8)
            ),
        ]
    )

    return augmentation


def get_processed_data(
    image_size: Tuple[int, int] = DEFAULT_IMG_SIZE,
    batch_size: int = 32,
    use_augmentation: bool = True,
    augmentation_factor: int = 2,  # Number of augmented versions per original image
):
    train, validation, test = get_crowd_seg_dataset_tfds(
        image_size=image_size,
    )

    print(f"Original dataset train length: {len(train)}")

    processed_train = train.cache()

    if use_augmentation:
        augmentation = get_training_augmentation()

        # Create multiple augmented versions of each sample
        for _ in range(augmentation_factor):
            augmented = processed_train.map(
                lambda x: {**x, "image": augmentation(x["image"])},
                num_parallel_calls=tf.data.AUTOTUNE,
            )
            processed_train = processed_train.concatenate(augmented)
        print(f"Augmented dataset train length before batching: {len(processed_train)}")

    processed_train = processed_train.shuffle(10000)

    processed_train = processed_train.map(
        lambda x: process_sample(x, image_size),
        num_parallel_calls=tf.data.AUTOTUNE,
    )

    processed_validation = validation.map(
        lambda x: process_sample(x, image_size),
        num_parallel_calls=tf.data.AUTOTUNE,
    )

    processed_test = test.map(
        lambda x: process_sample(x, image_size),
        num_parallel_calls=tf.data.AUTOTUNE,
    )

    return (
        processed_train.batch(batch_size).prefetch(tf.data.AUTOTUNE),
        processed_validation.batch(batch_size).prefetch(tf.data.AUTOTUNE),
        processed_test.batch(batch_size).prefetch(tf.data.AUTOTUNE),
    )


if __name__ == "__main__":
    target_size = (64, 64)
    batch_size = 8

    processed_train, processed_validation, processed_test = get_processed_data(
        image_size=target_size,
        batch_size=batch_size,
        use_augmentation=False,
    )
    print(len(processed_train))

    # Print dataset sizes for debugging
    print(f"Train dataset size: {len(processed_train)}")
    print(f"Validation dataset size: {len(processed_validation)}")
    print(f"Test dataset size: {len(processed_test)}")

    # Visualize only a few samples to avoid index errors
    for i, _ in enumerate(processed_train):
        try:
            fig = visualize_sample(
                processed_train,
                image_size=target_size,
                batch_index=i,
                sample_indexes=[0, 1, 2, 3],
            )
            plt.show()
        except Exception as e:
            print(f"Error visualizing batch {i}: {str(e)}")
            continue
