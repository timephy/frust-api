# frustrated-physicists-backend

## General

- python3.8

- serves on port 80

- this backend only acts as the API, it does not server static frontend files (any more)

## API

### Routes

`/api` (returns: `{"version": String}`)

`/api/history` click history (returns `[{"time": Int, "name": String, "comment": String?}]`)

`/api/socket.io` socket.io endpoint

### Socket.io Events

"users" (emitted every time usercount changes)

```typescript
{
    "count": Int
}
```

"stats" (emitted once when you connect, and periodically after)

```typescript
{
    "total": Int,
    "day": Int,
    "hour": Int
}
```

"click" (emitted ever time a corresponding click is received by the server)

```typescript
{
    "time": Int,
    "name": String,
    "comment": String?
}
```
