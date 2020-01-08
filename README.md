# frustrated-physicists-backend

## General

- python3.8

- serves on port 80

- this backend only acts as the API (serves frontend only for development)

## How to run

### Production

```bash
git clone https://github.com/timephy/frustrated-physicists-backend
cd frustrated-physicists-backend
python3.8 .
```

### Development

```bash
git clone https://github.com/timephy/frustrated-physicists-backend
git clone https://github.com/timephy/frustrated-physicists-frontend
cd frustrated-physicists-backend
ln -s ../frustrated-physicists-frontend frontend
python3.8 . --dev
```

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
    "day": Int
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
