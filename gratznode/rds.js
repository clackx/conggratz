const Redis = require('ioredis');

const host = process.env.RDS_HOST || 'localhost'
const port = process.env.RDS_PORT || 6379

const redis = new Redis({host, port});

const cacheEntity = (wdEntity, data) => {
    redis.set(wdEntity, JSON.stringify(data), 'EX', 86400, 'NX');
}

async function getEntities(wdEntities) {
    return await redis.mget(wdEntities)
}

exports.cacheEntity = cacheEntity;
exports.getEntities = getEntities;
