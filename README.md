# frustrated-physicists-backend (API)

## Routes

`/api/socket.io` socket.io endpoint

`/api/history` click history (returns `[Entry]`)

## Socket.io Events

`users` - `{"count": Int}` (gets emitted every time usercount changes)

`stats` - `Stats` (gets emitted once when you connect, and periodically after)

`click` - `{"name": String, "comment": String?}` (gets emitted ever time a click is received by the server)

## JSON Interfaces

```typescript
interface Entry {
    time: Int,
    name: String,
    comment: String?
}
```
