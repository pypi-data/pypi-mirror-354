
### Face Swap Photo <a name="create"></a>

Create a face swap photo. Each photo costs 5 credits. The height/width of the output image depends on your subscription. Please refer to our [pricing](/pricing) page for more details

**API Endpoint**: `POST /v1/face-swap-photo`

#### Synchronous Client

```python
from magic_hour import Client
from os import getenv

client = Client(token=getenv("API_TOKEN"))
res = client.v1.face_swap_photo.create(
    assets={
        "source_file_path": "api-assets/id/1234.png",
        "target_file_path": "api-assets/id/1234.png",
    },
    name="Face Swap image",
)

```

#### Asynchronous Client

```python
from magic_hour import AsyncClient
from os import getenv

client = AsyncClient(token=getenv("API_TOKEN"))
res = await client.v1.face_swap_photo.create(
    assets={
        "source_file_path": "api-assets/id/1234.png",
        "target_file_path": "api-assets/id/1234.png",
    },
    name="Face Swap image",
)

```

#### Parameters

| Parameter | Required | Description | Example |
|-----------|:--------:|-------------|--------|
| `assets` | ✓ | Provide the assets for face swap photo | `{"source_file_path": "api-assets/id/1234.png", "target_file_path": "api-assets/id/1234.png"}` |
| `name` | ✗ | The name of image | `"Face Swap image"` |
