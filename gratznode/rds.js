const Redis = require('ioredis');
const redis = new Redis({
    host: 'localhost',
    port: 6379,
});

const cacheEntity = (wdEntity, data) => {
    redis.set(wdEntity, JSON.stringify(data), 'EX', 86400, 'NX');
}

async function getEntities(wdEntities) {
    return await redis.mget(wdEntities)
}

exports.cacheEntity = cacheEntity;
exports.getEntities = getEntities;
