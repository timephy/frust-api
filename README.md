# frust-api

A website for fellow Physics students at [TUM](https://www.tum.de) to share their frustration and motivate another.

_This project is just for fun._

## To our fellow students

To keep this fun project going we count on you to create Issues or Pull Requests with your suggestions.

_Happy frustrated studying!_

## Architecture

- [Frontend](https://github.com/timephy/frust-web) is served by [nginx](https://www.nginx.com)
- Backend (python3.8) server is reverse proxied by [nginx](https://www.nginx.com) (`/api` paths)

### Libraries used

- [asyncio](https://docs.python.org/3/library/asyncio.html) as the asynchronous framework (event loop library)
- [aiohttp](https://github.com/aio-libs/aiohttp) as the webserver for http requests
- [socket.io](https://socket.io) is used for websocket/live communication
- [sqlite](https://www.sqlite.org/index.html) is the database, accessed using [sqlalchemy](https://www.sqlalchemy.org) as the ORM

## How to run

### Production

```bash
git clone https://github.com/timephy/frust-api
cd frustrated-physicists-backend
python3.8 .
```

Or run via docker:

```bash
docker pull docker.pkg.github.com/timephy/frust-api/frust-api:master
docker run -dit --name frust-api \
    -v /path/to/db.sqlite:/usr/src/app/db.sqlite \
    --network reverse-proxy-network \
    -p 80:80 \
    docker.pkg.github.com/timephy/frust-api/frust-api:master
```

Either use `--network` with a reverse proxy or `-p`.
Run `touch /path/to/db.sqlite` before running the container (otherwise the created path will be a directory).

### Development

In development mode the backend serves the frontend.

```bash
git clone https://github.com/timephy/frust-api
git clone https://github.com/timephy/frust-web
cd frust-api
ln -s ../frust-web frontend
python3.8 . --dev
```

## API

### Data Types

```typescript
interface Stats {
    click_count_total: number; // int
    event_count_total: number; // int
    click_count_today: number; // int
    event_count_today: number; // int
    click_count_hour: number; // int
    event_count_hour: number; // int
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
    click_count_total: number; // int
    event_count_today: number; // int
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

Clicks of today. [reversed order, limited to 10k elements]

##### `/api/latest_events` -> `[Events]`

Events of today. [reversed order, limited to 10k elements]

##### `/api/latest_hours` -> `[Hour]`

Hours of today and last 6 days.

##### `/api/users` -> `[User]`

All users with their overall stats.

##### `/api/online_users` -> `[User]`

Online users with their session stats.

##### `/api/current_stats` -> `Stats`

The current stats.

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

- `master` to frust.app and staging.frust.app

## Frontend

Also see the frontent implementation:

<https://github.com/timephy/frust-web>
