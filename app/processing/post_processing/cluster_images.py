import asyncio
import os
from pathlib import Path

import cv2
import numpy as np
from sqlalchemy import select
from tqdm import tqdm

from app.config.app_config import app_config
from app.data.database.database import get_session
from app.data.image_models import VisualInformationModel, ImageModel
from app.machine_learning.clustering.hdbscan_clustering import perform_clustering


async def experiment() -> None:
    async with get_session() as session:
        frames = (await session.execute(
            select(VisualInformationModel, ImageModel.relative_path)
            .join(VisualInformationModel.image)
        )).all()
        embeddings = np.vstack([frame[0].embedding.to_numpy() for frame in frames])
        cluster_labels = perform_clustering(
            embeddings,
            min_samples=2,
            min_cluster_size=3,
            cluster_selection_method='leaf',
            cluster_selection_epsilon=0.1
        )

        for i, (frame, relative_path) in tqdm(enumerate(frames), total=len(frames)):
            image = cv2.imread(app_config.images_dir / relative_path)
            if image is None:
                print(f"SKIP: {relative_path}")
                continue

            label = cluster_labels[i]
            if label == -1:
                label = 9999

            out_folder = Path('test_img_out') / str(label)
            if not out_folder.exists():
                out_folder.mkdir(parents=True)

            out_path = out_folder / f"{i}_{os.path.basename(relative_path)}.jpg"
            cv2.imwrite(str(out_path), image)


if __name__ == "__main__":
    asyncio.run(experiment())
