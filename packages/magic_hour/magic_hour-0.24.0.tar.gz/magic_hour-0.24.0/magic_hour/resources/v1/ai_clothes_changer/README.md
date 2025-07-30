
### AI Clothes Changer <a name="create"></a>

Change outfits in photos in seconds with just a photo reference. Each photo costs 25 credits.

**API Endpoint**: `POST /v1/ai-clothes-changer`

#### Synchronous Client

```python
from magic_hour import Client
from os import getenv

client = Client(token=getenv("API_TOKEN"))
res = client.v1.ai_clothes_changer.create(
    assets={
        "garment_file_path": "api-assets/id/outfit.png",
        "garment_type": "dresses",
        "person_file_path": "api-assets/id/model.png",
    },
    name="Clothes Changer image",
)

```

#### Asynchronous Client

```python
from magic_hour import AsyncClient
from os import getenv

client = AsyncClient(token=getenv("API_TOKEN"))
res = await client.v1.ai_clothes_changer.create(
    assets={
        "garment_file_path": "api-assets/id/outfit.png",
        "garment_type": "dresses",
        "person_file_path": "api-assets/id/model.png",
    },
    name="Clothes Changer image",
)

```

#### Parameters

| Parameter | Required | Description | Example |
|-----------|:--------:|-------------|--------|
| `assets` | ✓ | Provide the assets for clothes changer | `{"garment_file_path": "api-assets/id/outfit.png", "garment_type": "dresses", "person_file_path": "api-assets/id/model.png"}` |
| `name` | ✗ | The name of image | `"Clothes Changer image"` |
