
### Delete image <a name="delete"></a>

Permanently delete the rendered image. This action is not reversible, please be sure before deleting.

**API Endpoint**: `DELETE /v1/image-projects/{id}`

#### Synchronous Client

```python
from magic_hour import Client
from os import getenv

client = Client(token=getenv("API_TOKEN"))
res = client.v1.image_projects.delete(id="cm6pvghix03bvyz0zwash6noj")

```

#### Asynchronous Client

```python
from magic_hour import AsyncClient
from os import getenv

client = AsyncClient(token=getenv("API_TOKEN"))
res = await client.v1.image_projects.delete(id="cm6pvghix03bvyz0zwash6noj")

```

#### Parameters

| Parameter | Required | Description | Example |
|-----------|:--------:|-------------|--------|
| `id` | ✓ | The id of the image project | `"cm6pvghix03bvyz0zwash6noj"` |

### Get image details <a name="get"></a>

Get the details of a image project. The `downloads` field will be empty unless the image was successfully rendered.

The image can be one of the following status
- `draft` - not currently used
- `queued` - the job is queued and waiting for a GPU
- `rendering` - the generation is in progress
- `complete` - the image is successful created
- `error` - an error occurred during rendering
- `canceled` - image render is canceled by the user


**API Endpoint**: `GET /v1/image-projects/{id}`

#### Synchronous Client

```python
from magic_hour import Client
from os import getenv

client = Client(token=getenv("API_TOKEN"))
res = client.v1.image_projects.get(id="cm6pvghix03bvyz0zwash6noj")

```

#### Asynchronous Client

```python
from magic_hour import AsyncClient
from os import getenv

client = AsyncClient(token=getenv("API_TOKEN"))
res = await client.v1.image_projects.get(id="cm6pvghix03bvyz0zwash6noj")

```

#### Parameters

| Parameter | Required | Description | Example |
|-----------|:--------:|-------------|--------|
| `id` | ✓ | The id of the image project | `"cm6pvghix03bvyz0zwash6noj"` |
