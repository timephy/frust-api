# frustrated-physicists-backend

## Frontend Routes

`/`, `/index.html` main page

`/history.html` click history


## API Routes

`/api/ws` websocket for click posts and updates

`/api/history` click history (`[Entry]`)

`/api/status` status (`Status`)


## API JSON Interfaces

```typescript
interface Entry {
    time: Int,
    name: String,
    message: String?
}

interface Status {
    total: Int,
    day: Int,
    hour: Int
}

interface Click {
    name: String,
    message: String?
}
```
