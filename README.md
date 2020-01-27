# frustrated-physicists-backend

A website for fellow Physics students at TUM to show their frustration.

_This project is just for fun._

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

Or run via docker:

```bash
docker pull docker.pkg.github.com/timephy/frustrated-physicists-backend/frustrated-physicists-backend:master
docker run -dit --name frustrated-physicists-backend \
    -v /path/to/db.sqlite:/usr/src/app/db.sqlite \
    --network reverse-proxy-network \
    -p 80:80 \
    docker.pkg.github.com/timephy/frustrated-physicists-backend/frustrated-physicists-backend:master
```

Either use `--network` with a reverse proxy or `-p`.
Run `touch /path/to/db.sqlite` before running the container (otherwise the created path will be a directory).

### Development

```bash
git clone https://github.com/timephy/frustrated-physicists-backend
git clone https://github.com/timephy/frustrated-physicists-frontend
cd frustrated-physicists-backend
ln -s ../frustrated-physicists-frontend frontend
python3.8 . --dev
```

## API

### Data Types

```typescript
interface Stats {
    click_count_total: number; // int
    click_count_today: number; // int
}

interface Status {
    user_count: number; // int
}

interface Click {
    user: string;
    comment: string?;
    style: string?; // css classes
    timestamp: number; // int
}

interface Event {
    user: string;
    name: string; // id of the event
    timestamp: number; // int
}

interface Hour {
    timestamp: number; // int
    click_count: number; // int
    event_count: number; // int
}

interface User {
    name: string;
    click_count: number; // int
    event_count: number; // int
}

interface Message {
    text: string;
    style: string?;
    type: "toast" | "popup";
}
```

Optionals may be `null` or `undefined`.

### HTTP Routes

##### `/api` -> `{"version": string}`

A description of the backend server.

##### `/api/latest_clicks` -> `[Click]`

Clicks of today.

##### `/api/latest_events` -> `[Events]`

Events of today.

##### `/api/latest_hours` -> `[Hour]`

Hours of last 7 days.

##### `/api/users` -> `[User]`

All users with their overall stats.

##### `/api/online_users` -> `[User]`

Online users with their session stats.

##### `/api/socket.io`

The socket.io endpoint.

Connection example (JS):

```typescript
const socket = io({
  path: "/api/socket.io"
});

socket.connect();
```

### Socket.io Events

#### Server to Client

##### `click`(`Click`)

Sent every time a click occurs.

##### `event`(`Event`)

Sent every time an event occurs.

##### `stats`(`Stats`)

Sent on connection and when user_count changes.
Clients should keep count of incoming clicks.

##### `status`(`Status`)

Sent when a client connects/disconnects or the server state changes.

##### `message`(`Message`)

Sent for example when a user joins or leaves.

#### Client to Server

##### `click`(`Click` without `timestamp`, `id`)

Sent on click performed.

##### `event`(`Event` without `timestamp`)

Sent on event performed.

##### `auth`(`string`)

Sent on connect (if username was saved) to authenticate (let server know the name to show "user joined" message).

## Continuous delivery

- `master` to frustrierte-physiker.timephy.com and staging-fp.timephy.com

## Frontend

Also see the frontent implementation:

<https://github.com/timephy/frustrated-physicists-frontend>
